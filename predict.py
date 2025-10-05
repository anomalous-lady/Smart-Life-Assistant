import pickle
import re

class ExpensePredictor:
    """Easy-to-use expense predictor for new transactions"""
    
    def __init__(self, model_path='expense_categorizer.pkl'):
        """Load the trained model"""
        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.vectorizer = data['vectorizer']
                self.model = data['model']
            print("✓ Model loaded successfully!")
        except FileNotFoundError:
            print("ERROR: Model file not found. Please run the training script first!")
            raise
    
    def preprocess(self, text):
        """Preprocess transaction text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = ' '.join(text.split())
        return text
    
    def predict_category(self, transaction_text):
        """Predict category for a single transaction"""
        processed = self.preprocess(transaction_text)
        X_tfidf = self.vectorizer.transform([processed])
        
        category = self.model.predict(X_tfidf)[0]
        probabilities = self.model.predict_proba(X_tfidf)[0]
        confidence = max(probabilities) * 100
        
        top_indices = probabilities.argsort()[-3:][::-1]
        top_predictions = [(self.model.classes_[i], probabilities[i] * 100) 
                          for i in top_indices]
        
        return {
            'category': category,
            'confidence': confidence,
            'top_predictions': top_predictions
        }
    
    def predict_batch(self, transactions):
        """Predict categories for multiple transactions"""
        results = []
        for transaction in transactions:
            result = self.predict_category(transaction)
            result['transaction'] = transaction
            results.append(result)
        return results
    
    def interactive_mode(self):
        """Run interactive prediction mode"""
        print("\n" + "=" * 60)
        print("INTERACTIVE EXPENSE CATEGORIZER")
        print("=" * 60)
        print("Enter transaction descriptions (or 'quit' to exit)")
        print("-" * 60)
        
        while True:
            transaction = input("\nEnter transaction: ").strip()
            
            if transaction.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if not transaction:
                continue
            
            result = self.predict_category(transaction)
            
            print(f"\n📊 Prediction Results:")
            print(f"   Category: {result['category']}")
            print(f"   Confidence: {result['confidence']:.2f}%")
            print(f"\n   Top 3 predictions:")
            for i, (cat, prob) in enumerate(result['top_predictions'], 1):
                print(f"   {i}. {cat}: {prob:.2f}%")

# ========================
# USAGE EXAMPLES
# ========================

if __name__ == "__main__":
    predictor = ExpensePredictor()
    
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Single Transaction Prediction")
    print("=" * 60)
    
    transaction = "Swiggy order biryani 450"
    result = predictor.predict_category(transaction)
    print(f"\nTransaction: '{transaction}'")
    print(f"Predicted Category: {result['category']}")
    print(f"Confidence: {result['confidence']:.2f}%")
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch Predictions")
    print("=" * 60)
    
    transactions = [
        "Netflix subscription renewal",
        "Metro card recharge 500",
        "Amazon shopping electronics",
        "Hospital bill payment 5000",
        "Gym membership annual"
    ]
    
    results = predictor.predict_batch(transactions)
    
    print("\n{:<40} {:<20} {:<10}".format("Transaction", "Category", "Confidence"))
    print("-" * 70)
    for r in results:
        print("{:<40} {:<20} {:.2f}%".format(
            r['transaction'][:38], 
            r['category'], 
            r['confidence']
        ))
    
    predictor.interactive_mode()