from langgraph.graph import StateGraph
from state import AgentState

from nodes.memory_node import memory_node
from nodes.intent_node import intent_node
from nodes.planner_node import planner_node
from nodes.feedback_node import feedback_node
from nodes.memory_query_node import memory_query_node
from Tools.Search_tool import tavily_search_node

from memory import update_memory

def build_graph():
# 构建图
    builder = StateGraph(AgentState)

    builder.add_node("memory", memory_node)
    builder.add_node("intent", intent_node)
    builder.add_node("planner", planner_node)
    builder.add_node("feedback", feedback_node)
    builder.add_node("memory_query", memory_query_node)

    builder.add_node("search", tavily_search_node)

    builder.set_entry_point("memory")

    builder.add_edge("memory", "intent")

    builder.add_conditional_edges(
        "intent",
        lambda state: state["intent"],
        {
            "plan": "planner",
            "memory": "memory_query",
            "feedback": "feedback",
            "update": "planner",
            "search": "search"
        }
    )

    builder.add_edge("search", "planner")
    builder.add_edge("planner", "__end__")
    builder.add_edge("feedback", "__end__")

    return builder.compile()

app = build_graph()


# ✅ CLI 模式保留（不影响 API）
if __name__ == "__main__":
    while True:
        user_input = input("\n你：")

        result = app.invoke({
            "input": user_input
        })

        plan = result.get("plan", "")
        print("\nAI：", plan)

        if plan:
            update_memory("last_plan", plan)
