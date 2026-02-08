import streamlit as st
import sqlite3
from datetime import datetime
import streamlit_option_menu as option_menu

# 初始化數據庫（簡單SQLite，存帖子）
def init_db():
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, category TEXT, timestamp TEXT, replies TEXT)''')
    conn.commit()
    conn.close()

init_db()  # 第一次運行時創建數據庫

# 主頁函數
def main_page():
    st.title("GaySecret 討論區 - 香港LGBTQ+社區")
    st.write("歡迎嚟到呢個安全、匿名嘅討論空間！超過50萬用戶目標，一齊努力！😊")

    # 搜索功能
    search_term = st.text_input("搜索帖子（標題或內容）")
    
    # 顯示帖子
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    if search_term:
        c.execute("SELECT * FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY timestamp DESC", 
                  ('%' + search_term + '%', '%' + search_term + '%'))
    else:
        c.execute("SELECT * FROM posts ORDER BY timestamp DESC")
    posts = c.fetchall()
    conn.close()

    for post in posts:
        st.subheader(post[1])  # 標題
        st.write(f"分類: {post[3]} | 時間: {post[4]}")
        st.write(post[2])  # 內容
        st.write("回覆: " + (post[5] if post[5] else "無"))
        reply = st.text_input(f"回覆帖子 {post[0]}", key=f"reply_{post[0]}")
        if st.button(f"提交回覆 {post[0]}", key=f"submit_{post[0]}"):
            if reply:
                update_reply(post[0], reply)
                st.success("回覆成功！")
                st.experimental_rerun()

# 更新回覆
def update_reply(post_id, new_reply):
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute("SELECT replies FROM posts WHERE id=?", (post_id,))
    current_replies = c.fetchone()[0] or ""
    updated_replies = current_replies + "\n- " + new_reply + " (" + datetime.now().strftime("%Y-%m-%d %H:%M") + ")"
    c.execute("UPDATE posts SET replies=? WHERE id=?", (updated_replies, post_id))
    conn.commit()
    conn.close()

# 發帖頁
def post_page():
    st.title("發新帖")
    title = st.text_input("標題")
    content = st.text_area("內容")
    category = st.selectbox("分類", ["一般討論", "活動", "求助", "分享"])
    if st.button("提交"):
        if title and content:
            conn = sqlite3.connect('forum.db')
            c = conn.cursor()
            c.execute("INSERT INTO posts (title, content, category, timestamp) VALUES (?, ?, ?, ?)",
                      (title, content, category, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            st.success("帖子發佈成功！")
            st.experimental_rerun()
        else:
            st.error("請填寫標題同內容！")

# 主app
with st.sidebar:
    selected = option_menu.option_menu("導航", ["主頁", "發帖"], 
        icons=['house', 'pencil'], menu_icon="cast", default_index=0)

if selected == "主頁":
    main_page()
elif selected == "發帖":
    post_page()