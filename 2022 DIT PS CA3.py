from ast import dump
from cProfile import label
from cgitb import text
from dbm import dumb
from dis import dis
from glob import glob
from hashlib import new
from importlib.resources import path
from math import fabs
from operator import itemgetter
from tkinter import *
from tkinter.messagebox import *
import re
import json
import os.path
import time
from unicodedata import name
from matplotlib.pyplot import get
from numpy import record

from pyparsing import col

nameDB_path = "./name_database.json"
recordDB_path = "./record_database.json"

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
                    i = 0
                    while i < len(db_data):
                        name = db_data[i]["name"]
                        state = db_data[i]["state"]
                        #TODO Record 작성 if ()
                    try:
                        #TODO Record에 append 하는걸로 수정
                        match = next(db for db in db_data if db["name"] == entry_name.get())
                        if askyesno("Final Check", "Record this data?\nName: " + entry_name.get() + "\nEvent: " + radio_var.get() + "\nTime: " + entry_time.get() + "\nMeet: " + entry_meet.get()):
                            match["event"] = radio_var.get()
                            match["time"] = entry_time.get()
                            match["meet"] = entry_meet.get()
                            with open(nameDB_path, 'w') as fs:
                                json.dump(db_data, fs, indent=4)
                                showinfo("Success", "Successfully Recorded")
                    except:
                        showerror("No Swimmer Data", "Name " + entry_name.get() + " is not in database.\nRegister swimmer first.")
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

app = Tk()
regWindow = Button(app, text='Register Swimmer', command=createRegWindow)
remWindow = Button(app, text='Remove Swimmer', command=createRemWindow)
recWindow = Button(app, text='Record Swimmer\'s Timings', command=createRecWindow)
enqWindow = Button(app, text='Enquire Swimmer\'s Timings')
dispWindow = Button(app, text='Display Swimmer\'s Timings for Submission')

regWindow.grid(row=1, column=0)
remWindow.grid(row=1, column=2)
recWindow.grid(row=2, column=0)
enqWindow.grid(row=2, column=2)
dispWindow.grid(row=3, column=1)

app.title('SSA Administrative Program - 10240311 Yun Minseo DIT PS CA3 Individual Assignment')
app.mainloop()