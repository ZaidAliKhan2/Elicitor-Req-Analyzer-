import pickle
import re
import pandas as pd
from pathlib import Path
import numpy as np
import sys
import os

# Add parent directory to path to import feature_transformers
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import your feature extraction functions
try:
    from nlp.feature_transformers import extract_keyword_features, extract_pos_features
except ImportError:
    try:
        from feature_transformers import extract_keyword_features, extract_pos_features
    except ImportError:
        print("⚠️  Warning: Could not import feature_transformers. Make sure it's in the same directory.")
        print("   Feature extraction will not work correctly!")
        # Define dummy functions as fallback
        def extract_keyword_features(text):
            return {"fr_keyword_match": 0, "nfr_keyword_match": 0}
        def extract_pos_features(text):
            return {"num_verbs": 0, "num_nouns": 0, "num_adjectives": 0}

# -------------------------------
# MODEL PATHS
# -------------------------------
FR_NFR_MODEL = "backend/models/fr_nfr_model.pkl"
NFR_SUB_MODEL = "backend/models/nfr_sub_model.pkl"

# -------------------------------
# TEXT CLEANING FUNCTION
# -------------------------------
def clean_text(text: str) -> str:
    """
    Cleans input text before prediction.
    - Removes labels such as __label__FR
    - Removes extra symbols/digits
    - Normalizes whitespace
    """
    text = re.sub(r"__label__\w+", "", text)   # remove labels
    text = re.sub(r"[^a-zA-Z0-9\s.,]", " ", text)  # remove odd characters
    text = re.sub(r"\s+", " ", text).strip()   # normalize spaces
    return text

# -------------------------------
# TRANSFORM WITH CUSTOM FEATURES
# -------------------------------
def transform_with_custom_features(text_clean, vectorizer):
    """
    Transform text using TF-IDF + custom features
    Matches the training process: TF-IDF + keyword features + POS features
    """
    # Get TF-IDF features
    tfidf_vector = vectorizer.transform([text_clean])
    
    # Extract keyword features (2 features)
    keyword_features = extract_keyword_features(text_clean)
    
    # Extract POS features (3 features)
    pos_features = extract_pos_features(text_clean)
    
    # Combine: TF-IDF + keyword (2) + POS (3)
    tfidf_array = tfidf_vector.toarray()[0].tolist()
    extra_features = list(keyword_features.values()) + list(pos_features.values())
    combined = tfidf_array + extra_features
    
    # Convert back to numpy array with shape (1, n_features)
    return np.array([combined])

# -------------------------------
# LOAD MODELS
# -------------------------------
def load_fr_nfr_model():
    with open(FR_NFR_MODEL, "rb") as f:
        vec, model = pickle.load(f)
    return vec, model

def load_nfr_sub_model():
    with open(NFR_SUB_MODEL, "rb") as f:
        vec, model = pickle.load(f)
    return vec, model

# -------------------------------
# CONFIDENCE INTERPRETATION
# -------------------------------
def get_confidence_level(confidence):
    """Returns a textual confidence level"""
    if confidence >= 0.90:
        return "Very High"
    elif confidence >= 0.75:
        return "High"
    elif confidence >= 0.60:
        return "Moderate"
    elif confidence >= 0.45:
        return "Low"
    else:
        return "Very Low"

# -------------------------------
# PREDICTOR FUNCTION WITH CONFIDENCE
# -------------------------------
def classify_requirement(text):
    text_clean = clean_text(text)
    
    # Load FR/NFR main model
    vec1, model1 = load_fr_nfr_model()
    
    # Transform with custom features (TF-IDF + keyword + POS)
    X_transformed = transform_with_custom_features(text_clean, vec1)
    
    # Get prediction and probabilities
    main_pred = model1.predict(X_transformed)[0]
    
    # Get confidence scores
    if hasattr(model1, 'predict_proba'):
        main_proba = model1.predict_proba(X_transformed)[0]
        main_confidence = float(np.max(main_proba))
        
        # Get class labels
        classes = model1.classes_
        class_probabilities = {classes[i]: float(main_proba[i]) for i in range(len(classes))}
    else:
        # Fallback for models without predict_proba
        main_confidence = None
        class_probabilities = None
    
    result = {
        "main": main_pred,
        "main_confidence": main_confidence,
        "main_confidence_level": get_confidence_level(main_confidence) if main_confidence else "N/A",
        "main_class_probabilities": class_probabilities,
        "subcategory": None,
        "sub_confidence": None,
        "sub_confidence_level": None,
        "sub_class_probabilities": None
    }
    
    if main_pred == "FR":
        return result
    
    # Load NFR sub-category model
    vec2, model2 = load_nfr_sub_model()
    
    # Transform with custom features (TF-IDF + keyword + POS)
    X_transformed2 = transform_with_custom_features(text_clean, vec2)
    
    sub_pred = model2.predict(X_transformed2)[0]
    
    # Get subcategory confidence
    if hasattr(model2, 'predict_proba'):
        sub_proba = model2.predict_proba(X_transformed2)[0]
        sub_confidence = float(np.max(sub_proba))
        
        # Get subcategory class labels
        sub_classes = model2.classes_
        sub_class_probabilities = {sub_classes[i]: float(sub_proba[i]) for i in range(len(sub_classes))}
        
        result["subcategory"] = str(sub_pred)
        result["sub_confidence"] = sub_confidence
        result["sub_confidence_level"] = get_confidence_level(sub_confidence)
        result["sub_class_probabilities"] = sub_class_probabilities
    else:
        result["subcategory"] = str(sub_pred)
    
    return result

# -------------------------------
# DISPLAY RESULT FUNCTION
# -------------------------------
def display_result(result, show_all_probs=False):
    """Display prediction result in a user-friendly format"""
    print("\n" + "="*60)
    print("CLASSIFICATION RESULT")
    print("="*60)
    
    # Main category
    print(f"\n📊 Main Category: {result['main']}")
    if result['main_confidence']:
        confidence_pct = result['main_confidence'] * 100
        print(f"   Confidence: {confidence_pct:.2f}% ({result['main_confidence_level']})")
        
        if show_all_probs and result['main_class_probabilities']:
            print(f"\n   All Class Probabilities:")
            for cls, prob in sorted(result['main_class_probabilities'].items(), 
                                   key=lambda x: x[1], reverse=True):
                print(f"      {cls}: {prob*100:.2f}%")
    
    # Subcategory (if NFR)
    if result['subcategory']:
        print(f"\n📋 Sub-Category: {result['subcategory']}")
        if result['sub_confidence']:
            sub_confidence_pct = result['sub_confidence'] * 100
            print(f"   Confidence: {sub_confidence_pct:.2f}% ({result['sub_confidence_level']})")
            
            if show_all_probs and result['sub_class_probabilities']:
                print(f"\n   All Sub-Category Probabilities:")
                for cls, prob in sorted(result['sub_class_probabilities'].items(), 
                                       key=lambda x: x[1], reverse=True)[:5]:  # Show top 5
                    print(f"      {cls}: {prob*100:.2f}%")
    
    # Confidence warning
    if result['main_confidence'] and result['main_confidence'] < 0.60:
        print("\n⚠️  Warning: Low confidence prediction. Consider reviewing this classification.")
    
    print("="*60)

# -------------------------------
# FILE TESTING FUNCTION
# -------------------------------
def test_from_file(file_path: str, output_path: str = None):
    """
    Test requirements from a file.
    Supports: .txt, .csv, .xlsx
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ Error: File '{file_path}' not found!")
        return
    
    print(f"\n📂 Loading file: {file_path}")
    
    # Read file based on extension
    if file_path.suffix == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            requirements = [line.strip() for line in f if line.strip()]
        df = pd.DataFrame({'Requirement': requirements})
    
    elif file_path.suffix == '.csv':
        df = pd.read_csv(file_path)
        # Assume first column or 'Requirement' column contains text
        if 'Requirement' not in df.columns:
            df.columns = ['Requirement'] + list(df.columns[1:])
    
    elif file_path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
        if 'Requirement' not in df.columns:
            df.columns = ['Requirement'] + list(df.columns[1:])
    
    else:
        print(f"❌ Unsupported file format: {file_path.suffix}")
        print("Supported formats: .txt, .csv, .xlsx, .xls")
        return
    
    # Remove empty rows
    df = df[df['Requirement'].notna()]
    df = df[df['Requirement'].str.strip() != '']
    
    print(f"✓ Loaded {len(df)} requirements\n")
    print("🔄 Classifying requirements...\n")
    
    # Classify each requirement
    results = []
    for idx, row in df.iterrows():
        req_text = row['Requirement']
        prediction = classify_requirement(req_text)
        results.append({
            'Requirement': req_text,
            'Main_Category': prediction['main'],
            'Main_Confidence': f"{prediction['main_confidence']*100:.2f}%" if prediction['main_confidence'] else 'N/A',
            'Main_Confidence_Level': prediction['main_confidence_level'],
            'Sub_Category': prediction['subcategory'] if prediction['subcategory'] else 'N/A',
            'Sub_Confidence': f"{prediction['sub_confidence']*100:.2f}%" if prediction['sub_confidence'] else 'N/A',
            'Sub_Confidence_Level': prediction['sub_confidence_level'] if prediction['sub_confidence_level'] else 'N/A'
        })
        
        # Print progress every 100 rows
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(df)} requirements...")
    
    # Create results dataframe
    results_df = pd.DataFrame(results)
    
    # Display summary
    print("\n" + "="*60)
    print("CLASSIFICATION SUMMARY")
    print("="*60)
    print(f"\nTotal Requirements: {len(results_df)}")
    print(f"\nMain Category Distribution:")
    print(results_df['Main_Category'].value_counts())
    
    # Confidence statistics
    conf_values = [float(c.strip('%'))/100 for c in results_df['Main_Confidence'] if c != 'N/A']
    if conf_values:
        print(f"\nMain Category Confidence Statistics:")
        print(f"  Average: {np.mean(conf_values)*100:.2f}%")
        print(f"  Median: {np.median(conf_values)*100:.2f}%")
        print(f"  Min: {np.min(conf_values)*100:.2f}%")
        print(f"  Max: {np.max(conf_values)*100:.2f}%")
    
    nfr_df = results_df[results_df['Main_Category'] == 'NFR']
    if len(nfr_df) > 0:
        print(f"\nNFR Sub-Category Distribution:")
        print(nfr_df['Sub_Category'].value_counts())
        
        # NFR confidence statistics
        nfr_conf_values = [float(c.strip('%'))/100 for c in nfr_df['Sub_Confidence'] if c != 'N/A']
        if nfr_conf_values:
            print(f"\nNFR Sub-Category Confidence Statistics:")
            print(f"  Average: {np.mean(nfr_conf_values)*100:.2f}%")
            print(f"  Median: {np.median(nfr_conf_values)*100:.2f}%")
            print(f"  Min: {np.min(nfr_conf_values)*100:.2f}%")
            print(f"  Max: {np.max(nfr_conf_values)*100:.2f}%")
    
    # Save results
    if output_path is None:
        output_path = file_path.stem + '_results.csv'
    
    results_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n✓ Results saved to: {output_path}")
    
    # Show sample results
    print("\n" + "="*60)
    print("SAMPLE RESULTS (First 5)")
    print("="*60)
    for idx, row in results_df.head(5).iterrows():
        print(f"\n{idx + 1}. {row['Requirement'][:80]}...")
        print(f"   → Main: {row['Main_Category']} (Confidence: {row['Main_Confidence']})")
        if row['Sub_Category'] != 'N/A':
            print(f"   → Sub: {row['Sub_Category']} (Confidence: {row['Sub_Confidence']})")
    
    return results_df

# -------------------------------
# INTERACTIVE TESTING
# -------------------------------
def interactive_mode():
    print("\n=== Combined Requirement Classifier (FR/NFR + Subcategories) ===")
    print("Type 'exit' to stop.")
    print("Type 'detailed' to toggle detailed probability view.\n")
    
    show_detailed = False
    
    while True:
        user = input("Enter a requirement: ")
        
        if user.lower().strip() == "exit":
            break
        
        if user.lower().strip() == "detailed":
            show_detailed = not show_detailed
            print(f"\n{'Enabled' if show_detailed else 'Disabled'} detailed probability view.\n")
            continue
        
        result = classify_requirement(user)
        display_result(result, show_all_probs=show_detailed)

# -------------------------------
# MAIN ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print("REQUIREMENT CLASSIFIER - TEST MODE")
    print("="*60)
    print("\nChoose testing mode:")
    print("1. Interactive mode (type requirements manually)")
    print("2. File mode (test from file)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        interactive_mode()
    
    elif choice == "2":
        file_path = input("\nEnter file path (e.g., requirements.csv): ").strip()
        output_path = input("Enter output file name (press Enter for auto): ").strip()
        
        if not output_path:
            output_path = None
        
        test_from_file(file_path, output_path)
    
    elif choice == "3":
        print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Invalid choice!")