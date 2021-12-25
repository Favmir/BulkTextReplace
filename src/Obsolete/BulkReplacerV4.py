# BulkReplacer Version 4
# Author: FavmirY@gmail.com

import re
import glob
from tkinter import *
from tkinter.ttk import *
import os
import csv
import sys

CONTENT_LOC = os.getcwd()
WORKBOOK_FILENAME = 'BulkReplacer_List.csv'
WORKBOOK_LOC = os.getcwd()
WORKBOOK_PATH =  os.path.join(WORKBOOK_LOC, WORKBOOK_FILENAME)

# CUSTOM DIALECT delimiter=',', quotechar = '\x07', quoting = csv.QUOTE_NONE

def CreateSheet():
    if(os.path.exists(WORKBOOK_PATH)):
        print(WORKBOOK_FILENAME,' already exists, skipping file creation')
        pass
    else:
        f = open(WORKBOOK_PATH, 'w', newline = '', encoding='utf_8_sig')
        writer = csv.writer(f)
        writer.writerow(('Hi! This will be replaced by', 'this text!','This column doesn\'t do anything'))
        writer.writerow(('This row will be run', 'after the first row.','This column doesn\'t do anything'))
        f.close

def OpenSheet():
    os.startfile(WORKBOOK_PATH)

def ReplaceText(wordlist: list[list[str]]):
    files = ''
    for filename in glob.glob('*.txt'):
        files = files + ', ' + filename
        with open(os.path.join(CONTENT_LOC, filename), 'r+', newline = '', encoding = 'utf-8-sig') as f:
            content = f.read()
            for numrow, row in enumerate(wordlist, start = 1):
                content = re.sub(row[0], row[1], content)
            f.seek(0)
            f.write(content)
            f.truncate()
            f.close()
    print('Replaced texts in files: ', files)

def PreviewReplaceText(wordlist: list[list[str]]):
    files = ''
    matches = []
    for filename in glob.glob('*.txt'):
        files = files + ', ' + filename
        with open(os.path.join(CONTENT_LOC, filename), 'r', newline = '', encoding = 'utf-8-sig') as f:
            content = f.read()
            for row in wordlist:
                restofcontent = content
                while(restofcontent != None):
                    found = re.search(row[0], restofcontent)    # <re.Match object; span=(374, 377), match='는….'>
                    if found:
                        print("found: ", found)
                        foundtext = restofcontent[max(0,found.span()[0]-5): min(len(restofcontent),found.span()[1]+5)]
                        changedtext = re.sub(row[0], row[1], foundtext)
                        matches.append( (filename, '…'+re.sub('\n', ' ↵ ', foundtext)+'…', '…'+re.sub('\n', ' ↵ ', changedtext)+'…') )
                        restofcontent = restofcontent[found.span()[1]:]
                    else:
                        print("found no more ", row[0])
                        restofcontent = None
                    
            f.close()
    return matches

# returns list of full path for all .txt files in current folder
def GetFileNames(mypath: str):
    # filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    filenames = glob.glob(mypath + '\*.txt')
    return filenames

# returns list of (dirname, filname) for all .txt files in dirname
def search(dirname):
    answer = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        # full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(filename)[-1]
        if ext == '.txt': 
            answer.append((dirname,filename))
    return answer

class TreeBrowser(Frame):
    def __init__(self, master, columnslist: list, datalist: list) -> None:
        super().__init__(master)
        tree = DataTreeview(self, columnslist, datalist)
        tree.pack(side = 'left', expand = True, fill = 'both')
        verscrollbar = Scrollbar(self, orient ="vertical", command = tree.yview)
        verscrollbar.pack(side = 'right', fill = 'y')
        tree.configure(yscrollcommand=verscrollbar.set)
    def Refresh(self, newdata):
        self.tree.Refresh(self, newdata)

class DataTreeview(Treeview):
    def __init__(self, master, columnslist: list, datalist: list):      # datalist is a list of rowlists
        super().__init__(master)
        self.data = datalist
        self['columns'] = columnslist
        self.column('#0', width=0, stretch=NO)
        self.heading('#0', text='', anchor=CENTER)
        for colname in columnslist:
            self.column(colname, anchor = CENTER, stretch = True)
            self.heading(colname, text = colname, anchor=CENTER)
        for numrow, row in enumerate(self.data, start = 0):
            self.insert(parent = '', index = numrow, text = '', values = row)
    
    def Refresh(self, newdata):
        data = newdata
        self.delete(*self.get_children())
        for numrow, row in enumerate(data, start = 0):
            self.insert(parent = '', index = numrow, text = '', values = row)
        
    # def selectedItem():
    #     return self.selection()
    

# Load workbook (needed for assgining commands to gui buttons)
CreateSheet()
with open(WORKBOOK_PATH, newline = '', encoding = 'utf-8-sig') as f:
    csvReader = csv.reader(f, dialect = 'excel')
    wordlist = list(csvReader)
    print('Loaded workbook: ',wordlist)
    matcheslist = PreviewReplaceText(wordlist)


if __debug__:
    print(GetFileNames(WORKBOOK_LOC))

filelist = search(CONTENT_LOC)


# Gui
rootwindow = Tk()
rootwindow.title('Bulk Replacer')
rootwindow['bg'] = 'grey'
rootwindow.rowconfigure(0,weight = 0)   # title frame
rootwindow.rowconfigure(1,weight = 3)
rootwindow.rowconfigure(2,weight = 1)
rootwindow.rowconfigure(3,weight = 0)   # bottom frame
rootwindow.columnconfigure(0,weight = 0)
rootwindow.columnconfigure(1,weight = 2)

frametitle = Frame(master = rootwindow, relief = 'solid')
frame1 = Frame(master = rootwindow)
frame2 = Frame(master = rootwindow)
frame3 = Frame(master = rootwindow)
framebottom = Frame(master = rootwindow)

frametitle.grid(row = 0, column = 0, columnspan = 2, sticky = N, pady = 5)
frame1.grid(row = 1, column = 0, sticky = NSEW)
frame2.grid(row = 2, column = 0, sticky = NSEW)
frame3.grid(row = 1, column = 1, rowspan = 2, sticky = NSEW)
framebottom.grid(row = 3, column = 0, columnspan = 2, pady = 5)

frame1.rowconfigure(0,weight = 0)
frame1.rowconfigure(1,weight = 1)
frame3.rowconfigure(0,weight = 0)
frame3.rowconfigure(1,weight = 1)
frame3.rowconfigure(2,weight = 0)
frame3.columnconfigure(0,weight = 1)
frame3.columnconfigure(1,weight = 0)

# top frame
lbl_title = Label(
    master = frametitle,
    text = 'RegEx Bulk Replacer',
    font = ("Verdana", 16, "bold"),
    background = 'grey')
lbl_title.pack()

# frame1 (csv file view)
btn_createSheet = Button(
    master = frame1,
    text = 'Create Example ' + WORKBOOK_FILENAME,
    command = CreateSheet
)
btn_openSheet = Button(
    master = frame1,
    text = 'Open RegEx Sheet',
    command = OpenSheet)
tv_keywords = TreeBrowser(frame1, ('RegEx1', 'RegEx2', 'Comment'), wordlist)
btn_createSheet.grid(row = 0, column = 0, pady = 5)
btn_openSheet.grid(row = 0, column = 1, pady = 5)
tv_keywords.grid(row =  1, column = 0, columnspan= 2, padx = 10, pady = 5, sticky = NSEW)


# frame2 (file browser for *.txt files)
btn_files = Button(
    master = frame2,
    text = 'Refresh',
)
tv_files = TreeBrowser(frame2, ('Path', 'Filename'), filelist)
btn_files.grid(row =  0, column = 0, padx = 10, pady = 5)
tv_files.grid(row =  1, column = 0, padx = 10, pady = 5)

# frame3 (preview changes, run)
lbl_preview = Label(
    master = frame3,
    text = 'What will be changed:')
tv_preview = TreeBrowser(frame3, ('Path', 'Before', 'After'), matcheslist)
btn_preview = Button(
    master = frame3,
    text = 'Refresh preview window',
    # command = tv_preview.Refresh(PreviewReplaceText(wordlist))
)
btn_run = Button(
    master = frame3,
    text = 'Replace in every *.txt files selected',
    command = lambda: ReplaceText(wordlist) and tv_preview.Refresh(PreviewReplaceText(wordlist)))
lbl_preview.grid(row = 0, column = 0, pady = 5)
btn_preview.grid(row = 0, column = 1, padx = 5)
tv_preview.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 5, sticky = NSEW)
btn_run.grid(row = 2, column = 0, pady = 5)


rootwindow.mainloop()








