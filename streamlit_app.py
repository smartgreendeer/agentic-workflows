import streamlit as st
import workflow_setup

# Streamlit app
st.title("RetailX AI Assistant")
st.write("Ask a question about RetailX customers, products, and sales:")

question = st.text_input("Question")
if st.button("Submit"):
    if question:
        inputs = {"question": question}
        result = workflow_setup.app.invoke(inputs)
        st.write("Answer:", result['answer'])
    else:
        st.write("Please enter a question.")
