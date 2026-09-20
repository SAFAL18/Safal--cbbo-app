import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CBBO Management Portal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN CUSTOM STYLING ---
st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        h1, h2, h3 { font-family: 'Inter', sans-serif; color: #14532d; }
        .stButton>button {
            background-color: #16a34a;
            color: white;
            border-radius: 0.75rem;
            font-weight: 600;
            border: none;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover { background-color: #15803d; }
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
        st.markdown("Please enter your individual staff or admin credentials.")

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

# --- SIDEBAR & USER SESSION INFO ---
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
        <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Welcome back, {current_user_name}</p>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE MOCK DATABASE ---
today_str = str(datetime.date.today())
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {
            "Task_ID": "T-101",
            "Employee": "Rakesh",
            "CBBO_Name": "Ashok Agritech",
            "FPO_Name": "Kishni Safal Farmer Producer Company Limited",
            "Grant_Task": "3rd CBBO Cost Documentation",
            "Received_Date": today_str,
            "Status": "Pending",
            "Issues_Remarks": "Waiting for audit clearance"
        },
        {
            "Task_ID": "T-102",
            "Employee": "Ayushi",
            "CBBO_Name": "Ashok Agritech",
            "FPO_Name": "Narsinghpur FPO",
            "Grant_Task": "Grant 4 Documentation",
            "Received_Date": today_str,
            "Status": "Completed",
            "Issues_Remarks": "None"
        }
    ])

# --- NAVIGATION MENU BASED ON ROLES ---
if current_role == "Employee":
    menu = st.sidebar.selectbox("Navigation Menu", ["My Assigned Tasks", "Submit Daily Progress"])
else:
    menu = st.sidebar.selectbox("Navigation Menu", ["Admin Dashboard", "Assign New Task", "Master Task Ledger"])


# --- VIEW 1: EMPLOYEE - MY ASSIGNED TASKS ---
if menu == "My Assigned Tasks":
    st.subheader(f"📋 Tasks & Grants Assigned to {current_user_name}")
    
    my_tasks = st.session_state.tasks[st.session_state.tasks["Employee"] == current_user_name]
    
    if not my_tasks.empty:
        st.dataframe(my_tasks, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Update Task / Grant Status")
        
        with st.form("update_form"):
            selected_task_id = st.selectbox("Select Task ID to Update", my_tasks["Task_ID"].tolist())
            new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed"])
            new_remark = st.text_input("Add Issue / Remarks / Pending Items (e.g. Rent Agreement)")
            
            if st.form_submit_button("Save & Sync to Admin Portal"):
                st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Status"] = new_status
                st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Issues_Remarks"] = new_remark
                st.success("Task updated successfully! It is now reflected live on the Admin portal.")
                st.rerun()
    else:
        st.info("No tasks currently assigned to you.")

elif menu == "Submit Daily Progress":
    st.subheader("📝 Daily FPO Work & Grant Progress Form")
    with st.form("daily_progress"):
        col1, col2 = st.columns(2)
        with col1:
            cbbo_in = st.text_input("CBBO Name", value="Ashok Agritech")
            fpo_in = st.text_input("FPO Name", placeholder="e.g. Kishni Safal Farmer Producer Company Limited")
        with col2:
            grant_in = st.text_input("Grant / Task Name", placeholder="e.g. 3rd CBBO Cost")
            status_in = st.selectbox("Current Status", ["Pending", "In Progress", "Completed"])
            
        issues_in = st.text_area("Pending Details / Issues (e.g., Rent Agreement Etc)")
        
        if st.form_submit_button("Submit Daily Report"):
            new_id = f"T-10{len(st.session_state.tasks) + 1}"
            new_entry = {
                "Task_ID": new_id,
                "Employee": current_user_name,
                "CBBO_Name": cbbo_in,
                "FPO_Name": fpo_in,
                "Grant_Task": grant_in,
                "Received_Date": today_str,
                "Status": status_in,
                "Issues_Remarks": issues_in
            }
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Daily progress submitted successfully to Admin dashboard!")


# --- VIEW 2: ADMIN DASHBOARD ---
elif menu == "Admin Dashboard":
    st.subheader("👑 Admin Daily Performance & Activity Control Center")
    
    # Advanced Metrics Calculation
    total_tasks = len(st.session_state.tasks)
    came_today = len(st.session_state.tasks[st.session_state.tasks["Received_Date"] == today_str])
    submitted_completed = len(st.session_state.tasks[st.session_state.tasks["Status"] == "Completed"])
    pending_work = len(st.session_state.tasks[st.session_state.tasks["Status"] != "Completed"])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assigned Work", total_tasks)
    col2.metric("Came / Given Today", came_today)
    col3.metric("Submitted / Completed", submitted_completed)
    col4.metric("Pending Workload", pending_work)
    
    st.markdown("---")
    st.subheader("📋 Live Master Ledger (Task ID, Employee, CBBO, FPO)")
    st.dataframe(st.session_state.tasks, use_container_width=True)

elif menu == "Assign New Task":
    st.subheader("➕ Assign Task / Grant to Staff")
    
    with st.form("assign_form"):
        col1, col2 = st.columns(2)
        with col1:
            employee_target = st.selectbox("Select Staff", ["Rakesh", "Ayushi", "Praveen", "Navneet"])
            cbbo_name = st.text_input("CBBO Name", value="Ashok Agritech")
            fpo_name = st.text_input("FPO Name", value="Kishni Safal Farmer Producer Company Limited")
        with col2:
            grant_task = st.text_input("Grant / Task Description", value="3rd CBBO Cost")
            
        if st.form_submit_button("Assign Task"):
            new_id = f"T-10{len(st.session_state.tasks) + 1}"
            new_row = {
                "Task_ID": new_id,
                "Employee": employee_target,
                "CBBO_Name": cbbo_name,
                "FPO_Name": fpo_name,
                "Grant_Task": grant_task,
                "Received_Date": today_str,
                "Status": "Pending",
                "Issues_Remarks": "Assigned by Admin"
            }
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Task successfully assigned to {employee_target}! It will now show up on their individual login portal.")

elif menu == "Master Task Ledger":
    st.subheader("📊 Complete Status & Issue Tracker")
    st.dataframe(st.session_state.tasks, use_container_width=True)
