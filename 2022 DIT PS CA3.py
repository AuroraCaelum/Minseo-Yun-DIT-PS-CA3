# -------------------------------------------------------------------
# Env       -  Python 3.10.4 64-bit
# Author    -  Yun Minseo
# Github    -  https://github.com/dev-by-david/Minseo-Yun-DIT-PS-CA3
# Disc      -  Individual Assignment for ITSD002 Problem Solving
#              Singapore Institute of Management
#              Diploma in Information Technology
# -------------------------------------------------------------------

from datetime import datetime
from datetime import date
from this import d
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import re
import json
import os.path
import time

# Define DB file path
nameDB_path = "./name_database.json"
recordDB_path = "./record_database.json"

# Init - Check DB File existance
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

#Create Registering Window
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

    # Show input format hint
    entry_birth.insert(0, "YYYY-MM-DD")
    def deletePreInsert(event):
        if entry_birth.get() == "YYYY-MM-DD":
            entry_birth.delete(0, len(entry_birth.get()))
    def rewritePreInsert(event):
        if entry_birth.get() == "":
            entry_birth.insert(0, "YYYY-MM-DD")

    entry_birth.bind("<1>", deletePreInsert)
    entry_birth.bind("<FocusOut>", rewritePreInsert)

    # Data input function
    def inputSwimmerData(event):
        # Check null input
        if (entry_name.get() != "" and radio_var.get() != 0):
            # Validate input format (YYYY-MM-DD)
            regex = re.compile('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')
            regexMatch = regex.match(entry_birth.get())
            if (str(regexMatch) != 'None'):
                # Check DB Existence
                if os.path.isfile(nameDB_path):
                    # Load JSON
                    with open(nameDB_path, 'r') as db_json:
                        db_data = json.load(db_json)
                        # Check swimmer is already exist
                        i=0
                        check = None
                        while i < len(db_data):
                            name = db_data[i]["name"]
                            gender = db_data[i]["gender"]
                            birth = db_data[i]["birth"]
                            i+=1
                            if name == entry_name.get() and gender == radio_var.get() and birth == entry_birth.get():
                                if db_data[i-1]["state"] == "Inactive":
                                    if askyesno("Data Already Exist", "Name: " + name + "\nis already exist in database, but not active.\n\nChange " + entry_name.get() + " to active?"):
                                        # Update state Inactive -> Active
                                        db_data[i-1]["state"] = "Active"
                                        # Dump JSON
                                        with open(nameDB_path, 'w') as fs:
                                            json.dump(db_data, fs, indent=4)
                                        check = True
                                        break
                                    else:
                                        check = True
                                        break
                                else:
                                    showerror("Data Already Exist", "Name: " + name + "\n is already exist in database and active.")
                                    check = True
                            else: continue
                        # If swimmer is not already exist
                        if i == len(db_data) and check != True:
                            db_data.append({
                                "id": int(time.time()),
                                "name": entry_name.get(),
                                "gender": radio_var.get(),
                                "birth": entry_birth.get(),
                                "state": "Active"
                            })
                            # Dump JSON
                            with open(nameDB_path, 'w') as fs:
                                json.dump(db_data, fs, indent=4)
                                showinfo("Success", "Registration Successful")
                else:
                    # DB file has missing
                    showerror("Missing DB File", "Cannot find DB file. Please restart the program.")
            else:
                # Invalid birth data
                showerror("Error", "There\'s an error in date of birth input.\nInvalid value or incorrect input format.\n(YYYY-MM-DD)")
        else:
            # Null Input
            showerror("Error", "Some data is missing.\nPlease input all of the data.")

    btn_input.bind("<1>", inputSwimmerData)
    entry_birth.bind("<Return>", inputSwimmerData)

# Create Remove Window
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

    # Remove swimmer data function
    def removeSwimmer(event):
        # Check null input
        if (entry_name.get() != ""):
            # Check DB Existance
            if os.path.isfile(nameDB_path):
                # Load JSON
                with open(nameDB_path, 'r') as db_json:
                    db_data = json.load(db_json)
                # Check name is in DB
                try:
                    match = next(db for db in db_data if db["name"] == entry_name.get())
                    if askyesno("Confirm", "Name: " + match.get("name") + "\nGender: " + match.get("gender") + "\nDate of Birth: " + match.get("birth") + "\n\nReally want to delete?"):
                        # Update state Active -> Inactive
                        match["state"] = "Inactive"
                        # Dump JSON
                        with open(nameDB_path, 'w') as fs:
                            json.dump(db_data, fs, indent=4)
                except:
                    # No such name in DB
                    showerror("Data not exist", "Cannot find " + entry_name.get() + " in database.")
            else:
                # DB file has missing
                showerror("Missing DB File", "Cannot find DB File. Please restart the program.")
        else:
            # Null Input
            showerror("Error", "Please input name")

    btn_rem.bind("<1>", removeSwimmer)
    entry_name.bind("<Return>", removeSwimmer)

# Create Record Window
def createRecWindow():
    global newRecWindow
    newRecWindow = Toplevel(app)
    label_rec = Label(newRecWindow, text = "Record Swimmer\'s Timings")
    label_name = Label(newRecWindow, text = "Name")
    entry_name = Entry(newRecWindow)

    # RadioButton Set
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
    entry_meet.grid(row=10, column=1, columnspan=3, ipadx=65)
    button_record.grid(row=11, column=4)

    # Show input format hint
    entry_time.insert(0, "e.g., 1.03.56")
    def deletePreInsert(event):
        if entry_time.get() == "e.g., 1.03.56":
            entry_time.delete(0, len(entry_time.get()))
    def rewritePreInsert(event):
        if entry_time.get() == "":
            entry_time.insert(0, "e.g., 1.03.56")

    entry_time.bind("<1>", deletePreInsert)
    entry_time.bind("<FocusOut>", rewritePreInsert)

    # DB recording function
    def recordData(event):
        # Check null input
        if (entry_name.get() != "" and radio_var.get() != "" and entry_meet.get() != ""):
            # Validate Time Format (0.00.00 ~ 9.59.99)
            regex = re.compile('([0-9])\.([0-5][0-9])\.([0-9][0-9])')
            regexMatch = regex.match(entry_time.get())
            if (str(regexMatch) != 'None'):
                # Load JSON (Name DB)
                if os.path.isfile(nameDB_path):
                    with open(nameDB_path, 'r') as db_json:
                        db_data = json.load(db_json)
                    # Load JSON (Record DB)
                    if os.path.isfile(recordDB_path):
                        with open(recordDB_path, 'r') as recDB_json:
                            recDB_data = json.load(recDB_json)
                        # Search name in Name DB
                        i = 0
                        dbpos = None
                        while i < len(db_data):
                            name = db_data[i]["name"]
                            state = db_data[i]["state"]
                            if name == entry_name.get():
                                if state == "Active":
                                    dbpos = i
                            i+=1
                        # If swimmer registered
                        if dbpos != None:
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
                                # Dump JSON
                                with open(recordDB_path, 'w') as fs:
                                    json.dump(recDB_data, fs, indent=4)
                                    showinfo("Success", "Successfully Recorded")
                        else:
                            # Swimmer not registered
                            showerror("Cannot find such data", "Please check " + entry_name.get() + " is registered and currently active.")
                    else:
                        # Cannot find DB
                        showerror("Database Missing", "Please restart the program!")
                else:
                    # Cannot find DB
                    showerror("Database Missing", "Please restart the program!")
            else:
                # Invalid birth input format
                showerror("Error", "There\'s an error in time input.\nInvalid value or incorrect input format.\n(e.g. 1.03.56)")
        else:
            # Not completely inserted
            showerror("Error", "Some data is missing.\nPlease input all of the data.")

    button_record.bind("<1>", recordData)
    entry_meet.bind("<Return>", recordData)

# Create Enquire Window
def createEnqWindow():
    global newEnqWindow
    newEnqWindow = Toplevel(app)
    label_req = Label(newEnqWindow, text="Enquire Swimmer\'s Timings")
    label_name = Label(newEnqWindow, text="*Name")
    entry_name = Entry(newEnqWindow)
    label_event = Label(newEnqWindow, text="Event (Optional Filter)")
    combo_event = ttk.Combobox(newEnqWindow, values=["Freestyle", "Backstroke", "Breaststroke", "Butterfly", "Individual Medley",
                                                "50m Freestyle", "100m Freestyle", "200m Freestyle", "400m Freestyle", "800m Freestyle", "1500m Freestyle",
                                                "50m Backstroke", "100m Backstroke", "200m Backstroke",
                                                "50m Breaststroke", "100m Breaststroke", "200m Breaststroke",
                                                "50m Butterfly", "100m Butterfly", "200m Butterfly",
                                                "100m Individual Medley", "200m Individual Medley", "400m Individual Medley"])
    btn_search = Button(newEnqWindow, text="Search")
    tree_view = ttk.Treeview(newEnqWindow, columns=["Name", "Event", "Timing", "Meet", "Status"], displaycolumns=["Name", "Event", "Timing", "Meet", "Status"])

    label_req.grid(row=1, column=2)
    label_name.grid(row=2, column=0)
    entry_name.grid(row=2, column=1)
    label_event.grid(row=2, column=2)
    combo_event.grid(row=2, column=3)
    btn_search.grid(row=2, column=4)
    tree_view.grid(row=3, column=0, columnspan=5)

    # TreeView Setting
    tree_view.column("#0", width=30)
    tree_view.heading("#0", text="#")
    tree_view.column("#1", width=170)
    tree_view.heading("#1", text="Name")
    tree_view.column("#2", width=120)
    tree_view.heading("#2", text="Event")
    tree_view.column("#3", width=80)
    tree_view.heading("#3", text="Timing")
    tree_view.column("#4", width=300)
    tree_view.heading("#4", text="Meet")
    tree_view.column("#5", width=80)
    tree_view.heading("#5", text="Status")

    # Search Function
    def enqSearch(event):
        # Check null input
        if (entry_name.get() != ""):
            # Load JSON (Name DB)
            if os.path.isfile(nameDB_path):
                with open(nameDB_path, 'r') as db_json:
                    db_data = json.load(db_json)
                # Load JSON (Record DB)
                if os.path.isfile(recordDB_path):
                    with open(recordDB_path, 'r') as recDB_json:
                        recDB_data = json.load(recDB_json)
                    # Find name in Name DB
                    dbpos = None
                    for i in range(len(db_data)):
                        name = db_data[i]["name"]
                        if name == entry_name.get():
                                dbpos = i
                    # If name registered
                    if dbpos != None:
                        # Initialize TreeView
                        tree_view.delete(*tree_view.get_children())
                        id = db_data[dbpos]["id"]
                        j = 0
                        num = 1

                        # Insert data into TreeView
                        def insertTree(j):
                            rec_name = recDB_data[j]["name"]
                            event = recDB_data[j]["event"]
                            timing = recDB_data[j]["time"]
                            meet = recDB_data[j]["meet"]
                            status = recDB_data[j]["status"]
                            tree_view.insert('', 'end', text=num, values=[rec_name, event, timing, meet, status], iid=str(num))
                        
                        # Find recordings in Record DB (with name)
                        for j in range(len(recDB_data)):
                            if recDB_data[j]["id"] == id:
                                # If optional search
                                if combo_event.get() != "":
                                    if combo_event.get() == "Freestyle" or combo_event.get() == "Backstroke" or combo_event.get() == "Breaststroke" or combo_event.get() == "Butterfly" or combo_event.get() == "Individual Medley":
                                        if combo_event.get() in recDB_data[j]["event"]:
                                            insertTree(j)
                                            num += 1
                                        else:
                                            continue
                                    else:
                                        if recDB_data[j]["event"] == combo_event.get():
                                            insertTree(j)
                                            num += 1
                                        else:
                                            continue
                                else:
                                    insertTree(j)
                                    num += 1
                            else:
                                continue
                    else:
                        # Swimmer not registered
                        showerror("Database Not Found", "No such name in database!")
                else:
                    # Cannot find DB
                    showerror("Database Missing", "Please restart the program!")
            else:
                # Cannot find DB
                showerror("Database Missing", "Please restart the program")
        else:
            # Null Input
            showerror("Error", "You must input the name!")

    btn_search.bind("<1>", enqSearch)
    entry_name.bind("<Return>", enqSearch)

# Create Display Window
def createDispWindow():
    global newDispWindow
    newDispWindow = Toplevel(app)
    label_disp = Label(newDispWindow, text="Display Unposted Data for Submission")
    tree_view = ttk.Treeview(newDispWindow, columns=["Name", "Gender", "Event", "Time", "Meet", "Age"], displaycolumns=["Name", "Gender", "Event", "Time", "Meet", "Age"])
    btn_post = Button(newDispWindow, text="Continue to Post")
    
    label_disp.grid(row=1, column=4)
    tree_view.grid(row=2, column=0, columnspan=7)
    btn_post.grid(row=3, column=4)

    # TreeView Setting
    tree_view.column("#0", width=30)
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

    # Load JSON (Name DB)
    if os.path.isfile(nameDB_path):
        with open(nameDB_path, 'r') as db_json:
            db_data = json.load(db_json)
        # Load JSON (Record DB)
        if os.path.isfile(recordDB_path):
            with open(recordDB_path, 'r') as recDB_json:
                recDB_data = json.load(recDB_json)
            # Search Active Swimmer
            num = 1
            for i in range(len(db_data)):
                if db_data[i]["state"] == "Active":
                    name = db_data[i]["name"]
                    gender = db_data[i]["gender"]
                    # Calculate Age
                    today = date.today()
                    birth = datetime.strptime(db_data[i]["birth"], '%Y-%m-%d')
                    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
                    # Search Unposted Data and Display (with name)
                    for j in range(len(recDB_data)):
                        if recDB_data[j]["name"] == name and recDB_data[j]["status"] == "Unposted":
                            event = recDB_data[j]["event"]
                            timing = recDB_data[j]["time"]
                            meet = recDB_data[j]["meet"]
                            tree_view.insert('', 'end', text=num, values=[name, gender, event, timing, meet, age], iid=str(num))
                            num+=1
            # Loop until find all
        else:
            # Cannot find DB
            showerror("Database Missing", "Please restart the program.")
    else:
        # Cannot find DB
        showerror("Database Missing", "Please restart the program.")

    # Post DB (Update to 'Posted')
    def postData(event):
        # Load JSON (Record DB)
        with open(recordDB_path, 'r') as post_json:
            post_data = json.load(post_json)
        # Update status Unposted -> Posted
        if askyesno("Confirm to Post?", "Continue posting this data?"):
            for i in range(len(post_data)):
                if post_data[i]["status"] == "Unposted":
                    post_data[i]["status"] = "Posted"
                    # Dump JSON
                    with open(recordDB_path, 'w') as fs:
                        json.dump(post_data, fs, indent=4)
                        # Initialize TreeView
                        tree_view.delete(*tree_view.get_children())

    btn_post.bind("<1>", postData)

# Tkinter Main Page
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