import datetime
from numpy import datetime_as_string
import streamlit as st
import gspread
import json
import numpy as np
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

st.session_state.radio_dict = {}
if st.session_state.radio_dict is None:
    st.session_state.radio_dict = {}
    
#google_sheet_url ="https://docs.google.com/spreadsheets/d/1PYwm0Ji38YAbDK3FHU64K0bj7MGQJfXWZGn5uI5s9zc/edit?usp=sharing"
google_sheet_url = st.secrets["private_gsheets_url"]

def convert_datatime_to_string(date):
    """
    Convert datetime to a date string and time string
    Then reurn the date string and time string
    """
    date_string = datetime_as_string(date, unit='D')
    date_time_string = str(date)
    #time_string = datetime_as_string(date, unit='h')
    return date_string, date_time_string

def save_into_csv(date_time,cpt,wrvu):  
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        'https://www.googleapis.com/auth/drive',
    ],
    )
    #gc = gspread.authorize(credentials)
    #gc = gspread.service_account(filename= "credentials.json") 
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])      
    sh = gc.open_by_url(google_sheet_url)    
    worksheet = sh.get_worksheet(0)
    date,time_stamp = convert_datatime_to_string(date_time)
    worksheet.append_row([date,time_stamp,cpt,wrvu])

# Function to get the value of the selected radio button and return the value
def get_value(key):
    value = st.session_state[key]
    return value
#print(get_value("followup"))

#function that returns value from the dictionary based on the key
def get_rvu_value(key):   
    value = st.session_state.radio_dict[key]
    return value

def get_label():
    keys = ["followup", "newpatient", "procedures"]
    for key in keys:
        value = get_value(key)
        if value != "None":
            return value



# create python dictionary to store the values of the radio buttons 


st.session_state.radio_dict = {
    "None": 0,
    "Level 1 99211": 0.18,
    "Level 2 99212": 0.7,
    "Level 3 99213": 1.3,
    "Level 4 99214": 1.92,
    "Level 5 99215": 2.8,
    "Level 1 99201": 0,
    "Level 2 99202": 0.93,
    "Level 3 99203": 1.6,
    "Level 4 99204": 2.6,
    "Level 5 99205": 3.5,
    "1_FNA": 1.46,
    "2_FNA": 2.46,
    "CGM_read": 0.7,
}

st.title('RVU App')

dateco, timecol = st.columns(2)
with dateco:
    date = st.date_input(
    "Date of the visit",)
    
with timecol:
    time = st.time_input(
    "Time of the visit",)

with st.form("my_form",clear_on_submit=True):
    ucol1, ucol2, ucol3 = st.columns(3)
    
    with ucol1:
        st.radio(
        "Follow up visits",
        ["None", "Level 1 99211", "Level 2 99212", "Level 3 99213", "Level 4 99214", "Level 5 99215"],
        key="followup",
    )

    with ucol2:
        st.radio(     
        "New Patient visits",
        ["None", "Level 1 99201", "Level 2 99202", "Level 3 99203", "Level 4 99204", "Level 5 99205"],
        key="newpatient",
    )

    with ucol3:
        st.radio(     
        "Procedures",
        ["None", "CGM_read", "1_FNA", "2_FNA"],
        key="procedures",
    )

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("You selected:", get_label())
        cpt_code = get_label()
        rvu_value = get_rvu_value(cpt_code)
        save_into_csv(np.datetime64(datetime.datetime.now()),cpt_code,rvu_value)
        #save_into_csv(np.datetime64(datetime.datetime.now()),9401,1.8)
        st.write("Data saved into Google Sheet")

