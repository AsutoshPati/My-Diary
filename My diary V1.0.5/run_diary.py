#!/usr/bin/env python
# coding: utf-8

#          Project: My Diary
# Date of Creation: 17 Aug 2019
#      Author Name: Asutosh Pati
#          Purpose: Demo project for python short term batches
#      Description: This project will be used to record the story of every day
#                   like a diary. This program will simulate a virtual diary.
#                   With the help of this project students will able to
#                   understand how to create a program for actual uses and as
#                   well as they will be able to create GUI and database. More
#                   that it will be helpful for them to learn connection
#                   between python and database and GUI. With that they will
#                   learn how a real project is developed.
#         Versions:
#                   V1.0.0: Integration of GUI with python
#                   V1.0.1: Connection with database
#                   V1.0.2: Minor bugs fixed
#                   V1.0.3: Major bugs fixed
#                   V1.0.4: GUI style modified
#                   V1.0.5: Read issue fixed

# In[1]:


import sqlite3 as sql


# In[2]:


conn = sql.Connection("Udet.db")
conn.close()


# In[3]:


"""conn = sql.Connection("Udet.db")
query = '''CREATE TABLE auth(
ref_no INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT NOT NULL,
gender TEXT,
dob TEXT,
phone TEXT UNIQUE NOT NULL,
pwd TEXT NOT NULL)'''

conn.execute(query)
conn.commit()
conn.close()

print("table created")"""


# In[4]:


import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

import os
from datetime import datetime


# In[5]:


root = "user_data"
ref_id = None
user_dir = None


# In[6]:


def do_login():
    global ref_id, user_dir
    
    phno = login.lineEdit.text()
    pwd = login.lineEdit_2.text()
    
    conn = sql.Connection("Udet.db")
    query = 'SELECT * FROM auth WHERE phone="{}" AND pwd="{}"'.format(phno,pwd)
    ret = conn.execute(query)
    rows = ret.fetchall()
    if len(rows) > 0:
        ref_id = rows[0][0]
        user_dir = rows[0][4]
    conn.close()
    
    if ref_id != None:
        cancel_login()
        show_details_page()
    
def cancel_login():
    login.lineEdit.setText("")
    login.lineEdit_2.setText("")
    
def first_register():
    reg.show()


# In[7]:


def do_register():
    name = reg.lineEdit.text()
    gender = None
    if reg.radioButton.isChecked():
        gender="Male"
    elif reg.radioButton_2.isChecked():
        gender="Female"
    else:
        gender="Other"
    dob = reg.dateEdit.text()
    phone = reg.lineEdit_4.text()
    pwd = reg.lineEdit_5.text()
    
    conn = sql.Connection("Udet.db")
    query = '''INSERT INTO auth(full_name, gender, dob, phone, pwd)
    VALUES("{}", "{}", "{}", "{}", "{}")'''.format(name, gender, dob, phone,pwd)
    conn.execute(query)
    conn.commit()
    conn.close()
    
    os.mkdir(os.path.join(root, phone))
    
    cancel_registration()
    suc.show()
    reg.close()
    
    
def cancel_registration():
    reg.lineEdit.setText("")
    reg.radioButton_3.setChecked(True)
    reg.dateEdit.setDate(QDate(2000,1,1))
    reg.lineEdit_4.setText("")
    reg.lineEdit_5.setText("")


# In[8]:


def close_success():
    suc.close()


# In[9]:


def show_details_page():
    global ref_id
    
    login.close()
    edit_detail.close()
    read.close()
    write.close()
    
    conn = sql.Connection("Udet.db")
    query = "SELECT * FROM auth WHERE ref_no={}".format(ref_id)
    ret = conn.execute(query)
    rows = ret.fetchall()
    
    my_detail.label_3.setText(rows[0][1])
    my_detail.label_9.setText(rows[0][1])
    my_detail.label_11.setText(rows[0][2])
    my_detail.label_10.setText(rows[0][3])
    my_detail.label_8.setText(rows[0][4])
    
    my_detail.show()
    
    conn.close()


# In[10]:


def logout():
    global ref_id, user_dir
    
    ref_id = None
    user_dir = None
    
    my_detail.close()
    read.close()
    write.close()
    edit_detail.close()
    
    login.show()


# In[11]:


def show_write_page():
    global ref_id
    
    my_detail.close()
    read.close()
    edit_detail.close()
    
    today = datetime.now().strftime("%d - %B - %Y")
    write.label_6.setText(today)
    
    conn = sql.Connection("Udet.db")
    query = "SELECT * FROM auth WHERE ref_no={}".format(ref_id)
    ret = conn.execute(query)
    rows = ret.fetchall()
    write.label_3.setText(rows[0][1])
    conn.close()
    
    
    """my first method starts from here"""
    today_file = datetime.now().strftime("%d-%m-%Y")
    try:
        f = open(os.path.join(root,user_dir,today_file+".txt"),"r")
        existing_story = f.read()
        f.close()
    except:
        existing_story = ""
    finally:
        write.textEdit.setPlainText(existing_story)
    """comment(with 3 single quotes) upto this much to start second method"""
    
    
    '''
    """my second method will start from here"""
    write.textEdit.setPlainText("")
    """comment(with 3 single quotes) upto this much to execute the first method"""
    '''
    
    write.show()
    
def save_story():
    global user_dir
    today = datetime.now().strftime("%d-%m-%Y")
    story = write.textEdit.toPlainText()
    
    
    """my first method starts from here"""
    f = open(os.path.join(root,user_dir,today+".txt"),"w")
    f.write(story)
    f.close()
    """comment(with 3 single quotes) upto this much to start second method"""
    
    '''
    """my second method will start from here"""
    f = open(os.path.join(root,user_dir,today+".txt"),"a")
    f.write(story+"\n")
    f.close()
    write.textEdit.setPlainText("")
    """comment(with 3 single quotes) upto this much to execute the first method"""
    '''
    
    suc.show()


# In[12]:


def show_read_page():
    global ref_id
    
    my_detail.close()
    write.close()
    edit_detail.close()
    
    conn = sql.Connection("Udet.db")
    query = "SELECT * FROM auth WHERE ref_no={}".format(ref_id)
    ret = conn.execute(query)
    rows = ret.fetchall()
    read.label_3.setText(rows[0][1])
    conn.close()
    
    read.dateEdit.setDate(QDate(2000,1,1))
    read.textBrowser.setText("")
    
    read.show()

def display_story():
    story_date = read.dateEdit.text()
    
    f = open(os.path.join(root,user_dir,story_date+".txt"),"r")
    print(f)
    try:
        story_line = f.read()
        f.close()
        
        read.textBrowser.setText(story_line)
    except:
        read.textBrowser.setText("No stories found on this input date")


# In[13]:


def show_edit_detail_page():
    global ref_id
    
    my_detail.close()
    read.close()
    write.close()
    
    conn = sql.Connection("Udet.db")
    query = "SELECT * FROM auth WHERE ref_no={}".format(ref_id)
    ret = conn.execute(query)
    rows = ret.fetchall()
    
    edit_detail.label_3.setText(rows[0][1])
    edit_detail.lineEdit.setText(rows[0][1])
    
    if rows[0][2] == "Male":
        edit_detail.radioButton.setChecked(True)
    elif rows[0][2] == "Female":
        edit_detail.radioButton_2.setChecked(True)
    else:
        edit_detail.radioButton_3.setChecked(True)
    
    date = rows[0][3].split("-")    # the output will be -  ['19', '08', '2019']
    edit_detail.dateEdit.setDate(QDate(int(date[2]), int(date[1]), int(date[0])))
    
    edit_detail.lineEdit_4.setText(rows[0][4])
    edit_detail.lineEdit_5.setText(rows[0][5])
    
    conn.close()
    
    edit_detail.show()

def save_edits():
    global ref_id
    
    name = edit_detail.lineEdit.text()
    gender = None
    if edit_detail.radioButton.isChecked():
        gender="Male"
    elif edit_detail.radioButton_2.isChecked():
        gender="Female"
    else:
        gender="Other"
    dob = edit_detail.dateEdit.text()
    pwd = edit_detail.lineEdit_5.text()
    
    conn = sql.Connection("Udet.db")
    query = "UPDATE auth SET full_name='{}', gender='{}', dob='{}', pwd='{}' WHERE ref_no={}".format(name,gender,dob,pwd,ref_id)
    conn.execute(query)
    conn.commit()
    conn.close()
    
    show_edit_detail_page()
    suc.show()


# In[14]:


app = QtWidgets.QApplication([])

reg = uic.loadUi("registration.ui")
login = uic.loadUi("login page.ui")
my_detail = uic.loadUi("Details Page.ui")
edit_detail = uic.loadUi("edit details.ui")
read = uic.loadUi("Read Page.ui")
write = uic.loadUi("Write Page.ui")
suc = uic.loadUi("success.ui")

login.show()

login.pushButton.clicked.connect(do_login)
login.pushButton_2.clicked.connect(cancel_login)
login.pushButton_3.clicked.connect(first_register)

reg.pushButton.clicked.connect(do_register)
reg.pushButton_2.clicked.connect(cancel_registration)

suc.pushButton.clicked.connect(close_success)

my_detail.pushButton.clicked.connect(logout)
my_detail.pushButton_3.clicked.connect(show_read_page)
my_detail.pushButton_4.clicked.connect(show_write_page)
my_detail.pushButton_5.clicked.connect(show_edit_detail_page)

write.pushButton.clicked.connect(logout)
write.pushButton_2.clicked.connect(show_details_page)
write.pushButton_3.clicked.connect(show_read_page)
write.pushButton_5.clicked.connect(show_edit_detail_page)
write.pushButton_6.clicked.connect(save_story)

read.pushButton.clicked.connect(logout)
read.pushButton_2.clicked.connect(show_details_page)
read.pushButton_4.clicked.connect(show_write_page)
read.pushButton_5.clicked.connect(show_edit_detail_page)
read.pushButton_6.clicked.connect(display_story)

edit_detail.pushButton.clicked.connect(logout)
edit_detail.pushButton_2.clicked.connect(show_details_page)
edit_detail.pushButton_3.clicked.connect(show_read_page)
edit_detail.pushButton_4.clicked.connect(show_write_page)
edit_detail.pushButton_7.clicked.connect(save_edits)
edit_detail.pushButton_6.clicked.connect(show_edit_detail_page)

app.exec()
del app


# In[ ]:




