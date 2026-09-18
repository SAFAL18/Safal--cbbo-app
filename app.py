import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CBBO Employee Reporting Dashboard", layout="wide"
)

st.title("🌾 CBBO Employee Task & Grant Reporting Software")
st.markdown(
    "Track grant applications, task receipt timelines, and pending workloads efficiently."
)

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

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigation", ["Dashboard Summary", "Manage Tasks", "Manage Grants"]
)

# --- 1. DASHBOARD SUMMARY ---
if menu == "Dashboard Summary":
  st.header("📊 Executive Performance Dashboard")

  col1, col2, col3 = st.columns(3)

  total_tasks = len(st.session_state.tasks)
  pending_tasks = len(
      st.session_state.tasks[st.session_state.tasks["Status"] == "Pending"]
  )
  total_grants_applied = len(st.session_state.grants)

  col1.metric("Total Assigned Tasks", total_tasks)
  col2.metric(
      "Pending Tasks",
      pending_tasks,
      delta=f"-{pending_tasks} remaining",
      delta_color="inverse",
  )
  col3.metric("Total Grants Applied", total_grants_applied)

  st.subheader("Employee Workload Matrix")
  task_summary = (
      st.session_state.tasks.groupby("Employee")["Status"]
      .agg(
          Total_Tasks="count",
          Pending_Tasks=lambda x: (x == "Pending").sum(),
          Completed_Tasks=lambda x: (x == "Completed").sum(),
      )
      .reset_index()
  )

  grant_summary = (
      st.session_state.grants.groupby("Employee")["Grant_ID"]
      .count()
      .reset_index(name="Grants_Applied")
  )

  combined_report = pd.merge(
      task_summary, grant_summary, on="Employee", how="outer"
  ).fillna(0)
  st.dataframe(combined_report, use_container_width=True)

# --- 2. MANAGE TASKS ---
elif menu == "Manage Tasks":
  st.header("📝 Task Tracking (Received & Pending)")

  with st.form("task_form"):
    st.subheader("Assign New Task")
    emp_name = st.text_input("Employee Name")
    t_name = st.text_input("Task Description")
    rec_date = st.date_input("Received Date", datetime.date.today())
    deadline = st.date_input("Deadline")
    submitted = st.form_submit_button("Add Task")

    if submitted:
      new_row = {
          "Task_ID": f"T00{len(st.session_state.tasks)+1}",
          "Employee": emp_name,
          "Task_Name": t_name,
          "Received_Date": str(rec_date),
          "Deadline": str(deadline),
          "Status": "Pending",
      }
      st.session_state.tasks = pd.concat(
          [st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True
      )
      st.success("Task recorded successfully!")

  st.subheader("Current Task Ledger")
  st.dataframe(st.session_state.tasks, use_container_width=True)

# --- 3. MANAGE GRANTS ---
elif menu == "Manage Grants":
  st.header("💰 Grant Application Tracker")

  with st.form("grant_form"):
    st.subheader("Record Grant Application")
    g_emp = st.text_input("Employee Name")
    fpo_n = st.text_input("FPO Name")
    g_name = st.text_input("Grant Scheme Name")
    amount = st.number_input("Amount Applied (INR)", min_value=0.0, step=10000.0)
    app_date = st.date_input("Application Date", datetime.date.today())
    g_status = st.selectbox(
        "Status", ["Submitted", "Under Review", "Approved", "Rejected"]
    )
    g_submitted = st.form_submit_button("Submit Grant Entry")

    if g_submitted:
      new_grant = {
          "Grant_ID": f"G00{len(st.session_state.grants)+1}",
          "Employee": g_emp,
          "FPO_Name": fpo_n,
          "Grant_Name": g_name,
          "Amount": amount,
          "Application_Date": str(app_date),
          "Status": g_status,
      }
      st.session_state.grants = pd.concat(
          [st.session_state.grants, pd.DataFrame([new_grant])],
          ignore_index=True,
      )
      st.success("Grant application logged successfully!")

  st.subheader("Grants History")
  st.dataframe(st.session_state.grants, use_container_width=True)
