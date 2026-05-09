import sqlite3
import os
from datetime import datetime

DB_PATH = "data/memory.db"
os.makedirs("data", exist_ok=True)

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory
                 (key TEXT PRIMARY KEY, value TEXT, update_time TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# 加载所有记忆（返回字典，和你旧接口完全一样！）
def load_memory():
    c = conn.cursor()
    c.execute("SELECT key, value FROM memory")
    items = c.fetchall()
    return {k: v for k, v in items}

# 保存记忆（兼容旧接口！）
def save_memory(memory_dict):
    c = conn.cursor()
    for key, value in memory_dict.items():
        now = datetime.now().isoformat()
        c.execute("REPLACE INTO memory VALUES (?,?,?)",
                  (key, value, now))
    conn.commit()

# 更新单条记忆（兼容旧接口！）
def update_memory(key, value):
    now = datetime.now().isoformat()
    c = conn.cursor()
    c.execute("REPLACE INTO memory VALUES (?,?,?)",
              (key, value, now))
    conn.commit()