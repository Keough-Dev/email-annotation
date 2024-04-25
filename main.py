import streamlit as st
import pandas as pd
import json
import requests

if 'questions' not in st.session_state or 'answers' not in st.session_state:
    st.session_state.questions = ["Would you like to install a sensor or skip this step?"]
    st.session_state.answers = []
    st.session_state.current_index = 0

headers = {"Content-Type": "application/json"}

st.title('Node Chat')
st.image('https://nodeware-static.s3.amazonaws.com/img/node.png')

current_question = st.session_state.questions[st.session_state.current_index]
answer = st.text_input(current_question, key=str(st.session_state.current_index))

if st.button('Send'):
    if answer:
        response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/acceptinput', json={'body': answer}, headers=headers)
        response_data = response.json()
        new_question = response_data.get('next_question')
        response_message = response_data.get('message', '')

        st.session_state.answers.append(answer)

        if new_question:
            st.session_state.questions.append(new_question)
            st.session_state.current_index += 1
        else:
            st.write(response_message)
            st.write("Conversation ended.")
            st.write(st.session_state.questions)
            st.write(st.session_state.answers)


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
