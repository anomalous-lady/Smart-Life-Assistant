import json
from datetime import datetime, timedelta
import re

class AIStudyPlanAgent:
    """AI Agent that creates personalized daily study plans"""
    
    def __init__(self):
        self.learning_paths = {
            'machine_learning': {
                'name': 'Machine Learning Engineer',
                'duration_weeks': 12,
                'daily_hours': 3,
                'topics': [
                    {'week': 1, 'topic': 'Python Fundamentals', 'resources': ['Codecademy Python', 'HackerRank Practice']},
                    {'week': 2, 'topic': 'NumPy & Pandas', 'resources': ['Kaggle Learn', 'freeCodeCamp Video']},
                    {'week': 3, 'topic': 'Data Visualization', 'resources': ['Matplotlib Tutorial', 'Seaborn Docs']},
                    {'week': 4, 'topic': 'Statistics Basics', 'resources': ['Khan Academy', 'StatQuest YouTube']},
                    {'week': 5, 'topic': 'Linear Regression', 'resources': ['Scikit-learn Docs', 'Build 3 Projects']},
                    {'week': 6, 'topic': 'Classification Algorithms', 'resources': ['Google ML Crash Course', 'Practice on Kaggle']},
                    {'week': 7, 'topic': 'Model Evaluation', 'resources': ['Cross-validation Tutorial', 'Metrics Deep Dive']},
                    {'week': 8, 'topic': 'Feature Engineering', 'resources': ['Kaggle Feature Engineering', 'Real Dataset Practice']},
                    {'week': 9, 'topic': 'Ensemble Methods', 'resources': ['Random Forest Tutorial', 'XGBoost Guide']},
                    {'week': 10, 'topic': 'Neural Networks Intro', 'resources': ['3Blue1Brown Videos', 'TensorFlow Basics']},
                    {'week': 11, 'topic': 'Deep Learning', 'resources': ['Fast.ai Course', 'Build CNN Project']},
                    {'week': 12, 'topic': 'Deploy ML Models', 'resources': ['Flask Tutorial', 'Deploy on Heroku']}
                ]
            },
            'web_development': {
                'name': 'Full Stack Web Developer',
                'duration_weeks': 10,
                'daily_hours': 4,
                'topics': [
                    {'week': 1, 'topic': 'HTML & CSS Basics', 'resources': ['freeCodeCamp', 'Build 5 Pages']},
                    {'week': 2, 'topic': 'JavaScript Fundamentals', 'resources': ['JavaScript.info', '30 JS Projects']},
                    {'week': 3, 'topic': 'DOM Manipulation', 'resources': ['Web Dev Simplified', 'Interactive Projects']},
                    {'week': 4, 'topic': 'React Basics', 'resources': ['React Official Docs', 'Build Todo App']},
                    {'week': 5, 'topic': 'React Advanced', 'resources': ['Hooks Deep Dive', 'Build Dashboard']},
                    {'week': 6, 'topic': 'Backend with Node.js', 'resources': ['Node.js Tutorial', 'Express.js Guide']},
                    {'week': 7, 'topic': 'Databases (MongoDB)', 'resources': ['MongoDB University', 'CRUD Operations']},
                    {'week': 8, 'topic': 'REST APIs', 'resources': ['Build API Project', 'Authentication JWT']},
                    {'week': 9, 'topic': 'Full Stack Integration', 'resources': ['MERN Stack Project', 'Deploy MERN']},
                    {'week': 10, 'topic': 'DevOps Basics', 'resources': ['Docker Tutorial', 'Deploy to AWS/Vercel']}
                ]
            },
            'data_science': {
                'name': 'Data Scientist',
                'duration_weeks': 14,
                'daily_hours': 3,
                'topics': [
                    {'week': 1, 'topic': 'Python for Data Science', 'resources': ['DataCamp', 'Jupyter Notebooks']},
                    {'week': 2, 'topic': 'NumPy & Pandas Mastery', 'resources': ['Data Manipulation', '10 Datasets Analysis']},
                    {'week': 3, 'topic': 'Data Cleaning', 'resources': ['Real Messy Data', 'Kaggle Datasets']},
                    {'week': 4, 'topic': 'Exploratory Data Analysis', 'resources': ['EDA Techniques', 'Visualization']},
                    {'week': 5, 'topic': 'Statistics & Probability', 'resources': ['Khan Academy', 'Statistics Workbook']},
                    {'week': 6, 'topic': 'Hypothesis Testing', 'resources': ['A/B Testing', 'Real Experiments']},
                    {'week': 7, 'topic': 'Machine Learning Basics', 'resources': ['Scikit-learn', 'Build 5 Models']},
                    {'week': 8, 'topic': 'Feature Engineering', 'resources': ['Advanced Techniques', 'Kaggle Competition']},
                    {'week': 9, 'topic': 'Time Series Analysis', 'resources': ['ARIMA Models', 'Stock Price Prediction']},
                    {'week': 10, 'topic': 'NLP Fundamentals', 'resources': ['Text Processing', 'Sentiment Analysis']},
                    {'week': 11, 'topic': 'Deep Learning', 'resources': ['Neural Networks', 'Image Classification']},
                    {'week': 12, 'topic': 'Big Data Tools', 'resources': ['PySpark Basics', 'SQL Mastery']},
                    {'week': 13, 'topic': 'Data Visualization', 'resources': ['Tableau', 'Power BI', 'D3.js']},
                    {'week': 14, 'topic': 'Portfolio & Deployment', 'resources': ['Build 3 Projects', 'GitHub Portfolio']}
                ]
            },
            'interview_prep': {
                'name': 'Tech Interview Preparation',
                'duration_weeks': 8,
                'daily_hours': 4,
                'topics': [
                    {'week': 1, 'topic': 'Data Structures: Arrays & Strings', 'resources': ['LeetCode Easy', 'Solve 20 Problems']},
                    {'week': 2, 'topic': 'Linked Lists & Stacks', 'resources': ['GeeksforGeeks', 'Solve 15 Problems']},
                    {'week': 3, 'topic': 'Trees & Graphs', 'resources': ['Binary Trees', 'Graph Traversal', '20 Problems']},
                    {'week': 4, 'topic': 'Sorting & Searching', 'resources': ['Algorithm Patterns', '15 Problems']},
                    {'week': 5, 'topic': 'Dynamic Programming', 'resources': ['DP Patterns', 'Solve 20 Problems']},
                    {'week': 6, 'topic': 'System Design Basics', 'resources': ['Grokking System Design', 'Design 5 Systems']},
                    {'week': 7, 'topic': 'Behavioral Questions', 'resources': ['STAR Method', 'Mock Interviews']},
                    {'week': 8, 'topic': 'Mock Interviews', 'resources': ['Pramp', 'Interviewing.io', 'Practice Daily']}
                ]
            }
        }
    
    def create_study_plan(self, goal, available_hours_per_day, start_date=None):
        """Create personalized study plan based on user's goal"""
        
        if start_date is None:
            start_date = datetime.now()
        
        # Select learning path
        if goal not in self.learning_paths:
            return None
        
        path = self.learning_paths[goal]
        plan = {
            'goal': path['name'],
            'total_weeks': path['duration_weeks'],
            'hours_per_day': min(available_hours_per_day, path['daily_hours']),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'weekly_schedule': []
        }
        
        # Generate weekly breakdown
        for topic_info in path['topics']:
            week_num = topic_info['week']
            week_start = start_date + timedelta(weeks=week_num-1)
            
            week_plan = {
                'week': week_num,
                'start_date': week_start.strftime('%Y-%m-%d'),
                'topic': topic_info['topic'],
                'resources': topic_info['resources'],
                'daily_tasks': self._generate_daily_tasks(
                    topic_info['topic'], 
                    available_hours_per_day
                )
            }
            plan['weekly_schedule'].append(week_plan)
        
        return plan
    
    def _generate_daily_tasks(self, topic, hours_per_day):
        """Generate daily tasks for a topic"""
        
        tasks = {
            'Monday': [
                f'📚 Learn {topic} theory (1 hour)',
                f'📝 Take notes and summarize key concepts',
                f'🎥 Watch tutorial videos'
            ],
            'Tuesday': [
                f'💻 Practice coding exercises (1.5 hours)',
                f'🔍 Review yesterday\'s notes',
                f'✍️ Solve problems on the topic'
            ],
            'Wednesday': [
                f'🛠️ Build mini-project using {topic}',
                f'📖 Read documentation',
                f'🤔 Debug and understand errors'
            ],
            'Thursday': [
                f'🔄 Review and practice more problems',
                f'👥 Discuss with community/forums',
                f'📊 Analyze your progress'
            ],
            'Friday': [
                f'🚀 Build a complete project',
                f'💡 Apply {topic} in real scenario',
                f'📝 Document your code'
            ],
            'Saturday': [
                f'🎯 Challenge problems (advanced)',
                f'🔍 Deep dive into edge cases',
                f'💪 Push your limits'
            ],
            'Sunday': [
                f'📚 Weekly review of {topic}',
                f'✅ Test your knowledge (quiz/mock test)',
                f'🎉 Celebrate weekly progress!',
                f'📝 Plan next week'
            ]
        }
        
        # Adjust based on available hours
        if hours_per_day < 2:
            for day in tasks:
                tasks[day] = tasks[day][:2]  # Reduce tasks
        elif hours_per_day >= 4:
            for day in tasks:
                tasks[day].append('🔥 Extra practice session')
        
        return tasks
    
    def get_today_plan(self, full_plan, current_date=None):
        """Get today's specific study tasks"""
        
        if current_date is None:
            current_date = datetime.now()
        
        start_date = datetime.strptime(full_plan['start_date'], '%Y-%m-%d')
        days_diff = (current_date - start_date).days
        
        if days_diff < 0:
            return {'status': 'not_started', 'message': 'Your study plan hasn\'t started yet!'}
        
        week_num = (days_diff // 7) + 1
        day_name = current_date.strftime('%A')
        
        if week_num > full_plan['total_weeks']:
            return {
                'status': 'completed',
                'message': '🎉 Congratulations! You\'ve completed the entire study plan!'
            }
        
        current_week = full_plan['weekly_schedule'][week_num - 1]
        today_tasks = current_week['daily_tasks'].get(day_name, [])
        
        return {
            'status': 'active',
            'week': week_num,
            'day': day_name,
            'topic': current_week['topic'],
            'tasks': today_tasks,
            'resources': current_week['resources'],
            'hours_allocated': full_plan['hours_per_day']
        }
    
    def save_plan(self, plan, filename='my_study_plan.json'):
        """Save study plan to file"""
        with open(filename, 'w') as f:
            json.dump(plan, f, indent=2)
        print(f"✓ Study plan saved as {filename}")
    
    def load_plan(self, filename='my_study_plan.json'):
        """Load study plan from file"""
        try:
            with open(filename, 'r') as f:
                plan = json.load(f)
            print(f"✓ Study plan loaded from {filename}")
            return plan
        except FileNotFoundError:
            print(f"✗ No saved plan found at {filename}")
            return None
    
    def interactive_plan_creator(self):
        """Interactive mode to create study plan"""
        
        print("\n" + "=" * 70)
        print("🎓 AI STUDY PLAN AGENT - CREATE YOUR PERSONALIZED PLAN")
        print("=" * 70)
        
        # Show available goals
        print("\n📚 Available Learning Paths:")
        for idx, (key, path) in enumerate(self.learning_paths.items(), 1):
            print(f"  {idx}. {path['name']} ({path['duration_weeks']} weeks)")
        
        # Get user choice
        print("\nEnter the number of your goal (1-4):")
        choice = input("Your choice: ").strip()
        
        goal_map = {
            '1': 'machine_learning',
            '2': 'web_development',
            '3': 'data_science',
            '4': 'interview_prep'
        }
        
        if choice not in goal_map:
            print("Invalid choice!")
            return
        
        goal = goal_map[choice]
        
        # Get available hours
        print("\n⏰ How many hours can you study per day?")
        hours = input("Hours (1-8): ").strip()
        try:
            hours = float(hours)
            if hours < 1 or hours > 8:
                hours = 3
        except:
            hours = 3
        
        # Create plan
        print("\n🚀 Creating your personalized study plan...")
        plan = self.create_study_plan(goal, hours)
        
        # Display plan
        print("\n" + "=" * 70)
        print(f"📋 YOUR STUDY PLAN: {plan['goal']}")
        print("=" * 70)
        print(f"Duration: {plan['total_weeks']} weeks")
        print(f"Daily commitment: {plan['hours_per_day']} hours")
        print(f"Start date: {plan['start_date']}")
        
        print("\n📅 Weekly Breakdown:")
        for week in plan['weekly_schedule']:
            print(f"\n  Week {week['week']}: {week['topic']}")
            print(f"  Resources: {', '.join(week['resources'])}")
        
        # Save plan
        save = input("\n💾 Save this plan? (yes/no): ").strip().lower()
        if save in ['yes', 'y']:
            self.save_plan(plan)
        
        # Show today's plan
        show_today = input("\n📅 Show today's tasks? (yes/no): ").strip().lower()
        if show_today in ['yes', 'y']:
            today = self.get_today_plan(plan)
            self._display_today_plan(today)
        
        return plan
    
    def _display_today_plan(self, today_plan):
        """Display today's study tasks"""
        
        print("\n" + "=" * 70)
        print("📅 TODAY'S STUDY PLAN")
        print("=" * 70)
        
        if today_plan['status'] == 'not_started':
            print(today_plan['message'])
        elif today_plan['status'] == 'completed':
            print(today_plan['message'])
        else:
            print(f"Week {today_plan['week']} | {today_plan['day']}")
            print(f"Topic: {today_plan['topic']}")
            print(f"Time allocated: {today_plan['hours_allocated']} hours")
            
            print("\n✅ Today's Tasks:")
            for task in today_plan['tasks']:
                print(f"  {task}")
            
            print("\n📚 Resources:")
            for resource in today_plan['resources']:
                print(f"  • {resource}")
        
        print("=" * 70)


# ========================
# USAGE EXAMPLE
# ========================

if __name__ == "__main__":
    agent = AIStudyPlanAgent()
    
    # Interactive mode
    agent.interactive_plan_creator()