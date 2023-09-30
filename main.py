import streamlit as st
import random
import time  # Import the time module at the top of your script

# Function to load questions from the file
def load_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    questions = []
    question_text = ''
    answers = []
    correct_answer_index = None

    for line in lines:
        if line.startswith('<>'):
            if question_text:
                questions.append((question_text, answers, correct_answer_index))
                question_text = ''
                answers = []
                correct_answer_index = None
            question_text = line[2:].strip()

        elif line.endswith('#\n'):
            try:
                correct_answer_index_str = line[:-2].strip()
                if correct_answer_index_str.isdigit():
                    correct_answer_index = int(correct_answer_index_str) - 1
                else:
                    st.write(f'Unexpected correct answer index format in line: {line}')
                    correct_answer_index = None
            except Exception as e:
                st.write(f'Error parsing correct answer index from line: {line}, Error: {e}')
                correct_answer_index = None

        elif line.strip():
            answers.append(line.strip())

    if question_text:
        questions.append((question_text, answers, correct_answer_index))

    return questions


# Load questions
questions = load_questions('out.txt')
random.shuffle(questions)  # Shuffle the questions

# Check if questions were loaded
if not questions:
    st.error('No questions were loaded. Please check the file path and format.')
    st.stop()

# Streamlit app
st.title('Quiz App')
# Check if the shuffled questions are already stored in session_state
# Check if the shuffled questions are already stored in session_state
if 'shuffled_questions' not in st.session_state:
    # Load and shuffle questions only once
    questions = load_questions('out.txt')
    random.shuffle(questions)
    st.session_state['shuffled_questions'] = questions
else:
    # Retrieve the shuffled questions from session_state
    questions = st.session_state['shuffled_questions']

# Check if questions were loaded
if not questions:
    st.error('No questions were loaded. Please check the file path and format.')
    st.stop()


# Check if questions were loaded
if not questions:
    st.error('No questions were loaded. Please check the file path and format.')
    st.stop()

# Session state to keep track of the current question, score, and incorrect answers
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = 0
    st.session_state['correct'] = 0
    st.session_state['incorrect'] = 0

question_text, answers, correct_answer_index = questions[st.session_state['current_question']]

st.write(f'Question: {question_text}')

def process_answer():
    selected_index = answers.index(answer_selected)
    if selected_index == correct_answer_index:
        st.success('Correct!')
        st.session_state['correct'] += 1
    else:
        st.error(f'Incorrect. The correct answer is: {answers[correct_answer_index]}')
        st.session_state['incorrect'] += 1

answer_selected = st.radio(
    'Choose an answer:',
    answers,
    key=f'question_{st.session_state["current_question"]}',
    on_change=process_answer
)



# Add a "Next" button to proceed to the next question
if st.button('Next'):
    st.session_state['current_question'] = (st.session_state['current_question'] + 1) % len(questions)
    st.experimental_rerun()  # Rerun the script to update the displayed question

st.write(f'Correct Answers: {st.session_state["correct"]}')
st.write(f'Incorrect Answers: {st.session_state["incorrect"]}')