"""
Smart Budget Planner - Flask Backend
Main application file with REST API routes
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from database import (
    init_database, add_expense, get_all_expenses, get_expense_by_id,
    update_expense, delete_expense, set_monthly_budget, get_monthly_budget,
    get_total_expenses, get_expenses_by_category
)
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize database on startup
init_database()


# ============================================================================
# DASHBOARD ROUTES
# ============================================================================

@app.route('/')
def index():
    """
    Render the main dashboard page
    """
    return render_template('index.html')


# ============================================================================
# EXPENSE API ROUTES
# ============================================================================

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """
    GET /api/expenses
    Fetch all expenses
    
    Returns:
        JSON: List of all expenses with status 200
    """
    try:
        expenses = get_all_expenses()
        return jsonify({
            'success': True,
            'data': expenses,
            'total_count': len(expenses)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/expenses', methods=['POST'])
def create_expense():
    """
    POST /api/expenses
    Create a new expense
    
    JSON Body:
        - amount (float, required): Expense amount
        - category (str, required): Expense category
        - description (str, optional): Expense description
        - date (str, required): Expense date (YYYY-MM-DD format)
    
    Returns:
        JSON: Created expense data with status 201, or error with 400
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'amount' not in data or 'category' not in data or 'date' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: amount, category, date'
            }), 400
        
        # Validate amount is a positive number
        try:
            amount = float(data['amount'])
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid amount: {str(e)}'
            }), 400
        
        # Validate date format
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
        
        # Add expense to database
        expense_id = add_expense(
            amount=amount,
            category=data['category'],
            description=data.get('description', ''),
            date=data['date']
        )
        
        if expense_id:
            expense = get_expense_by_id(expense_id)
            return jsonify({
                'success': True,
                'data': expense,
                'message': 'Expense created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create expense'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/expenses/<int:expense_id>', methods=['GET'])
def get_single_expense(expense_id):
    """
    GET /api/expenses/<expense_id>
    Fetch a specific expense by ID
    
    Returns:
        JSON: Expense data with status 200, or error with 404
    """
    try:
        expense = get_expense_by_id(expense_id)
        if expense:
            return jsonify({
                'success': True,
                'data': expense
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Expense not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_single_expense(expense_id):
    """
    PUT /api/expenses/<expense_id>
    Update an existing expense
    
    JSON Body:
        - amount (float, optional): Updated amount
        - category (str, optional): Updated category
        - description (str, optional): Updated description
        - date (str, optional): Updated date
    
    Returns:
        JSON: Updated expense data with status 200, or error
    """
    try:
        data = request.get_json()
        
        # Get existing expense
        expense = get_expense_by_id(expense_id)
        if not expense:
            return jsonify({
                'success': False,
                'error': 'Expense not found'
            }), 404
        
        # Update fields or keep existing values
        amount = data.get('amount', expense['amount'])
        category = data.get('category', expense['category'])
        description = data.get('description', expense['description'])
        date = data.get('date', expense['date'])
        
        # Validate amount if provided
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid amount: {str(e)}'
            }), 400
        
        # Validate date if provided
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
        
        # Update expense
        if update_expense(expense_id, amount, category, description, date):
            updated_expense = get_expense_by_id(expense_id)
            return jsonify({
                'success': True,
                'data': updated_expense,
                'message': 'Expense updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update expense'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_single_expense(expense_id):
    """
    DELETE /api/expenses/<expense_id>
    Delete an expense
    
    Returns:
        JSON: Success message with status 200, or error with 404
    """
    try:
        # Check if expense exists
        expense = get_expense_by_id(expense_id)
        if not expense:
            return jsonify({
                'success': False,
                'error': 'Expense not found'
            }), 404
        
        if delete_expense(expense_id):
            return jsonify({
                'success': True,
                'message': 'Expense deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete expense'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# BUDGET API ROUTES
# ============================================================================

@app.route('/api/budget', methods=['GET'])
def get_budget():
    """
    GET /api/budget
    Fetch current budget and calculate remaining amount
    
    Returns:
        JSON: Budget information with status 200
    """
    try:
        monthly_limit = get_monthly_budget()
        total_spent = get_total_expenses()
        remaining = monthly_limit - total_spent
        budget_percentage = (total_spent / monthly_limit * 100) if monthly_limit > 0 else 0
        
        # Determine budget status
        if budget_percentage >= 100:
            status = 'exceeded'
        elif budget_percentage >= 80:
            status = 'warning'
        else:
            status = 'safe'
        
        return jsonify({
            'success': True,
            'data': {
                'monthly_limit': monthly_limit,
                'total_spent': round(total_spent, 2),
                'remaining': round(remaining, 2),
                'percentage_used': round(budget_percentage, 2),
                'status': status
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/budget', methods=['POST'])
def set_budget():
    """
    POST /api/budget
    Set or update the monthly budget
    
    JSON Body:
        - monthly_limit (float, required): New monthly budget limit
    
    Returns:
        JSON: Updated budget with status 200, or error with 400
    """
    try:
        data = request.get_json()
        
        if not data or 'monthly_limit' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: monthly_limit'
            }), 400
        
        try:
            amount = float(data['monthly_limit'])
            if amount <= 0:
                raise ValueError("Monthly limit must be positive")
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid amount: {str(e)}'
            }), 400
        
        if set_monthly_budget(amount):
            return jsonify({
                'success': True,
                'data': {
                    'monthly_limit': amount
                },
                'message': 'Budget updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update budget'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ANALYSIS & INSIGHTS ROUTES
# ============================================================================

@app.route('/api/analytics/category-summary', methods=['GET'])
def get_category_summary():
    """
    GET /api/analytics/category-summary
    Get spending summary by category using Pandas
    
    Returns:
        JSON: Category-wise spending analysis with status 200
    """
    try:
        expenses = get_all_expenses()
        
        if not expenses:
            return jsonify({
                'success': True,
                'data': {
                    'categories': [],
                    'highest_category': None,
                    'total': 0
                }
            }), 200
        
        # Create DataFrame from expenses
        df = pd.DataFrame(expenses)
        
        # Get current month expenses
        current_date = datetime.now()
        year_month = f"{current_date.year}-{current_date.month:02d}"
        df['date'] = pd.to_datetime(df['date'])
        df_current = df[df['date'].dt.to_period('M') == df['date'].dt.to_period('M').iloc[0]]
        
        # Aggregate by category
        category_summary = df_current.groupby('category')['amount'].agg(['sum', 'count']).round(2)
        category_summary = category_summary.sort_values('sum', ascending=False)
        
        # Convert to dict for JSON response
        categories_data = []
        for category, row in category_summary.iterrows():
            categories_data.append({
                'category': category,
                'total': round(row['sum'], 2),
                'count': int(row['count']),
                'average': round(row['sum'] / row['count'], 2)
            })
        
        # Get highest spending category
        highest = categories_data[0] if categories_data else None
        
        return jsonify({
            'success': True,
            'data': {
                'categories': categories_data,
                'highest_category': highest,
                'total': round(df_current['amount'].sum(), 2),
                'average_spending': round(df_current['amount'].mean(), 2)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analytics/trends', methods=['GET'])
def get_expense_trends():
    """
    GET /api/analytics/trends
    Get expense trends over time (last 30 days)
    
    Returns:
        JSON: Daily expense trends with status 200
    """
    try:
        expenses = get_all_expenses()
        
        if not expenses:
            return jsonify({
                'success': True,
                'data': {
                    'daily_expenses': [],
                    'weekly_summary': []
                }
            }), 200
        
        # Create DataFrame
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        
        # Get last 30 days
        df = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
        
        # Daily summary
        daily_summary = df.groupby(df['date'].dt.date)['amount'].sum().round(2)
        daily_data = [{'date': str(date), 'amount': amount} for date, amount in daily_summary.items()]
        
        # Weekly summary
        df['week'] = df['date'].dt.to_period('W').apply(lambda x: str(x.start_time.date()))
        weekly_summary = df.groupby('week')['amount'].sum().round(2)
        weekly_data = [{'week': week, 'amount': amount} for week, amount in weekly_summary.items()]
        
        return jsonify({
            'success': True,
            'data': {
                'daily_expenses': daily_data,
                'weekly_summary': weekly_data
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analytics/insights', methods=['GET'])
def get_insights():
    """
    GET /api/analytics/insights
    Generate smart spending insights
    
    Returns:
        JSON: Spending insights and recommendations with status 200
    """
    try:
        expenses = get_all_expenses()
        monthly_limit = get_monthly_budget()
        total_spent = get_total_expenses()
        
        insights = []
        
        if not expenses:
            insights.append({
                'type': 'info',
                'message': 'No expenses recorded yet. Start adding expenses to get insights!'
            })
        else:
            df = pd.DataFrame(expenses)
            df['date'] = pd.to_datetime(df['date'])
            
            # Get current month data
            current_date = datetime.now()
            year_month = f"{current_date.year}-{current_date.month:02d}"
            df_current = df[df['date'].dt.to_period('M') == df['date'].dt.to_period('M').iloc[0]]
            
            if len(df_current) > 0:
                avg_daily = df_current['amount'].sum() / current_date.day
                projected_monthly = avg_daily * 30
                
                # Budget warning
                if total_spent > monthly_limit:
                    insights.append({
                        'type': 'danger',
                        'message': f'⚠️ Budget exceeded by ${round(total_spent - monthly_limit, 2)}!'
                    })
                elif total_spent / monthly_limit >= 0.8:
                    insights.append({
                        'type': 'warning',
                        'message': f'💡 You have used {round(total_spent / monthly_limit * 100, 1)}% of your budget'
                    })
                else:
                    insights.append({
                        'type': 'success',
                        'message': f'✓ You are on track with your budget'
                    })
                
                # Category insights
                category_spending = df_current.groupby('category')['amount'].sum().sort_values(ascending=False)
                if len(category_spending) > 0:
                    top_category = category_spending.index[0]
                    top_amount = category_spending.iloc[0]
                    insights.append({
                        'type': 'info',
                        'message': f'📊 Highest spending: {top_category} (${round(top_amount, 2)})'
                    })
                
                # Projection insights
                if projected_monthly > monthly_limit:
                    over_amount = projected_monthly - monthly_limit
                    insights.append({
                        'type': 'warning',
                        'message': f'📈 Based on current rate, you might exceed budget by ${round(over_amount, 2)}'
                    })
        
        return jsonify({
            'success': True,
            'data': {
                'insights': insights,
                'total_spent': round(total_spent, 2),
                'monthly_limit': monthly_limit,
                'remaining': round(monthly_limit - total_spent, 2)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analytics/chart-data', methods=['GET'])
def get_chart_data():
    """
    GET /api/analytics/chart-data
    Get data formatted for Chart.js visualizations
    
    Returns:
        JSON: Data for pie, bar, and line charts with status 200
    """
    try:
        expenses = get_all_expenses()
        
        if not expenses:
            return jsonify({
                'success': True,
                'data': {
                    'pie_chart': {'labels': [], 'data': []},
                    'bar_chart': {'labels': [], 'data': []},
                    'line_chart': {'labels': [], 'data': []}
                }
            }), 200
        
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        
        # Current month data
        current_date = datetime.now()
        year_month = f"{current_date.year}-{current_date.month:02d}"
        df_current = df[df['date'].dt.to_period('M') == df['date'].dt.to_period('M').iloc[0]]
        
        # PIE CHART: Category distribution
        category_totals = df_current.groupby('category')['amount'].sum().sort_values(ascending=False)
        pie_labels = category_totals.index.tolist()
        pie_data = [round(x, 2) for x in category_totals.values.tolist()]
        
        # BAR CHART: Last 7 days
        df_last_7 = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
        daily_totals = df_last_7.groupby(df_last_7['date'].dt.date)['amount'].sum()
        bar_labels = [str(date) for date in daily_totals.index]
        bar_data = [round(x, 2) for x in daily_totals.values]
        
        # LINE CHART: Last 30 days (daily trend)
        df_last_30 = df[df['date'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
        daily_30 = df_last_30.groupby(df_last_30['date'].dt.date)['amount'].sum()
        line_labels = [str(date) for date in daily_30.index]
        line_data = [round(x, 2) for x in daily_30.values]
        
        return jsonify({
            'success': True,
            'data': {
                'pie_chart': {
                    'labels': pie_labels,
                    'data': pie_data
                },
                'bar_chart': {
                    'labels': bar_labels,
                    'data': bar_data
                },
                'line_chart': {
                    'labels': line_labels,
                    'data': line_data
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Route not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run Flask development server
    app.run(debug=True, host='localhost', port=5000)
