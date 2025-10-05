"""
SMART LIFE ASSISTANT
Combines Expense Categorizer + AI Study Plan Agent
"""

import pickle
import re
import json
from datetime import datetime, timedelta

# Import our modules
try:
    from predict import ExpensePredictor
except:
    print("Warning: Could not import ExpensePredictor")

try:
    from study_plan_agent import AIStudyPlanAgent
except:
    print("Warning: Could not import AIStudyPlanAgent")


class SmartLifeAssistant:
    """Unified assistant for expenses and study planning"""
    
    def __init__(self):
        try:
            self.expense_predictor = ExpensePredictor()
            print("✓ Expense Categorizer loaded")
        except:
            self.expense_predictor = None
            print("✗ Expense Categorizer not available")
        
        self.study_agent = AIStudyPlanAgent()
        print("✓ Study Plan Agent loaded")
        
        self.user_data = self._load_user_data()
    
    def _load_user_data(self):
        """Load user data from file"""
        try:
            with open('user_data.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'expenses': [],
                'study_plan': None,
                'monthly_budget': 0,
                'learning_budget': 0
            }
    
    def _save_user_data(self):
        """Save user data to file"""
        with open('user_data.json', 'w') as f:
            json.dump(self.user_data, f, indent=2)
    
    def add_expense(self, transaction_text, amount=None):
        """Add and categorize an expense"""
        if not self.expense_predictor:
            return None
        
        result = self.expense_predictor.predict_category(transaction_text)
        
        # Extract amount if not provided
        if amount is None:
            numbers = re.findall(r'\d+', transaction_text)
            amount = int(numbers[0]) if numbers else 0
        
        expense = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'transaction': transaction_text,
            'amount': amount,
            'category': result['category'],
            'confidence': result['confidence']
        }
        
        self.user_data['expenses'].append(expense)
        self._save_user_data()
        
        return expense
    
    def get_spending_summary(self, days=30):
        """Get spending summary for last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        summary = {}
        total = 0
        
        for expense in self.user_data['expenses']:
            exp_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if exp_date >= cutoff_date:
                category = expense['category']
                amount = expense['amount']
                
                summary[category] = summary.get(category, 0) + amount
                total += amount
        
        return {
            'total_spent': total,
            'by_category': summary,
            'period_days': days
        }
    
    def get_smart_suggestions(self):
        """Get AI suggestions based on expenses and study plan"""
        
        summary = self.get_spending_summary(30)
        suggestions = []
        
        # Analyze spending patterns
        if summary['total_spent'] > 0:
            by_category = summary['by_category']
            
            # Check food spending
            food_spent = by_category.get('Food', 0)
            if food_spent > 8000:
                suggestions.append({
                    'type': 'expense',
                    'category': 'Food',
                    'message': f"💰 You spent ₹{food_spent} on food this month. Consider meal prep to save money!",
                    'action': 'Learn cooking basics or use budget meal planning'
                })
            
            # Check education spending
            edu_spent = by_category.get('Education', 0)
            if edu_spent > 5000:
                suggestions.append({
                    'type': 'learning',
                    'category': 'Education',
                    'message': f"📚 You invested ₹{edu_spent} in education! Create a study plan to maximize your learning.",
                    'action': 'Use the AI Study Plan Agent to structure your learning'
                })
            
            # Check entertainment vs education
            entertainment = by_category.get('Entertainment', 0)
            education = by_category.get('Education', 0)
            if entertainment > education * 2 and education > 0:
                suggestions.append({
                    'type': 'balance',
                    'message': f"⚖️ Entertainment (₹{entertainment}) > Education (₹{education}). Consider balancing your investments!",
                    'action': 'Redirect some entertainment budget to skill development'
                })
        
        # Study plan suggestions
        if self.user_data.get('study_plan') is None:
            suggestions.append({
                'type': 'study',
                'message': "🎓 You don't have a study plan yet. Let's create one!",
                'action': 'Start the AI Study Plan Agent'
            })
        else:
            # Check study plan progress
            plan = self.user_data['study_plan']
            start_date = datetime.strptime(plan['start_date'], '%Y-%m-%d')
            days_since_start = (datetime.now() - start_date).days
            current_week = (days_since_start // 7) + 1
            
            if current_week <= plan['total_weeks']:
                suggestions.append({
                    'type': 'study',
                    'message': f"📅 You're in Week {current_week} of your {plan['goal']} plan. Keep going!",
                    'action': 'Check today\'s study tasks'
                })
        
        return suggestions
    
    def main_menu(self):
        """Interactive main menu"""
        
        while True:
            print("\n" + "=" * 70)
            print("🌟 SMART LIFE ASSISTANT")
            print("=" * 70)
            print("1. 💰 Add Expense (Auto-categorize)")
            print("2. 📊 View Spending Summary")
            print("3. 🎓 Create/View Study Plan")
            print("4. 📅 Today's Study Tasks")
            print("5. 💡 Get Smart Suggestions")
            print("6. 📈 Full Dashboard")
            print("7. 🚪 Exit")
            print("=" * 70)
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self._add_expense_interactive()
            elif choice == '2':
                self._view_spending_summary()
            elif choice == '3':
                self._manage_study_plan()
            elif choice == '4':
                self._show_today_tasks()
            elif choice == '5':
                self._show_suggestions()
            elif choice == '6':
                self._show_dashboard()
            elif choice == '7':
                print("\n👋 Goodbye! Keep learning and spending wisely!")
                break
            else:
                print("Invalid choice. Try again.")
    
    def _add_expense_interactive(self):
        """Add expense interactively"""
        print("\n" + "=" * 70)
        print("💰 ADD NEW EXPENSE")
        print("=" * 70)
        
        transaction = input("Enter transaction (e.g., 'Swiggy order 450'): ").strip()
        
        if not transaction:
            print("Empty transaction!")
            return
        
        expense = self.add_expense(transaction)
        
        if expense:
            print(f"\n✓ Expense added!")
            print(f"  Category: {expense['category']}")
            print(f"  Amount: ₹{expense['amount']}")
            print(f"  Confidence: {expense['confidence']:.1f}%")
    
    def _view_spending_summary(self):
        """View spending summary"""
        print("\n" + "=" * 70)
        print("📊 SPENDING SUMMARY (Last 30 Days)")
        print("=" * 70)
        
        summary = self.get_spending_summary(30)
        
        print(f"\nTotal Spent: ₹{summary['total_spent']:,}")
        print("\nBy Category:")
        
        for category, amount in sorted(summary['by_category'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / summary['total_spent'] * 100) if summary['total_spent'] > 0 else 0
            print(f"  {category:20s} ₹{amount:8,}  ({percentage:.1f}%)")
    
    def _manage_study_plan(self):
        """Manage study plan"""
        print("\n" + "=" * 70)
        print("🎓 STUDY PLAN MANAGER")
        print("=" * 70)
        
        if self.user_data.get('study_plan'):
            print("\nYou have an existing study plan:")
            plan = self.user_data['study_plan']
            print(f"  Goal: {plan['goal']}")
            print(f"  Duration: {plan['total_weeks']} weeks")
            print(f"  Started: {plan['start_date']}")
            
            choice = input("\nCreate new plan? (yes/no): ").strip().lower()
            if choice not in ['yes', 'y']:
                return
        
        # Create new plan
        plan = self.study_agent.interactive_plan_creator()
        if plan:
            self.user_data['study_plan'] = plan
            self._save_user_data()
    
    def _show_today_tasks(self):
        """Show today's study tasks"""
        
        if not self.user_data.get('study_plan'):
            print("\n✗ No study plan found. Create one first!")
            return
        
        today_plan = self.study_agent.get_today_plan(self.user_data['study_plan'])
        self.study_agent._display_today_plan(today_plan)
    
    def _show_suggestions(self):
        """Show AI suggestions"""
        print("\n" + "=" * 70)
        print("💡 SMART SUGGESTIONS")
        print("=" * 70)
        
        suggestions = self.get_smart_suggestions()
        
        if not suggestions:
            print("\n✓ You're doing great! No suggestions at the moment.")
            return
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion['message']}")
            print(f"   Action: {suggestion['action']}")
    
    def _show_dashboard(self):
        """Show complete dashboard"""
        print("\n" + "=" * 70)
        print("📈 SMART LIFE DASHBOARD")
        print("=" * 70)
        
        # Spending section
        print("\n💰 FINANCES:")
        summary = self.get_spending_summary(30)
        print(f"  Total spent (30 days): ₹{summary['total_spent']:,}")
        
        top_3 = sorted(summary['by_category'].items(), key=lambda x: x[1], reverse=True)[:3]
        print("  Top 3 categories:")
        for category, amount in top_3:
            print(f"    • {category}: ₹{amount:,}")
        
        # Study section
        print("\n🎓 LEARNING:")
        if self.user_data.get('study_plan'):
            plan = self.user_data['study_plan']
            start_date = datetime.strptime(plan['start_date'], '%Y-%m-%d')
            days_since_start = (datetime.now() - start_date).days
            current_week = (days_since_start // 7) + 1
            
            print(f"  Goal: {plan['goal']}")
            print(f"  Progress: Week {current_week}/{plan['total_weeks']}")
            print(f"  Daily commitment: {plan['hours_per_day']} hours")
        else:
            print("  No active study plan")
        
        # Suggestions
        print("\n💡 SUGGESTIONS:")
        suggestions = self.get_smart_suggestions()
        for suggestion in suggestions[:3]:
            print(f"  • {suggestion['message']}")
        
        print("\n" + "=" * 70)


# ========================
# MAIN EXECUTION
# ========================

if __name__ == "__main__":
    print("\n🚀 Initializing Smart Life Assistant...")
    
    assistant = SmartLifeAssistant()
    assistant.main_menu()