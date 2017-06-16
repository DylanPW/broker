#
#
#
#

from Tkinter import *
import ttk
from sqlite3 import *
# Initalise the window and set the maximum size
window = Tk()
window.title('Wrex Database Management')
window.maxsize(750,500)
window.minsize(750,500)

#Insert the title label
titleLabel = Label(window, text='database_name_here', font = ('Ariel', 24))
titleLabel.pack(side = "top", fill = X, expand = False, padx = 10, pady = 10)

#Add the main frame (har har)
mainFrame = LabelFrame(window, text='bepis', padx = 10, pady = 10)
mainFrame.pack(side = "left", fill = BOTH, expand = True, padx = 2, pady = 2)

#Add the tabs to the main window
tabs = ttk.Notebook(mainFrame)
viewTable = ttk.Frame(tabs)
viewEntries = ttk.Frame(tabs)
addEntries = ttk.Frame(tabs)
tabs.(side = "left", fill = BOTH, expand = True)

tabs.add(viewTable, text='View Table')
tabs.add(viewEntries, text='View Entries')
tabs.add(addEntries, text='Add Entries')

window.mainloop()
