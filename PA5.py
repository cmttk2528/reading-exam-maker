import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)

# Making the exam
prompt1 = """Act as exam maker. You will be given a passage.
Create reading comprehension exam and provide 5 four-choice questions based on the passage. 
Question number 1 must ask about the main idea of the passage.
pattern: 1.question
            A) choice A
            B) choice B
            C) choice C
            D) choice D
"""
# Making the answer key
prompt2 = """list the answer key of the questions from prompt1 in a JSON format.
            each answer key should have 2 fields: question with question number and answer.
"""

# Making the difficult words list from the passage
prompt3 = """list the difficult words from the passage in a JSON format.
each word should have 4 fields: word, part of speech, definition, and synonyms."""

st.title('Reading Comprehension Exam Maker')
st.markdown('***:rainbow[!Review your comprehension and practice the reading exam!]***')
st.markdown(""":grey[Input the passage that you want to make a reading comprehension exam.]  
:grey[You will get] ***a reading exam*** :grey[and some] ***lists of vocabulary*** :grey[from the passage.]
""")

user_input = st.text_area("The passage that you want to make an exam:", "Enter your passage here")

if st.button('Submit'):
    st.subheader('Reading Comprehension', divider='rainbow')
    messages_so_far = [
        {"role": "system", "content": prompt1},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far
    )
    exam_result = response.choices[0].message.content
    st.text(user_input+'\n'
            '********************'
            )
    st.text('Read the passage and answer the following questions.\n'
            + exam_result)
    
    # Answer key
    st.subheader('Answer Key', divider='rainbow')
    messages_so_far2 = [
        {"role": "system", "content": prompt2},
        {'role': 'user', 'content': exam_result},
    ]
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far2
    )
    answer_key = response2.choices[0].message.content

    answer_table = json.loads(answer_key)
    print(answer_table)

    answer_df = pd.DataFrame.from_dict(answer_table)
    print(answer_df)

    st.table(answer_df)

    # Difficult words
    st.subheader('Vocabulary', divider='rainbow')

    messages_so_far3 = [
        {"role": "system", "content": prompt3},
        {'role': 'user', 'content': user_input},
    ]

    response3 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far3
    )

    vocab_result = response3.choices[0].message.content

    vocab_table = json.loads(vocab_result)
    print(vocab_table)

    vocab_df = pd.DataFrame.from_dict(vocab_table)
    print(vocab_df)

    st.table(vocab_df)


    





