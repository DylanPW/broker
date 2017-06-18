# Created by DylanPW; https://github.com/DylanPW
#
#
#


#Import applicable modules
from Tkinter import *
import ttk
from sqlite3 import *

#Variables for text
dbname = "Database Name Here"
padding = 5


#Functions for user actions

#Clicking on the element within the list
def SelectEntry(event):
    items = map(int, listTable.curselection())
    aliasVar.set(str(items))
    nameVar.set(str(items))
    emailVar.set(str(items))
    phoneVar.set(str(items))
    websiteVar.set(str(items))
    facebookVar.set(str(items))
    twitterVar.set(str(items))
    instagramVar.set(str(items))
    linkedinVar.set(str(items))
    otherVar.set(str(items))
    window.update()

###############################################################################
#tkinter GUI elements
###############################################################################

# Initalise the window and set the maximum size
window = Tk()
window.title(dbname)
window.maxsize(750,500)
window.minsize(750,500)

#View Entry text variables
aliasVar = StringVar()
nameVar = StringVar()
emailVar = StringVar()
phoneVar = StringVar()
websiteVar = StringVar()
facebookVar = StringVar()
twitterVar = StringVar()
instagramVar = StringVar()
linkedinVar = StringVar()
otherVar = StringVar()

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

# Pack the fram
listFrame.pack(side = "left", fill = BOTH, expand = True)

# Add the tabs to the main window
tabs = ttk.Notebook(mainFrame)
viewEntries = ttk.Frame(tabs)
addEntries = ttk.Frame(tabs)
tabs.pack(side = "right", fill = BOTH, expand = True)
tabs.add(viewEntries, text='View Entry')
tabs.add(addEntries, text='Add Entries')

# Add the labels to the viewentries tabs
aliasViewLabel = Label(viewEntries, text = "Name/Alias: ", padx = padding, pady = padding)
nameViewLabel = Label(viewEntries, text = "Full Name: ", padx = padding, pady = padding)
emailViewLabel = Label(viewEntries, text = "Email: ", padx = padding, pady = padding)
phoneViewLabel = Label(viewEntries, text = "Phone Number: ", padx = padding, pady = padding)
webViewLabel = Label(viewEntries, text = "Website: ", padx = padding, pady = padding)
facebookViewLabel = Label(viewEntries, text = "Facebook: ", padx = padding, pady = padding)
twitterViewLabel = Label(viewEntries, text = "Twitter: ", padx = padding, pady = padding)
instagramViewLabel = Label(viewEntries, text = "Instragram: ", padx = padding, pady = padding)
linkedinViewLabel = Label(viewEntries, text = "Linkedin: ", padx = padding, pady = padding)
otherViewLabel = Label(viewEntries, text = "Other Information: ", padx = padding, pady = padding)

# Add the text entries
aliasViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = aliasVar)
nameViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = nameVar)
emailViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = emailVar)
phoneViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = phoneVar)
webViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = websiteVar)
facebookViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = facebookVar)
twitterViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = twitterVar)
instagramViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = instagramVar)
linkedinViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = linkedinVar)
otherViewEntry = Entry(viewEntries, state = "readonly", width = 52, textvariable = otherVar)

# Add the labels into a grid
aliasViewLabel.grid(row = 1, column = 1, sticky = 'w')
nameViewLabel.grid(row = 2, column = 1, sticky = 'w')
emailViewLabel.grid(row = 3, column = 1, sticky = 'w')
phoneViewLabel.grid(row = 4, column = 1, sticky = 'w')
webViewLabel.grid(row = 5, column = 1, sticky = 'w')
facebookViewLabel.grid(row = 6, column = 1, sticky = 'w')
twitterViewLabel.grid(row = 7, column = 1, sticky = 'w')
instagramViewLabel.grid(row = 8, column = 1, sticky = 'w')
linkedinViewLabel.grid(row = 9, column = 1, sticky = 'w')
otherViewLabel.grid(row = 10, column = 1, sticky = 'w')

# add the entryboxes into a grid
aliasViewEntry.grid(row = 1, column = 2, sticky = 'e')
nameViewEntry.grid(row = 2, column = 2, sticky = 'e')
emailViewEntry.grid(row = 3, column = 2, sticky = 'e')
phoneViewEntry.grid(row = 4, column = 2, sticky = 'e')
webViewEntry.grid(row = 5, column = 2, sticky = 'e')
facebookViewEntry.grid(row = 6, column = 2, sticky = 'e')
twitterViewEntry.grid(row = 7, column = 2, sticky = 'e')
instagramViewEntry.grid(row = 8, column = 2, sticky = 'e')
linkedinViewEntry.grid(row = 9, column = 2, sticky = 'e')
otherViewEntry.grid(row = 10, column = 2, sticky = 'e')

################################################################################
# DEBUGGING
###############################################################################
for i in range (100):
    listTable.insert(END, i)
listTable.select_set(0)
# start the window
window.mainloop()
