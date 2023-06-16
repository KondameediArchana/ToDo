# from flask import request
from matplotlib import pyplot as plt
from rest_framework import status
import streamlit as st
import requests
import pandas as pd
import os
import altair as alt
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
session_state=st.session_state
local_host = 'http://127.0.0.1:8000/'
def get_jwt_token(username, password):
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
def get_data(token):
    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def login_page():
    st.markdown("<h1 style='text-align: center; '>Login Page</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2,col3,col4,col5 = st.columns(5)
        with col3:
            login_button = st.button("Login")

    if login_button:
        token = get_jwt_token(username, password)
        st.write(token)
        if token:
            # st.success('Authentication successful!')
            # st.write('JWT Token:', token)
            data = get_data(token)
            st.write(data)
            if data:
                return True  

        else:
            st.error("Invalid username or password.")
            return False 
        
        
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login_success = login_page()

    if login_success:
        st.session_state['logged_in'] = True
        st.experimental_rerun()
else:
    
    st.markdown("<h1 style='text-align: center; '>To Do</h1> <br>", unsafe_allow_html=True)
    
    
    col1,col2,col3,col4= st.columns(4)
    with col1:
        selected = option_menu(
            menu_title = "ToDo Task",
            options = ["To-Do","History"],
            orientation= "horizontal"
        )
        if selected == "History":
            response = requests.get("http://127.0.0.1:8000/Details/")
            if response.status_code==200:
                df = response.json()
                filtered_data = [obj for obj in df if obj["task_status"] == "Complete"]
                df=pd.DataFrame(filtered_data)
                st.write(df)
                    
        if selected == "To-Do":
            st.subheader("Add Task")
            user =st.text_input("user")
            Task= st.text_input("Task Title")
            # Description = st.text_input("Description")
            task_status = st.selectbox('status',['Pending','Complete','In-Progress'])
            
            if task_status == 'Complete':
                
                uploaded_file = st.file_uploader("please upload a file")
                if uploaded_file is not None:
                    file_contents = uploaded_file.read()
                    save_directory = "/home/archana/Project/folder"
                    file_name = uploaded_file.name
                    save_path = os.path.join(save_directory,file_name)
                    with open(save_path, "wb") as f:
                        f.write(file_contents)
                        st.success("file saved successfully")
                    st.write("")
                    st.header("Description")
                    Description = st.text_area("Enter Description ")
                    if st.button(" Save Description"):
                        st.success("Description Saved Successfully")
            elif task_status in ["Pending","In-Progress"]:
                st.write("")
                Description = st.text_area("Description", value="Description cannot be added")
                st.info("Description cannot be edited for Pending or In-Progress ")
            
            if st.button("Add"):
                task_data = {
                    "user":user,
                    "Task":Task,
                    "Description":Description,
                    "task_status":task_status
                }
                response = requests.post("http://127.0.0.1:8000/Details/",json = task_data)
                if response.status_code==200:
                    st.success("task completed successfully")
                else:
                    st.error("failed to submit the task.please try again")
                if task_status =='Complete':


                    uploaded_file = st.file_uploader("choose a file",type=["txt","csv","xlsx","pdf"])
                    if uploaded_file is not None:
                        df = pd.read_csv(uploaded_file)
                        st.dataframe(df)
                        if response.status_code == 200:
                            st.success("task completed successfully")
        
    with col4:
        selected = option_menu(
            menu_title = "User Details",
            options = ["Username","Profile"],
            orientation= "horizontal"
        )
