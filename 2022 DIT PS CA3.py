from cgitb import text
from dis import dis
from tkinter import *
from tkinter.messagebox import *
import re

def createRegWindow():
    global newRegWindow
    newRegWindow = Toplevel(app)
    label_intro = Label(newRegWindow, text = "Input Swimmer\'s Information")
    label_name = Label(newRegWindow, text = "Name")
    entry_name = Entry(newRegWindow)
    label_gender = Label(newRegWindow, text = "Gender")
    radio_var = IntVar()
    radio_male = Radiobutton(newRegWindow, text = "Male", variable=radio_var, value=1)
    radio_female = Radiobutton(newRegWindow, text = "Female", variable=radio_var, value=2)
    label_birth = Label(newRegWindow, text = "Date of Birth")
    entry_birth = Entry(newRegWindow)
    btn_input = Button(newRegWindow, text = "Input Data")

    label_intro.grid(row=1, column=1)
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

    entry_birth.bind("<1>", deletePreInsert)

    def inputSwimmerData(event):
        regex = re.compile('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')
        regexMatch = regex.match(entry_birth.get())
        print(regexMatch)
        if (str(regexMatch) != 'None'):
            print("OK")
        else:
            # invalid birth data
            showerror("Error", "There\'s an error in date of birth input.\nInvalid value or incorrect input format.\n(YYYY-MM-DD)")

    btn_input.bind("<1>", inputSwimmerData)

app = Tk()
regWindow = Button(app, text='Register Swimmer', command=createRegWindow)
remWindow = Button(app, text='Remove Swimmer')
recWindow = Button(app, text='Record Swimmer\'s Timings')
enqWindow = Button(app, text='Enquire Swimmer\'s Timings')
dispWindow = Button(app, text='Display Swimmer\'s Timings for Submission')

regWindow.grid(row=1, column=0)
remWindow.grid(row=1, column=2)
recWindow.grid(row=2, column=0)
enqWindow.grid(row=2, column=2)
dispWindow.grid(row=3, column=1)

app.title('SSA Administrative Program - 10240311 Yun Minseo DIT PS CA3 Individual Assignment')
app.mainloop()