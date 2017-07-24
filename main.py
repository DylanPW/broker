# Created by DylanPW; https://github.com/DylanPW
#
# A simple contacts database application, featuring exporting to csv.
#
# Version 0.3c;
#
# Please see README for additional details and changelog.
#
#
# Please report any bugs or issues as you see fit.


#Import applicable
try:
    from Tkinter import *
except:
    from tkinter import *
# from tkMessageBox import *
import ttk, Tkconstants, tkFileDialog, platform, os.path, sys, csv, re, tkMessageBox
from sqlite3 import *
#Variables for text
dbname = "Database Name Here"
padding = 5

###############################################################################
#Functions for user actions
###############################################################################

# Key Variables
searchActive = False
editing = False
currentID = 0

#Create new database (first launch)
def createNewDB():
    tkMessageBox.askyesno("Database not found!","Database not found! Create new Database?")
    if True:
        statusLabel.text = "Creating..."
        db = connect(database = "contacts.db")
        db.row_factory = lambda cursor, row: row[0]
        db_connect = db.cursor()
        db_connect.execute("CREATE TABLE Contacts (id integer PRIMARY KEY, alias text NOT NULL, name text, email text, address text, phone text, website text, facebook text, twitter text, instagram text, linkedin text, other text)")

    else:
        exitError = tkMessageBox.showerror("Error", "No database, exiting ...")
        ErrorMsg()


# Initalise the database connection
def initialiseDB():
    #Globalise Variables
    global db, db_connect, osPlatform, homeDir, entries, width, status
    #Check if the database exists, if it does not prompt the user to create
    if os.path.exists("contacts.db"):
        db = connect(database = "contacts.db")
        db_connect = db.cursor()
        statusLabel.configure(text = "Database Connected")
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
            width = 64
        else:
            homeDir = "$HOME"
            width = 52

        window.update()
    else:
        createNewDB()
        window.destroy()
        os.system('python main.py')

# Select the information from the database
def SelectEntry(event):
    global index, currentID
    try:
        tabs.select(0)
        statusLabel.configure(text = "Selecting Entry...")
        #Take the index of the list and search main list of entries for it
        index = [str(r) for r in listTable.curselection()]
        # index = [i for i, v in enumerate(entries) if v[0] == index]
        currentID = str(entries[int(index[0][0])])
        currentID = currentID[1]

        db_connect.execute("SELECT * FROM Contacts WHERE id = (?)",(currentID,))
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
        statusLabel.configure(text = "Ready")
        window.update()
    except:
        tkMessageBox.showerror("Error", "No index selected.")


# change the values of the View Entry Boxes to accept modifications
def editValues():
    global index, editing, results, currentID
    global aliasVar, nameVar, emailVar, phoneVar, websiteVar, facebookVar, twitterVar, instagramVar, linkedinVar, otherVar
    global aliasBackup, nameBackup, emailBackup, addressBackup, phoneBackup, websiteBackup, facebookBackup, twitterBackup, instagramBackup, linkedinBackup, otherBackup
    global aliasViewEntry, nameViewEntry, emailViewEntry, phoneViewEntry, websiteViewEntry, facebookViewEntry, twitterViewEntry, instagramViewEntry, linkedinViewEntry, otherViewEntry
    try:
        if index != 0:
            statusLabel.configure(text = "Saving Values...")
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
                    listTable.delete(0, END)
                    db_connect.execute("SELECT id, alias FROM Contacts")
                    results = db_connect.fetchall()
                    entries = results
                    for r in results:
                        listTable.insert(END, r[1])
                    index = 0
                    db_connect.execute("SELECT * FROM Contacts WHERE id = (?)",(currentID,))
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
                    statusLabel.configure(text = "Entry Saved!")

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
                    statusLabel.configure(text = "Cancelled!")
            else:
                # Save the previous contents of the entries
                statusLabel.configure(text = "Editing Values...")
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
    except:
        tkMessageBox.showerror("Error","An error occured!")

# Delete existing entry
def deleteEntry():
    try:
        if currentID != 0:
            deletePrompt = tkMessageBox.askyesno("Delete?", "Are you sure you want to delete?")
            if deletePrompt == True:
                db_connect.execute("DELETE FROM Contacts WHERE id = (?)",(currentID,))
                db.commit()
                if searchActive == True:
                    if str(aliasSearchBox.get()) != "":
                        searchText = str("%"+str(aliasSearchBox.get())+"%")
                        db_connect.execute("SELECT id, alias FROM Contacts WHERE alias LIKE (?)", (searchText,))
                        results = db_connect.fetchall()
                        entries = results
                        listTable.delete(0, END)
                        for r in results:
                            listTable.insert(END, r[1])
                else:
                    db_connect.execute("SELECT id, alias FROM Contacts")
                    listTable.delete(0, END)
                    results = db_connect.fetchall()
                    entries = results
                    for r in results:
                        listTable.insert(END, r[1])
                    global index
                    index = 0

                aliasVar.set("")
                nameVar.set("")
                emailVar.set("")
                addressVar.set("")
                phoneVar.set("")
                websiteVar.set("")
                facebookVar.set("")
                twitterVar.set("")
                instagramVar.set("")
                linkedinVar.set("")
                otherVar.set("")
                window.update()
                statusLabel.configure(text = "Entry Deleted!")
        else:
            tkMessageBox.showerror("Error","Please select an Entry")
    except:
        tkMessageBox.showerror("Error", "An error occured!")

# function to add an entry
def addEntry():
    global entries
    try:
        if aliasEditEntry.get() != "":

            statusLabel.configure(text = "Adding Entry...")
            db_connect.execute("INSERT INTO Contacts (alias, name, email, address, phone, website, facebook, twitter, instagram, linkedin, other) \
            VALUES (('"+ aliasEditEntry.get() +"'),('"+ nameEditEntry.get() +"'),('"+ emailEditEntry.get() +"'),('"+ addressEditEntry.get() +"'), \
            ('"+ phoneEditEntry.get() +"'),('"+ webEditEntry.get() +"'),('"+ facebookEditEntry.get() +"'),('"+ twitterEditEntry.get() +"'), \
            ('"+ instagramEditEntry.get() +"'),('"+ linkedinEditEntry.get() +"'),('"+ otherEditEntry.get() +"'))")
            db.commit()

            #Reload the list
            db_connect.execute("SELECT id, alias FROM Contacts")
            listTable.delete(0, END)
            results = db_connect.fetchall()
            entries = results
            for r in results:
                listTable.insert(END, r[1])
            global index
            index = 0
            aliasSearchBox.delete(0, END)

            #Clear the editentries
            aliasEditEntry.delete(0, END)
            nameEditEntry.delete(0, END)
            emailEditEntry.delete(0, END)
            addressEditEntry.delete(0, END)
            phoneEditEntry.delete(0, END)
            webEditEntry.delete(0, END)
            facebookEditEntry.delete(0, END)
            twitterEditEntry.delete(0, END)
            instagramEditEntry.delete(0, END)
            linkedinEditEntry.delete(0, END)
            otherEditEntry.delete(0, END)
            statusLabel.configure(text = "Entry Added!")
            window.update()

        else:
            tkMessageBox.showerror("Error","You must have an alias")
    except:
        tkMessageBox.showerror("Error","An error occured.")


def saveCSV():
    global homeDir
    saveFile = tkFileDialog.asksaveasfilename(initialdir = homeDir, title = "Select Save Location", filetypes = (("CSV","*.csv"),("All Files","*.*")), defaultextension = ".csv")
    statusLabel.configure(text = "Exporting CSV...")

    try:
        with open(saveFile, "wb") as writeFile:
            writeFile.write("id,alias,name,email,address,phone,website,facebook,twitter,instagram,linkedin,other\n")
            for row in db_connect.execute("SELECT * FROM Contacts"):
                writeRow = ",".join(str(dex) for dex in row)
                writeFile.write(writeRow.encode())
                writeFile.write("\n")
                statusLabel.configure(text = "Exporting Successful!")

    except:
        tkMessageBox.showerror("Error","File not saved!")

# Search the database
def searchDB():
    global searchText, searchActive
    try:
        statusLabel.configure(text = "Searching...")
        searchText = str("%"+str(aliasSearchBox.get())+"%")
        db_connect.execute("SELECT id, alias FROM Contacts WHERE alias LIKE (?)", (searchText,))
        results = db_connect.fetchall()
        entries = results
        listTable.delete(0, END)
        for r in results:
            listTable.insert(END, r[1])
        statusLabel.configure(text = "Search Complete!")
        searchActive = True

    except:
        tkMessageBox.showerror("Error","An error occured, did your search contain invalid strings?")

#Clear the search field
def clearSearch():
    try:
        listTable.delete(0, END)
        db_connect.execute("SELECT id, alias FROM Contacts")
        results = db_connect.fetchall()
        entries = results
        for r in results:
            listTable.insert(END, r[1])
        aliasSearchBox.delete(0, END)
        statusLabel.configure(text = "Search cleared!")
        searchActive = False

    except:
        tkMessageBox.showerror("Error","An error occured!")



#Clear the editentries
def clearEntries():
    aliasEditEntry.delete(0, END)
    nameEditEntry.delete(0, END)
    emailEditEntry.delete(0, END)
    addressEditEntry.delete(0, END)
    phoneEditEntry.delete(0, END)
    webEditEntry.delete(0, END)
    facebookEditEntry.delete(0, END)
    twitterEditEntry.delete(0, END)
    instagramEditEntry.delete(0, END)
    linkedinEditEntry.delete(0, END)
    otherEditEntry.delete(0, END)
    statusLabel.configure(text = "Cleared!")

# triggered off left button click on entrybox
def copy_text(event):
    field_value = event.widget.get()
    window.clipboard_clear()
    window.clipboard_append(field_value)
    statusLabel.configure(text = "Text Copied!...")

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

osPlatform = platform.system()
if osPlatform == 'Windows':
    boxWidth = 64
else:
    boxWidth = 51

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
mainFrame.pack(side = "top", fill = BOTH, expand = True)

# add a status frame
statusFrame = Frame(window)
statusFrame.pack(side = "bottom", fill = BOTH, expand = True)

statusLabel = Label(statusFrame, text = "", font = ('Ariel', 10))
statusLabel.pack(side = RIGHT)

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
aliasViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = aliasVar, font = ("Ariel", 10))
nameViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = nameVar, font = ("Ariel", 10))
emailViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = emailVar, font = ("Ariel", 10))
addressViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = addressVar, font = ("Ariel", 10))
phoneViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = phoneVar, font = ("Ariel", 10))
webViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = websiteVar, font = ("Ariel", 10))
facebookViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = facebookVar, font = ("Ariel", 10))
twitterViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = twitterVar, font = ("Ariel", 10))
instagramViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = instagramVar, font = ("Ariel", 10))
linkedinViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = linkedinVar, font = ("Ariel", 10))
otherViewEntry = Entry(viewEntries, state = "readonly", width =boxWidth, textvariable = otherVar, font = ("Ariel", 10))

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
aliasViewEntry.grid(row = 1, column = 2, sticky = 'w')
nameViewEntry.grid(row = 2, column = 2, sticky = 'w')
emailViewEntry.grid(row = 3, column = 2, sticky = 'w')
addressViewEntry.grid(row = 4, column = 2, sticky = 'w')
phoneViewEntry.grid(row = 5, column = 2, sticky = 'w')
webViewEntry.grid(row = 6, column = 2, sticky = 'w')
facebookViewEntry.grid(row = 7, column = 2, sticky = 'w')
twitterViewEntry.grid(row = 8, column = 2, sticky = 'w')
instagramViewEntry.grid(row = 9, column = 2, sticky = 'w')
linkedinViewEntry.grid(row = 10, column = 2, sticky = 'w')
otherViewEntry.grid(row = 11, column = 2, sticky = 'w')

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
searchFrame = Frame(viewEntries, bd = 1, relief = GROOVE)
searchFrame.grid(row = 0, column = 1, columnspan = 2, sticky = 'we')
aliasSearchLabel = Label(searchFrame, text = 'Search: ', padx = padding, pady = padding, font = ("Ariel", 10))
aliasSearchLabel.grid(row = 0, column = 0)
aliasSearchBox = Entry(searchFrame, font = ("Ariel", 10), width = boxWidth)
aliasSearchBox.grid(row = 0, column = 1, sticky = 'we', columnspan = 2)
aliasSearchButton = Button(searchFrame, command = searchDB, text = 'Search', font = ("Ariel", 10), width = 5)
aliasSearchButton.grid(row = 0, column = 2, sticky = 'e')
aliasClearButton = Button(searchFrame, command = clearSearch, text = 'Clear',font = ("Ariel", 10), width  = 5)
aliasClearButton.grid(row = 0, column = 3, sticky = 'e')

# Add a button to edit
editButton = Button(viewEntries, text = "Edit Entry", command = editValues, width = 8)
editButton.grid(row = 12, column = 2, columnspan =  2)

# Add a button to delete
delButton = Button(viewEntries, text = "Delete Entry", command = deleteEntry, width = 8)
delButton.grid(row = 12, column = 1)


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
aliasEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
nameEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
emailEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
addressEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
phoneEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
webEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
facebookEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
twitterEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
instagramEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
linkedinEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))
otherEditEntry = Entry(addEntries, state = "normal", width = boxWidth, font = ("Ariel", 10))

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

#Implement a dummy search frame for UI continuity
dummysearchFrame = Frame(addEntries, bd = 1, relief = GROOVE)
dummysearchFrame.grid(row = 0, column = 1, columnspan = 2, sticky = 'we')
dummyaliasSearchLabel = Label(dummysearchFrame, text = 'Search: ', padx = padding, pady = padding, font = ("Ariel", 10), state = DISABLED)
dummyaliasSearchLabel.grid(row = 0, column = 0)
dummyaliasSearchBox = Entry(dummysearchFrame, font = ("Ariel", 10), width = boxWidth, state = DISABLED)
dummyaliasSearchBox.grid(row = 0, column = 1, sticky = 'we', columnspan = 2)
dummyaliasSearchButton = Button(dummysearchFrame, text = 'Search', font = ("Ariel", 10), width = 5, state = DISABLED)
dummyaliasSearchButton.grid(row = 0, column = 2, sticky = 'e')
dummyaliasClearButton = Button(dummysearchFrame, text = 'Clear',font = ("Ariel", 10), width  = 5, state = DISABLED)
dummyaliasClearButton.grid(row = 0, column = 3, sticky = 'e')

#Implement the add entry button
addButton = Button(addEntries, command = addEntry, text = "Add Entry", width = 8)
addButton.grid(row = 12, column = 2)

# Add a button to delete
clearButton = Button(addEntries, text = "Clear Entry", command = clearEntries, width = 8)
clearButton.grid(row = 12, column = 1)

################################################################################
# STARTING UP
################################################################################
# intialize the database
initialiseDB()

# start the window
window.mainloop()
