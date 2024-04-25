import streamlit as st
import pandas as pd
import json
import requests

# st.title('Node Chat')
# st.image('https://nodeware-static.s3.amazonaws.com/img/node.png')

# headers = {"Content-Type": "application/json"}

# user_input = st.text_input("Enter your query here:")

# # Button to send the message
# if st.button('Submit'):
#     if user_input:  # Check if the input is not empty
#         # Sending the user input to the API Gateway via a POST request
#         response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/accept-query', json={'body': user_input}, headers=headers)
#         if response.status_code == 200:
#             # Optionally, handle the response from the server
#             # st.success("Message sent successfully!")
#             st.write((response.json()['body']))  # Display the JSON response if API sends something back
#         else:
#             st.error("Failed to send the message. Status code: {}".format(response.status_code))
#     else:
#         st.error("Please enter a message before submitting.")







 

questions = ["Would you like to install a sensor or skip this step?", "Would you like to install a software sensor or virutal appliance?", "What operating system are you working off of?"]

def reset_session():

    st.session_state.questions = questions

    st.session_state.answers = []

    st.session_state.current_index = 0

 

# Initialize session state only if it has not been initialized before

if 'current_index' not in st.session_state:

    st.session_state.questions = questions

    st.session_state.answers = []

    st.session_state.current_index = 0

 

headers = {"Content-Type": "application/json"}

 

st.title('Node Chat')

st.image('https://nodeware-static.s3.amazonaws.com/img/node.png')

 

# Get the current question based on current_index

current_question = st.session_state.questions[st.session_state.current_index]

answer = st.text_input(current_question, key=str(st.session_state.current_index))

 

if st.button('Send'):

    if answer:

        response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/acceptinput', json={'body': answer}, headers=headers)

        response_data = response.json()

        response_message = response_data.get('body', '')

        try:

            response_processed = json.loads(response_message)['body']

        except:

            response_processed = ''

 

        html_text = response_processed.replace("\n", "<br>")
        st.write(html_text)
        st.markdown(html_text, unsafe_allow_html=True)

 

 

        # Append the answer to the answers list

        st.session_state.answers.append(answer)

 

        # Check if there are more questions to ask

        if st.session_state.current_index < len(st.session_state.questions) - 1:

            st.session_state.current_index += 1

        else:

            st.write("Conversation ended.")

            st.write("Your responses:")

            for q, a in zip(st.session_state.questions, st.session_state.answers):

                st.write(f"{q}: {a}")

            # st.write(response_message)

            # st.button("Reset", on_click=reset_session)

# else:

#     st.session_state.current_index = 0

 

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

    df_responses = df_responses._append(temp_df, ignore_index = True)

 

# Submit button

if st.button('Submit Responses'):

    st.write("You submitted:")

    st.write(df_responses)

    response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/feedbackresults', json={'body': df_responses.to_json()}, headers=headers)

    if response.status_code == 200:

        # Display the response in the chat

        st.write(value=f'{response.json()["body"]}', height=300)

    else:

        st.error("Failed to get a response from the server.")








    

# def reset_session():
#     st.session_state['questions'] = ["Would you like to install a sensor or skip this step?", "would you like sensor or virtual", "What operating system are you working off of?"]
#     st.session_state['answers'] = []
#     st.session_state['current_index'] = 0
#     st.session_state['submit'] = False

# # Initialize session state only if it has not been initialized before
# if 'current_index' not in st.session_state:
#     reset_session()

# headers = {"Content-Type": "application/json"}

# st.title('Node Chat')
# st.image('https://nodeware-static.s3.amazonaws.com/img/node.png')

# # Get the current question based on current_index
# current_question = st.session_state['questions'][st.session_state['current_index']]
# answer = st.text_input(current_question, key=st.session_state['current_index'], on_change=lambda: st.session_state.update({"submit": True}))

# if st.button('Send') or st.session_state['submit']:
#     if answer.strip():
#         response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/acceptinput', json={'body': answer}, headers=headers)
#         response_data = response.json()
#         response_message = response_data.get('body', '')

#         st.session_state['answers'].append(answer)

#         # Increment to move to the next question or end conversation
#         if st.session_state['current_index'] < len(st.session_state['questions']) - 1:
#             st.session_state['current_index'] += 1
#         else:
#             st.write("Conversation ended.")
#             st.write("Your responses:")
#             for q, a in zip(st.session_state['questions'], st.session_state['answers']):
#                 st.write(f"{q}: {a}")
#             st.write(response_message)
#             reset_session()  # Optionally reset the session at the end of the conversation

#     st.session_state['submit'] = False  # Reset the submit trigger

# # Optionally, add a button to reset the conversation
# if st.button("Reset Conversation"):
#     reset_session()



# # Questions for the survey
# questions = {
#     "Question 1": "Your overall satisfaction with the sensor/agent installation process.",
#     "Question 2": "How helpful was the AI assistant during the sensor/agent installation process and onboarding experience",
#     "Question 3": "The accuracy of the assistance and information provided?",
#     "Question 4": "Your overall satisfaction with the onboarding experience after sensor/agent installation process?",
#     "Question 5": "How likely are you to recommend the Nodeware sensor/agent to others based on the installation process and onboarding experience?"
# }

# # Create a DataFrame to store responses
# df_responses = pd.DataFrame(columns=["Question", "Response"])

# # Display radio buttons for each question
# for question, label in questions.items():
#     response = st.radio(label, [1, 2, 3, 4, 5], key=question)
#     temp_df = {"Question": question, "Response": response}
#     st.write(temp_df)
#     df_responses = df_responses._append(temp_df, ignore_index = True)

# # Submit button
# if st.button('Submit Responses'):
#     st.write("You submitted:")
#     st.write(df_responses)
#     response = requests.post('https://66oms19la2.execute-api.us-east-1.amazonaws.com/demo/feedbackresults', json={'body': df_responses.to_json()}, headers=headers)
#     if response.status_code == 200:
#         # Display the response in the chat
#         st.text_area("Chat", value=f'You: {user_input}\nBot: {response.json()["body"]}', height=300)
#     else:
#         st.error("Failed to get a response from the server.")
