import streamlit as st
import pandas as pd
import json
import requests

# Chat interface
st.title('Node Chat')
st.image('https://nodeware-static.s3.amazonaws.com/img/node.png')

current_question = st.session_state.questions[-1]
answer = st.text_input(current_question, key=str(len(st.session_state.questions)))

if 'questions' not in st.session_state:
    st.session_state.questions = ["Would you like to install a sensor or skip this step?"]
    st.session_state.answers = []

if st.button('Send'):
    if answer:
        response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/acceptinput', json={'body': answer}, headers=headers)
        new_question = response.get('next_question', None)
        response_message = response.get('message', '')

        st.session_state.answers.append(answer)

        if new_question:
            st.session_state.questions.append(new_question)
            st.experimental_r

# # Button to send the message
# if st.button('Send'):
#     # Sending the user input to AWS Lambda via API Gateway
#     response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/acceptinput', json={'body': answer}, headers=headers)
#     if response.status_code == 200:
#         # Display the response in the chat
#         st.text_area("Chat", value=f'You: {user_input}\nBot: {response.json()["body"]}', height=300)
#     else:
#         st.error("Failed to get a response from the server.")

# Questions for the survey
questions = {
    "Question 1": "Your overall satisfaction with the sensor/agent installation process.",
    "Question 2": "How helpful was the AI assistant during the sensor/agent installation process and onboarding experience",
    "Question 3": "The accuracy of the assistance and information provided?",
    "Question 4": "Your overall satisfaction with the onboarding experience after sensor/agent installation process?",
    "Question 5": "How likely are you to recommend the Nodeware sensor/agent to others based on the installation process and onboarding experience?"
}

# Create a DataFrame to store responses
df_responses = pd.DataFrame(columns=["Question", "Response"])

# Display radio buttons for each question
for question, label in questions.items():
    response = st.radio(label, [1, 2, 3, 4, 5], key=question)
    temp_df = {"Question": question, "Response": response}
    st.write(temp_df)
    df_responses = df_responses._append(temp_df, ignore_index = True)

# Submit button
if st.button('Submit Responses'):
    st.write("You submitted:")
    st.write(df_responses)
    response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/feedbackresults', json={'body': df_responses.to_json()}, headers=headers)
    if response.status_code == 200:
        # Display the response in the chat
        st.text_area("Chat", value=f'You: {user_input}\nBot: {response.json()["body"]}', height=300)
    else:
        st.error("Failed to get a response from the server.")
