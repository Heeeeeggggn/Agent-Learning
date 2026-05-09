import os
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = "data/chroma_db"
DOCUMENTS_PATH = "data/documents"

class RAGManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model="text-embedding-3-small"
        )
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.vector_store = Chroma(
            client=self.client,
            embedding_function=self.embeddings,
            collection_name="learning_docs"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )
        
        os.makedirs(DOCUMENTS_PATH, exist_ok=True)

    def load_document(self, file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        docs = loader.load()
        return self.text_splitter.split_documents(docs)

    def add_documents(self, file_paths):
        all_docs = []
        for file_path in file_paths:
            docs = self.load_document(file_path)
            all_docs.extend(docs)
        
        if all_docs:
            self.vector_store.add_documents(all_docs)
            return len(all_docs)
        return 0

    def similarity_search(self, query, k=3):
        results = self.vector_store.similarity_search(query, k=k)
        return results

    def get_context(self, query, k=3):
        docs = self.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    def get_collection_stats(self):
        collection = self.client.get_collection("learning_docs")
        return collection.count()

    def clear_documents(self):
        collection = self.client.get_collection("learning_docs")
        collection.delete()
        return True

rag_manager = RAGManager()