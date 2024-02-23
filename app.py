# import streamlit as st
# import os
# from Comment_analyzer import sentiment_scores,analyze_sentiment
# from Comment_scrapper import save_comments_to_file

# st.title("YouTube Comment Analysis")

# url_input = st.text_input("Enter a YouTube video URL:")

# start_button = st.button("Start Analysis")

# if start_button:
#     if not url_input:
#         st.error("Please enter a valid YouTube video URL.")
#     else:
#         try:
#             comment_scrape=save_comments_to_file(url_input)
#             analysis_results = analyze_sentiment()

#             positive_button = st.button("Positive Comments")
#             negative_button = st.button("Negative Comments")
#             neutral_button = st.button("Neutral Comments")
#             questions_button = st.button("Questions Asked")

#             # Display comments based on clicked button
#             if positive_button:
#                 st.header("Positive Comments:")
#                 st.write("\n".join(analysis_results['positive_comments']))
#             elif negative_button:
#                 st.header("Negative Comments:")
#                 st.write("\n".join(analysis_results['negative_comments']))
#             elif neutral_button:
#                 st.header("Neutral Comments:")
#                 st.write("\n".join(analysis_results['neutral_comments']))
#             elif questions_button:
#                 st.header("Questions Asked:")
#                 st.write("\n".join(analysis_results['questions']))

#         except Exception as e:
#             st.error("An error occurred")

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























