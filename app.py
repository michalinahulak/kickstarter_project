import streamlit as st
import joblib
import pandas as pd
import urllib.request
from io import BytesIO
import requests

st.write("# Kickstarter fundraising prediction")

col1, col2 = st.columns(2)

# getting user input

title = col1.text_input("Title")

category = col2.selectbox("Select main category", ["Comics", "Crafts", 'Dance', 'Design',
                                                  'Fashion', 'Film & Video', 'Food',
                                                  'Games', 'Journalism', 'Music', 'Photography',
                                                  'Publishing', 'Technology', 'Theater'
                                                  ])

goal = col1.number_input("Enter goal in your currency", step=10)

days = col2.number_input("How many days does the fundraiser last?",  step=1)

country = col1.selectbox("Select your country", ["AU", "BE", 'CA', 'CH', 'DE', 'DK',
                                                'ES', 'FR', 'GB', 'HK', 'IE', 'IT',
                                                'JP', 'LU', 'MX', 'NL', 'NO', 'NZ',
                                                'SE', 'SG', 'US'
                                                ])

launch_hour = col2.selectbox("Select the time of day to start the fundraiser", ["6-12", "12-18", '18-22', '22-24', '24-6'])

# Create a 'title_length' column and count the characters in the title
title_lenght = len(title)

# collecting data for prediction in one DataFrame
df_predict = pd.DataFrame([[category, goal, country, days, launch_hour, title_lenght]],
                          columns=['main_category',	'goal',	'country',	'days',	'launch_hour',	'title_lenght'])


#upload pipeline from Github:
my_link = 'https://github.com/michalinahulak/kickstarter_project/blob/main/pipeline_rf.joblib?raw=true'
pipeline = joblib.load(BytesIO(requests.get(my_link).content))
prediction = pipeline.predict(df_predict)

# upload local:
# path = 'C:/Users/User/projekt_kick/pipeline_rf.joblib'  # enter your path
# pipeline = joblib.load(path)
# prediction = pipeline.predict(df_predict)

if st.button('Predict'):

    if(prediction[0]=='failed'):
        st.write('<p class="big-font"> Your fundraiser will probably fail. </p>', unsafe_allow_html=True)

    else:
        st.write('<p class="big-font">Your fundraiser is likely to be successful.</p>',  unsafe_allow_html=True)