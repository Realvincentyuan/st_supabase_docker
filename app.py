import streamlit as st
import os
import json
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Initialize Supabase connection
@st.cache_resource
def init_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return {"url": url, "key": key}

# Page config
st.set_page_config(
    page_title="Streamlit + Supabase",
    page_icon="🚀",
    layout="centered"
)

# Initialize session state
if 'supabase' not in st.session_state:
    st.session_state.supabase = init_supabase()
    # Debug: show what values were loaded
    with st.sidebar:
        with st.expander("🔧 Debug Info"):
            st.code(f"URL: {st.session_state.supabase['url']}")
            st.code(f"Key prefix: {st.session_state.supabase['key'][:30]}...")

def make_request(method, endpoint, data=None, query=None):
    """Make HTTP request to Supabase REST API"""
    url = f"{st.session_state.supabase['url']}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "apikey": st.session_state.supabase['key']
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=query)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, params=query)
        
        response.raise_for_status()
        return response.json() if response.text else None
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")

# Main app
st.title("🚀 Streamlit + Supabase Demo")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Menu")
    page = st.radio("Select a page:", ["Home", "Add Item", "View Items"])

# Home page
if page == "Home":
    st.subheader("Welcome to Streamlit + Supabase")
    st.info("""
    This is a simple demo app that integrates:
    - **Streamlit** - For the web interface
    - **Supabase** - For data storage
    - **Docker** - For easy deployment
    
    Use the sidebar to navigate and start adding items!
    """)

# Add Item page
elif page == "Add Item":
    st.subheader("Add New Item")
    
    with st.form("add_item_form"):
        name = st.text_input("Item Name")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Item")
        
        if submitted:
            if name and description:
                try:
                    data = {
                        "name": name,
                        "description": description
                    }
                    result = make_request("POST", "/items", data=data)
                    st.success("✅ Item added successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error adding item: {str(e)}")
            else:
                st.warning("Please fill in all fields")

# View Items page
elif page == "View Items":
    st.subheader("All Items")
    
    try:
        items = make_request("GET", "/items")
        
        if items and len(items) > 0:
            for item in items:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{item['name']}**")
                        st.write(item['description'])
                    with col2:
                        if st.button("Delete", key=item['id']):
                            make_request("DELETE", f"/items", query={"id": f"eq.{item['id']}"})
                            st.rerun()
                    st.divider()
        else:
            st.info("No items yet. Add one from the 'Add Item' page!")
            
    except Exception as e:
        st.error(f"❌ Error fetching items: {str(e)}")
        st.info("Make sure Supabase is running and the 'items' table exists.")
