# BulkReplacer Version 3
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

def OpenSheet():
    os.startfile(WORKBOOK_PATH)

def ReplaceText(wordlist: list[list[str]]):
    files = ''
    for filename in glob.glob('*.txt'):
        files = files + ', ' + filename
        with open(os.path.join(CONTENT_LOC, filename), 'r+', encoding = 'utf-8') as f:
            content = f.read()
            for numrow, row in enumerate(wordlist, start = 1):
                content = re.sub(row[0], row[1], content, flags = re.M)
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
        with open(os.path.join(CONTENT_LOC, filename), 'r', encoding = 'utf-8') as f:
            content = f.read()
            for numrow, row in enumerate(wordlist, start = 1):
                temp = []
                found = re.findall(row[0], content)
                for i, singlefound in enumerate(found):
                    matches.append( (filename, found[i], re.sub(row[0], row[1], found[i], flags = re.M)) )
            f.close()
    return matches

def GetFileNames(mypath: str):
    # filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    filenames = glob.glob(mypath + '\*.txt')
    return filenames

def search(dirname):
    answer = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        # full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(filename)[-1]
        if ext == '.txt': 
            answer.append((dirname,filename))
    return answer

class TreeBrowser(Treeview):
    def __init__(self, master, columnslist: list, datalist: list):      # datalist is a list of rowlists
        super().__init__(master)
        self.data = datalist
        self['columns'] = columnslist
        self.column('#0', width=0, stretch=NO)
        self.heading('#0', text='', anchor=CENTER)
        for colname in columnslist:
            self.column(colname, anchor = CENTER, width = 150)
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
with open(WORKBOOK_PATH, newline = '', encoding = 'utf-8') as f:
    csvReader = csv.reader(f, delimiter='\t', quotechar = '\x07', quoting = csv.QUOTE_NONE)
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

frametitle = Frame(master = rootwindow, relief = 'solid')
frameleft = Frame(master = rootwindow)
framemiddle = Frame(master = rootwindow)
frameright = Frame(master = rootwindow)
framebottom = Frame(master = rootwindow)

frametitle.grid(row = 0, column = 0, sticky = N, pady = 5)
frameleft.grid(row = 1, column = 0, padx = 3)
framemiddle.grid(row = 1, column = 1, padx = 3)
frameright.grid(row = 1, column = 2, padx = 3)
framebottom.grid(row = 2, column = 0, pady = 5)

# top frame
lbl_title = Label(
    master = frametitle,
    text = 'RegEx Bulk Replacer',
    font = ("Verdana", 16, "bold"),
    background = 'grey')
lbl_title.pack()

# left frame (csv file view)
btn_openSheet = Button(
    master = frameleft,
    text = 'Open ' + WORKBOOK_FILENAME,
    command = OpenSheet)
tv_keywords = TreeBrowser(frameleft, ('RegEx1', 'RegEx2', 'Comment'), wordlist)
btn_openSheet.grid(row = 0, column = 0, pady = 5)
tv_keywords.grid(row =  1, column = 0, padx = 10, pady = 5)


# middle frame (file browser for *.txt files)
btn_files = Button(
    master = framemiddle,
    text = 'Refresh',
#     command = lambda: filelist = 
)
tv_files = TreeBrowser(framemiddle, ('Path', 'Filename'), filelist)
btn_files.grid(row =  0, column = 0, padx = 10, pady = 5)
tv_files.grid(row =  1, column = 0, padx = 10, pady = 5)

# right frame (preview changes, run)
lbl_preview = Label(
    master = frameright,
    text = 'What will be changed:')
tv_preview = TreeBrowser(frameright, ('Path', 'Before', 'After'), matcheslist)
btn_preview = Button(
    master = frameright,
    text = 'Refresh preview window',
    command = tv_preview.Refresh(PreviewReplaceText(wordlist))
)
btn_run = Button(
    master = frameright,
    text = 'Replace in every *.txt files selected',
    command = lambda: ReplaceText(wordlist) and tv_preview.Refresh(PreviewReplaceText(wordlist)))
lbl_preview.grid(row = 0, column = 0, pady = 5)
btn_preview.grid(row = 0, column = 1, padx = 5)
tv_preview.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 5)
btn_run.grid(row = 2, column = 0, pady = 5)


rootwindow.mainloop()








