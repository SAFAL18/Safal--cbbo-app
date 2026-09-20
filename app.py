import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="CBBO Management Portal", layout="wide")

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
    st.title("🔐 CBBO Software Login Portal")
    st.markdown("Please enter your individual username and password.")

    with st.form("login_form"):
        username_input = st.text_input("Username (e.g. rakesh, admin)").strip().lower()
        password_input = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")

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

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

current_user_name = st.session_state.name
current_role = st.session_state.role

st.title("🌾 CBBO Task & FPO Grant Management Portal")
st.markdown(f"Welcome, **{current_user_name}** ({current_role})")

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
    menu = st.sidebar.selectbox("Navigation", ["My Assigned Tasks", "Submit Daily Progress"])
else:
    menu = st.sidebar.selectbox("Navigation", ["Admin Dashboard", "Assign New Task", "All Tasks Status"])


# --- VIEW: EMPLOYEE - MY ASSIGNED TASKS ---
if menu == "My Assigned Tasks":
    st.header(f"📋 Tasks Assigned to {current_user_name}")
    
    my_tasks = st.session_state.tasks[st.session_state.tasks["Employee"] == current_user_name]
    
    if not my_tasks.empty:
        st.dataframe(my_tasks, use_container_width=True)
        
        st.subheader("Update Task Status")
        selected_task_id = st.selectbox("Select Task ID to Update", my_tasks["Task_ID"].tolist())
        new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed"])
        new_remark = st.text_input("Add Issue / Remarks (if any)")
        
        if st.button("Save Task Progress"):
            st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Status"] = new_status
            st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task_id, "Issues_Remarks"] = new_remark
            st.success("Task updated successfully! It is now updated on the Admin portal.")
            st.rerun()
    else:
        st.info("No tasks currently assigned to you.")

elif menu == "Submit Daily Progress":
    st.header("📝 Daily FPO Work Progress Form")
    with st.form("daily_progress"):
        fpo_target = st.text_input("FPO Name", value="Kishni Safal Farmer Producer Company Limited")
        work_done = st.text_area("Today's Work Details / Documents Completed")
        status_update = st.selectbox("Current Status", ["Pending", "In Progress", "Completed"])
        issues = st.text_input("Pending Items / Issues (e.g., Rent Agreement Etc)")
        
        if st.form_submit_button("Submit Update"):
            st.success("Daily progress recorded!")


# --- VIEW: ADMIN DASHBOARD ---
elif menu == "Admin Dashboard":
    st.header("👑 Admin Overview & Control Center")
    
    total_t = len(st.session_state.tasks)
    pending_t = len(st.session_state.tasks[st.session_state.tasks["Status"] == "Pending"])
    completed_t = len(st.session_state.tasks[st.session_state.tasks["Status"] == "Completed"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", total_t)
    col2.metric("Pending Tasks", pending_t)
    col3.metric("Completed Tasks", completed_t)
    
    st.subheader("Live Master Task Ledger")
    st.dataframe(st.session_state.tasks, use_container_width=True)

elif menu == "Assign New Task":
    st.header("➕ Assign Task to Staff")
    
    with st.form("assign_form"):
        employee_target = st.selectbox("Select Staff", ["Rakesh", "Ayushi", "Praveen", "Navneet"])
        fpo_name = st.text_input("FPO Name", placeholder="e.g., Kishni Safal Farmer Producer Company Limited")
        task_desc = st.text_input("Task Description (e.g., 3rd CBBO Cost)")
        deadline = st.date_input("Deadline Date")
        
        if st.form_submit_button("Assign Task"):
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
            st.success(f"Task successfully assigned to {employee_target}! It will now show up on their portal as Pending.")

elif menu == "All Tasks Status":
    st.header("📋 Complete Status Tracker")
    st.dataframe(st.session_state.tasks, use_container_width=True)
