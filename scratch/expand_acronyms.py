import os
from pathlib import Path
import re

ACRONYMS = {
    r'\bSVD\b': 'Singular Value Decomposition (SVD)',
    r'\bPCA\b': 'Principal Component Analysis (PCA)',
    r'\bOLS\b': 'Ordinary Least Squares (OLS)',
    r'\bGANs\b': 'Generative Adversarial Networks (GANs)',
    r'\bGAN\b': 'Generative Adversarial Network (GAN)',
    r'\bCNNs\b': 'Convolutional Neural Networks (CNNs)',
    r'\bCNN\b': 'Convolutional Neural Network (CNN)',
    r'\bSVMs\b': 'Support Vector Machines (SVMs)',
    r'\bSVM\b': 'Support Vector Machine (SVM)',
    r'\bLDA\b': 'Linear Discriminant Analysis (LDA)', # Note: Context sensitive, but usually LDA in this math repo
    r'\bNLP\b': 'Natural Language Processing (NLP)',
    r'\bLSA\b': 'Latent Semantic Analysis (LSA)',
    r'\bQR\b': 'QR Decomposition',
    r'\bLU\b': 'LU Decomposition',
}

def expand_acronyms(text):
    # We want to avoid double-expanding if it's already expanded
    # e.g. "Singular Value Decomposition (SVD)" shouldn't become "Singular Value Decomposition (Singular Value Decomposition (SVD))"
    
    for pattern, replacement in ACRONYMS.items():
        # Check if the replacement already exists near the pattern
        # This is a bit tricky with regex, so we'll do a simple check:
        # If the replacement's full name part is already there, skip.
        full_name = replacement.split(' (')[0]
        
        # We only replace if the full name is NOT immediately preceding
        # and the whole replacement is NOT already there.
        if full_name in text and replacement in text:
            continue
            
        text = re.sub(pattern, replacement, text)
        
    # Fix double expansions like "Principal Component Analysis (Principal Component Analysis (PCA))"
    for pattern, replacement in ACRONYMS.items():
        full_name = replacement.split(' (')[0]
        # Regex to find "Full Name (Full Name (ACRONYM))"
        double_pattern = f"{re.escape(full_name)} \({re.escape(replacement)}\)"
        text = re.sub(double_pattern, replacement, text)
        
    return text

def process_all_files():
    content_dir = Path('content')
    for p in content_dir.rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        new_text = expand_acronyms(text)
        if text != new_text:
            p.write_text(new_text, encoding='utf-8')
            print(f"Expanded acronyms in {p}")

if __name__ == "__main__":
    process_all_files()
