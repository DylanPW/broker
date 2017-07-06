# Created by DylanPW; https://github.com/DylanPW
#
# A simple contacts database application, featuring exporting to csv.
#
# Currently a work in progress.
#


#Import applicable modules
from Tkinter import *
import ttk, Tkconstants, tkFileDialog, tkMessageBox, platform, os.path, sys, csv, re
from sqlite3 import *
#Variables for text
dbname = "Database Name Here"
padding = 5

###############################################################################
#Functions for user actions
###############################################################################

# Key Variables
editing = False
currentID = 0

# Initalise the database connection
def initialiseDB():
    #Globalise Variables
    global db, db_connect, osPlatform, homeDir, entries
    #Check if the database exists, if it does not prompt the user to create
    if os.path.exists("contacts.db"):
        db = connect(database = "contacts.db")
        db_connect = db.cursor()
    else:
        createNew = tkMessageBox.askyesno("Database not found!","Database not found! Create new Database?")
        if createNew == True:
            db = connect(database = "contacts.db")
            db.row_factory = lambda cursor, row: row[0]
            db_connect = db.cursor()
            db_connect.execute("CREATE TABLE Contacts (id integer PRIMARY KEY, alias text NOT NULL, name text, email text, address text, phone text, website text, facebook text, twitter text, instagram text, linkedin text, other text)")
        elif createNew == False:
            exitError = tkMessageBox.showerror("Error", "No database, exiting ...")
            if exitError == "ok":
                ErrorMsg()

    #Select the aliases from the database
    db_connect.execute("SELECT id, alias FROM Contacts")
    results = db_connect.fetchall()
    entries = results
    for r in results:
        listTable.insert(END, r[1])
    global index
    index = 0

    #Check the platform
    osPlatform = platform.system()
    if osPlatform == 'Windows':
        homeDir = "%Homedrive%%Homepath%"
    else:
        homeDir = "$HOME"
# Select the information from the database
def SelectEntry(event):
    global index, currentID
    #Take the index of the list and search main list of entries for it
    index = [str(r) for r in listTable.curselection()]
    index = int(index[0]) + 1
    index = [i for i, v in enumerate(entries) if v[0] == index]
    index[0] += 1
    currentID = str(index)
    db_connect.execute("SELECT * FROM Contacts WHERE id = (?)",(index))
    results = db_connect.fetchall()

    aliasVar.set(results[0][1])
    nameVar.set(results[0][2])
    emailVar.set(results[0][3])
    addressVar.set(results[0][4])
    phoneVar.set(results[0][5])
    websiteVar.set(results[0][6])
    facebookVar.set(results[0][7])
    twitterVar.set(results[0][8])
    instagramVar.set(results[0][9])
    linkedinVar.set(results[0][10])
    otherVar.set(results[0][11])

    window.update()


# change the values of the View Entry Boxes to accept modifications
def editValues():
    global index, editing, results, currentID
    global aliasVar, nameVar, emailVar, phoneVar, websiteVar, facebookVar, twitterVar, instagramVar, linkedinVar, otherVar
    global aliasBackup, nameBackup, emailBackup, addressBackup, phoneBackup, websiteBackup, facebookBackup, twitterBackup, instagramBackup, linkedinBackup, otherBackup
    global aliasViewEntry, nameViewEntry, emailViewEntry, phoneViewEntry, websiteViewEntry, facebookViewEntry, twitterViewEntry, instagramViewEntry, linkedinViewEntry, otherViewEntry

    if index != 0:
        # Change the state to readonly and save the entries to the database
        if editing == True:
            aliasViewEntry.configure(state = "readonly")
            nameViewEntry.configure(state = "readonly")
            emailViewEntry.configure(state = "readonly")
            addressViewEntry.configure(state = "readonly")
            phoneViewEntry.configure(state = "readonly")
            webViewEntry.configure(state = "readonly")
            facebookViewEntry.configure(state = "readonly")
            twitterViewEntry.configure(state = "readonly")
            instagramViewEntry.configure(state = "readonly")
            linkedinViewEntry.configure(state = "readonly")
            otherViewEntry.configure(state = "readonly")
            editButton.configure(text = "Edit Entry")
            editing = False

            promptResult = tkMessageBox.askokcancel("Save Entry?","Would you like to save this entry?")
            if promptResult == True and aliasViewEntry.get() != "":
                db_connect.execute("UPDATE Contacts SET alias = ('"+ aliasViewEntry.get() +"'), name = ('"+ nameViewEntry.get() +"'), email = ('"+ emailViewEntry.get() +"'), address = ('"+ addressViewEntry.get() +"'), \
                phone  = ('"+ phoneViewEntry.get() +"'), website = ('"+ webViewEntry.get() +"'), facebook = ('"+ facebookViewEntry.get() +"'), twitter = ('"+ twitterViewEntry.get() +"'), \
                instagram = ('"+ instagramViewEntry.get() +"'), linkedin = ('"+ linkedinViewEntry.get() +"'), other  = ('"+ otherViewEntry.get() +"') WHERE id = ('"+ currentID +"')")
                db.commit()
                #Reload the list
                db_connect.execute("SELECT alias FROM Contacts")
                results = db_connect.fetchall()
                listTable.delete(0, END)
                for r in results:
                    listTable.insert(END, r)
                aliasSearchBox.delete(0, END)

            elif promptResult == False:
                aliasVar.set(aliasBackup)
                nameVar.set(nameBackup)
                emailVar.set(emailBackup)
                addressVar.set(addressBackup)
                phoneVar.set(phoneBackup)
                websiteVar.set(websiteBackup)
                facebookVar.set(facebookBackup)
                twitterVar.set(twitterBackup)
                instagramVar.set(instagramBackup)
                linkedinVar.set(linkedinBackup)
                otherVar.set(otherBackup)

                window.update()
        else:
            # Save the previous contents of the entries
            aliasBackup = aliasViewEntry.get()
            nameBackup = nameViewEntry.get()
            emailBackup = emailViewEntry.get()
            addressBackup = addressViewEntry.get()
            phoneBackup = phoneViewEntry.get()
            websiteBackup = webViewEntry.get()
            facebookBackup = facebookViewEntry.get()
            twitterBackup = twitterViewEntry.get()
            instagramBackup = instagramViewEntry.get()
            linkedinBackup = linkedinViewEntry.get()
            otherBackup = otherViewEntry.get()

            aliasViewEntry.configure(state = "normal")
            nameViewEntry.configure(state = "normal")
            emailViewEntry.configure(state = "normal")
            addressViewEntry.configure(state = "normal")
            phoneViewEntry.configure(state = "normal")
            webViewEntry.configure(state = "normal")
            facebookViewEntry.configure(state = "normal")
            twitterViewEntry.configure(state = "normal")
            instagramViewEntry.configure(state = "normal")
            linkedinViewEntry.configure(state = "normal")
            otherViewEntry.configure(state = "normal")
            editButton.configure(text = "Save Entry")
            editing = True
            window.update()
    else:
        tkMessageBox.showerror("Error","Please select an Entry")
#Search for applicable

def saveCSV():
    global homeDir
    saveFile = tkFileDialog.asksaveasfilename(initialdir = homeDir, title = "Select Save Location", filetypes = (("CSV","*.csv"),("All Files","*.*")), defaultextension = ".csv")
    try:
        with open(saveFile, "wb") as writeFile:
            writeFile.write("id,alias,name,email,address,phone,website,facebook,twitter,instagram,linkedin,other\n")
            for row in db_connect.execute("SELECT * FROM Contacts"):
                writeRow = ",".join(str(dex) for dex in row)
                writeFile.write(writeRow.encode())
                writeFile.write("\n")
    except:
        tkMessageBox.showerror("Error","File not saved!")

# Search the database
def searchDB():
    global searchText
    searchText = str("%"+str(aliasSearchBox.get())+"%")
    db_connect.execute("SELECT id, alias FROM Contacts WHERE alias LIKE (?)", (searchText,))
    results = db_connect.fetchall()
    entries = results
    listTable.delete(0, END)
    for r in results:
        listTable.insert(END, r[1])

def clearSearch():
    listTable.delete(0, END)
    db_connect.execute("SELECT id, alias FROM Contacts")
    results = db_connect.fetchall()
    entries = results
    for r in results:
        listTable.insert(END, r[1])
    aliasSearchBox.delete(0, END)

# triggered off left button click on text_field
def copy_text(event):
    field_value = event.widget.get()
    window.clipboard_clear()
    window.clipboard_append(field_value)

# Exit the application, closing any database connections in the process.
def exitApp():
    db_connect.close()
    db.close()
    sys.exit(0)

def ErrorMsg():
    sys.exit(0)

###############################################################################
#tkinter GUI elements
###############################################################################

# Initalise the window and set the maximum size
window = Tk()
window.title(dbname)
window.maxsize(750,525)
window.minsize(750,525)

#View Entry text variables
aliasVar = StringVar()
nameVar = StringVar()
emailVar = StringVar()
addressVar = StringVar()
phoneVar = StringVar()
websiteVar = StringVar()
facebookVar = StringVar()
twitterVar = StringVar()
instagramVar = StringVar()
linkedinVar = StringVar()
otherVar = StringVar()


# Add the menubar
menuBar = Menu(window)
fileMenu = Menu(menuBar, tearoff = 0, relief = 'flat')
fileMenu.add_command(label = "Export CSV", command  = saveCSV)
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = exitApp)
menuBar.add_cascade(label = "File", menu = fileMenu)
window.config(menu = menuBar)

# Insert the title label
titleLabel = Label(window, text= dbname, font = ('Ariel', 24), padx = 10, pady = 10)
titleLabel.pack(side = "top", fill = X, expand = False)

# Add the main frame (har har)
mainFrame = LabelFrame(window, text='Client Information', padx = 5, pady = 5)
mainFrame.pack(side = "left", fill = BOTH, expand = True)

# Add the listbox Frame
listFrame = Frame(mainFrame, bd = 1, relief = SUNKEN)

# Add the scrollbar to the listbox frame
listTableScrollbar = Scrollbar(listFrame)
listTableScrollbar.pack(side = RIGHT, fill = Y)

# Add the listbox and bind doubleclicking on an entry to open that applicable entry
listTable = Listbox(listFrame, bd = 0, yscrollcommand=listTableScrollbar.set)
listTable.pack(side = "left", fill = BOTH, expand = True)
listTable.bind("<Double-Button-1>", SelectEntry)
listTableScrollbar.configure(command = listTable.yview)

# Pack the frame
listFrame.pack(side = "left", fill = BOTH, expand = True)

# Add the tabs to the main window
tabs = ttk.Notebook(mainFrame)
viewEntries = ttk.Frame(tabs)
addEntries = ttk.Frame(tabs)
tabs.pack(side = "right", fill = BOTH, expand = True)
tabs.add(viewEntries, text='View Entry')
tabs.add(addEntries, text='Add Entries')

################################################################################
# SETTING UP VIEWENTRIES
################################################################################

# Add the labels to the viewentries tabs
aliasViewLabel = Label(viewEntries, text = "Name/Alias: ", padx = padding, pady = padding, font = ("Ariel", 10))
nameViewLabel = Label(viewEntries, text = "Full Name: ", padx = padding, pady = padding, font = ("Ariel", 10))
emailViewLabel = Label(viewEntries, text = "Email: ", padx = padding, pady = padding, font = ("Ariel", 10))
addressViewLabel = Label(viewEntries, text = "Address: ", padx = padding, pady = padding, font = ("Ariel", 10))
phoneViewLabel = Label(viewEntries, text = "Phone Number: ", padx = padding, pady = padding, font = ("Ariel", 10))
webViewLabel = Label(viewEntries, text = "Website: ", padx = padding, pady = padding, font = ("Ariel", 10))
facebookViewLabel = Label(viewEntries, text = "Facebook: ", padx = padding, pady = padding, font = ("Ariel", 10))
twitterViewLabel = Label(viewEntries, text = "Twitter: ", padx = padding, pady = padding, font = ("Ariel", 10))
instagramViewLabel = Label(viewEntries, text = "Instragram: ", padx = padding, pady = padding, font = ("Ariel", 10))
linkedinViewLabel = Label(viewEntries, text = "Linkedin: ", padx = padding, pady = padding, font = ("Ariel", 10))
otherViewLabel = Label(viewEntries, text = "Other Information: ", padx = padding, pady = padding, font = ("Ariel", 10))

# Add the text entries
aliasViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = aliasVar, font = ("Ariel", 10))
nameViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = nameVar, font = ("Ariel", 10))
emailViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = emailVar, font = ("Ariel", 10))
addressViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = addressVar, font = ("Ariel", 10))
phoneViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = phoneVar, font = ("Ariel", 10))
webViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = websiteVar, font = ("Ariel", 10))
facebookViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = facebookVar, font = ("Ariel", 10))
twitterViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = twitterVar, font = ("Ariel", 10))
instagramViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = instagramVar, font = ("Ariel", 10))
linkedinViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = linkedinVar, font = ("Ariel", 10))
otherViewEntry = Entry(viewEntries, state = "readonly", width = 51, textvariable = otherVar, font = ("Ariel", 10))

# Add the labels into a grid
aliasViewLabel.grid(row = 1, column = 1, sticky = 'w')
nameViewLabel.grid(row = 2, column = 1, sticky = 'w')
emailViewLabel.grid(row = 3, column = 1, sticky = 'w')
addressViewLabel.grid(row = 4, column = 1, sticky = 'w')
phoneViewLabel.grid(row = 5, column = 1, sticky = 'w')
webViewLabel.grid(row = 6, column = 1, sticky = 'w')
facebookViewLabel.grid(row = 7, column = 1, sticky = 'w')
twitterViewLabel.grid(row = 8, column = 1, sticky = 'w')
instagramViewLabel.grid(row = 9, column = 1, sticky = 'w')
linkedinViewLabel.grid(row = 10, column = 1, sticky = 'w')
otherViewLabel.grid(row = 11, column = 1, sticky = 'w')

# add the entryboxes into a grid
aliasViewEntry.grid(row = 1, column = 2, sticky = 'e')
nameViewEntry.grid(row = 2, column = 2, sticky = 'e')
emailViewEntry.grid(row = 3, column = 2, sticky = 'e')
addressViewEntry.grid(row = 4, column = 2, sticky = 'e')
phoneViewEntry.grid(row = 5, column = 2, sticky = 'e')
webViewEntry.grid(row = 6, column = 2, sticky = 'e')
facebookViewEntry.grid(row = 7, column = 2, sticky = 'e')
twitterViewEntry.grid(row = 8, column = 2, sticky = 'e')
instagramViewEntry.grid(row = 9, column = 2, sticky = 'e')
linkedinViewEntry.grid(row = 10, column = 2, sticky = 'e')
otherViewEntry.grid(row = 11, column = 2, sticky = 'e')

# bind left clicking on the entryboxes to
aliasViewEntry.bind("<Button-3>", copy_text)
nameViewEntry.bind("<Button-3>", copy_text)
emailViewEntry.bind("<Button-3>", copy_text)
addressViewEntry.bind("<Button-3>", copy_text)
phoneViewEntry.bind("<Button-3>", copy_text)
webViewEntry.bind("<Button-3>", copy_text)
facebookViewEntry.bind("<Button-3>", copy_text)
twitterViewEntry.bind("<Button-3>", copy_text)
instagramViewEntry.bind("<Button-3>", copy_text)
linkedinViewEntry.bind("<Button-3>", copy_text)
otherViewEntry.bind("<Button-3>", copy_text)

#Implement the Search Frame
searchFrame = Frame(viewEntries, bd = 1, relief = GROOVE, padx = padding/2, pady = padding/2)
searchFrame.grid(row = 0, column = 1, columnspan = 2, sticky = 'we')
aliasSearchLabel = Label(searchFrame, text = 'Search: ', padx = padding, pady = padding, font = ("Ariel", 10))
aliasSearchLabel.grid(row = 0, column = 0)
aliasSearchBox = Entry(searchFrame, font = ("Ariel", 10), width = 50)
aliasSearchBox.grid(row = 0, column = 1, sticky = 'we', columnspan = 2)
aliasSearchButton = Button(searchFrame, command = searchDB, text = 'Search', font = ("Ariel", 10), width = 5)
aliasSearchButton.grid(row = 0, column = 2, sticky = 'e')
aliasClearButton = Button(searchFrame, command = clearSearch, text = 'Clear',font = ("Ariel", 10), width  = 5)
aliasClearButton.grid(row = 0, column = 3, sticky = 'e')

# Add a button to edit
editButton = Button(viewEntries, text = "Edit Entry", command = editValues, width = 8)
editButton.grid(row = 12, column = 2)

################################################################################
# SETTING UP ADDENTRIES
################################################################################

# Add the labels to the addentries tabs
aliasEditLabel = Label(addEntries, text = "Name/Alias: ", padx = padding, pady = padding, font = ("Ariel", 10))
nameEditLabel = Label(addEntries, text = "Full Name: ", padx = padding, pady = padding, font = ("Ariel", 10))
emailEditLabel = Label(addEntries, text = "Email: ", padx = padding, pady = padding, font = ("Ariel", 10))
addressEditLabel = Label(addEntries, text = "Address: ", padx = padding, pady = padding, font = ("Ariel", 10))
phoneEditLabel = Label(addEntries, text = "Phone Number: ", padx = padding, pady = padding, font = ("Ariel", 10))
webEditLabel = Label(addEntries, text = "Website: ", padx = padding, pady = padding, font = ("Ariel", 10))
facebookEditLabel = Label(addEntries, text = "Facebook: ", padx = padding, pady = padding, font = ("Ariel", 10))
twitterEditLabel = Label(addEntries, text = "Twitter: ", padx = padding, pady = padding, font = ("Ariel", 10))
instagramEditLabel = Label(addEntries, text = "Instragram: ", padx = padding, pady = padding, font = ("Ariel", 10))
linkedinEditLabel = Label(addEntries, text = "Linkedin: ", padx = padding, pady = padding, font = ("Ariel", 10))
otherEditLabel = Label(addEntries, text = "Other Information: ", padx = padding, pady = padding, font = ("Ariel", 10))

# Add the text entry fields
aliasEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
nameEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
emailEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
addressEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
phoneEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
webEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
facebookEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
twitterEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
instagramEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
linkedinEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))
otherEditEntry = Entry(addEntries, state = "normal", width = 51, font = ("Ariel", 10))

# Add the labels into a grid
aliasEditLabel.grid(row = 1, column = 1, sticky = 'w')
nameEditLabel.grid(row = 2, column = 1, sticky = 'w')
emailEditLabel.grid(row = 3, column = 1, sticky = 'w')
addressEditLabel.grid(row = 4, column = 1, sticky = 'w')
phoneEditLabel.grid(row = 5, column = 1, sticky = 'w')
webEditLabel.grid(row = 6, column = 1, sticky = 'w')
facebookEditLabel.grid(row = 7, column = 1, sticky = 'w')
twitterEditLabel.grid(row = 8, column = 1, sticky = 'w')
instagramEditLabel.grid(row = 9, column = 1, sticky = 'w')
linkedinEditLabel.grid(row = 10, column = 1, sticky = 'w')
otherEditLabel.grid(row = 11, column = 1, sticky = 'w')

# add the entryboxes into a grid
aliasEditEntry.grid(row = 1, column = 2, sticky = 'e')
nameEditEntry.grid(row = 2, column = 2, sticky = 'e')
emailEditEntry.grid(row = 3, column = 2, sticky = 'e')
addressEditEntry.grid(row = 4, column = 2, sticky = 'e')
phoneEditEntry.grid(row = 5, column = 2, sticky = 'e')
webEditEntry.grid(row = 6, column = 2, sticky = 'e')
facebookEditEntry.grid(row = 7, column = 2, sticky = 'e')
twitterEditEntry.grid(row = 8, column = 2, sticky = 'e')
instagramEditEntry.grid(row = 9, column = 2, sticky = 'e')
linkedinEditEntry.grid(row = 10, column = 2, sticky = 'e')
otherEditEntry.grid(row = 11, column = 2, sticky = 'e')

addButton = Button(addEntries, text = "Add Entry", width = 8)
addButton.grid(row = 12, column = 2)

################################################################################
# STARTING UP
################################################################################
# intialize the database
initialiseDB()
listTable.select_set(0)

# start the window
window.mainloop()
