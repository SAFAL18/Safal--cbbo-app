import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG & MODERN CSS STYLING ---
st.set_page_config(
    page_title="CBBO Management Portal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        /* Main Theme & Font Styling */
        .main {
            background-color: #f8fafc;
        }
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            color: #14532d;
        }
        /* Metric Card Styling */
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 20px;
            border-radius: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        /* Custom Button Styling */
        .stButton>button {
            background-color: #16a34a;
            color: white;
            border-radius: 0.75rem;
            font-weight: 600;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #15803d;
        }
    </style>
""", unsafe_allow_html=True)

# --- USER CREDENTIALS DATABASE ---
USER_CREDENTIALS = {
    "admin": {"password": "adminpassword123", "role": "Employer / Admin", "name": "Admin Boss"},
    "rakesh": {"password": "rakesh123", "role": "Employee", "name": "Rakesh"},
    "ayushi": {"password": "ayushi123", "role": "Employee", "name": "Ayushi"},
    "praveen": {"password": "praveen123", "role": "Employee", "name": "Praveen"},
    "navneet": {"password": "navneet123", "role": "Employee", "name": "Navneet"},
}

# --- LOGIN SCREEN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 🌾 CBBO Connect Portal Login")
        st.markdown("Please enter your credentials to access your dashboard.")

        with st.form("login_form"):
            username_input = st.text_input("Username (e.g. rakesh, admin)").strip().lower()
            password_input = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Secure Login")

            if submit_login:
                if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input]["password"] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.role = USER_CREDENTIALS[username_input]["role"]
                    st.session_state.name = USER_CREDENTIALS[username_input]["name"]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    st.stop()

# --- SIDEBAR & USER INFO ---
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.name}")
    st.markdown(f"**Role:** `{st.session_state.role}`")
    st.markdown("---")
    if st.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.rerun()

current_user_name = st.session_state.name
current_role = st.session_state.role

# --- HEADER BANNER ---
st.markdown(f"""
    <div style="background: linear-gradient(to right, #15803d, #14532d); padding: 20px; border-radius: 1rem; color: white; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">CBBO Task & Grant Command Center</h2>
        <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Welcome back, {current_user_name} | Managing FPO Workloads & Task Timelines</p>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE MOCK DATABASE ---
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {
            "Task_ID": "T001",
            "Employee": "Rakesh",
            "FPO_Name": "Kishni Safal Farmer Producer Company Limited",
            "Task_Desc": "3rd CBBO Cost Documentation",
            "Received_Date": "2026-09-01",
            "Deadline": "2026-09-25",
            "Status": "Pending",
            "Issues_Remarks": "Waiting for audit clearance"
        }
    ])

# --- NAVIGATION ---
if current_role == "Employee":
    menu = st.sidebar.selectbox("Navigation Menu", ["My Assigned Tasks", "Submit Daily Progress"])
else:
    menu = st.sidebar.selectbox("Navigation Menu", ["Admin Dashboard", "Assign New Task", "Master Task Ledger"])


# --- VIEW: EMPLOYEE - MY ASSIGNED TASKS ---
if menu == "My Assigned Tasks":
    st.subheader(f"📋 Tasks Assigned to {current_user_name}")
    
    my_tasks = st.session_state.tasks[st.session_state.tasks["Employee"] == current_user_name]
    
    if not my_tasks.empty:
        st.dataframe(my_tasks, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Update Task Status")
        
        with st.form("update_form"):
            selected_task_id = st.selectbox("Select Task ID to Update", my_tasks["Task_ID"].tolist())
            new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed"])
            new_remark = st.text_input("Add Issue / Remarks (if any)")
            
            if st.form_submit_button("Save Task Progress"):
                st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Status"] = new_status
                st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Issues_Remarks"] = new_remark
                st.success("Task updated successfully! Changes are now live on the Admin portal.")
                st.rerun()
    else:
        st.info("No tasks currently assigned to you.")

elif menu == "Submit Daily Progress":
    st.subheader("📝 Daily FPO Work Progress Form")
    with st.form("daily_progress"):
        fpo_target = st.text_input("FPO Name", value="Kishni Safal Farmer Producer Company Limited")
        work_done = st.text_area("Today's Work Details / Documents Completed")
        status_update = st.selectbox("Current Status", ["Pending", "In Progress", "Completed"])
        issues = st.text_input("Pending Items / Issues (e.g., Rent Agreement Etc)")
        
        if st.form_submit_button("Submit Daily Update"):
            st.success("Daily progress recorded successfully!")


# --- VIEW: ADMIN DASHBOARD ---
elif menu == "Admin Dashboard":
    st.subheader("👑 Admin Performance Control Center")
    
    total_t = len(st.session_state.tasks)
    pending_t = len(st.session_state.tasks[st.session_state.tasks["Status"] == "Pending"])
    completed_t = len(st.session_state.tasks[st.session_state.tasks["Status"] == "Completed"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks Assigned", total_t)
    col2.metric("Pending Tasks", pending_t)
    col3.metric("Completed Tasks", completed_t)
    
    st.markdown("---")
    st.subheader("Live Master Task Ledger")
    st.dataframe(st.session_state.tasks, use_container_width=True)

elif menu == "Assign New Task":
    st.subheader("➕ Assign Task to Staff Member")
    
    with st.form("assign_form"):
        col1, col2 = st.columns(2)
        with col1:
            employee_target = st.selectbox("Select Staff", ["Rakesh", "Ayushi", "Praveen", "Navneet"])
            fpo_name = st.text_input("FPO Name", value="Kishni Safal Farmer Producer Company Limited")
        with col2:
            task_desc = st.text_input("Task Description", value="3rd CBBO Cost")
            deadline = st.date_input("Deadline Date", datetime.date.today() + datetime.timedelta(days=10))
        
        if st.form_submit_button("Assign Task Now"):
            new_id = f"T00{len(st.session_state.tasks) + 1}"
            new_row = {
                "Task_ID": new_id,
                "Employee": employee_target,
                "FPO_Name": fpo_name,
                "Task_Desc": task_desc,
                "Received_Date": str(datetime.date.today()),
                "Deadline": str(deadline),
                "Status": "Pending",
                "Issues_Remarks": "None"
            }
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Task successfully assigned to {employee_target}! It is now visible on their individual login portal.")

elif menu == "Master Task Ledger":
    st.subheader("📋 Complete Status Tracker (All Staff)")
    st.dataframe(st.session_state.tasks, use_container_width=True)
