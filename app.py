import re
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA = {
    "Python": {
        "What is recursion in Python?": {
            "reference": "Recursion is a process where a function calls itself to solve a smaller version of a problem. A base case is used to stop the recursion.",

            "concepts": {
                "function calls itself": "A recursive function calls itself again.",
                "smaller problem": "Recursion usually solves a smaller version of the same problem.",
                "base case": "A base case gives the stopping condition so recursion does not continue forever."
            },

            "followups": {
                "function calls itself": "What does a recursive function do repeatedly?",
                "smaller problem": "In recursion, does the function usually solve the same problem or a smaller version of the problem?",
                "base case": "What happens if a recursive function keeps calling itself without stopping?"
            },

            "followup_keywords": {
                "function calls itself": ["call", "again", "itself"],
                "smaller problem": ["smaller", "version", "problem"],
                "base case": ["keep", "calling", "error"]
            }
        },

        "What is a list in Python?": {
            "reference": "A list is a collection in Python that is ordered, changeable, and allows duplicate values.",

            "concepts": {
                "collection": "A list stores multiple values together.",
                "ordered": "List elements have a defined order.",
                "changeable": "List elements can be changed after creation.",
                "duplicates": "A list can contain duplicate values."
            },

            "followups": {
                "collection": "Why do we use a list in Python?",
                "ordered": "Does a Python list keep its elements in an order?",
                "changeable": "Can we change an element of a Python list after creating it?",
                "duplicates": "Can a Python list contain the same value more than once?"
            },

            "followup_keywords": {
                "collection": ["store", "multiple", "values"],
                "ordered": ["order", "position", "sequence"],
                "changeable": ["change", "modify", "element"],
                "duplicates": ["duplicate", "same", "more"]
            }
        }
    },

    "Java": {
        "What is inheritance in Java?": {
            "reference": "Inheritance is a feature in Java where one class acquires properties and methods of another class. It supports code reuse.",

            "concepts": {
                "one class acquires": "A child class can acquire properties and methods from another class.",
                "properties and methods": "Inheritance allows a class to use properties and methods of another class.",
                "code reuse": "Inheritance helps reuse existing code."
            },

            "followups": {
                "one class acquires": "What can a child class get from a parent class?",
                "properties and methods": "What two common things can be inherited from another class?",
                "code reuse": "How does inheritance help programmers?"
            },

            "followup_keywords": {
                "one class acquires": ["properties", "methods", "parent"],
                "properties and methods": ["properties", "methods"],
                "code reuse": ["reuse", "code", "existing"]
            }
        },

        "What is a constructor in Java?": {
            "reference": "A constructor is a special method-like block used to initialize objects. It has the same name as the class and has no return type.",

            "concepts": {
                "initialize objects": "A constructor is used to initialize an object.",
                "same name as class": "The constructor has the same name as its class.",
                "no return type": "A constructor does not have a return type."
            },

            "followups": {
                "initialize objects": "Why is a constructor used in Java?",
                "same name as class": "What name does a constructor have?",
                "no return type": "Does a constructor have a return type?"
            },

            "followup_keywords": {
                "initialize objects": ["initialize", "object"],
                "same name as class": ["same", "class", "name"],
                "no return type": ["no", "return", "type"]
            }
        }
    }
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def similarity_score(student_answer, reference):
    texts = [
        clean_text(student_answer),
        clean_text(reference)
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)

    score = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0] * 100

    return round(score)


def check_concepts(answer, concepts):
    words = set(clean_text(answer).split())

    covered = []
    missing = []

    for concept in concepts:
        keywords = concept.split()

        matches = sum(
            1 for word in keywords
            if word in words
        )

        if matches >= max(1, len(keywords) / 2):
            covered.append(concept)
        else:
            missing.append(concept)

    return covered, missing


def check_followup(answer, keywords):
    words = set(clean_text(answer).split())

    matches = sum(
        1 for keyword in keywords
        if keyword in words
    )

    score = round(
        (matches / len(keywords)) * 100
    )

    return max(0, min(score, 100))


st.set_page_config(
    page_title="AI Answer Reality Checker",
    page_icon="🧠",
    layout="centered"
)


st.title("🧠 AI Answer Reality Checker")

st.subheader(
    "AI-Based Student Understanding Evaluation"
)

st.write(
    "A correct answer does not always mean the student "
    "fully understands the concept. This tool checks the "
    "answer, identifies covered and missing concepts, "
    "asks a suitable follow-up question, and gives "
    "learning feedback."
)


subject = st.selectbox(
    "Select Subject",
    list(DATA.keys())
)


question = st.selectbox(
    "Select Question",
    list(DATA[subject].keys())
)


student_answer = st.text_area(
    "Enter your own answer:",
    placeholder="Write the answer in your own words..."
)


if st.button(
    "🔍 Check My Answer",
    type="primary"
):

    if not student_answer.strip():

        st.warning(
            "Please enter an answer first."
        )

    else:

        qdata = DATA[subject][question]

        similarity = similarity_score(
            student_answer,
            qdata["reference"]
        )

        covered, missing = check_concepts(
            student_answer,
            qdata["concepts"]
        )

        concept_score = round(
            (len(covered) /
             len(qdata["concepts"])) * 100
        )

        initial_score = round(
            (similarity + concept_score) / 2
        )


        st.divider()

        st.subheader(
            "📊 Initial Evaluation"
        )

        st.metric(
            "Answer Similarity",
            f"{similarity}%"
        )

        st.metric(
            "Initial Understanding",
            f"{initial_score}%"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.success(
                "Covered Concepts"
            )

            if covered:

                for item in covered:
                    st.write(
                        "✅",
                        item
                    )

            else:

                st.write(
                    "No major concepts detected."
                )


        with col2:

            st.error(
                "Missing Concepts"
            )

            if missing:

                for item in missing:
                    st.write(
                        "❌",
                        item
                    )

            else:

                st.write(
                    "No major concepts missing."
                )


        if missing:

            missing_concept = missing[0]

            followup = qdata[
                "followups"
            ][missing_concept]

            expected_keywords = qdata[
                "followup_keywords"
            ][missing_concept]


            st.divider()

            st.subheader(
                "🧩 Understanding Check"
            )

            st.info(
                f"Missing concept: **{missing_concept}**\n\n"
                f"Easy follow-up question: **{followup}**"
            )


            followup_answer = st.text_area(
                "Answer the follow-up question:",
                key="followup_answer"
            )


            if st.button(
                "✅ Check Understanding"
            ):

                if not followup_answer.strip():

                    st.warning(
                        "Please answer the follow-up question."
                    )

                else:

                    followup_score = check_followup(
                        followup_answer,
                        expected_keywords
                    )

                    final_score = round(
                        (initial_score * 0.65) +
                        (followup_score * 0.35)
                    )


                    st.divider()

                    st.subheader(
                        "🎯 Final Result"
                    )

                    st.metric(
                        "Understanding Check",
                        f"{followup_score}%"
                    )

                    st.metric(
                        "Final Understanding Score",
                        f"{final_score}%"
                    )


                    if followup_score >= 80:

                        st.success(
                            "Good understanding! "
                            "Your follow-up answer shows "
                            "that you understand the "
                            "missing concept."
                        )

                    elif followup_score >= 50:

                        st.warning(
                            "Partial understanding. "
                            "Review the missing concept "
                            "and try again."
                        )

                    else:

                        st.error(
                            "The missing concept needs "
                            "more practice. Review the "
                            "explanation below."
                        )


                    st.write(
                        "**Concept Explanation:**"
                    )

                    st.write(
                        qdata["concepts"][
                            missing_concept
                        ]
                    )


                    st.caption(
                        "Final score = 65% initial "
                        "evaluation + 35% understanding check."
                    )


        else:

            st.divider()

            st.success(
                "🎉 All important concepts were "
                "detected in your answer. "
                "No follow-up question is required."
            )

            st.metric(
                "Final Understanding Score",
                f"{initial_score}%"
            )


st.divider()

st.caption(
    "Mini Project | Python + Streamlit + NLP + "
    "TF-IDF + Cosine Similarity"
)
