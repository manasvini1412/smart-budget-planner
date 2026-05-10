/**
 * Smart Budget Planner - JavaScript Frontend
 * Handles UI interactions, API calls, and Chart.js integration
 */

// ============================================================================
// GLOBAL VARIABLES
// ============================================================================

// Chart instances
let pieChart = null;
let barChart = null;
let lineChart = null;

// Current editing expense ID (null if adding new)
let editingExpenseId = null;

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize the application on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Budget Planner App Initialized');
    
    // Set today's date as default in expense form
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('expense-date').value = today;
    
    // Load dashboard on startup
    loadDashboard();
    
    // Add smooth scrolling
    setupScrolling();
});

/**
 * Setup smooth scrolling for navigation
 */
function setupScrolling() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            // Remove active class from all links
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
}

// ============================================================================
// NAVIGATION & SECTION MANAGEMENT
// ============================================================================

/**
 * Show a specific section and hide others
 * @param {string} sectionId - ID of section to show
 */
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
    }
    
    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'expenses': 'Manage Expenses',
        'analytics': 'Spending Analytics',
        'settings': 'Budget Settings'
    };
    document.getElementById('page-title').textContent = titles[sectionId] || 'Dashboard';
    
    // Load section-specific data
    if (sectionId === 'analytics') {
        loadAnalytics();
    }
}

// ============================================================================
// DASHBOARD OPERATIONS
// ============================================================================

/**
 * Load and display dashboard data
 */
async function loadDashboard() {
    try {
        showSection('dashboard');
        
        // Fetch budget info
        const budgetResponse = await fetch('/api/budget');
        const budgetData = await budgetResponse.json();
        
        // Fetch insights
        const insightsResponse = await fetch('/api/analytics/insights');
        const insightsData = await insightsResponse.json();
        
        // Fetch chart data
        const chartResponse = await fetch('/api/analytics/chart-data');
        const chartData = await chartResponse.json();
        
        if (budgetData.success) {
            updateDashboardMetrics(budgetData.data);
        }
        
        if (insightsData.success) {
            updateInsights(insightsData.data.insights);
        }
        
        if (chartData.success) {
            updateCharts(chartData.data);
        }
        
        // Display alerts
        displayBudgetAlerts(budgetData.data);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Error loading dashboard', 'error');
    }
}

/**
 * Update dashboard metric cards
 * @param {object} budgetData - Budget information
 */
function updateDashboardMetrics(budgetData) {
    // Format currency values
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(value);
    };
    
    // Update metric cards
    document.getElementById('metric-budget').textContent = formatCurrency(budgetData.monthly_limit);
    document.getElementById('metric-spent').textContent = formatCurrency(budgetData.total_spent);
    document.getElementById('metric-remaining').textContent = formatCurrency(budgetData.remaining);
    document.getElementById('metric-percentage').textContent = `${budgetData.percentage_used}% Used`;
    
    // Update progress bar
    const progressFill = document.getElementById('progress-fill');
    progressFill.style.width = `${Math.min(budgetData.percentage_used, 100)}%`;
    
    // Change progress bar color based on status
    if (budgetData.status === 'exceeded') {
        progressFill.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
    } else if (budgetData.status === 'warning') {
        progressFill.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
    } else {
        progressFill.style.background = 'linear-gradient(90deg, #6366f1, #818cf8)';
    }
}

/**
 * Display budget alerts based on spending status
 * @param {object} budgetData - Budget information
 */
function displayBudgetAlerts(budgetData) {
    const alertsContainer = document.getElementById('alerts-container');
    alertsContainer.innerHTML = '';
    
    const percentage = budgetData.percentage_used;
    
    if (budgetData.status === 'exceeded') {
        const alert = createAlert(
            'danger',
            '❌ Budget Exceeded',
            `Your spending has exceeded your monthly budget by ₹${(budgetData.total_spent - budgetData.monthly_limit).toFixed(2)}`
        );
        alertsContainer.appendChild(alert);
    } else if (budgetData.status === 'warning') {
        const alert = createAlert(
            'warning',
            '⚠️ High Spending Alert',
            `You have used ${percentage}% of your monthly budget. Please be cautious with remaining expenses.`
        );
        alertsContainer.appendChild(alert);
    } else {
        const alert = createAlert(
            'success',
            '✓ On Budget',
            `You have ₹${budgetData.remaining.toFixed(2)} remaining in your budget for this month.`
        );
        alertsContainer.appendChild(alert);
    }
}

/**
 * Create an alert element
 * @param {string} type - Alert type (success, warning, danger, info)
 * @param {string} title - Alert title
 * @param {string} message - Alert message
 * @returns {HTMLElement} Alert element
 */
function createAlert(type, title, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${type}`;
    alertDiv.innerHTML = `
        <div class="alert-icon">
            ${type === 'success' ? '✓' : type === 'warning' ? '⚠️' : type === 'danger' ? '❌' : 'ℹ️'}
        </div>
        <div>
            <strong>${title}</strong>
            <p style="margin-top: 0.25rem;">${message}</p>
        </div>
    `;
    return alertDiv;
}

/**
 * Update insights section
 * @param {array} insights - Array of insight objects
 */
function updateInsights(insights) {
    const insightsContainer = document.getElementById('insights-container');
    insightsContainer.innerHTML = '';
    
    insights.forEach(insight => {
        const insightDiv = document.createElement('div');
        insightDiv.className = `insight-item ${insight.type}`;
        insightDiv.innerHTML = `<div class="insight-message">${insight.message}</div>`;
        insightsContainer.appendChild(insightDiv);
    });
}

// ============================================================================
// CHART OPERATIONS
// ============================================================================

/**
 * Update all charts with new data
 * @param {object} chartData - Chart data from API
 */
function updateCharts(chartData) {
    updatePieChart(chartData.pie_chart);
    updateBarChart(chartData.bar_chart);
    updateLineChart(chartData.line_chart);
}

/**
 * Update or create pie chart (category distribution)
 * @param {object} pieData - Pie chart data
 */
function updatePieChart(pieData) {
    const pieCtx = document.getElementById('pieChart');
    
    // Define color palette
    const colors = [
        '#6366f1',
        '#ec4899',
        '#10b981',
        '#f59e0b',
        '#3b82f6',
        '#8b5cf6',
        '#ef4444',
        '#14b8a6'
    ];
    
    // Destroy existing chart if it exists
    if (pieChart) {
        pieChart.destroy();
    }
    
    // Create new pie chart
    pieChart = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: pieData.labels,
            datasets: [{
                data: pieData.data,
                backgroundColor: colors.slice(0, pieData.labels.length),
                borderColor: '#ffffff',
                borderWidth: 2,
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 12
                        },
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = '₹' + context.parsed.toFixed(2);
                            return label + ': ' + value;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Update or create bar chart (last 7 days)
 * @param {object} barData - Bar chart data
 */
function updateBarChart(barData) {
    const barCtx = document.getElementById('barChart');
    
    // Destroy existing chart if it exists
    if (barChart) {
        barChart.destroy();
    }
    
    // Create new bar chart
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: barData.labels,
            datasets: [{
                label: 'Daily Spending',
                data: barData.data,
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                borderColor: 'rgb(99, 102, 241)',
                borderWidth: 1,
                borderRadius: 5,
                hoverBackgroundColor: 'rgba(79, 70, 229, 0.9)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '₹' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

/**
 * Update or create line chart (30-day trend)
 * @param {object} lineData - Line chart data
 */
function updateLineChart(lineData) {
    const lineCtx = document.getElementById('lineChart');
    
    // Destroy existing chart if it exists
    if (lineChart) {
        lineChart.destroy();
    }
    
    // Create new line chart
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: lineData.labels,
            datasets: [{
                label: '30-Day Spending Trend',
                data: lineData.data,
                borderColor: 'rgb(99, 102, 241)',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: 'rgb(99, 102, 241)',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointHoverRadius: 6,
                hoverBackgroundColor: 'rgba(99, 102, 241, 0.8)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '₹' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

// ============================================================================
// EXPENSE MANAGEMENT
// ============================================================================

/**
 * Open the add expense modal/form
 */
function openExpenseModal() {
    editingExpenseId = null;
    document.getElementById('form-title').textContent = 'Add New Expense';
    document.getElementById('expense-form').reset();
    
    // Set today's date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('expense-date').value = today;
    
    document.getElementById('expense-form-container').classList.remove('hidden');
}

/**
 * Close the expense form
 */
function closeExpenseForm() {
    document.getElementById('expense-form-container').classList.add('hidden');
    document.getElementById('expense-form').reset();
    editingExpenseId = null;
}

/**
 * Handle expense form submission (add or update)
 * @param {Event} event - Form submit event
 */
async function handleExpenseSubmit(event) {
    event.preventDefault();
    
    // Get form values
    const amount = parseFloat(document.getElementById('expense-amount').value);
    const category = document.getElementById('expense-category').value;
    const description = document.getElementById('expense-description').value;
    const date = document.getElementById('expense-date').value;
    
    // Validate form
    if (!amount || amount <= 0) {
        showToast('Please enter a valid amount', 'error');
        return;
    }
    
    if (!category) {
        showToast('Please select a category', 'error');
        return;
    }
    
    if (!date) {
        showToast('Please select a date', 'error');
        return;
    }
    
    try {
        let response;
        let url = '/api/expenses';
        let method = 'POST';
        
        // Prepare data
        const expenseData = {
            amount: amount,
            category: category,
            description: description,
            date: date
        };
        
        if (editingExpenseId) {
            // Update existing expense
            url = `/api/expenses/${editingExpenseId}`;
            method = 'PUT';
        }
        
        response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(expenseData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(
                editingExpenseId ? 'Expense updated successfully' : 'Expense added successfully',
                'success'
            );
            closeExpenseForm();
            loadExpenses();
            loadDashboard();
        } else {
            showToast('Error: ' + (data.error || 'Failed to save expense'), 'error');
        }
    } catch (error) {
        console.error('Error submitting expense:', error);
        showToast('Error saving expense', 'error');
    }
}

/**
 * Load and display all expenses
 */
async function loadExpenses() {
    try {
        showSection('expenses');
        
        const response = await fetch('/api/expenses');
        const data = await response.json();
        
        if (data.success) {
            displayExpenses(data.data);
        } else {
            showToast('Error loading expenses', 'error');
        }
    } catch (error) {
        console.error('Error loading expenses:', error);
        showToast('Error loading expenses', 'error');
    }
}

/**
 * Display expenses in table format
 * @param {array} expenses - Array of expense objects
 */
function displayExpenses(expenses) {
    const tbody = document.getElementById('expenses-tbody');
    const emptyMessage = document.getElementById('empty-expenses-message');
    
    tbody.innerHTML = '';
    
    if (expenses.length === 0) {
        emptyMessage.style.display = 'block';
        return;
    }
    
    emptyMessage.style.display = 'none';
    
    // Get category emojis
    const categoryEmojis = {
        'Food': '🍔',
        'Transportation': '🚗',
        'Entertainment': '🎬',
        'Shopping': '🛍️',
        'Utilities': '⚡',
        'Healthcare': '⚕️',
        'Education': '📚',
        'Other': '📌'
    };
    
    expenses.forEach(expense => {
        const row = document.createElement('tr');
        const emoji = categoryEmojis[expense.category] || '📌';
        
        row.innerHTML = `
            <td>${formatDate(expense.date)}</td>
            <td>${emoji} ${expense.category}</td>
            <td>${expense.description}</td>
            <td class="expense-amount">₹${parseFloat(expense.amount).toFixed(2)}</td>
            <td>
                <div class="table-actions">
                    <button class="btn btn-sm btn-edit" onclick="editExpense(${expense.id})">Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteExpense(${expense.id})">Delete</button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Edit an existing expense
 * @param {number} expenseId - ID of expense to edit
 */
async function editExpense(expenseId) {
    try {
        const response = await fetch(`/api/expenses/${expenseId}`);
        const data = await response.json();
        
        if (data.success) {
            const expense = data.data;
            
            // Populate form with expense data
            editingExpenseId = expenseId;
            document.getElementById('form-title').textContent = 'Edit Expense';
            document.getElementById('expense-amount').value = expense.amount;
            document.getElementById('expense-category').value = expense.category;
            document.getElementById('expense-description').value = expense.description;
            document.getElementById('expense-date').value = expense.date;
            
            // Show form
            document.getElementById('expense-form-container').classList.remove('hidden');
            document.getElementById('expense-amount').focus();
        } else {
            showToast('Error loading expense', 'error');
        }
    } catch (error) {
        console.error('Error editing expense:', error);
        showToast('Error loading expense', 'error');
    }
}

/**
 * Delete an expense after confirmation
 * @param {number} expenseId - ID of expense to delete
 */
async function deleteExpense(expenseId) {
    if (!confirm('Are you sure you want to delete this expense? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/expenses/${expenseId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Expense deleted successfully', 'success');
            loadExpenses();
            loadDashboard();
        } else {
            showToast('Error deleting expense', 'error');
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
        showToast('Error deleting expense', 'error');
    }
}

// ============================================================================
// ANALYTICS OPERATIONS
// ============================================================================

/**
 * Load and display analytics
 */
async function loadAnalytics() {
    try {
        // Fetch category summary
        const categoryResponse = await fetch('/api/analytics/category-summary');
        const categoryData = await categoryResponse.json();
        
        // Fetch trends
        const trendsResponse = await fetch('/api/analytics/trends');
        const trendsData = await trendsResponse.json();
        
        if (categoryData.success) {
            displayCategorySummary(categoryData.data);
        }
        
        if (trendsData.success) {
            displayTrendsSummary(trendsData.data);
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        showToast('Error loading analytics', 'error');
    }
}

/**
 * Display category-wise spending summary
 * @param {object} data - Category summary data
 */
function displayCategorySummary(data) {
    const container = document.getElementById('category-summary');
    container.innerHTML = '';
    
    if (data.categories.length === 0) {
        container.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; color: #94a3b8;">No expenses in any category yet</p>';
        return;
    }
    
    data.categories.forEach(cat => {
        const categoryDiv = document.createElement('div');
        categoryDiv.className = 'category-item';
        categoryDiv.innerHTML = `
            <div class="category-name">${cat.category}</div>
            <div class="category-info">
                <span>Total: ₹${cat.total}</span>
                <span>${cat.count} expenses</span>
            </div>
            <div class="category-info" style="margin-top: 0.5rem;">
                <span>Avg: ₹${cat.average}</span>
            </div>
        `;
        container.appendChild(categoryDiv);
    });
}

/**
 * Display spending trends (daily and weekly)
 * @param {object} data - Trends data
 */
function displayTrendsSummary(data) {
    const container = document.getElementById('trends-summary');
    container.innerHTML = '';
    
    if (data.daily_expenses.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #94a3b8;">No expense data available</p>';
        return;
    }
    
    // Create simple trend table
    let html = '<table class="trend-table"><thead><tr><th>Date</th><th>Amount</th></tr></thead><tbody>';
    
    data.daily_expenses.forEach(expense => {
        html += `
            <tr>
                <td>${formatDate(expense.date)}</td>
                <td>₹${parseFloat(expense.amount).toFixed(2)}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// ============================================================================
// SETTINGS OPERATIONS
// ============================================================================

/**
 * Update monthly budget
 */
async function updateBudget() {
    const budgetInput = document.getElementById('budget-input');
    const amount = parseFloat(budgetInput.value);
    
    if (!amount || amount <= 0) {
        showToast('Please enter a valid budget amount', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/budget', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                monthly_limit: amount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Budget updated successfully', 'success');
            loadDashboard();
        } else {
            showToast('Error updating budget', 'error');
        }
    } catch (error) {
        console.error('Error updating budget:', error);
        showToast('Error updating budget', 'error');
    }
}

/**
 * Export data to CSV
 */
function exportData() {
    try {
        // Fetch all expenses
        fetch('/api/expenses')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.data.length > 0) {
                    // Create CSV content
                    let csv = 'Date,Category,Description,Amount\n';
                    
                    data.data.forEach(expense => {
                        const amount = parseFloat(expense.amount).toFixed(2);
                        const description = (expense.description || '').replace(/"/g, '""');
                        csv += `"${expense.date}","${expense.category}","${description}","₹${amount}"\n`;
                    });
                    
                    // Create blob and download
                    const blob = new Blob([csv], { type: 'text/csv' });
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = `budget_planner_export_${new Date().toISOString().split('T')[0]}.csv`;
                    link.click();
                    
                    showToast('Data exported successfully', 'success');
                } else {
                    showToast('No data to export', 'warning');
                }
            });
    } catch (error) {
        console.error('Error exporting data:', error);
        showToast('Error exporting data', 'error');
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Format date string to readable format
 * @param {string} dateStr - Date string (YYYY-MM-DD)
 * @returns {string} Formatted date
 */
function formatDate(dateStr) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateStr).toLocaleDateString('en-US', options);
}

/**
 * Show toast notification
 * @param {string} message - Toast message
 * @param {string} type - Toast type (success, error, warning, info)
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div>${message}</div>
    `;
    
    // Add to container
    container.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

// Update budget input when dashboard loads
window.addEventListener('load', function() {
    // Fetch current budget and populate settings
    fetch('/api/budget')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('budget-input').value = data.data.monthly_limit;
            }
        })
        .catch(error => console.error('Error loading budget:', error));
});
