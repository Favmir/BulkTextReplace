# BulkReplacer Version 1.1
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

def OpenFile():
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

# Load workbook (needed for assgining commands to gui buttons)
with open(WORKBOOK_PATH, newline = '', encoding = 'utf-8') as f:
    csvReader = csv.reader(f, delimiter='\t', quotechar = '\x07', quoting = csv.QUOTE_NONE)
    wordlist = list(csvReader)
    print('Loaded workbook: ',wordlist)

# Gui
rootwindow = Tk()
rootwindow.title('Bulk Replacer')
rootwindow['bg'] = 'grey'

lbl_title = Label(
    master = rootwindow,
    text = 'RegEx Bulk Replacer',
    background = 'grey')
btn_openSheet = Button(
    master = rootwindow,
    text = 'Open ' + WORKBOOK_FILENAME,
    command = OpenFile,)
btn_preview = Button(
    master = rootwindow,
    text = 'Preview changes',
    # command = lambda: PreviewChange(wordlist)
    )
lbl_preview = Label(
    master = rootwindow,
    text = '')

tv_keywords = Treeview(rootwindow)
tv_keywords['columns'] = ('regex1', 'regex2', 'comment')
tv_keywords.column('#0', width=0, stretch=NO)
tv_keywords.column('regex1', anchor=CENTER, width=150)
tv_keywords.column('regex2', anchor=CENTER, width=150)
tv_keywords.column('comment', anchor=CENTER, width=200)
tv_keywords.heading('#0', text='', anchor=CENTER)
tv_keywords.heading('regex1', text='Original RegEx', anchor=CENTER)
tv_keywords.heading('regex2', text='Replacement RegEx', anchor=CENTER)
tv_keywords.heading('comment', text='Comment', anchor=CENTER)
for numrow, row in enumerate(wordlist, start = 0):
    tv_keywords.insert(parent = '', index = numrow, text = '', values = row)


btn_run = Button(
    master = rootwindow,
    text = 'Replace in every *.txt files',
    command = lambda: ReplaceText(wordlist))

lbl_title.grid(row = 0, column = 0, sticky = N, pady = 5)
btn_openSheet.grid(row = 1, column = 0, sticky = W, pady = 2)
btn_preview.grid(row = 1, column = 1, padx = 10)
tv_keywords.grid(row =  2, column = 1, padx = 10, pady = 5)
btn_run.grid(row = 3, column = 0, pady = 10)


rootwindow.mainloop()








