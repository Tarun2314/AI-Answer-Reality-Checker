# 🧠 AI Answer Reality Checker

## AI-Based Student Understanding Evaluation

This project checks whether a student's answer shows actual understanding of a concept.

A correct answer does not always mean that a student completely understands the topic. This system analyzes the student's answer, identifies covered and missing concepts, asks a suitable follow-up question, and provides an understanding score.

## 🔍 How It Works

1. Student selects a subject and question.
2. Student enters an answer in their own words.
3. The system compares the answer with a reference answer.
4. Important concepts are identified.
5. Missing concepts are detected.
6. An easier follow-up question is asked.
7. The follow-up answer is checked.
8. A final understanding score and feedback are provided.

## 🛠 Technologies Used

- Python
- Streamlit
- Scikit-learn
- Natural Language Processing (NLP)
- TF-IDF
- Cosine Similarity

## 📊 Scoring

The final score is calculated using:

**65% Initial Evaluation + 35% Understanding Check**

The score is an educational indicator and is not a perfect measurement of a student's knowledge.

## 🚀 Run the Project

Install the required libraries:

```bash
pip install -r requirements.txt
streamlit run app.py
