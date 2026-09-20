import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="CBBO Employee Reporting Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Complete HTML & Tailwind Dashboard Embedded
dashboard_html = """
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBBO Employee Reporting Dashboard</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0fdf4',
                            100: '#dcfce7',
                            500: '#22c55e',
                            600: '#16a34a',
                            700: '#15803d',
                            800: '#166534',
                            900: '#14532d',
                        }
                    }
                }
            }
        }
    </script>
    <!-- Inter Font -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 h-full flex flex-col">

    <!-- Top Header -->
    <header class="bg-brand-800 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="bg-brand-600 p-2.5 rounded-xl shadow-inner text-white flex items-center justify-center">
                    <i class="fa-solid fa-seedling text-2xl"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight">CBBO Connect</h1>
                    <p class="text-xs text-brand-100">Capacity Building & Businessing Organization Portal</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <span id="currentDateDisplay" class="text-xs bg-brand-900 px-3 py-1.5 rounded-full text-brand-100 font-medium"></span>
                <button onclick="openModal('exportModal')" class="bg-brand-700 hover:bg-brand-600 text-white text-xs font-semibold px-4 py-2 rounded-lg transition shadow-sm flex items-center gap-2">
                    <i class="fa-solid fa-download"></i> Export Data
                </button>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs Bar -->
    <nav class="bg-white border-b border-gray-200 shadow-xs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-8 overflow-x-auto">
            <button onclick="switchTab('dashboard')" id="tab-dashboard" class="tab-btn py-4 px-1 border-b-2 font-medium text-sm border-brand-600 text-brand-700 flex items-center gap-2 whitespace-nowrap">
                <i class="fa-solid fa-chart-pie"></i> Dashboard Overview
            </button>
            <button onclick="switchTab('tasks')" id="tab-tasks" class="tab-btn py-4 px-1 border-b-2 font-medium text-sm border-transparent text-gray-500 hover:text-gray-700 flex items-center gap-2 whitespace-nowrap">
                <i class="fa-solid fa-list-check"></i> Task Tracking
            </button>
            <button onclick="switchTab('grants')" id="tab-grants" class="tab-btn py-4 px-1 border-b-2 font-medium text-sm border-transparent text-gray-500 hover:text-gray-700 flex items-center gap-2 whitespace-nowrap">
                <i class="fa-solid fa-file-invoice-dollar"></i> Grant Applications
            </button>
            <button onclick="switchTab('employees')" id="tab-employees" class="tab-btn py-4 px-1 border-b-2 font-medium text-sm border-transparent text-gray-500 hover:text-gray-700 flex items-center gap-2 whitespace-nowrap">
                <i class="fa-solid fa-users"></i> Employee Workload
            </button>
        </div>
    </nav>

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 overflow-y-auto">

        <!-- ==================== TAB 1: DASHBOARD ==================== -->
        <div id="view-dashboard" class="space-y-6">
            <!-- Welcome Banner -->
            <div class="bg-gradient-to-r from-brand-700 to-brand-900 rounded-2xl p-6 text-white shadow-md flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 class="text-2xl font-bold">Welcome back, CBBO Admin</h2>
                    <p class="text-sm text-brand-100 mt-1">Here is your real-time overview of FPO grants applied, task timeliness, and employee pending workloads.</p>
                </div>
                <div class="flex gap-2">
                    <button onclick="openModal('taskModal')" class="bg-white text-brand-800 hover:bg-brand-50 text-xs font-bold px-4 py-2.5 rounded-xl transition shadow-xs flex items-center gap-2">
                        <i class="fa-solid fa-plus text-brand-600"></i> New Task
                    </button>
                    <button onclick="openModal('grantModal')" class="bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition shadow-xs flex items-center gap-2 border border-brand-500">
                        <i class="fa-solid fa-coins"></i> Record Grant
                    </button>
                </div>
            </div>

            <!-- Metrics Cards Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-xs flex items-center justify-between">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-wider text-gray-500">Total Grants Applied</p>
                        <h3 id="stat-total-grants" class="text-3xl font-bold text-gray-900 mt-1">0</h3>
                        <p class="text-xs text-brand-600 mt-1 font-medium"><i class="fa-solid fa-arrow-up"></i> <span id="stat-grant-amount">₹0</span> Total FPO Funding</p>
                    </div>
                    <div class="w-12 h-12 bg-emerald-50 text-brand-600 rounded-xl flex items-center justify-center text-xl shadow-inner">
                        <i class="fa-solid fa-hand-holding-dollar"></i>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-xs flex items-center justify-between">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-wider text-gray-500">Total Assigned Tasks</p>
                        <h3 id="stat-total-tasks" class="text-3xl font-bold text-gray-900 mt-1">0</h3>
                        <p class="text-xs text-blue-600 mt-1 font-medium">Active workloads recorded</p>
                    </div>
                    <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center text-xl shadow-inner">
                        <i class="fa-solid fa-tasks"></i>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-xs flex items-center justify-between">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-wider text-gray-500">Pending Tasks</p>
                        <h3 id="stat-pending-tasks" class="text-3xl font-bold text-amber-600 mt-1">0</h3>
                        <p class="text-xs text-amber-600 mt-1 font-medium">Requires attention & follow-up</p>
                    </div>
                    <div class="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center text-xl shadow-inner">
                        <i class="fa-solid fa-clock-rotate-left"></i>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-xs flex items-center justify-between">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-wider text-gray-500">Task Completion Rate</p>
                        <h3 id="stat-completion-rate" class="text-3xl font-bold text-purple-600 mt-1">0%</h3>
                        <p class="text-xs text-purple-600 mt-1 font-medium">Efficiency metric</p>
                    </div>
                    <div class="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center text-xl shadow-inner">
                        <i class="fa-solid fa-chart-line"></i>
                    </div>
                </div>
            </div>

            <!-- Quick Summaries Section -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Recent Pending Tasks Widget -->
                <div class="bg-white rounded-2xl border border-gray-100 shadow-xs p-6 flex flex-col">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-gray-900 flex items-center gap-2">
                            <i class="fa-solid fa-triangle-exclamation text-amber-500"></i> Urgent Pending Tasks
                        </h3>
                        <button onclick="switchTab('tasks')" class="text-xs text-brand-600 font-semibold hover:underline">View All</button>
                    </div>
                    <div id="dashboard-pending-list" class="space-y-3 overflow-y-auto max-h-80">
                        <!-- Populated by JS -->
                    </div>
                </div>

                <!-- Recent Grants Widget -->
                <div class="bg-white rounded-2xl border border-gray-100 shadow-xs p-6 flex flex-col">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-gray-900 flex items-center gap-2">
                            <i class="fa-solid fa-award text-emerald-600"></i> Latest Grant Applications
                        </h3>
                        <button onclick="switchTab('grants')" class="text-xs text-brand-600 font-semibold hover:underline">View All</button>
                    </div>
                    <div id="dashboard-grants-list" class="space-y-3 overflow-y-auto max-h-80">
                        <!-- Populated by JS -->
                    </div>
                </div>
            </div>
        </div>

        <!-- ==================== TAB 2: TASKS ==================== -->
        <div id="view-tasks" class="space-y-6 hidden">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-gray-100 shadow-xs">
                <div>
                    <h2 class="text-xl font-bold text-gray-900">Task Receipt & Status Tracking</h2>
                    <p class="text-xs text-gray-500 mt-0.5">Track when employees received tasks, deadlines, and current pending status.</p>
                </div>
                <div class="flex items-center gap-3 w-full sm:w-auto">
                    <input type="text" id="taskSearchInput" placeholder="Search tasks or employee..." onkeyup="renderTasksTable()" class="text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 w-full sm:w-64">
                    <button onclick="openModal('taskModal')" class="bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold px-4 py-2.5 rounded-xl transition shadow-xs flex items-center gap-2 whitespace-nowrap">
                        <i class="fa-solid fa-plus"></i> Add Task
                    </button>
                </div>
            </div>

            <!-- Tasks Table Container -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-xs overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gray-50 border-b border-gray-100 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                <th class="py-3.5 px-6">Task ID / Name</th>
                                <th class="py-3.5 px-6">Employee</th>
                                <th class="py-3.5 px-6">Received Date</th>
                                <th class="py-3.5 px-6">Deadline</th>
                                <th class="py-3.5 px-6">Status</th>
                                <th class="py-3.5 px-6 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="tasksTableBody" class="divide-y divide-gray-100 text-sm">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ==================== TAB 3: GRANTS ==================== -->
        <div id="view-grants" class="space-y-6 hidden">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-gray-100 shadow-xs">
                <div>
                    <h2 class="text-xl font-bold text-gray-900">Grant Applications Ledger</h2>
                    <p class="text-xs text-gray-500 mt-0.5">Monitor all grants applied by CBBO staff on behalf of FPOs.</p>
                </div>
                <div class="flex items-center gap-3 w-full sm:w-auto">
                    <input type="text" id="grantSearchInput" placeholder="Search FPO or grant..." onkeyup="renderGrantsTable()" class="text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 w-full sm:w-64">
                    <button onclick="openModal('grantModal')" class="bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold px-4 py-2.5 rounded-xl transition shadow-xs flex items-center gap-2 whitespace-nowrap">
                        <i class="fa-solid fa-plus"></i> Record Grant
                    </button>
                </div>
            </div>

            <!-- Grants Table Container -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-xs overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gray-50 border-b border-gray-100 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                <th class="py-3.5 px-6">Grant ID</th>
                                <th class="py-3.5 px-6">FPO Name</th>
                                <th class="py-3.5 px-6">Grant Scheme</th>
                                <th class="py-3.5 px-6">Employee In-Charge</th>
                                <th class="py-3.5 px-6">Amount Applied</th>
                                <th class="py-3.5 px-6">Application Date</th>
                                <th class="py-3.5 px-6">Status</th>
                                <th class="py-3.5 px-6 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="grantsTableBody" class="divide-y divide-gray-100 text-sm">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ==================== TAB 4: EMPLOYEES ==================== -->
        <div id="view-employees" class="space-y-6 hidden">
            <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-xs flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h2 class="text-xl font-bold text-gray-900">Employee Workload Summary</h2>
                    <p class="text-xs text-gray-500 mt-0.5">Aggregated breakdown of tasks assigned, pending tasks, and grant submissions per employee.</p>
                </div>
            </div>

            <!-- Employee Matrix Table -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-xs overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gray-50 border-b border-gray-100 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                <th class="py-3.5 px-6">Employee Name</th>
                                <th class="py-3.5 px-6">Total Tasks Assigned</th>
                                <th class="py-3.5 px-6">Tasks Pending</th>
                                <th class="py-3.5 px-6">Tasks Completed</th>
                                <th class="py-3.5 px-6">Grants Applied Count</th>
                                <th class="py-3.5 px-6">Total Grant Value (₹)</th>
                            </tr>
                        </thead>
                        <tbody id="employeeSummaryTableBody" class="divide-y divide-gray-100 text-sm">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- MODAL 1: ADD / EDIT TASK -->
    <div id="taskModal" class="fixed inset-0 bg-black/50 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-xl border border-gray-100">
            <div class="flex justify-between items-center mb-4">
                <h3 id="taskModalTitle" class="text-lg font-bold text-gray-900">Assign New Task</h3>
                <button onclick="closeModal('taskModal')" class="text-gray-400 hover:text-gray-600 p-1"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <form id="taskForm" onsubmit="handleTaskSubmit(event)" class="space-y-4">
                <input type="hidden" id="editTaskId">
                <div>
                    <label class="block text-xs font-semibold text-gray-700 mb-1">Task Title / Description</label>
                    <input type="text" id="taskNameInput" required placeholder="e.g. FPO Business Plan Drafting" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 mb-1">Employee Name</label>
                    <input type="text" id="taskEmpInput" required placeholder="e.g. Aarav Sharma" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-700 mb-1">Received Date</label>
                        <input type="date" id="taskRecDateInput" required class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-700 mb-1">Deadline</label>
                        <input type="date" id="taskDeadlineInput" required class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 mb-1">Status</label>
                    <select id="taskStatusInput" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                        <option value="Pending">Pending</option>
                        <option value="In Progress">In Progress</option>
                        <option value="Completed">Completed</option>
                    </select>
                </div>
                <div class="flex justify-end gap-3 pt-2">
                    <button type="button" onclick="closeModal('taskModal')" class="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl transition">Cancel</button>
                    <button type="submit" class="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-xl transition shadow-sm">Save Task</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL 2: ADD / EDIT GRANT -->
    <div id="grantModal" class="fixed inset-0 bg-black/50 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-xl border border-gray-100">
            <div class="flex justify-between items-center mb-4">
                <h3 id="grantModalTitle" class="text-lg font-bold text-gray-900">Record Grant Application</h3>
                <button onclick="closeModal('grantModal')" class="text-gray-400 hover:text-gray-600 p-1"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <form id="grantForm" onsubmit="handleGrantSubmit(event)" class="space-y-4">
                <input type="hidden" id="editGrantId">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-700 mb-1">FPO Name</label>
                        <input type="text" id="grantFpoInput" required placeholder="e.g. Krishi Vikas FPO" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-700 mb-1">Grant Scheme Name</label>
                        <input type="text" id="grantSchemeInput" required placeholder="e.g. Equity Grant Scheme" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 mb-1">Employee In-Charge</label>
                    <input type="text" id="grantEmpInput" required placeholder="e.g. Priya Verma" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-700 mb-1">Amount Applied (₹)</label>
                        <input type="number" id="grantAmountInput" min="0" step="1000" required placeholder="1500000" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-700 mb-1">Application Date</label>
                        <input type="date" id="grantDateInput" required class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-700 mb-1">Application Status</label>
                    <select id="grantStatusInput" class="w-full text-xs px-3.5 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:outline-none">
                        <option value="Submitted">Submitted</option>
                        <option value="Under Review">Under Review</option>
                        <option value="Sanctioned">Sanctioned</option>
                        <option value="Rejected">Rejected</option>
                    </select>
                </div>
                <div class="flex justify-end gap-3 pt-2">
                    <button type="button" onclick="closeModal('grantModal')" class="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl transition">Cancel</button>
                    <button type="submit" class="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-xl transition shadow-sm">Save Grant</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL 3: EXPORT DATA -->
    <div id="exportModal" class="fixed inset-0 bg-black/50 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-gray-100 text-center space-y-4">
            <div class="w-14 h-14 bg-emerald-50 text-brand-600 rounded-2xl flex items-center justify-center text-2xl mx-auto shadow-inner">
                <i class="fa-solid fa-file-excel"></i>
            </div>
            <h3 class="text-lg font-bold text-gray-900">Export CBBO Reports</h3>
            <p class="text-xs text-gray-500">Download active task logs and grant application records in CSV format for local reporting.</p>
            <div class="flex flex-col gap-2 pt-2">
                <button onclick="exportCSV('tasks')" class="w-full py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold rounded-xl transition shadow-xs flex items-center justify-center gap-2">
                    <i class="fa-solid fa-download"></i> Download Tasks Report (.csv)
                </button>
                <button onclick="exportCSV('grants')" class="w-full py-2.5 bg-gray-900 hover:bg-gray-800 text-white text-xs font-semibold rounded-xl transition shadow-xs flex items-center justify-center gap-2">
                    <i class="fa-solid fa-download"></i> Download Grants Report (.csv)
                </button>
                <button onclick="closeModal('exportModal')" class="mt-2 text-xs text-gray-500 hover:text-gray-700 font-medium">Close</button>
            </div>
        </div>
    </div>

    <!-- Application JavaScript Logic -->
    <script>
        let tasks = JSON.parse(localStorage.getItem('cbbo_tasks')) || [
            { id: 'T-101', name: 'FPO Business Plan Formulation', employee: 'Aarav Sharma', receivedDate: '2026-09-01', deadline: '2026-09-18', status: 'Pending' },
            { id: 'T-102', name: 'Soil & Water Testing Campaign', employee: 'Priya Verma', receivedDate: '2026-09-04', deadline: '2026-09-15', status: 'Completed' },
            { id: 'T-103', name: 'Matching Equity Grant Documentation', employee: 'Aarav Sharma', receivedDate: '2026-09-08', deadline: '2026-09-25', status: 'Pending' },
            { id: 'T-104', name: 'Organic Certification Audit Prep', employee: 'Ramesh Gupta', receivedDate: '2026-09-10', deadline: '2026-09-22', status: 'In Progress' }
        ];

        let grants = JSON.parse(localStorage.getItem('cbbo_grants')) || [
            { id: 'G-501', fpo: 'Krishi Vikas FPO', scheme: 'Equity Grant Scheme', employee: 'Aarav Sharma', amount: 1500000, date: '2026-09-02', status: 'Sanctioned' },
            { id: 'G-502', fpo: 'Annapurna Organic FPO', scheme: 'Infrastructure & Machinery Grant', employee: 'Priya Verma', amount: 2500000, date: '2026-09-06', status: 'Submitted' },
            { id: 'G-503', fpo: 'Kisan Shakti FPO', scheme: 'Working Capital Support', employee: 'Ramesh Gupta', amount: 1000000, date: '2026-09-11', status: 'Under Review' }
        ];

        function saveData() {
            localStorage.setItem('cbbo_tasks', JSON.stringify(tasks));
            localStorage.setItem('cbbo_grants', JSON.stringify(grants));
            updateMetrics();
        }

        document.getElementById('currentDateDisplay').innerText = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });

        function switchTab(tabId) {
            ['dashboard', 'tasks', 'grants', 'employees'].forEach(t => {
                document.getElementById(`view-${t}`).classList.add('hidden');
                document.getElementById(`tab-${t}`).classList.remove('border-brand-600', 'text-brand-700');
                document.getElementById(`tab-${t}`).classList.add('border-transparent', 'text-gray-500');
            });
            document.getElementById(`view-${tabId}`).classList.remove('hidden');
            document.getElementById(`tab-${tabId}`).classList.add('border-brand-600', 'text-brand-700');
            document.getElementById(`tab-${tabId}`).classList.remove('border-transparent', 'text-gray-500');

            if(tabId === 'dashboard') renderDashboard();
            if(tabId === 'tasks') renderTasksTable();
            if(tabId === 'grants') renderGrantsTable();
            if(tabId === 'employees') renderEmployeeSummary();
        }

        function openModal(modalId) {
            if(modalId === 'taskModal') {
                document.getElementById('taskForm').reset();
                document.getElementById('editTaskId').value = '';
                document.getElementById('taskModalTitle').innerText = 'Assign New Task';
                document.getElementById('taskRecDateInput').valueAsDate = new Date();
            } else if(modalId === 'grantModal') {
                document.getElementById('grantForm').reset();
                document.getElementById('editGrantId').value = '';
                document.getElementById('grantModalTitle').innerText = 'Record Grant Application';
                document.getElementById('grantDateInput').valueAsDate = new Date();
            }
            document.getElementById(modalId).classList.remove('hidden');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.add('hidden');
        }

        function updateMetrics() {
            const totalTasks = tasks.length;
            const pendingTasks = tasks.filter(t => t.status === 'Pending' || t.status === 'In Progress').length;
            const completedTasks = tasks.filter(t => t.status === 'Completed').length;
            const totalGrants = grants.length;
            const totalAmount = grants.reduce((acc, curr) => acc + Number(curr.amount), 0);
            const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

            document.getElementById('stat-total-tasks').innerText = totalTasks;
            document.getElementById('stat-pending-tasks').innerText = pendingTasks;
            document.getElementById('stat-total-grants').innerText = totalGrants;
            document.getElementById('stat-grant-amount').innerText = formatCurrency(totalAmount);
            document.getElementById('stat-completion-rate').innerText = completionRate + '%';

            renderDashboardWidgets();
        }

        function formatCurrency(amount) {
            if(amount >= 10000000) return '₹' + (amount / 10000000).toFixed(2) + ' Cr';
            if(amount >= 100000) return '₹' + (amount / 100000).toFixed(2) + ' Lakh';
            return '₹' + amount.toLocaleString('en-IN');
        }

        function renderDashboardWidgets() {
            const pendingListEl = document.getElementById('dashboard-pending-list');
            const pendingTasks = tasks.filter(t => t.status !== 'Completed');
            if(pendingTasks.length === 0) {
                pendingListEl.innerHTML = '<p class="text-xs text-gray-400 text-center py-4">No pending tasks. Great job!</p>';
            } else {
                pendingListEl.innerHTML = pendingTasks.map(t => `
                    <div class="p-3 bg-amber-50/50 border border-amber-100 rounded-xl flex items-center justify-between text-xs">
                        <div>
                            <p class="font-bold text-gray-800">${t.name}</p>
                            <p class="text-gray-500 mt-0.5"><i class="fa-solid fa-user-tie"></i> ${t.employee} &bull; <i class="fa-regular fa-calendar"></i> Recv: ${t.receivedDate}</p>
                        </div>
                        <span class="px-2.5 py-1 bg-amber-100 text-amber-800 rounded-full font-semibold text-[10px]">${t.status}</span>
                    </div>
                `).join('');
            }

            const grantsListEl = document.getElementById('dashboard-grants-list');
            if(grants.length === 0) {
                grantsListEl.innerHTML = '<p class="text-xs text-gray-400 text-center py-4">No grants recorded yet.</p>';
            } else {
                grantsListEl.innerHTML = grants.slice(0, 4).map(g => `
                    <div class="p-3 bg-emerald-50/50 border border-emerald-100 rounded-xl flex items-center justify-between text-xs">
                        <div>
                            <p class="font-bold text-gray-800">${g.fpo}</p>
                            <p class="text-gray-500 mt-0.5">${g.scheme} (${formatCurrency(g.amount)})</p>
                        </div>
                        <span class="px-2.5 py-1 bg-emerald-100 text-emerald-800 rounded-full font-semibold text-[10px]">${g.status}</span>
                    </div>
                `).join('');
            }
        }

        function renderTasksTable() {
            const query = (document.getElementById('taskSearchInput')?.value || '').toLowerCase();
            const tbody = document.getElementById('tasksTableBody');
            const filtered = tasks.filter(t => t.name.toLowerCase().includes(query) || t.employee.toLowerCase().includes(query) || t.id.toLowerCase().includes(query));

            if(filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="text-center py-8 text-gray-400 text-xs">No tasks found matching your search.</td></tr>`;
                return;
            }

            tbody.innerHTML = filtered.map(t => {
                let badgeColor = 'bg-amber-100 text-amber-800';
                if(t.status === 'Completed') badgeColor = 'bg-emerald-100 text-emerald-800';
                if(t.status === 'In Progress') badgeColor = 'bg-blue-100 text-blue-800';

                return `
                    <tr class="hover:bg-gray-50/50 transition">
                        <td class="py-4 px-6 font-semibold text-gray-900">
                            <div>${t.name}</div>
                            <div class="text-[11px] text-gray-400 font-normal">ID: ${t.id}</div>
                        </td>
                        <td class="py-4 px-6 text-gray-600 font-medium">${t.employee}</td>
                        <td class="py-4 px-6 text-gray-600">${t.receivedDate}</td>
                        <td class="py-4 px-6 text-gray-600">${t.deadline}</td>
                        <td class="py-4 px-6"><span class="px-2.5 py-1 rounded-full text-xs font-semibold ${badgeColor}">${t.status}</span></td>
                        <td class="py-4 px-6 text-right space-x-2">
                            <button onclick="editTask('${t.id}')" class="text-gray-400 hover:text-brand-600 p-1"><i class="fa-solid fa-pen-to-square"></i></button>
                            <button onclick="deleteTask('${t.id}')" class="text-gray-400 hover:text-red-600 p-1"><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function renderGrantsTable() {
            const query = (document.getElementById('grantSearchInput')?.value || '').toLowerCase();
            const tbody = document.getElementById('grantsTableBody');
            const filtered = grants.filter(g => g.fpo.toLowerCase().includes(query) || g.scheme.toLowerCase().includes(query) || g.employee.toLowerCase().includes(query));

            if(filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-gray-400 text-xs">No grant records found.</td></tr>`;
                return;
            }

            tbody.innerHTML = filtered.map(g => {
                let badgeColor = 'bg-amber-100 text-amber-800';
                if(g.status === 'Sanctioned') badgeColor = 'bg-emerald-100 text-emerald-800';
                if(g.status === 'Rejected') badgeColor = 'bg-red-100 text-red-800';
                if(g.status === 'Under Review') badgeColor = 'bg-blue-100 text-blue-800';

                return `
                    <tr class="hover:bg-gray-50/50 transition">
                        <td class="py-4 px-6 font-semibold text-gray-500 text-xs">${g.id}</td>
                        <td class="py-4 px-6 font-bold text-gray-900">${g.fpo}</td>
                        <td class="py-4 px-6 text-gray-600">${g.scheme}</td>
                        <td class="py-4 px-6 text-gray-600 font-medium">${g.employee}</td>
                        <td class="py-4 px-6 font-bold text-brand-700">${formatCurrency(g.amount)}</td>
                        <td class="py-4 px-6 text-gray-600">${g.date}</td>
                        <td class="py-4 px-6"><span class="px-2.5 py-1 rounded-full text-xs font-semibold ${badgeColor}">${g.status}</span></td>
                        <td class="py-4 px-6 text-right space-x-2">
                            <button onclick="editGrant('${g.id}')" class="text-gray-400 hover:text-brand-600 p-1"><i class="fa-solid fa-pen-to-square"></i></button>
                            <button onclick="deleteGrant('${g.id}')" class="text-gray-400 hover:text-red-600 p-1"><i class="fa-solid fa-trash"></i></button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function renderEmployeeSummary() {
            const tbody = document.getElementById('employeeSummaryTableBody');
            const empMap = {};
            tasks.forEach(t => {
                if(!empMap[t.employee]) empMap[t.employee] = { totalTasks: 0, pendingTasks: 0, completedTasks: 0, grantsCount: 0, grantsAmount: 0 };
                empMap[t.employee].totalTasks++;
                if(t.status === 'Pending' || t.status === 'In Progress') empMap[t.employee].pendingTasks++;
                if(t.status === 'Completed') empMap[t.employee].completedTasks++;
            });

            grants.forEach(g => {
                if(!empMap[g.employee]) empMap[g.employee] = { totalTasks: 0, pendingTasks: 0, completedTasks: 0, grantsCount: 0, grantsAmount: 0 };
                empMap[g.employee].grantsCount++;
                empMap[g.employee].grantsAmount += Number(g.amount);
            });

            const employees = Object.keys(empMap);
            if(employees.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="text-center py-8 text-gray-400 text-xs">No employee records available.</td></tr>`;
                return;
            }

            tbody.innerHTML = employees.map(emp => {
                const data = empMap[emp];
                return `
                    <tr class="hover:bg-gray-50/50 transition">
                        <td class="py-4 px-6 font-bold text-gray-900 flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-xs">${emp.charAt(0)}</div>
                            ${emp}
                        </td>
                        <td class="py-4 px-6 text-gray-700 font-semibold">${data.totalTasks}</td>
                        <td class="py-4 px-6 font-bold text-amber-600">${data.pendingTasks}</td>
                        <td class="py-4 px-6 font-semibold text-emerald-600">${data.completedTasks}</td>
                        <td class="py-4 px-6 text-gray-700 font-semibold">${data.grantsCount}</td>
                        <td class="py-4 px-6 font-bold text-brand-700">${formatCurrency(data.grantsAmount)}</td>
                    </tr>
                `;
            }).join('');
        }

        function handleTaskSubmit(e) {
            e.preventDefault();
            const editId = document.getElementById('editTaskId').value;
            const name = document.getElementById('taskNameInput').value;
            const employee = document.getElementById('taskEmpInput').value;
            const receivedDate = document.getElementById('taskRecDateInput').value;
            const deadline = document.getElementById('taskDeadlineInput').value;
            const status = document.getElementById('taskStatusInput').value;

            if(editId) {
                tasks = tasks.map(t => t.id === editId ? { ...t, name, employee, receivedDate, deadline, status } : t);
            } else {
                const newId = 'T-' + Math.floor(100 + Math.random() * 900);
                tasks.unshift({ id: newId, name, employee, receivedDate, deadline, status });
            }

            saveData();
            closeModal('taskModal');
            renderTasksTable();
            renderDashboard();
        }

        function handleGrantSubmit(e) {
            e.preventDefault();
            const editId = document.getElementById('editGrantId').value;
            const fpo = document.getElementById('grantFpoInput').value;
            const scheme = document.getElementById('grantSchemeInput').value;
            const employee = document.getElementById('grantEmpInput').value;
            const amount = document.getElementById('grantAmountInput').value;
            const date = document.getElementById('grantDateInput').value;
            const status = document.getElementById('grantStatusInput').value;

            if(editId) {
                grants = grants.map(g => g.id === editId ? { ...g, fpo, scheme, employee, amount, date, status } : g);
            } else {
                const newId = 'G-' + Math.floor(500 + Math.random() * 500);
                grants.unshift({ id: newId, fpo, scheme, employee, amount, date, status });
            }

            saveData();
            closeModal('grantModal');
            renderGrantsTable();
            renderDashboard();
        }

        function editTask(id) {
            const task = tasks.find(t => t.id === id);
            if(!task) return;
            document.getElementById('editTaskId').value = task.id;
            document.getElementById('taskNameInput').value = task.name;
            document.getElementById('taskEmpInput').value = task.employee;
            document.getElementById('taskRecDateInput').value = task.receivedDate;
            document.getElementById('taskDeadlineInput').value = task.deadline;
            document.getElementById('taskStatusInput').value = task.status;
            document.getElementById('taskModalTitle').innerText = 'Edit Task Details';
            document.getElementById('taskModal').classList.remove('hidden');
        }

        function deleteTask(id) {
            if(confirm('Are you sure you want to delete this task?')) {
                tasks = tasks.filter(t => t.id !== id);
                saveData();
                renderTasksTable();
            }
        }

        function editGrant(id) {
            const grant = grants.find(g => g.id === id);
            if(!grant) return;
            document.getElementById('editGrantId').value = grant.id;
            document.getElementById('grantFpoInput').value = grant.fpo;
            document.getElementById('grantSchemeInput').value = grant.scheme;
            document.getElementById('grantEmpInput').value = grant.employee;
            document.getElementById('grantAmountInput').value = grant.amount;
            document.getElementById('grantDateInput').value = grant.date;
            document.getElementById('grantStatusInput').value = grant.status;
            document.getElementById('grantModalTitle').innerText = 'Edit Grant Application';
            document.getElementById('grantModal').classList.remove('hidden');
        }

        function deleteGrant(id) {
            if(confirm('Are you sure you want to delete this grant record?')) {
                grants = grants.filter(g => g.id !== id);
                saveData();
                renderGrantsTable();
            }
        }

        function exportCSV(type) {
            let csvContent = "data:text/csv;charset=utf-8,";
            if(type === 'tasks') {
                csvContent += "Task ID,Task Name,Employee,Received Date,Deadline,Status\\r\\n";
                tasks.forEach(t => {
                    csvContent += `"${t.id}","${t.name}","${t.employee}","${t.receivedDate}","${t.deadline}","${t.status}"\\r\\n`;
                });
            } else {
                csvContent += "Grant ID,FPO Name,Scheme,Employee,Amount,Application Date,Status\\r\\n";
                grants.forEach(g => {
                    csvContent += `"${g.id}","${g.fpo}","${g.scheme}","${g.employee}","${g.amount}","${g.date}","${g.status}"\\r\\n`;
                });
            }

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `CBBO_${type}_report.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            closeModal('exportModal');
        }

        function renderDashboard() {
            updateMetrics();
            renderDashboardWidgets();
        }

        window.onload = function() {
            updateMetrics();
            renderDashboard();
        }
    </script>
</body>
</html>
"""

# Render the dashboard inside Streamlit application container
components.html(dashboard_html, height=850, scrolling=True)
