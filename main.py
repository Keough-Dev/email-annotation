import streamlit as st
import pandas as pd
import json
import re  # Import regular expressions

# Function to convert dictionary to dataframe
def dict_to_df(d):
    return pd.DataFrame([d])

# Function to annotate text with regular expression for better matching
def annotate_text(body, data):
    # Create annotations dictionary excluding certain keys
    annotations = {key: str(value) for key, value in data.items() if key not in ['contact_row', 'company_row', 'body']}
    
    # Use regular expressions to replace each key with an HTML link for annotation
    for key, value in annotations.items():
        # Regex to match word boundaries taking care of case insensitivity
        pattern = r'\b{}\b'.format(re.escape(value))
        url = f"http://example.com/{key}"  # Placeholder URL for demonstration
        body = re.sub(pattern, f'<a href="{url}" style="background-color: yellow;">{value}</a>', body, flags=re.IGNORECASE)
    
    return body

def main():
    st.title('Email Data Processor')

    # Text area for user input of JSON data
    data = st.text_area("Paste your JSON data here:", height=300)
    if st.button("Process Data"):
        try:
            # Load data as dictionary
            data_dict = json.loads(data)
            
            # Extract body text and display it
            body_text = data_dict.get('body', '')
            st.write("## Original Body Text")
            st.write(body_text)
            
            # Display contact and company rows as dataframes
            st.write("## Contact Details (DataFrame)")
            contact_df = dict_to_df(data_dict['contact_row'])
            st.dataframe(contact_df)
            
            st.write("## Company Details (DataFrame)")
            company_df = dict_to_df(data_dict['company_row'])
            st.dataframe(company_df)
            
            # Annotate and display the body text
            st.write("## Annotated Body Text")
            annotated_body = annotate_text(body_text, data_dict)
            st.markdown(annotated_body, unsafe_allow_html=True)
        
        except json.JSONDecodeError:
            st.error("Invalid JSON data. Please check and try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()







# import streamlit as st
# import re

# def highlight_text(text, keywords):
#     # Create a regular expression from the keywords
#     regex_pattern = '|'.join(map(re.escape, keywords))
    
#     # Substitute the keywords with highlighted version
#     highlighted_text = re.sub(f"({regex_pattern})", r'<span style="background-color:yellow;">\1</span>', text, flags=re.IGNORECASE)
    
#     return highlighted_text

# def find_keywords(text):
#     # Simple keyword logic: highlight some common words for demonstration
#     # You can modify this function to use more complex logic or NLP models
#     return ['confidential', 'urgent', 'immediately', 'please respond']

# def main():
#     st.title("Email Highlighter App")
    
#     # Text area for user input
#     email_content = st.text_area("Enter your email text here:", height=300)
    
#     if st.button("Process Email"):
#         if email_content:
#             # Find keywords in the text
#             keywords = find_keywords(email_content)
            
#             # Highlight the keywords in the text
#             highlighted_email = highlight_text(email_content, keywords)
            
#             # Display the highlighted text
#             st.markdown(highlighted_email, unsafe_allow_html=True)
#         else:
#             st.warning("Please enter some text to process.")

# if __name__ == "__main__":
#     main()
