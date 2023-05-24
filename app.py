import streamlit as st
import pandas as pd
import gdown
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
import os
import joblib

#upload dataset
output = 'kickstarter_dataset_clean.csv'
if not os.path.exists(output):
    url = 'https://drive.google.com/uc?id=14VrYF7tHd4GxgUd9gTf5sIjBlvD23FyK'
    gdown.download(url, output, quiet=False)
df = pd.read_csv(output)

# create my_pipeline
output_pipeline = 'my_pipeline.joblib'

if not os.path.exists(output_pipeline):
    # create pipeline
    X = df.drop(['state'], axis=1)
    y = df['state']

    # Split data into train, test, validation sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    # select categorical cols
    categorical_cols = ['main_category', 'country', 'launch_hour']

    # select numerical cols
    numerical_cols = ['goal', 'days', 'title_lenght']

    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    numerical_transformer = MinMaxScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_cols),
            ('num', numerical_transformer, numerical_cols)])

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    my_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    my_pipeline.fit(X_train, y_train)

    # Save the pipeline
    joblib.dump(my_pipeline, output_pipeline)

else:
    # Load the pipeline
    my_pipeline = joblib.load(output_pipeline)


# streamlite
#st.write("# Kickstarter fundraising prediction")
st.title("Kickstarter Fundraising Prediction")
st.markdown("Enter the details of your fundraiser and click **Predict**.")

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
launch_hour = col2.selectbox("Select the time of day to start the fundraiser", ["6-12",
                                                                                "12-18",
                                                                                '18-22',
                                                                                '22-24',
                                                                                '24-6'])

# Create a 'title_length' column and count the characters in the title
title_length = len(title)

# collecting data for prediction in one DataFrame
df_predict = pd.DataFrame([[category, goal, country, days, launch_hour, title_length]],
                          columns=['main_category',	'goal',	'country',	'days',	'launch_hour',	'title_lenght'])


prediction = my_pipeline.predict(df_predict)

if st.button('Predict'):

    if(prediction[0] == 'failed'):
        st.write('<p class="big-font"> Your fundraiser will probably fail. </p>', unsafe_allow_html=True)

    else:
        st.write('<p class="big-font">Your fundraiser is likely to be successful.</p>',  unsafe_allow_html=True)