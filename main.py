import streamlit as st
import re

def highlight_text(text, keywords):
    # Create a regular expression from the keywords
    regex_pattern = '|'.join(map(re.escape, keywords))
    
    # Substitute the keywords with highlighted version
    highlighted_text = re.sub(f"({regex_pattern})", r'<span style="background-color:yellow;">\1</span>', text, flags=re.IGNORECASE)
    
    return highlighted_text

def find_keywords(text):
    # Simple keyword logic: highlight some common words for demonstration
    # You can modify this function to use more complex logic or NLP models
    return ['confidential', 'urgent', 'immediately', 'please respond']

def main():
    st.title("Email Highlighter App")
    
    # Text area for user input
    email_content = st.text_area("Enter your email text here:", height=300)
    
    if st.button("Process Email"):
        if email_content:
            # Find keywords in the text
            keywords = find_keywords(email_content)
            
            # Highlight the keywords in the text
            highlighted_email = highlight_text(email_content, keywords)
            
            # Display the highlighted text
            st.markdown(highlighted_email, unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to process.")

if __name__ == "__main__":
    main()
