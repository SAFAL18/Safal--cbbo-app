import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CBBO Enterprise Portal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        h1, h2, h3 { font-family: 'Inter', sans-serif; color: #14532d; }
        .card-pending {
            background: #fffbeb; border: 1px solid #fef3c7; padding: 16px; border-radius: 12px; margin-bottom: 12px;
        }
        .card-granted {
            background: #f0fdf4; border: 1px solid #dcfce7; padding: 16px; border-radius: 12px; margin-bottom: 12px;
        }
        .stButton>button {
            background-color: #16a34a; color: white; border-radius: 0.75rem; font-weight: 600; border: none; padding: 0.5rem 1rem;
        }
        .stButton>button:hover { background-color: #15803d; }
    </style>
""", unsafe_allow_html=True)

# --- USER CREDENTIALS & HIERARCHY DATABASE ---
USER_CREDENTIALS = {
    "admin": {"password": "adminpassword123", "role": "Admin", "name": "Admin Boss"},
    "ayushi": {"password": "ayushi123", "role": "Manager", "name": "Ayushi"},
    "rakesh": {"password": "rakesh123", "role": "Employee", "name": "Rakesh"},
    "praveen": {"password": "praveen123", "role": "Restricted", "name": "Praveen"},
    "navneet": {"password": "navneet123", "role": "Employee", "name": "Navneet"},
}

# --- LOGIN SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 🌾 CBBO Connect Portal Login")
        st.markdown("Please enter your login credentials.")

        with st.form("login_form"):
            username_input = st.text_input("Username").strip().lower()
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
today_str = str(datetime.date.today())

# --- HEADER BANNER ---
st.markdown(f"""
    <div style="background: linear-gradient(to right, #15803d, #14532d); padding: 20px; border-radius: 1rem; color: white; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">CBBO Task & Grant Command Center</h2>
        <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Welcome back, {current_user_name}</p>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZE DATABASE STATE ---
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame([
        {
            "Task_ID": "T-101",
            "Employee": "Rakesh",
            "CBBO_Name": "Ashok Agritech",
            "FPO_Name": "Kishni Safal Farmer Producer Company Limited",
            "Grant_Task": "3rd CBBO Cost Documentation",
            "Amount": 1500000,
            "Received_Date": today_str,
            "Status": "Pending",
            "Issues_Remarks": "Waiting for audit clearance",
            "Document_Name": "None"
        },
        {
            "Task_ID": "T-102",
            "Employee": "Praveen",
            "CBBO_Name": "Ashok Agritech",
            "FPO_Name": "Narsinghpur FPO",
            "Grant_Task": "Grant 4 Restricted Audit",
            "Amount": 2500000,
            "Received_Date": today_str,
            "Status": "Completed",
            "Issues_Remarks": "Confidential",
            "Document_Name": "Audit_Report.pdf"
        }
    ])

# --- NAVIGATION MENU BASED ON ROLES ---
if current_role == "Employee" and current_user_name == "Rakesh":
    menu = st.sidebar.selectbox("Navigation", ["My Assigned Tasks", "Assign Sub-Task", "Submit Daily Progress"])
elif current_role == "Employee" or current_role == "Manager":
    menu = st.sidebar.selectbox("Navigation", ["My Assigned Tasks", "Submit Daily Progress"])
elif current_role == "Restricted":
    menu = st.sidebar.selectbox("Navigation", ["My Assigned Tasks"])
else: # Admin
    menu = st.sidebar.selectbox("Navigation", ["Admin Dashboard", "Assign New Task", "Master Task Ledger"])


# --- VIEW: MY ASSIGNED TASKS ---
if menu == "My Assigned Tasks":
    st.subheader(f"📋 Tasks & Grants Assigned to {current_user_name}")
    
    # Visibility Filter: Praveen's tasks only visible to Admin. Rakesh can see his tasks & completed ones.
    if current_user_name == "Praveen":
        my_tasks = st.session_state.tasks[st.session_state.tasks["Employee"] == "Praveen"]
    elif current_user_name == "Rakesh":
        # Rakesh can see his own tasks + completed tasks across team (except strict restrictions if any)
        my_tasks = st.session_state.tasks[(st.session_state.tasks["Employee"] == "Rakesh") | ((st.session_state.tasks["Status"] == "Completed") & (st.session_state.tasks["Employee"] != "Praveen"))]
    elif current_role == "Admin":
        my_tasks = st.session_state.tasks
    else:
        my_tasks = st.session_state.tasks[st.session_state.tasks["Employee"] == current_user_name]
    
    if not my_tasks.empty:
        st.dataframe(my_tasks, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Update Status & Upload Document / PDF")
        
        with st.form("update_form"):
            selected_task_id = st.selectbox("Select Task ID to Update", my_tasks["Task_ID"].tolist())
            new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed"])
            new_remark = st.text_input("Add Issue / Remarks / Pending Items (e.g. Rent Agreement)")
            uploaded_file = st.file_uploader("Upload Completed Document / PDF", type=["pdf", "png", "jpg", "docx"])
            
            if st.form_submit_button("Save & Upload"):
                doc_name = uploaded_file.name if uploaded_file else "No File Uploaded"
                st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Status"] = new_status
                st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Issues_Remarks"] = new_remark
                st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Document_Name"] = doc_name
                st.success(f"Task updated successfully with document: {doc_name}!")
                st.rerun()
    else:
        st.info("No tasks available in your view.")

# --- RAKESH SUB-TASK ASSIGNMENT PORTAL ---
elif menu == "Assign Sub-Task":
    st.subheader("🔀 Rakesh's Task Delegation Portal")
    st.markdown("Assign tasks or sub-responsibilities down the line.")
    
    with st.form("rakesh_assign"):
        sub_emp = st.selectbox("Assign To", ["Navneet", "Self / Field Team"])
        fpo_n = st.text_input("FPO Name")
        task_d = st.text_input("Task Description")
        amt = st.number_input("Grant Amount (₹)", value=100000)
        
        if st.form_submit_button("Delegate Task"):
            new_id = f"T-20{len(st.session_state.tasks) + 1}"
            new_row = {
                "Task_ID": new_id,
                "Employee": sub_emp,
                "CBBO_Name": "Ashok Agritech",
                "FPO_Name": fpo_n,
                "Grant_Task": task_d,
                "Amount": amt,
                "Received_Date": today_str,
                "Status": "Pending",
                "Issues_Remarks": "Delegated by Rakesh",
                "Document_Name": "None"
            }
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Sub-task successfully assigned!")

elif menu == "Submit Daily Progress":
    st.subheader("📝 Daily FPO Work & Grant Progress Form")
    with st.form("daily_progress"):
        col1, col2 = st.columns(2)
        with col1:
            cbbo_in = st.text_input("CBBO Name", value="Ashok Agritech")
            fpo_in = st.text_input("FPO Name", placeholder="e.g. Kishni Safal FPO")
        with col2:
            grant_in = st.text_input("Grant / Task Name", placeholder="e.g. 3rd CBBO Cost")
            amt_in = st.number_input("Grant Amount (₹)", min_value=0, step=10000, value=500000)
            
        status_in = st.selectbox("Current Status", ["Pending", "In Progress", "Completed"])
        issues_in = st.text_area("Pending Details / Issues")
        uploaded_doc = st.file_uploader("Upload Supporting PDF/Document", type=["pdf", "png", "jpg"])
        
        if st.form_submit_button("Submit Daily Report"):
            doc_name = uploaded_doc.name if uploaded_doc else "None"
            new_id = f"T-10{len(st.session_state.tasks) + 1}"
            new_entry = {
                "Task_ID": new_id,
                "Employee": current_user_name,
                "CBBO_Name": cbbo_in,
                "FPO_Name": fpo_in,
                "Grant_Task": grant_in,
                "Amount": amt_in,
                "Received_Date": today_str,
                "Status": status_in,
                "Issues_Remarks": issues_in,
                "Document_Name": doc_name
            }
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Daily progress & document submitted successfully!")

# --- ADMIN DASHBOARD ---
elif menu == "Admin Dashboard":
    st.subheader("👑 Admin Performance & Activity Control Center")
    
    total_tasks = len(st.session_state.tasks)
    came_today = len(st.session_state.tasks[st.session_state.tasks["Received_Date"] == today_str])
    submitted_completed = len(st.session_state.tasks[st.session_state.tasks["Status"] == "Completed"])
    pending_work = len(st.session_state.tasks[st.session_state.tasks["Status"] != "Completed"])
    total_grant_val = st.session_state.tasks["Amount"].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assigned Work", total_tasks)
    col2.metric("Came / Given Today", came_today)
    col3.metric("Submitted / Completed", submitted_completed)
    col4.metric("Pending Workload", pending_work)
    
    st.info(f"💰 Total Tracked Grant Funding Value: ₹{total_grant_val:,.2f}")
    st.markdown("---")

    st.subheader("📋 Master Task, Grant & Document Ledger (Includes Praveen's Restricted Data)")
    st.dataframe(st.session_state.tasks, use_container_width=True)

elif menu == "Assign New Task":
    st.subheader("➕ Assign Task / Grant to Staff (Ayushi / Rakesh / Navneet / Praveen)")
    
    with st.form("assign_form"):
        col1, col2 = st.columns(2)
        with col1:
            employee_target = st.selectbox("Select Staff", ["Ayushi", "Rakesh", "Navneet", "Praveen"])
            cbbo_name = st.text_input("CBBO Name", value="Ashok Agritech")
            fpo_name = st.text_input("FPO Name", value="Kishni Safal Farmer Producer Company Limited")
        with col2:
            grant_task = st.text_input("Grant / Task Description", value="3rd CBBO Cost")
            amount_in = st.number_input("Grant Amount (₹)", value=1500000, step=50000)
            
        if st.form_submit_button("Assign Task Now"):
            new_id = f"T-10{len(st.session_state.tasks) + 1}"
            new_row = {
                "Task_ID": new_id,
                "Employee": employee_target,
                "CBBO_Name": cbbo_name,
                "FPO_Name": fpo_name,
                "Grant_Task": grant_task,
                "Amount": amount_in,
                "Received_Date": today_str,
                "Status": "Pending",
                "Issues_Remarks": "Assigned by Admin",
                "Document_Name": "None"
            }
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Task successfully assigned to {employee_target}!")

elif menu == "Master Task Ledger":
    st.subheader("📊 Complete Status & Grant Tracker")
    st.dataframe(st.session_state.tasks, use_container_width=True)
