# AI Powered Descriptive Answer Evaluation System (AI-DAES)

## Overview
AI-DAES is an AI-driven system designed to evaluate descriptive answers provided by students in an online assessment environment. The system utilizes advanced NLP techniques, including TF-IDF vectorization, SBERT embeddings, LDA topic modeling, and T5-generated answers, to assess student responses with high accuracy.

## Features
- **Speech-to-Text Answer Submission**: Students provide answers verbally, which are converted into text using DeepSpeech.
- **AI-Based Answer Evaluation**: ML model scores responses based on similarity with the ideal answer.
- **Admin Panel**: Upload questions, set evaluation criteria, and monitor scores.
- **Student Panel**: Secure login, real-time answering, and auto-submission when time expires.
- **Automated Scoring**: Evaluates answers using semantic similarity and topic modeling.
- **Secure Authentication**: Role-based access control for students and admins.

## Technology Stack
### Backend
- **Django** - Web framework for authentication, database operations, and API endpoints.
- **Django REST Framework (DRF)** - Modular RESTful API design.
- **SQLite** - Database to store questions, answers, and scores.
- **DeepSpeech** - Converts speech to text.
- **Scikit-learn, TensorFlow** - ML models for answer evaluation.

### Frontend
- **Django Templates (HTML, CSS, JavaScript, Bootstrap)** - User interface.
- **AJAX / Fetch API** - Handles exam navigation without page reloads.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip
- virtualenv
- Node.js (for frontend enhancement, if needed)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-DAES.git
   cd AI-DAES
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

## Usage
### Admin Panel
1. Log in at `/admin`.
2. Upload JSON files containing questions and ideal answers.
3. Monitor student responses and evaluation results.

### Student Panel
1. Log in with a registration number and secret key.
2. Answer questions verbally; responses will be converted into text.
3. Submit answers before time expires or allow auto-submission.

## Evaluation Pipeline
1. **Preprocessing**: Converts text to lowercase, removes stopwords, and applies lemmatization.
2. **Feature Extraction**:
   - TF-IDF for keyword importance.
   - LDA Topic Modeling for topic distribution.
   - SBERT embeddings for deep semantic similarity.
   - T5 Model for answer generation and comparison.
3. **Scoring**:
   - Computes cosine similarity for LDA, SBERT, and T5 results.
   - Adjusts for answer length penalties.
   - Aggregates a final score on a 10-point scale.

## Security
- **Role-Based Access Control (RBAC)**: Differentiated permissions for students and admins.
- **CSRF Protection & Password Hashing**: Ensures security best practices.

## Contributors
- **P. A. Mohammed Fayad** (Develop the machine learning-based answer evaluation system using TF-IDF, LDA, SBERT, and T5 models.
Implement algorithms to compute similarity scores and assign final grades.
)
- **S Nandhagopan** (Develop the student panel for authentication, exam participation, and answer submissions.
Implement the admin panel to manage exams, student registrations, and monitor exam activity.
)
- **Mohammed Shamil Abdul Salam** (Design and implement database models to store students, exams, answers, and scores.
Develop API endpoints using Django DRF for handling exam questions, answer submissions, and score retrieval.
)
- **Mohammed Irshan CT** (Develop an automated JavaScript-based exam timer that ensures timely submission of responses.
Implement DeepSpeech, Speech-to-Text API for converting spoken answers into text.
)

## License
This project is licensed under the MIT License.

## Future Enhancements
- **Robotics Integration**: Automate physical answer sheet evaluation.
- **Expanded ML Model Training**: Enhance evaluation accuracy with larger datasets.
- **Blockchain Integration**: Ensure immutable answer records.

---

For queries or contributions, please raise an issue or pull request in the repository.
