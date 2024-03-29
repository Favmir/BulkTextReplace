######|| BulkReplacer Program ||######
# Replaces text across multiple files via RegEx
# Version 4.3(2021/12/26)
# Author: FavmirY@gmail.com
# CSV Sheet file must be '`utf-8-sig' with ',' as delimiter
# (This was chosen because it's how excel processes .csv data)
# (Excel cannot read contents of a csv file if formatted in 'utf-8')
# .txt files getting replaced should be 'utf-8'

import re
import glob
from tkinter import *
from tkinter.ttk import *
import os
import csv
import sys
from io import StringIO

# os.getcwd() gives you current working directory
# os.path.dirname(os.path.abspath(__file__)) gives you location of python script
CONTENT_LOC = os.path.dirname(os.path.abspath(__file__))
WORKBOOK_FILENAME = 'BulkReplacer_List.csv'
WORKBOOK_LOC = os.path.dirname(os.path.abspath(__file__))
WORKBOOK_PATH =  os.path.join(WORKBOOK_LOC, WORKBOOK_FILENAME)
REGEXDATA = []

# dialect: delimiter='\t', quotechar = '\x07', quoting = csv.QUOTE_NONE

def CreateSheet():
    if(os.path.exists(WORKBOOK_PATH)):
        print(WORKBOOK_FILENAME,' already exists, skipping file creation')
        pass
    else:
        f = open(WORKBOOK_PATH, 'w', newline = '', encoding='utf-8-sig')
        writer = csv.writer(f, delimiter='\t', quoting = csv.QUOTE_NONE)
        writer.writerow(('hell', 'heck','hell will be replaced with heck(not capitalized)'))
        writer.writerow(('([hH])ell', '\\1eck','using RegEx to turn \'hell\' into \'heck\', and \'Hell\' into \'Heck\''))
        f.close

def OpenSheet():
    os.startfile(WORKBOOK_PATH)

def ReplaceText(wordlist: 'list[list[str]]'):
    files = ''
    for (path,filename) in SearchSub(CONTENT_LOC):
        files = files + ', ' + filename
        with open(os.path.join(path, filename), 'r+', encoding = 'utf-8') as f:
            content = f.read()
            for numrow, row in enumerate(wordlist, start = 1):
                content = re.sub(row[0], row[1], content)
            f.seek(0)
            f.write(content)
            f.truncate()
            f.close()
    print('Replaced texts in files: ', files)

def PreviewReplaceText(wordlist: 'list[list[str]]') -> 'list[list[str]]':
    matches = []
    
    for (path,filename) in SearchSub(CONTENT_LOC):
        with open(os.path.join(path, filename), 'r', encoding = 'utf-8') as f:
            content = f.read()
            for row in wordlist:
                restofcontent = content
                while(restofcontent != None):
                    # <re.Match object; span=(374, 377), match='는….'>
                    found = re.search(row[0], restofcontent)
                    if found:
                        print("found: ", found)
                        foundtext = restofcontent[found.span()[0]: found.span()[1]]
                        foundtextb = restofcontent[max(0,found.span()[0]-5): min(len(restofcontent),
                            found.span()[0])]
                        foundtexta = restofcontent[max(0,found.span()[1]): min(len(restofcontent),
                            found.span()[1]+5)]
                        changedtext = re.sub(row[0], row[1], foundtext)
                        matches.append( (filename,
                            re.sub('\n', '↵', '…'+foundtextb+foundtext+foundtexta+'…'),
                            re.sub('\n', '↵', '…'+foundtextb+changedtext+foundtexta+'…')) )
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

'''def return list of file paths for all text files in a folder, including subfolders'''

# returns list of (dirname, filname) for all .txt files in dirname
def Search(dirname: str):
    filelist = []
    for filename in os.listdir(dirname):
        # full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(filename)[-1]
        if ext == '.txt': 
            filelist.append((dirname,filename))
    return filelist
def SearchSub(path: str):
    filelist = []
    for (path,dir,filenames) in os.walk(path):
        # full_filename = os.path.join(os.path.join(path, dir), filename)
        for filename in filenames:
            ext = os.path.splitext(filename)[-1]
            if ext == '.txt': 
                filelist.append((path,filename))
    return filelist

class TreeBrowser(Frame):
    def __init__(self, master: Frame, columnslist: list, datalist: list) -> None:
        super().__init__(master)
        self.tree = DataTreeview(self, columnslist, datalist)
        verscrollbar = Scrollbar(self, orient ='vertical', command = self.tree.yview)
        horscrollbar = Scrollbar(self, orient = 'horizontal', command = self.tree.xview)
        self.tree.configure(yscrollcommand = verscrollbar.set)
        self.tree.configure(xscrollcommand = horscrollbar.set)
        verscrollbar.pack(side = 'right', fill = 'y')
        horscrollbar.pack(side = 'bottom', fill = 'x')
        self.tree.pack(expand = True, fill = 'both')
    def Update(self, datalist: 'list[list[str]]'):
        self.tree.Update(datalist)


class DataTreeview(Treeview):
    # datalist is a list of rowlists
    def __init__(self, master, columnslist: 'list[str]', datalist: 'list'):
        super().__init__(master)
        self.data = datalist
        self['columns'] = columnslist
        self.column('#0', width=0, stretch=NO)
        self.heading('#0', text='', anchor=CENTER)
        for colname in columnslist:
            self.column(colname, anchor = CENTER, stretch =NO)
            self.heading(colname, text = colname, anchor=CENTER)  
        self.Update(self.data)
    
    def Update(self, datalist: 'list[list[str]]'):
        self.delete(*self.get_children())
        for numrow, row in enumerate(datalist, start = 0):
            self.insert(parent = '', index = numrow, text = '', values = row)
        
    # def selectedItem():
    #     return self.selection()

def LoadSheet():
    global REGEXDATA
    with open(WORKBOOK_PATH, newline = '', encoding = 'utf-8-sig') as f:
        newList = list()
        for line in f:
            if (line == '\r\n' or line == '\n'):
                continue
            else:
                line = re.sub('[\t]+', '\t', line)
                if (line == '\t\r\n' or line == '\t\n'):
                    continue
                newList.append(line)
        print('Loaded workbook: ')
        for change in newList:
            print(change)
        csvReader = csv.reader(newList, delimiter='\t', quoting=csv.QUOTE_NONE)
        REGEXDATA = list(csvReader)
        #print('Loaded workbook: ',REGEXDATA)
    return REGEXDATA

################ Program Start ################

CreateSheet()
LoadSheet()

if __debug__:
    print(GetFileNames(WORKBOOK_LOC))

# Gui
rootwindow = Tk()
rootwindow.title('Bulk Replacer')
rootwindow['bg'] = 'grey'
rootwindow.rowconfigure(0,weight = 0)   # title frame
rootwindow.rowconfigure(1,weight = 3)
rootwindow.rowconfigure(2,weight = 0)
rootwindow.rowconfigure(3,weight = 0)   # bottom frame
rootwindow.columnconfigure(0,weight = 0)
rootwindow.columnconfigure(1,weight = 2)

# frame1 (csv file view)
# frame2 (file browser for *.txt files)
# frame3 (preview changes, run)
frametitle = Frame(master = rootwindow, relief = 'solid')
frame1 = Frame(master = rootwindow)
frame2 = Frame(master = rootwindow)
frame3 = Frame(master = rootwindow)
framebottom = Frame(master = rootwindow)

frametitle.grid(row = 0, column = 0, columnspan = 2, sticky = N, pady = 5)
frame1.grid(row = 1, column = 0, sticky = NSEW)
frame2.grid(row = 2, column = 0, sticky = S+EW)
frame3.grid(row = 1, column = 1, rowspan = 2, sticky = NSEW)
framebottom.grid(row = 3, column = 0, columnspan = 2, pady = 5)

frame1.rowconfigure(0,weight = 0)
frame1.rowconfigure(1,weight = 1)
frame2.columnconfigure(0,weight = 1)
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
tv_keywords = TreeBrowser(frame1, ('RegEx1', 'RegEx2', 'Comment'), REGEXDATA)
btn_createSheet = Button(
    master = frame1,
    text = 'Create Example ' + WORKBOOK_FILENAME,
    command = CreateSheet
)
btn_openSheet = Button(
    master = frame1,
    text = 'Open RegEx Sheet',
    command = OpenSheet
)
btn_reloadSheet = Button(
    master = frame1,
    text = 'Reload RegEx Sheet',
    command = lambda: LoadSheet and tv_keywords.Update(REGEXDATA)
)
btn_createSheet.grid(row = 0, column = 0, pady = 5)
btn_openSheet.grid(row = 0, column = 1, pady = 5)
btn_reloadSheet.grid(row = 0, column = 2, pady = 5)
tv_keywords.grid(row =  1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = NSEW)

# frame2 (file browser for *.txt files)
tv_files = TreeBrowser(frame2, ('Path', 'Filename'), SearchSub(CONTENT_LOC))
btn_files = Button(
    master = frame2,
    text = 'Refresh File List',
    command = lambda: tv_files.Update(SearchSub(CONTENT_LOC))
)
tv_files.grid(row =  0, column = 0, padx = 10, pady = 5, sticky = EW)
tv_files.tree.column(0, anchor=W, width=400)
tv_files.tree.column(1, anchor=E)
btn_files.grid(row =  1, column = 0, padx = 10, pady = 5)


# frame3 (preview changes, run)
lbl_preview = Label(
    master = frame3,
    text = 'What will be changed:')
tv_preview = TreeBrowser(frame3, ('Filename', 'Before', 'After'), PreviewReplaceText(REGEXDATA))
btn_preview = Button(
    master = frame3,
    text = 'Refresh preview window',
    command = lambda: LoadSheet and tv_preview.Update(PreviewReplaceText(REGEXDATA))
)
btn_run = Button(
    master = frame3,
    text = 'Replace in every *.txt files selected',
    command = lambda: ReplaceText(REGEXDATA)
)
lbl_preview.grid(row = 0, column = 0, pady = 5)
btn_preview.grid(row = 0, column = 1, padx = 5)
tv_preview.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 5, sticky = NSEW)
tv_preview.tree.column(0, width = 120, stretch=NO, anchor=W)
tv_preview.tree.column(1, width = 250, minwidth = 150)
tv_preview.tree.column(2, width = 250, minwidth = 150)
btn_run.grid(row = 2, column = 0, pady = 5)


rootwindow.mainloop()








