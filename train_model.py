import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import pickle
import re
from datetime import datetime

# ========================
# 1. CREATE LABELED DATASET
# ========================

def create_sample_dataset():
    """Create a labeled transaction dataset"""
    
    transactions = [
        # FOOD & DINING
        "Swiggy order 450", "Zomato payment 320", "McDonald's 250", "Dominos Pizza 599",
        "Starbucks Coffee 180", "KFC Chicken 399", "Subway sandwich 200", "Pizza Hut 550",
        "Cafe Coffee Day 150", "Burger King 300", "Haldirams 280", "Food panda 420",
        "Restaurant bill 850", "Dinner at Hotel 1200", "Lunch expense 300", "Breakfast cafe 180",
        "Swiggy Genie 50", "Zomato Pro 299", "Biryani order 400", "Chinese food 350",
        
        # TRAVEL & TRANSPORT
        "Uber ride 300", "Ola cab 250", "Rapido bike 80", "Metro card recharge 500",
        "Petrol pump 2000", "Fuel expense 1500", "Bus ticket 50", "Train ticket 350",
        "Auto rickshaw 120", "Taxi fare 450", "Parking fee 50", "Toll tax 100",
        "Uber Moto 60", "Ola Auto 90", "Flight booking 8500", "IndiGo airlines 6500",
        "Rapido Auto 100", "Metro ticket 40", "Bike rental 200", "Car service 5000",
        
        # SHOPPING
        "Amazon purchase 1299", "Flipkart order 899", "Myntra clothing 1599", "Ajio fashion 2100",
        "Big Bazaar 650", "Reliance Trends 1200", "Decathlon sports 3500", "Nike store 4500",
        "Lifestyle store 2800", "Shopper Stop 1900", "Electronics shop 15000", "Mobile purchase 25000",
        "Laptop bought 45000", "Headphones 2500", "Grocery shopping 1200", "Supermarket 850",
        "Online shopping 999", "Clothing store 1800", "Shoes purchase 3200", "Watch bought 5500",
        
        # ENTERTAINMENT
        "Netflix subscription 649", "Amazon Prime 299", "Disney Hotstar 499", "Spotify Premium 119",
        "PVR movie tickets 600", "INOX cinema 450", "BookMyShow 800", "Concert tickets 2500",
        "Gaming subscription 799", "YouTube Premium 129", "Apple Music 99", "Movie outing 1200",
        "Theatre tickets 350", "Gaming purchase 1999", "PlayStation game 3500", "Xbox pass 699",
        "Theme park 1500", "Water park entry 800", "Museum ticket 200", "Zoo entry 100",
        
        # UTILITIES & BILLS
        "Electricity bill 1500", "Water bill 300", "Gas cylinder 850", "Internet bill 799",
        "Mobile recharge 299", "DTH recharge 350", "Broadband payment 999", "Phone bill 550",
        "Airtel recharge 399", "Jio prepaid 239", "Vi postpaid 499", "BSNL bill 450",
        "WiFi payment 700", "Landline bill 200", "Maintenance charge 3500", "Society bill 2000",
        "LPG booking 900", "Electricity payment 1800", "Water charges 250", "Municipal tax 5000",
        
        # HEALTHCARE
        "Apollo Pharmacy 450", "Medicine purchase 680", "Doctor consultation 800", "Hospital bill 5500",
        "Medical test 2200", "Lab report 1500", "Health checkup 3000", "Dental clinic 1200",
        "Eye checkup 500", "Physiotherapy 800", "Medical store 350", "Health insurance 8500",
        "Clinic visit 600", "Surgery payment 25000", "X-ray 800", "MRI scan 4500",
        "Blood test 600", "Pharmacy bill 520", "Ayurvedic medicine 400", "Health supplements 900",
        
        # EDUCATION
        "Course fee 15000", "Book purchase 850", "Udemy course 799", "Coursera subscription 3999",
        "School fee 25000", "Tuition payment 5000", "Stationery shop 450", "Notebook 120",
        "Exam fee 1500", "Online class 2500", "Coaching center 8000", "University fee 50000",
        "Library membership 500", "Study material 650", "Educational app 299", "Skill course 4999",
        "Training program 12000", "Workshop fee 3500", "Seminar registration 1200", "Certification 8500",
        
        # PERSONAL CARE
        "Salon visit 600", "Haircut 250", "Spa treatment 2500", "Gym membership 3000",
        "Fitness center 1500", "Yoga class 800", "Beauty parlour 1200", "Grooming 450",
        "Cosmetics 850", "Perfume 1800", "Skincare products 1200", "Haircare 600",
        "Gym equipment 5000", "Protein powder 2500", "Supplements 1500", "Massage 1000",
        "Manicure pedicure 400", "Facial 800", "Hair color 1500", "Personal trainer 5000",
        
        # INVESTMENT & SAVINGS
        "Mutual fund SIP 5000", "Stock purchase 10000", "Fixed deposit 50000", "PPF deposit 20000",
        "Insurance premium 8500", "Life insurance 12000", "Gold purchase 25000", "Savings account 15000",
        "Investment app 3000", "Zerodha trading 8000", "Groww investment 5000", "SIP payment 10000",
        "Recurring deposit 2000", "NPS contribution 5000", "ELSS fund 15000", "Equity investment 20000",
        "Bonds purchase 30000", "Real estate 500000", "Crypto investment 5000", "Portfolio 25000",
        
        # MISCELLANEOUS
        "ATM withdrawal 5000", "Bank charges 150", "Credit card bill 8500", "Loan EMI 12000",
        "Gift purchase 1500", "Donation 1000", "Charity 500", "Pet supplies 800",
        "Vet visit 1200", "Plant nursery 400", "Home decor 2500", "Furniture 15000",
        "Appliance repair 800", "Plumber 600", "Electrician 500", "Carpenter 1200",
        "Courier charges 100", "Post office 50", "Legal fee 5000", "Consultant 3000"
    ]
    
    categories = [
        # FOOD & DINING (20)
        "Food", "Food", "Food", "Food", "Food", "Food", "Food", "Food",
        "Food", "Food", "Food", "Food", "Food", "Food", "Food", "Food",
        "Food", "Food", "Food", "Food",
        
        # TRAVEL & TRANSPORT (20)
        "Travel", "Travel", "Travel", "Travel", "Travel", "Travel", "Travel", "Travel",
        "Travel", "Travel", "Travel", "Travel", "Travel", "Travel", "Travel", "Travel",
        "Travel", "Travel", "Travel", "Travel",
        
        # SHOPPING (20)
        "Shopping", "Shopping", "Shopping", "Shopping", "Shopping", "Shopping", "Shopping", "Shopping",
        "Shopping", "Shopping", "Shopping", "Shopping", "Shopping", "Shopping", "Shopping", "Shopping",
        "Shopping", "Shopping", "Shopping", "Shopping",
        
        # ENTERTAINMENT (20)
        "Entertainment", "Entertainment", "Entertainment", "Entertainment", "Entertainment", "Entertainment",
        "Entertainment", "Entertainment", "Entertainment", "Entertainment", "Entertainment", "Entertainment",
        "Entertainment", "Entertainment", "Entertainment", "Entertainment", "Entertainment", "Entertainment",
        "Entertainment", "Entertainment",
        
        # UTILITIES & BILLS (20)
        "Utilities", "Utilities", "Utilities", "Utilities", "Utilities", "Utilities", "Utilities", "Utilities",
        "Utilities", "Utilities", "Utilities", "Utilities", "Utilities", "Utilities", "Utilities", "Utilities",
        "Utilities", "Utilities", "Utilities", "Utilities",
        
        # HEALTHCARE (20)
        "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare",
        "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare", "Healthcare",
        "Healthcare", "Healthcare", "Healthcare", "Healthcare",
        
        # EDUCATION (20)
        "Education", "Education", "Education", "Education", "Education", "Education", "Education", "Education",
        "Education", "Education", "Education", "Education", "Education", "Education", "Education", "Education",
        "Education", "Education", "Education", "Education",
        
        # PERSONAL CARE (20)
        "Personal Care", "Personal Care", "Personal Care", "Personal Care", "Personal Care", "Personal Care",
        "Personal Care", "Personal Care", "Personal Care", "Personal Care", "Personal Care", "Personal Care",
        "Personal Care", "Personal Care", "Personal Care", "Personal Care", "Personal Care", "Personal Care",
        "Personal Care", "Personal Care",
        
        # INVESTMENT & SAVINGS (20)
        "Investment", "Investment", "Investment", "Investment", "Investment", "Investment", "Investment", "Investment",
        "Investment", "Investment", "Investment", "Investment", "Investment", "Investment", "Investment", "Investment",
        "Investment", "Investment", "Investment", "Investment",
        
        # MISCELLANEOUS (20)
        "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous",
        "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous",
        "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous", "Miscellaneous",
        "Miscellaneous", "Miscellaneous"
    ]
    
    df = pd.DataFrame({
        'transaction': transactions,
        'category': categories
    })
    
    return df

# ========================
# 2. TEXT PREPROCESSING
# ========================

def preprocess_text(text):
    """Clean and preprocess transaction text"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers (keep the text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

# ========================
# 3. BUILD AND TRAIN MODEL
# ========================

class ExpenseCategorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2),  # Use unigrams and bigrams
            min_df=1
        )
        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            multi_class='multinomial'
        )
        
    def train(self, X_train, y_train):
        """Train the model"""
        # Transform text to TF-IDF features
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        
        # Train the logistic regression model
        self.model.fit(X_train_tfidf, y_train)
        
    def predict(self, X_test):
        """Make predictions"""
        X_test_tfidf = self.vectorizer.transform(X_test)
        return self.model.predict(X_test_tfidf)
    
    def predict_proba(self, X_test):
        """Get prediction probabilities"""
        X_test_tfidf = self.vectorizer.transform(X_test)
        return self.model.predict_proba(X_test_tfidf)
    
    def save_model(self, filename='expense_categorizer.pkl'):
        """Save the trained model"""
        with open(filename, 'wb') as f:
            pickle.dump({'vectorizer': self.vectorizer, 'model': self.model}, f)
        print(f"Model saved as {filename}")
    
    def load_model(self, filename='expense_categorizer.pkl'):
        """Load a trained model"""
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.vectorizer = data['vectorizer']
            self.model = data['model']
        print(f"Model loaded from {filename}")

# ========================
# 4. MAIN EXECUTION
# ========================

def main():
    print("=" * 60)
    print("SMART EXPENSE CATEGORIZER - ML MODEL")
    print("=" * 60)
    
    # Step 1: Create dataset
    print("\n[1/5] Creating labeled dataset...")
    df = create_sample_dataset()
    print(f"Dataset created with {len(df)} transactions")
    print(f"Categories: {df['category'].unique()}")
    print(f"\nSample data:")
    print(df.head(10))
    
    # Step 2: Preprocess
    print("\n[2/5] Preprocessing text...")
    df['processed_text'] = df['transaction'].apply(preprocess_text)
    
    # Step 3: Split data
    print("\n[3/5] Splitting data into train and test sets...")
    X = df['processed_text']
    y = df['category']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Step 4: Train model
    print("\n[4/5] Training ML model...")
    categorizer = ExpenseCategorizer()
    categorizer.train(X_train, y_train)
    print("Model trained successfully!")
    
    # Step 5: Evaluate
    print("\n[5/5] Evaluating model...")
    y_pred = categorizer.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    
    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(classification_report(y_test, y_pred))
    
    # Save model
    categorizer.save_model()
    
    # Demo predictions
    print("\n" + "=" * 60)
    print("DEMO PREDICTIONS")
    print("=" * 60)
    
    demo_transactions = [
        "Swiggy dinner 450",
        "Uber to airport 800",
        "Amazon shopping 1200",
        "Netflix monthly subscription",
        "Electricity bill payment",
        "Doctor consultation fee",
        "Gym membership renewal",
        "Udemy course purchase"
    ]
    
    for transaction in demo_transactions:
        processed = preprocess_text(transaction)
        prediction = categorizer.predict([processed])[0]
        probabilities = categorizer.predict_proba([processed])[0]
        confidence = max(probabilities) * 100
        
        print(f"\nTransaction: '{transaction}'")
        print(f"Category: {prediction} (Confidence: {confidence:.2f}%)")
    
    print("\n" + "=" * 60)
    print("Training Complete! Model saved as 'expense_categorizer.pkl'")
    print("=" * 60)

if __name__ == "__main__":
    main()