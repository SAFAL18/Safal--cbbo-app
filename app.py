import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CBBO Employee Reporting Dashboard", layout="wide"
)

# --- USER CREDENTIALS DATABASE ---
# You can add or change employee usernames and passwords here!
USER_CREDENTIALS = {
    "admin": {"password": "adminpassword123", "role": "Employer / Admin", "name": "Admin Boss"},
    "aarav": {"password": "password123", "role": "Employee", "name": "Aarav Sharma"},
    "priya": {"password": "password456", "role": "Employee", "name": "Priya Verma"},
    "rahul": {"password": "password789", "role": "Employee", "name": "Rahul Singh"},
 "ayushi": {"password": "password421", "role": "Employee", "name": "Ayushi Agrawal"},
}

# --- LOGIN SCREEN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 CBBO Software Login Portal")
    st.markdown("Please enter your employee username and password to access your dashboard.")

    with st.form("login_form"):
        username_input = st.text_input("Username").strip().lower()
        password_input = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")

        if submit_login:
            if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.role = USER_CREDENTIALS[username_input]["role"]
                st.session_state.name = USER_CREDENTIALS[username_input]["name"]
                st.success("Login successful! Loading dashboard...")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")
    st.stop()

# --- LOGOUT BUTTON IN SIDEBAR ---
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

current_user_name = st.session_state.name
current_role = st.session_state.role

st.title("🌾 CBBO Employee Task & Grant Reporting Software")
st.markdown(f"Welcome back, **{current_user_name}** ({current_role})")

# Mock Database / State Initialization
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(
        [
            {
                "Task_ID": "T001",
                "Employee": "Aarav Sharma",
                "Task_Name": "FPO Business Plan Draft",
                "Received_Date": "2026-09-01",
                "Deadline": "2026-09-15",
                "Status": "Pending",
            },
            {
                "Task_ID": "T002",
                "Employee": "Priya Verma",
                "Task_Name": "Soil Testing Camp Org",
                "Received_Date": "2026-09-05",
                "Deadline": "2026-09-18",
                "Status": "Completed",
            },
            {
                "Task_ID": "T003",
                "Employee": "Aarav Sharma",
                "Task_Name": "Matching Grant Form Submission",
                "Received_Date": "2026-09-10",
                "Deadline": "2026-09-25",
                "Status": "Pending",
            },
            {
                "Task_ID": "T004",
                "Employee": "Ayushi Agrawal",
                "Date": "2026-09-18",
            "CBBO_Name": "Ashok Agritech",
            "FPO_Name": "Narsinghpur FPO",
            "Grant_Name": "Grant 4",
            "Total_Documents": 10,
            "Completed_Documents": 4,
            "Progress_Percent": 40,
            "Pending_Details": Rent Agreement Etc,
            "Issues_Remarks": Document verification delayed due to stamp paper shortage,
        }
            },
        ]
    )

if "grants" not in st.session_state:
    st.session_state.grants = pd.DataFrame(
        [
            {
                "Grant_ID": "G001",
                "Employee": "Aarav Sharma",
                "FPO_Name": "Krishi Vikas FPO",
                "Grant_Name": "Equity Grant Scheme",
                "Amount": 1500000,
                "Application_Date": "2026-09-02",
                "Status": "Submitted",
            },
            {
                "Grant_ID": "G002",
                "Employee": "Priya Verma",
                "Task_Name": "Infrastructure Grant",
                "FPO_Name": "Annapurna FPO",
                "Amount": 1000000,
                "Application_Date": "2026-09-08",
                "Status": "Approved",
            },
        ]
    )

# --- ROLE-BASED NAVIGATION ---
if current_role == "Employee":
    menu = st.sidebar.selectbox("Navigation", ["My Tasks", "Log Grant Application"])
else:
    menu = st.sidebar.selectbox("Navigation", ["Admin Dashboard", "Manage All Tasks", "Manage All Grants"])


# --- VIEW 1: EMPLOYEE - MY TASKS ---
if menu == "My Tasks":
    st.header(f"📝 Tasks Assigned to {current_user_name}")
    
    my_tasks = st.session_state.tasks[st.session_state.tasks["Employee"] == current_user_name]
    st.dataframe(my_tasks, use_container_width=True)

    st.subheader("Update Task Status")
    if not my_tasks.empty:
        selected_task = st.selectbox("Select Task ID to Update", my_tasks["Task_ID"].tolist())
        new_status = st.selectbox("New Status", ["Pending", "Completed"])
        if st.button("Update My Task Status"):
            st.session_state.tasks.loc[st.session_state.tasks["Task_ID"] == selected_task, "Status"] = new_status
            st.success("Task status updated successfully!")
            st.rerun()
    else:
        st.info("You have no tasks currently assigned.")

# --- VIEW 2: EMPLOYEE - LOG GRANT APPLICATION ---
elif menu == "Log Grant Application":
    st.header("💰 Log Grant Application")
    with st.form("grant_form"):
        fpo_n = st.text_input("FPO Name")
        g_name = st.text_input("Grant Scheme Name")
        amount = st.number_input("Amount Applied (INR)", min_value=0.0, step=10000.0)
        app_date = st.date_input("Application Date", datetime.date.today())
        g_status = st.selectbox("Status", ["Submitted", "Under Review", "Approved", "Rejected"])
        g_submitted = st.form_submit_button("Submit Grant Entry")

        if g_submitted:
            new_grant = {
                "Grant_ID": f"G00{len(st.session_state.grants)+1}",
                "Employee": current_user_name,
                "FPO_Name": fpo_n,
                "Grant_Name": g_name,
                "Amount": amount,
                "Application_Date": str(app_date),
                "Status": g_status,
            }
            st.session_state.grants = pd.concat([st.session_state.grants, pd.DataFrame([new_grant])], ignore_index=True)
            st.success("Grant application logged successfully!")

    st.subheader("Your Submitted Grants")
    my_grants = st.session_state.grants[st.session_state.grants["Employee"] == current_user_name]
    st.dataframe(my_grants, use_container_width=True)


# --- VIEW 3: ADMIN DASHBOARD ---
elif menu == "Admin Dashboard":
    st.header("📊 Employer / Admin Performance Control Center")

    col1, col2, col3 = st.columns(3)
    total_tasks = len(st.session_state.tasks)
    pending_tasks = len(st.session_state.tasks[st.session_state.tasks["Status"] == "Pending"])
    total_grants = len(st.session_state.grants)

    col1.metric("Total Tasks Assigned", total_tasks)
    col2.metric("Total Pending Tasks", pending_tasks)
    col3.metric("Total Grants Applied", total_grants)

    st.subheader("All Employees Workload Summary")
    task_summary = st.session_state.tasks.groupby("Employee")["Status"].agg(
        Total_Tasks="count",
        Pending_Tasks=lambda x: (x == "Pending").sum(),
        Completed_Tasks=lambda x: (x == "Completed").sum()
    ).reset_index()

    grant_summary = st.session_state.grants.groupby("Employee")["Grant_ID"].count().reset_index(name="Grants_Applied")
    combined_report = pd.merge(task_summary, grant_summary, on="Employee", how="outer").fillna(0)
    st.dataframe(combined_report, use_container_width=True)


# --- VIEW 4: ADMIN - MANAGE TASKS ---
elif menu == "Manage All Tasks":
    st.header("📋 Assign & Manage All Employee Tasks")

    with st.form("assign_task"):
        emp_target = st.selectbox("Assign To Employee", ["Aarav Sharma", "Priya Verma", "Rahul Singh"])
        t_name = st.text_input("Task Description")
        rec_date = st.date_input("Received Date", datetime.date.today())
        deadline = st.date_input("Deadline")
        if st.form_submit_button("Assign Task"):
            new_row = {
                "Task_ID": f"T00{len(st.session_state.tasks)+1}",
                "Employee": emp_target,
                "Task_Name": t_name,
                "Received_Date": str(rec_date),
                "Deadline": str(deadline),
                "Status": "Pending",
            }
            st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Task successfully assigned to {emp_target}!")

    st.subheader("Complete Master Task Ledger")
    st.dataframe(st.session_state.tasks, use_container_width=True)


# --- VIEW 5: ADMIN - MANAGE GRANTS ---
elif menu == "Manage All Grants":
    st.header("💰 Master Grants Ledger (All Employees)")
    st.dataframe(st.session_state.grants, use_container_width=True)
