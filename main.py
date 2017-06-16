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

def listElementClick(event):
    items = map(int, listTable.curselection())
    print items
# Initalise the window and set the maximum size
window = Tk()
window.title(dbname)
window.maxsize(750,500)
window.minsize(750,500)

# Insert the title label
titleLabel = Label(window, text= dbname, font = ('Ariel', 24), padx = 10, pady = 10)
titleLabel.pack(side = "top", fill = X, expand = False)

# Add the main frame (har har)
mainFrame = LabelFrame(window, text='bepis', padx = 5, pady = 5)
mainFrame.pack(side = "left", fill = BOTH, expand = True)

# Add the listbox Frame
listFrame = Frame(mainFrame, bd = 1, relief = SUNKEN)

# Add the scrollbar to the listbox frame
listTableScrollbar = Scrollbar(listFrame)
listTableScrollbar.pack(side = RIGHT, fill = Y)

# Add the listbox
listTable = Listbox(listFrame, bd = 0, yscrollcommand=listTableScrollbar.set)
listTable.pack(side = "left", fill = BOTH, expand = True)
listTable.bind("<Double-Button-1>", listElementClick)
# Pack the fram
listFrame.pack(side = "left", fill = BOTH, expand = True)

# Add the tabs to the main window
tabs = ttk.Notebook(mainFrame)
viewTable = ttk.Frame(tabs)
viewEntries = ttk.Frame(tabs)
addEntries = ttk.Frame(tabs)
tabs.pack(side = "right", fill = BOTH, expand = True)

tabs.add(viewTable, text='View Table')
tabs.add(viewEntries, text='View Entries')
tabs.add(addEntries, text='Add Entries')

for i in range (100):
    listTable.insert(END, i)
listTable.select_set(0)
# start the window
window.mainloop()
