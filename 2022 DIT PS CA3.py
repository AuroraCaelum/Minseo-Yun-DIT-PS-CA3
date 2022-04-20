from ast import dump
from cProfile import label
from cgitb import text
from datetime import datetime
from dbm import dumb
from dis import dis
from glob import glob
from hashlib import new
from importlib.resources import path
from math import fabs
from operator import itemgetter
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import re
import json
import os.path
import time
from unicodedata import name
from matplotlib.pyplot import get, show
from numpy import append, rec, record
from datetime import date

from pyparsing import col

nameDB_path = "./name_database.json"
recordDB_path = "./record_database.json"

#TODO os.path.isfile이나 fs:같이 자주 쓰는거 사전 정의해보기
#TODO 동명이인 검증
# Check DB File exist
if os.path.isfile(nameDB_path) != True and os.path.isfile(recordDB_path) != True:
    datafile = {}
    datafile = []
    with open(nameDB_path, 'w') as nfs:
        json.dump(datafile, nfs, indent=4)
        with open(recordDB_path, 'w') as rfs:
            json.dump(datafile, rfs, indent=4)
            showinfo("Initialize Complete", "Database Successfully Created")
elif os.path.isfile(nameDB_path) != True:
    datafile = {}
    datafile = []
    with open(nameDB_path, 'w') as fs:
        json.dump(datafile, fs, indent=4)
        showinfo("Missing Swimmer Database", "Swimmer Database has Re-created")
elif os.path.isfile(recordDB_path) != True:
    datafile = {}
    datafile = []
    with open(recordDB_path, 'w') as fs:
        json.dump(datafile, fs, indent=4)
        showinfo("Missing Swimmer Database", "Record Database hs Re-created")

def createRegWindow():
    global newRegWindow
    newRegWindow = Toplevel(app)
    label_reg = Label(newRegWindow, text = "Input Swimmer\'s Information")
    label_name = Label(newRegWindow, text = "Name")
    entry_name = Entry(newRegWindow)
    label_gender = Label(newRegWindow, text = "Gender")
    radio_var = StringVar()
    radio_male = Radiobutton(newRegWindow, text = "Male", variable=radio_var, value="Male")
    radio_female = Radiobutton(newRegWindow, text = "Female", variable=radio_var, value="Female")
    label_birth = Label(newRegWindow, text = "Date of Birth")
    entry_birth = Entry(newRegWindow)
    btn_input = Button(newRegWindow, text = "Input Data")

    label_reg.grid(row=1, column=1)
    label_name.grid(row=2, column=0)
    entry_name.grid(row=2, column=2)
    label_gender.grid(row=3, column=0)
    radio_male.grid(row=3, column=1)
    radio_female.grid(row=3, column=2)
    label_birth.grid(row=4, column=0)
    entry_birth.grid(row=4, column=2)
    btn_input.grid(row=5,column=1)

    entry_birth.insert(0, "YYYY-MM-DD")
    def deletePreInsert(event):
        if entry_birth.get() == "YYYY-MM-DD":
            entry_birth.delete(0, len(entry_birth.get()))
    def rewritePreInsert(event):
        if entry_birth.get() == "":
            entry_birth.insert(0, "YYYY-MM-DD")

    entry_birth.bind("<1>", deletePreInsert)
    entry_birth.bind("<FocusOut>", rewritePreInsert)

    def inputSwimmerData(event):
        if (entry_name.get() != "" and radio_var.get() != 0):
            regex = re.compile('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')
            regexMatch = regex.match(entry_birth.get())
            # Validate Birth Data
            if (str(regexMatch) != 'None'):
                # Validate File Existence
                if os.path.isfile(nameDB_path):
                    # TODO INACTIVE에 이름 있는지 확인 -> 있을경우 Active로 변경
                    with open(nameDB_path, 'r') as db_json:
                        db_data = json.load(db_json)
                    #try:
                        i=0
                        check = None
                        while i < len(db_data):
                            name = db_data[i]["name"]
                            gender = db_data[i]["gender"]
                            birth = db_data[i]["birth"]
                            i+=1
                            if name == entry_name.get() and gender == radio_var.get() and birth == entry_birth.get():
                                #gender = db_data[i]["gender"]
                                #birth = db_data[i]["birth"]
                                #if gender == radio_var.get() and birth == entry_birth.get():
                                if askyesno("Data Already Exist", "Name: " + name + "\nis already exist in database, but not active.\n\nChange " + entry_name.get() + " to active?"):
                                    db_data[i-1]["state"] = 1
                                    with open(nameDB_path, 'w') as fs:
                                        json.dump(db_data, fs, indent=4)
                                    check = True
                                    break
                                else:
                                    check = True
                                    break
                            else: continue
                        print(i)
                        print(len(db_data))
                        if i == len(db_data) and check != True:
                            db_data.append({
                                "id": int(time.time()),
                                "name": entry_name.get(),
                                "gender": radio_var.get(),
                                "birth": entry_birth.get(),
                                "state": 1
                            })
                            with open(nameDB_path, 'w') as fs:
                                json.dump(db_data, fs, indent=4)
                                showinfo("Success", "Registeration Successful")
                            #TODO 선수 데이터베이스와 기록 데이터베이스 분리하기
                            #"event": "",
                            #"time": "",
                            #"meet": ""
                       # })
                        #db_data["Active"].append({
                        #    "name": entry_name.get(),
                        #    "gender": radio_var.get(),
                        #    "birth": entry_birth.get()
                        #})
                       # with open(nameDB_path, 'w') as fs:
                        #    json.dump(db_data, fs, indent=4)
                         #   showinfo("Success", "Registeration Successful")
                else:
                    # DB file has missing
                    showerror("Missing DB File", "Cannot find DB file. Please restart the program.")
            else:
                # Invalid birth data
                showerror("Error", "There\'s an error in date of birth input.\nInvalid value or incorrect input format.\n(YYYY-MM-DD)")
        else:
                # Not completely inserted
                showerror("Error", "Some data is missing.\nPlease input all of the data.")

    btn_input.bind("<1>", inputSwimmerData)

def createRemWindow():
    global newRemWindow
    newRemWindow = Toplevel(app)
    label_rem = Label(newRemWindow, text="Input Swimmer\'s name for remove")
    label_name = Label(newRemWindow, text="Name")
    entry_name = Entry(newRemWindow)
    btn_rem = Button(newRemWindow, text="Remove From Active")

    label_rem.grid(row=1, column=1)
    label_name.grid(row=2, column=0)
    entry_name.grid(row=2, column=2)
    btn_rem.grid(row=3, column=1)

    def removeSwimmer(event):
        if (entry_name.get() != ""):
            if os.path.isfile(nameDB_path):
                with open(nameDB_path, 'r') as db_json:
                    db_data = json.load(db_json)
                # TODO 데이터 유무 체크
                # Check name is already in database
                try:
                    match = next(db for db in db_data if db["name"] == entry_name.get())
                    if askyesno("Confirm", "Name: " + match.get("name") + "\nGender: " + match.get("gender") + "\nDate of Birth: " + match.get("birth") + "\n\nReally want to delete?"):
                        match["state"] = 0
                        with open(nameDB_path, 'w') as fs:
                            json.dump(db_data, fs, indent=4)
                except:
                    showerror("Data not exist", "Cannot find " + entry_name.get() + " in database.")
                #print(entry_name.get() in db_data["Active"])
            else:
                # DB file has missing
                showerror("Missing DB File", "Cannot find DB File. Please restart the program.")
        else:
            # Not Completely Inserted
            showerror("Error", "Please input name")

    btn_rem.bind("<1>", removeSwimmer)

def createRecWindow():
    global newRecWindow
    newRecWindow = Toplevel(app)
    label_rec = Label(newRecWindow, text = "Record Swimmer\'s Timings")
    label_name = Label(newRecWindow, text = "Name")
    entry_name = Entry(newRecWindow)
    label_event = Label(newRecWindow, text = "Event")
    label_freestyle = Label(newRecWindow, text = "Freestyle")
    label_backstroke = Label(newRecWindow, text = "Backstroke")
    label_breaststroke = Label(newRecWindow, text = "Breaststroke")
    label_butterfly = Label(newRecWindow, text = "Butterfly")
    label_indiv = Label(newRecWindow, text = "Individual Medley")
    radio_var = StringVar()
    radio_free50 = Radiobutton(newRecWindow, text = "50m", variable=radio_var, value = "50m Freestyle")
    radio_free100 = Radiobutton(newRecWindow, text = "100m", variable=radio_var, value = "100m Freestyle")
    radio_free200 = Radiobutton(newRecWindow, text = "200m", variable=radio_var, value = "200m Freestyle")
    radio_free400 = Radiobutton(newRecWindow, text = "400m", variable=radio_var, value = "400m Freestyle")
    radio_free800 = Radiobutton(newRecWindow, text = "800m", variable=radio_var, value = "800m Freestyle")
    radio_free1500 = Radiobutton(newRecWindow, text = "1500m", variable=radio_var, value = "1500m Freestyle")
    radio_back50 = Radiobutton(newRecWindow, text = "50m", variable=radio_var, value = "50m Backstroke")
    radio_back100 = Radiobutton(newRecWindow, text = "100m", variable=radio_var, value = "100m Backstroke")
    radio_back200 = Radiobutton(newRecWindow, text = "200m", variable=radio_var, value = "200m Backstroke")
    radio_breast50 = Radiobutton(newRecWindow, text = "50m", variable=radio_var, value = "50m Breaststroke")
    radio_breast100 = Radiobutton(newRecWindow, text = "100m", variable=radio_var, value = "100m Breaststroke")
    radio_breast200 = Radiobutton(newRecWindow, text = "200m", variable=radio_var, value = "200m Breaststroke")
    radio_fly50 = Radiobutton(newRecWindow, text = "50m", variable=radio_var, value = "50m Butterfly")
    radio_fly100 = Radiobutton(newRecWindow, text = "100m", variable=radio_var, value = "100m Butterfly")
    radio_fly200 = Radiobutton(newRecWindow, text = "200m", variable=radio_var, value = "200m Butterfly")
    radio_indiv100 = Radiobutton(newRecWindow, text = "100m", variable=radio_var, value = "100m Individual Medley")
    radio_indiv200 = Radiobutton(newRecWindow, text = "200m", variable=radio_var, value = "200m Individual Medley")
    radio_indiv400 = Radiobutton(newRecWindow, text = "400m", variable=radio_var, value = "400m Individual Medley")
    label_time = Label(newRecWindow, text = "Time")
    entry_time = Entry(newRecWindow)
    label_meet = Label(newRecWindow, text = "Meet")
    entry_meet = Entry(newRecWindow)
    button_record = Button(newRecWindow, text="Record Data")

    label_rec.grid(row=1, column=4)
    label_name.grid(row=2, column=0)
    entry_name.grid(row=2, column=1)
    label_event.grid(row=3, column=0)
    label_freestyle.grid(row=4, column=0)
    radio_free50.grid(row=4, column=1)
    radio_free100.grid(row=4, column=2)
    radio_free200.grid(row=4, column=3)
    radio_free400.grid(row=4, column=4)
    radio_free800.grid(row=4, column=5)
    radio_free1500.grid(row=4, column=6)
    label_backstroke.grid(row=5, column=0)
    radio_back50.grid(row=5, column=1)
    radio_back100.grid(row=5, column=2)
    radio_back200.grid(row=5, column=3)
    label_breaststroke.grid(row=6, column=0)
    radio_breast50.grid(row=6, column=1)
    radio_breast100.grid(row=6, column=2)
    radio_breast200.grid(row=6, column=3)
    label_butterfly.grid(row=7, column=0)
    radio_fly50.grid(row=7, column=1)
    radio_fly100.grid(row=7, column=2)
    radio_fly200.grid(row=7, column=3)
    label_indiv.grid(row=8, column=0)
    radio_indiv100.grid(row=8, column=1)
    radio_indiv200.grid(row=8, column=2)
    radio_indiv400.grid(row=8, column=3)
    label_time.grid(row=9, column=0)
    entry_time.grid(row=9, column=1)
    label_meet.grid(row=10, column=0)
    entry_meet.grid(row=10, column=1)
    button_record.grid(row=11, column=4)

    entry_time.insert(0, "e.g., 1.03.56")
    def deletePreInsert(event):
        if entry_time.get() == "e.g., 1.03.56":
            entry_time.delete(0, len(entry_time.get()))
    def rewritePreInsert(event):
        if entry_time.get() == "":
            entry_time.insert(0, "e.g., 1.03.56")

    entry_time.bind("<1>", deletePreInsert)
    entry_time.bind("<FocusOut>", rewritePreInsert)

    def recordData(event):
        if (entry_name.get() != "" and radio_var.get() != "" and entry_meet.get() != ""):
            regex = re.compile('([0-9])\.([0-5][0-9])\.([0-9][0-9])')
            regexMatch = regex.match(entry_time.get())
            # Validate Time Format
            if (str(regexMatch) != 'None'):
                if os.path.isfile(nameDB_path):
                    with open(nameDB_path, 'r') as db_json:
                        db_data = json.load(db_json)
                    if os.path.isfile(recordDB_path):
                        with open(recordDB_path, 'r') as recDB_json:
                            recDB_data = json.load(recDB_json)
                        i = 0
                        dbpos = None
                        while i < len(db_data):
                            name = db_data[i]["name"]
                            state = db_data[i]["state"]
                            if name == entry_name.get():
                                if state == 1:
                                    dbpos = i
                            i+=1
                        if dbpos != None: #TODO pos가 여러개면 다른정보 확인하는 기능?
                            if askyesno("Final Check", "Record this data?\nName: " + entry_name.get() + "\nEvent: " + radio_var.get() + "\nTime: " + entry_time.get() + "\nMeet: " + entry_meet.get()):
                                id = db_data[dbpos]["id"]
                                recDB_data.append({
                                    "id": int(id),
                                    "name": entry_name.get(),
                                    "event": radio_var.get(),
                                    "time": entry_time.get(),
                                    "meet": entry_meet.get(),
                                    "status": "Unposted"
                                })
                                with open(recordDB_path, 'w') as fs:
                                    json.dump(recDB_data, fs, indent=4)
                                    showinfo("Success", "Successfully Recorded")
                        else:
                            showerror("Cannot find such data", "Please check " + entry_name.get() + " is registered and currently active.")
                    else:
                        showerror("Database Missing", "Please restart the program!")
                else:
                    showerror("Database Missing", "Please restart the program!")
            else:
                # Invalid birth data
                showerror("Error", "There\'s an error in time input.\nInvalid value or incorrect input format.\n(e.g. 1.03.56)")
        else:
            # Not completely inserted
            showerror("Error", "Some data is missing.\nPlease input all of the data.")
        #else:
            # Cannot find DB File
        #    showerror("Error", "Cannot find DB file.")

    button_record.bind("<1>", recordData)

def createEnqWindow():
    global newEnqWindow
    newEnqWindow = Toplevel(app)
    label_req = Label(newEnqWindow, text="Enquire Swimmer\'s Timings")
    label_name = Label(newEnqWindow, text="*Name")
    entry_name = Entry(newEnqWindow)
    label_event = Label(newEnqWindow, text="Event (Optional Filter)")
    combo_event = ttk.Combobox(newEnqWindow, values=["50m Freestyle", "100m Freestyle", "200m Freestyle", "400m Freestyle", "800m Freestyle", "1500m Freestyle",
                                                "50m Backstroke", "100m Backstroke", "200m Backstroke",
                                                "50m Breaststroke", "100m Breaststroke", "200m Breaststroke",
                                                "50m Butterfly", "100m Butterfly", "200m Butterfly",
                                                "100m Individual Medley", "200m Individual Medley", "400m Individual Medley"])
    btn_search = Button(newEnqWindow, text="Search")
    tree_view = ttk.Treeview(newEnqWindow, columns=["Name", "Event", "Timing", "Meet"], displaycolumns=["Name", "Event", "Timing", "Meet"])

    label_req.grid(row=1, column=2)
    label_name.grid(row=2, column=0)
    entry_name.grid(row=2, column=1)
    label_event.grid(row=2, column=2)
    combo_event.grid(row=2, column=3)
    btn_search.grid(row=2, column=4)
    tree_view.grid(row=3, column=0, columnspan=5)

    tree_view.column("#0", width=50)
    tree_view.heading("#0", text="#")
    tree_view.column("#1", width=100)
    tree_view.heading("#1", text="Name")
    tree_view.column("#2", width=170)
    tree_view.heading("#2", text="Event")
    tree_view.column("#3", width=100)
    tree_view.heading("#3", text="Timing")
    tree_view.column("#4", width=250)
    tree_view.heading("#4", text="Meet")

    def enqSearch(event):
        if (entry_name.get() != ""):
            if os.path.isfile(nameDB_path):
                with open(nameDB_path, 'r') as db_json:
                    db_data = json.load(db_json)
                if os.path.isfile(recordDB_path):
                    with open(recordDB_path, 'r') as recDB_json:
                        recDB_data = json.load(recDB_json)
                    i=0
                    dbpos = None
                    #TODO for i in db_data 해보자
                    while i < len(db_data):
                        name = db_data[i]["name"]
                        state = db_data[i]["state"]
                        if name == entry_name.get():
                            #if state == 1:
                                dbpos = i
                        i+=1
                    if dbpos != None: #TODO pos 중복 확인
                        tree_view.delete(*tree_view.get_children())
                        id = db_data[dbpos]["id"]
                        j = 0
                        num = 1

                        def insertTree(j):
                            rec_name = recDB_data[j]["name"]
                            event = recDB_data[j]["event"]
                            timing = recDB_data[j]["time"]
                            meet = recDB_data[j]["meet"]
                            tree_view.insert('', 'end', text=num, values=[rec_name, event, timing, meet], iid=str(num))
                                    
                        while j < len(recDB_data):
                            if recDB_data[j]["id"] == id:
                                if combo_event.get() != "":
                                    if recDB_data[j]["event"] == combo_event.get():
                                        insertTree(j)
                                        num+=1
                                        j+=1
                                    else:
                                        j+=1
                                        continue
                                else:
                                    insertTree(j)
                                    num+=1
                                    j+=1
                            else:
                                j+=1
                                continue
                    else:
                        showerror("Database Not Found", "No such name in database!")
                else:
                    showerror("Database Missing", "Please restart the program!")
            else:
                showerror("Database Missing", "Please restart the program")
        else:
            showerror("Error", "You must input the name!")

    btn_search.bind("<1>", enqSearch)

def createDispWindow():
    global newDispWindow
    newDispWindow = Toplevel(app)
    label_disp = Label(newDispWindow, text="Display Unposted Data for Submission")
    tree_view = ttk.Treeview(newDispWindow, columns=["Name", "Gender", "Event", "Time", "Meet", "Age"], displaycolumns=["Name", "Gender", "Event", "Time", "Meet", "Age"])
    btn_post = Button(newDispWindow, text="Continue to Post")
    
    label_disp.grid(row=1, column=3)
    tree_view.grid(row=2, column=0, columnspan=5)
    btn_post.grid(row=3, column=4)
    
    tree_view.column("#0", width=50)
    tree_view.heading("#0", text="#")
    tree_view.column("#1", width=150)
    tree_view.heading("#1", text="Name")
    tree_view.column("#2", width=80)
    tree_view.heading("#2", text="Gender")
    tree_view.column("#3", width=120)
    tree_view.heading("#3", text="Event")
    tree_view.column("#4", width=120)
    tree_view.heading("#4", text="Timing")
    tree_view.column("#5", width=150)
    tree_view.heading("#5", text="Meet")
    tree_view.column("#6", width=50)
    tree_view.heading("#6", text="Age")

    if os.path.isfile(nameDB_path):
        with open(nameDB_path, 'r') as db_json:
            db_data = json.load(db_json)
        if os.path.isfile(recordDB_path):
            with open(recordDB_path, 'r') as recDB_json:
                recDB_data = json.load(recDB_json)
            num = 1
            for i in range(len(db_data)):
                if db_data[i]["state"] == 1:
                    name = db_data[i]["name"]
                    gender = db_data[i]["gender"]
                    today = date.today()
                    birth = datetime.strptime(db_data[i]["birth"], '%Y-%m-%d')
                    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
                    for j in range(len(recDB_data)):
                        if recDB_data[j]["name"] == name and recDB_data[j]["status"] == "Unposted":
                            event = recDB_data[j]["event"]
                            timing = recDB_data[j]["event"]
                            meet = recDB_data[j]["meet"]
                            tree_view.insert('', 'end', text=num, values=[name, gender, event, timing, meet, age], iid=str(num))
                            num+=1
                            #TODO else 처리

    def postData(event):
        with open(recordDB_path, 'r') as post_json:
            post_data = json.load(post_json)
        if askyesno("Confirm to Post?", "Continue posting this data?"):
            for i in range(len(post_data)):
                if post_data[i]["status"] == "Unposted":
                    post_data[i]["status"] = "Posted"
                    with open(recordDB_path, 'w') as fs:
                        json.dump(post_data, fs, indent=4)
                        tree_view.delete(*tree_view.get_children())

    btn_post.bind("<1>", postData)

app = Tk()
regWindow = Button(app, text='Register Swimmer', command=createRegWindow)
remWindow = Button(app, text='Remove Swimmer', command=createRemWindow)
recWindow = Button(app, text='Record Swimmer\'s Timings', command=createRecWindow)
enqWindow = Button(app, text='Enquire Swimmer\'s Timings', command=createEnqWindow)
dispWindow = Button(app, text='Display Swimmer\'s Timings for Submission', command=createDispWindow)

regWindow.grid(row=1, column=0)
remWindow.grid(row=1, column=2)
recWindow.grid(row=2, column=0)
enqWindow.grid(row=2, column=2)
dispWindow.grid(row=3, column=1)

app.title('SSA Administrative Program - 10240311 Yun Minseo DIT PS CA3 Individual Assignment')
app.mainloop()