import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Import our modules
from predict import ExpensePredictor
from study_plan_agent import AIStudyPlanAgent

# Page config
st.set_page_config(
    page_title="Smart Life Assistant",
    page_icon="🌟",
    layout="wide"
)

# Initialize
@st.cache_resource
def load_models():
    try:
        expense_predictor = ExpensePredictor()
        study_agent = AIStudyPlanAgent()
        return expense_predictor, study_agent
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

# Load user data
def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as f:
            return json.load(f)
    return {'expenses': [], 'study_plan': None}

def save_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f, indent=2)

# Main app
def main():
    st.title("🌟 Smart Life Assistant")
    st.markdown("### AI-Powered Expense Tracking & Study Planning")
    
    # Load models
    expense_predictor, study_agent = load_models()
    user_data = load_user_data()
    
    # Sidebar
    st.sidebar.title("📱 Navigation")
    page = st.sidebar.radio(
        "Choose a feature:",
        ["🏠 Dashboard", "💰 Add Expense", "📊 Expense Analysis", "🎓 Study Plan", "📅 Today's Tasks"]
    )
    
    # Dashboard
    if page == "🏠 Dashboard":
        st.header("📈 Your Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Financial Overview")
            if user_data['expenses']:
                total = sum(e['amount'] for e in user_data['expenses'])
                st.metric("Total Expenses", f"₹{total:,}")
                
                # Category breakdown
                category_totals = {}
                for e in user_data['expenses']:
                    cat = e['category']
                    category_totals[cat] = category_totals.get(cat, 0) + e['amount']
                
                df = pd.DataFrame(list(category_totals.items()), columns=['Category', 'Amount'])
                df = df.sort_values('Amount', ascending=False)
                
                st.bar_chart(df.set_index('Category'))
            else:
                st.info("No expenses tracked yet. Add your first expense!")
        
        with col2:
            st.subheader("🎓 Learning Progress")
            if user_data.get('study_plan'):
                plan = user_data['study_plan']
                st.success(f"**Goal:** {plan['goal']}")
                
                start_date = datetime.strptime(plan['start_date'], '%Y-%m-%d')
                days_since = (datetime.now() - start_date).days
                current_week = (days_since // 7) + 1
                
                progress = min(current_week / plan['total_weeks'] * 100, 100)
                st.progress(progress / 100)
                st.write(f"Week {current_week} of {plan['total_weeks']}")
            else:
                st.info("No study plan yet. Create one to start learning!")
    
    # Add Expense
    elif page == "💰 Add Expense":
        st.header("💰 Add New Expense")
        
        with st.form("expense_form"):
            transaction = st.text_input("Enter transaction (e.g., 'Swiggy order 450')")
            submitted = st.form_submit_button("Categorize & Add")
            
            if submitted and transaction:
                if expense_predictor:
                    result = expense_predictor.predict_category(transaction)
                    
                    # Extract amount
                    import re
                    numbers = re.findall(r'\d+', transaction)
                    amount = int(numbers[0]) if numbers else 0
                    
                    # Add to data
                    expense = {
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'transaction': transaction,
                        'amount': amount,
                        'category': result['category'],
                        'confidence': result['confidence']
                    }
                    user_data['expenses'].append(expense)
                    save_user_data(user_data)
                    
                    st.success("✅ Expense added!")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Category", result['category'])
                    col2.metric("Amount", f"₹{amount}")
                    col3.metric("Confidence", f"{result['confidence']:.1f}%")
    
    # Expense Analysis
    elif page == "📊 Expense Analysis":
        st.header("📊 Expense Analysis")
        
        if not user_data['expenses']:
            st.warning("No expenses to analyze. Add some expenses first!")
        else:
            # Create DataFrame
            df = pd.DataFrame(user_data['expenses'])
            df['date'] = pd.to_datetime(df['date'])
            
            # Stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Expenses", f"₹{df['amount'].sum():,}")
            col2.metric("Transactions", len(df))
            col3.metric("Avg Transaction", f"₹{df['amount'].mean():.0f}")
            
            # Category breakdown
            st.subheader("By Category")
            category_df = df.groupby('category')['amount'].sum().sort_values(ascending=False)
            st.bar_chart(category_df)
            
            # Recent transactions
            st.subheader("Recent Transactions")
            st.dataframe(df[['date', 'transaction', 'category', 'amount']].tail(10))
    
    # Study Plan
    elif page == "🎓 Study Plan":
        st.header("🎓 AI Study Plan Creator")
        
        if user_data.get('study_plan'):
            plan = user_data['study_plan']
            st.success(f"**Active Plan:** {plan['goal']}")
            st.write(f"**Duration:** {plan['total_weeks']} weeks")
            st.write(f"**Daily Hours:** {plan['hours_per_day']}")
            st.write(f"**Started:** {plan['start_date']}")
            
            if st.button("Create New Plan"):
                user_data['study_plan'] = None
                save_user_data(user_data)
                st.rerun()
        else:
            st.write("### Choose Your Learning Path")
            
            goal_options = {
                'Machine Learning Engineer': 'machine_learning',
                'Full Stack Web Developer': 'web_development',
                'Data Scientist': 'data_science',
                'Tech Interview Prep': 'interview_prep'
            }
            
            selected_goal = st.selectbox("Select your goal:", list(goal_options.keys()))
            hours_per_day = st.slider("Hours you can study daily:", 1, 8, 3)
            
            if st.button("Create Study Plan"):
                goal_key = goal_options[selected_goal]
                plan = study_agent.create_study_plan(goal_key, hours_per_day)
                user_data['study_plan'] = plan
                save_user_data(user_data)
                st.success("✅ Study plan created!")
                st.rerun()
    
    # Today's Tasks
    elif page == "📅 Today's Tasks":
        st.header("📅 Today's Study Tasks")
        
        if not user_data.get('study_plan'):
            st.warning("No study plan found. Create one first!")
        else:
            today_plan = study_agent.get_today_plan(user_data['study_plan'])
            
            if today_plan['status'] == 'active':
                st.success(f"**Week {today_plan['week']}:** {today_plan['topic']}")
                st.info(f"**Time Allocated:** {today_plan['hours_allocated']} hours")
                
                st.subheader("✅ Today's Tasks")
                for task in today_plan['tasks']:
                    st.write(f"• {task}")
                
                st.subheader("📚 Resources")
                for resource in today_plan['resources']:
                    st.write(f"• {resource}")
            else:
                st.info(today_plan.get('message', 'No tasks for today'))

if __name__ == "__main__":
    main()