import torch
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pickle
import numpy as np

# Load the models
def load_tfidf_lda_models():
    with open('student_panel/models/tfidf_vectorizer.pkl', 'rb') as file:
        tfidf_vectorizer = pickle.load(file)

    with open('student_panel/models/lda_model.pkl', 'rb') as file:
        lda_model = pickle.load(file)

    return tfidf_vectorizer, lda_model

def load_sbert_t5_models():
    sbert_model = SentenceTransformer('student_panel/models/sbert_model')
    t5_tokenizer = T5Tokenizer.from_pretrained('student_panel/models/t5-small')
    t5_model = T5ForConditionalGeneration.from_pretrained('student_panel/models/t5-small')

    return sbert_model, t5_tokenizer, t5_model

# Preprocessing the answers (this would be the same as you used during training)
def preprocess_text(text):
    # Example: Lowercasing and removing special characters.
    return text.lower().strip()

def evaluate_answer(question, ideal_answer, student_answer):
    tfidf_vectorizer, lda_model = load_tfidf_lda_models()
    sbert_model, t5_tokenizer, t5_model = load_sbert_t5_models()

    # Preprocess the answers
    ideal_cleaned = preprocess_text(ideal_answer)
    student_cleaned = preprocess_text(student_answer)

    # TF-IDF for the single answer
    tfidf_ideal = tfidf_vectorizer.transform([ideal_cleaned])
    tfidf_student = tfidf_vectorizer.transform([student_cleaned])

    # LDA similarity score
    lda_ideal = lda_model.transform(tfidf_ideal)
    lda_student = lda_model.transform(tfidf_student)
    lda_score = cosine_similarity(lda_ideal, lda_student)[0][0]

    # SBERT similarity score
    sbert_similarity = cosine_similarity(
        [sbert_model.encode(ideal_answer)],
        [sbert_model.encode(student_answer)]
    )[0][0]

    # T5 similarity score
    t5_input = t5_tokenizer(f"generate answer: {ideal_answer}", return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        t5_output = t5_model.generate(input_ids=t5_input['input_ids'], attention_mask=t5_input['attention_mask'])
    t5_generated_answer = t5_tokenizer.decode(t5_output[0], skip_special_tokens=True)
    t5_similarity = cosine_similarity(
        [sbert_model.encode(t5_generated_answer)],
        [sbert_model.encode(student_answer)]
    )[0][0]

    # Length penalty for short answers
    ideal_length = len(ideal_answer.split())
    student_length = len(student_answer.split())
    length_ratio = student_length / ideal_length
    length_penalty = 1 if length_ratio >= 0.8 else max(0.5, length_ratio)

    # Compute final score with length penalty
    raw_final_score = (lda_score + sbert_similarity + t5_similarity) / 3
    scaled_score = raw_final_score * length_penalty * 10  # Scale to 10-point scale

    # Return the scores (for storing or display)
    return {
        "lda_score": lda_score,
        "sbert_score": sbert_similarity,
        "t5_score": t5_similarity,
        "length_penalty": length_penalty,
        "raw_final_score": raw_final_score,
        "scaled_score": round(scaled_score, 2)
    }
