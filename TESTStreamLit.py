import numpy as np
import pandas as pd
from sqlalchemy import null
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect
import streamlit as st
st.set_page_config(layout="wide")


"""# 2022-23 DownGoesBrown NHL Prediction Contest Entry Form
Welcome to the 2022-23 DownGoesBrown NHL Prediction Contest! Due to 
changes on The Athletic's website regarding web scraping of comment, 
this form is being used to collect entries for this year's contest. As
a result of this change, the contest entry form does have to request 
your name and your email address. After submitting your entry, you 
may update your entry by submitting another entry and using the same
name and email address. 

Please be sure to provide a name for Sean to refer to you by when he
discusses how your entry was perfect and won the contest (or how your 
entry was terrible and you should've known better). Also, please be sure
to provide a working email address that you check regularly, just in 
case you get lucky and win, so that Sean can contact you about mailing 
you a prize. If he can't get ahold of you, you won't get your prize, 
and no one will ever believe that you won a contest on the internet. 

Your email address will not be used for any other purpose. 

RULES: For each question, up to 5 answers may be provided to earn
increasing points per correct answer (1 answer = 1 point, 2 answers = 
3 points, 3 answers = 6 points, 4 answers = 10 points, and 5 answers = 
15 points) on a particular question. ANY incorrect answer on a 
particular question will result in 0 points for that question, no 
matter how many right answers were provided. You are _not required_ to 
provide 5 answers for each question, so you can choose whether to take
the risk and go for maximum possible points, or play it safe with a 
few "sure things" to get some points on the board.  

Good luck with this year's contest! You're gonna need it!
"""

with st.form("contest_entry_form"):

    "### Entrant name & email address:"
    entrant_name = st.text_input("Your name")
    if len(entrant_name) < 1:
        st.error("Please provide a valid name.")
    entrant_email = st.text_input("Your email address")
    if entrant_email.find("@") == -1:
        st.error("Please provide a valid email address.")
    if entrant_email.find(".") == -1:
        st.error("Please provide a valid email address.")

    "### Q1: Provide up to five teams which will **definitely** make the playoffs in the 2022-23 season:"
    accepted_teams = ["Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres", "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche", "Columbus Blue Jackets", "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers", "Florida Panthers", "Los Angeles Kings", "Minnesota Wild", "Montreal Canadiens", "Nashville Predators", "New Jersey Devils", "New York Islanders", "New York Rangers", "Ottawa Senators", "Philadelphia Flyers", "Pittsburght Penguins", "San Jose Sharks", "Seattle Kraken", "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs", "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"]
    col1, col2, col3, col4, col5 = st.columns(5)
    q1a1 = col1.selectbox("Question 1, Answer 1", ["PASS"] + accepted_teams)
    q1a2 = col2.selectbox("Question 1, Answer 2", ["PASS"] + accepted_teams)
    q1a3 = col3.selectbox("Question 1, Answer 3", ["PASS"] + accepted_teams)
    q1a4 = col4.selectbox("Question 1, Answer 4", ["PASS"] + accepted_teams)
    q1a5 = col5.selectbox("Question 1, Answer 5", ["PASS"] + accepted_teams)
    temp_answers = [q1a1, q1a2, q1a3, q1a4, q1a5]
    for answer in temp_answers:
        if answer == "PASS":
            continue
        else:
            if temp_answers.count(answer) != 1:
                answer_index = temp_answers.index(answer)
                temp_answers.pop(answer_index)
                temp_answers.insert(answer_index, "PASS")
                st.write("Removed duplicate answer!")
    q1a1, q1a2, q1a3, q1a4, q1a5 = temp_answers

    "### Q2: Provide up to five teams which will **definitely** not make the playoffs in the 2022-23 season:"
    col1, col2, col3, col4, col5 = st.columns(5)
    q2a1 = col1.selectbox("Question 2, Answer 1", ["PASS"] + accepted_teams)
    q2a2 = col2.selectbox("Question 2, Answer 2", ["PASS"] + accepted_teams)
    q2a3 = col3.selectbox("Question 2, Answer 3", ["PASS"] + accepted_teams)
    q2a4 = col4.selectbox("Question 2, Answer 4", ["PASS"] + accepted_teams)
    q2a5 = col5.selectbox("Question 2, Answer 5", ["PASS"] + accepted_teams)
    temp_answers = [q2a1, q2a2, q2a3, q2a4, q2a5]
    for answer in temp_answers:
        if answer == "PASS":
            continue
        else:
            if temp_answers.count(answer) != 1:
                answer_index = temp_answers.index(answer)
                temp_answers.pop(answer_index)
                temp_answers.insert(answer_index, "PASS")
                st.write("Removed duplicate answer!")
        q2a1, q2a2, q2a3, q2a4, q2a5 = temp_answers

    # Other questions go here once we have this working
    # entry_variables = [entrant_name, entrant_email, q1a1, q1a2, q1a3, q1a4, q1a5, q2a1, q2a2, q2a3, q2a4, q2a5]
    submitted = st.form_submit_button("Submit your entry!")
    if submitted:

        # Use Shillelagh to insert the info to the spreadsheet
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], 
            scopes=["https://www.googleapis.com/auth/spreadsheets",],)
        connection = connect(":memory:", adapter_kwargs={
            "gsheetaspi" : { 
            "service_account_info" : {
                "type" : st.secrets[type],
                "project_id" : st.secrets["project_id"],
                "private_key_id" : st.secrets["private_key_id"],
                "private_key" : st.secrets["private_key"],
                "client_email" : st.secrets["client_email"],
                "client_id" : st.secrets["client_id"],
                "auth_uri" : st.secrets["auth_uri"],
                "token_uri" : st.secrets["token_uri"],
                "auth_provider_x509_cert_url" : st.secrets["auth_provider_x509_cert_url"],
                "client_x509_cert_url" : st.secrets["client_x509_cert_url"],
                }
            },
        })

        

        # connection = connect(":memory:")
        cursor = connection.cursor()
        sheet_url = st.secrets["private_gsheets_url"]
        # query = f'INSERT INTO "{sheet_url}" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        # cursor.execute(query, (entrant_name, entrant_email, q1a1, q1a2, q1a3, q1a4, q1a5, q2a1, q2a2, q2a3, q2a4, q2a5))
        query = f'INSERT INTO "{sheet_url}" VALUES ("{entrant_name}", "{entrant_email}", "{q1a1}", "{q1a2}", "{q1a3}", "{q1a4}", "{q1a5}", "{q2a1}", "{q2a2}", "{q2a3}", "{q2a4}", "{q2a5}")'
        cursor.execute(query)
        
        st.write(f"{entrant_name}, your entry associated with {entrant_email} has been submitted with the following selections:  \nQuestion 1:{q1a1}, {q1a2}, {q1a3}, {q1a4}, {q1a5}  \nQuestion 2:{q2a1}, {q2a2}, {q2a3}, {q2a4}, {q2a5}")











# entry_variables = [entrant_name, entrant_email, q1a1, q1a2, q1a3, q1a4, q1a5, q2a1, q2a2, q2a3, q2a4, q2a5]
# entry_data = pd.Series(entry_variables)
