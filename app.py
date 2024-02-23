import streamlit as st
from Comment_scrapper import save_comments_to_file
from Comment_analyzer import analyze_sentiment

st.image("ytlogo.jpeg",width=300)

st.title("Youtube Comments Analyzer ")

user_input=st.text_input("Paste your Youtube URL here!")
if st.button("Analyze"):
    st.write("Fetching Comments..")
    save_comments_to_file(user_input)
    st.write("Analyzing Comments..")
    result=analyze_sentiment()

    col1, col2, col3=st.columns(3)
    col1_expander=col1.expander("Positive Comments")
    with col1_expander:
        for i in result["positive_comments"]:
            col1_expander.write(i)

    col2_expander=col2.expander("Negative Comments")
    with col2_expander:
        for i in result["negative_comments"]:
            col2_expander.write(i)   

    col3_expander=col3.expander("Questions")
    with col3_expander:
        for i in result["questions"]:
            col3_expander.write(i)   























