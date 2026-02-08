"""Final Test Before Deploy"""
import sqlite3
import os

print("🧪 最終測試...")
print("="*50)

db_path = '/Users/danny/.openclaw/workspace/forum_final_test.db'
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create all tables
c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, 
    role TEXT DEFAULT 'user', avatar TEXT DEFAULT NULL,
    bio TEXT DEFAULT '', email TEXT DEFAULT '',
    join_date TEXT, last_active TEXT
)''')

c.execute('''CREATE TABLE posts (
    id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT, 
    date TEXT, category TEXT DEFAULT '一般', view_count INTEGER DEFAULT 0
)''')

c.execute('''CREATE TABLE messages (
    id INTEGER PRIMARY KEY, post_id INTEGER, content TEXT, 
    author TEXT, date TEXT
)''')

c.execute('''CREATE TABLE notifications (
    id INTEGER PRIMARY KEY, user TEXT, type TEXT, 
    message TEXT, link TEXT, date TEXT, read INTEGER DEFAULT 0
)''')

conn.commit()

# Test user registration flow
import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Simulate registration
c.execute("INSERT INTO users (username, password_hash, role, bio, email, join_date, last_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
         ('admin', hash_password('admin123'), 'admin', '測試管理員', 'admin@test.com', '2026-02-07', '2026-02-07'))
conn.commit()

c.execute("INSERT INTO users (username, password_hash, role, join_date) VALUES (?, ?, ?, ?)",
         ('user1', hash_password('pass123'), 'user', '2026-02-07'))
conn.commit()

# Test post creation
c.execute("INSERT INTO posts (title, content, author, date, category, view_count) VALUES (?, ?, ?, ?, ?, ?)",
         ('歡迎來到討論區', '呢度係Gay Spa香港討論區！歡迎大家！', 'admin', '2026-02-07 23:55', '通知', 10))
conn.commit()

c.execute("INSERT INTO messages (post_id, content, author, date) VALUES (?, ?, ?, ?)",
         (1, '好正呀！呢個討論區！', 'user1', '23:56'))
conn.commit()

# Test notification
c.execute("INSERT INTO notifications (user, type, message, date, read) VALUES (?, ?, ?, ?, ?)",
         ('admin', 'new_user', '新用戶user1已加入！', '2026-02-07', 0))
conn.commit()

# Verify all data
tests = [
    ("User count", "SELECT COUNT(*) FROM users", 2),
    ("Post count", "SELECT COUNT(*) FROM posts", 1),
    ("Message count", "SELECT COUNT(*) FROM messages", 1),
    ("Notification count", "SELECT COUNT(*) FROM notifications", 1),
    ("Admin exists", "SELECT username FROM users WHERE role='admin'", 'admin'),
    ("User post count", "SELECT COUNT(*) FROM posts WHERE author='user1'", 1),
    ("Unread notifs", "SELECT COUNT(*) FROM notifications WHERE read=0", 1),
]

all_pass = True
for name, query, expected in tests:
    c.execute(query)
    result = c.fetchone()[0]
    status = "✅" if result == expected else "❌"
    if result != expected:
        all_pass = False
    print(f"  {status} {name}: {result} (expected: {expected})")

conn.close()
os.remove(db_path)

print("\n" + "="*50)
if all_pass:
    print("✅ 所有測試通過！可以Deploy！")
else:
    print("❌ 有測試失敗，請檢查！")
