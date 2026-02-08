import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="GaySecret Forum", page_icon="🌈")

st.title("🌈 GaySecret Forum")
st.write("Safe anonymous space for Hong Kong LGBTQ+ community!")

# Session state for posts
if "posts" not in st.session_state:
    st.session_state.posts = []

# Navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Create Post"])

# Home page
if menu == "Home":
    st.header("All Posts")
    
    if not st.session_state.posts:
        st.info("No posts yet. Be the first to share!")
    else:
        for i, post in enumerate(st.session_state.posts):
            st.markdown("---")
            st.subheader(post["title"])
            st.write(f"📁 {post['category']} | 🕐 {post['time']}")
            st.write(post["content"])
            
            # Replies section
            st.write("💬 Replies:")
            if post["replies"]:
                for reply in post["replies"]:
                    st.write(f"  • {reply}")
            else:
                st.write("  _No replies yet_")
            
            # Add reply
            reply = st.text_input(f"Reply to post #{i+1}", key=f"reply_{i}")
            if st.button(f"Submit Reply #{i+1}", key=f"btn_reply_{i}"):
                if reply:
                    post["replies"].append(f"{reply}")
                    st.success("Reply submitted!")
                    st.rerun()

# Create post page
elif menu == "Create Post":
    st.header("Create New Post")
    
    title = st.text_input("Title")
    content = st.text_area("Content")
    category = st.selectbox("Category", ["General", "Events", "Help", "Share"])
    
    if st.button("Publish Post"):
        if title and content:
            st.session_state.posts.append({
                "title": title,
                "content": content,
                "category": category,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "replies": []
            })
            st.success("✅ Post published successfully!")
            st.balloons()
        else:
            st.error("Please fill in title and content!")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("🌈 GaySecret Forum v1.0")
st.sidebar.write("Made with Streamlit")
