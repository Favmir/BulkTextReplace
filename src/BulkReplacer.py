######|| BulkReplacer Program ||######
# Replaces text across multiple files via RegEx
# Version 5(2022/10/06)
# Author: FavmirY@gmail.com
# CSV Sheet file uses '\t' as delimiter. You can use multiple tabs to separate columns.
# don't put empty lines in CSV file.
# .txt files getting replaced should be 'utf-8'
# always use \n for regex newline, not \r\n.

import re
import glob
from tkinter import *
from tkinter.ttk import *
import tkinter.font
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
    for filename in glob.glob('*.txt'):
        files = files + ', ' + filename
        with open(os.path.join(CONTENT_LOC, filename), 'r+', encoding = 'utf-8') as f:
            content = f.read()
            for numrow, row in enumerate(wordlist, start = 1):
                content = re.sub(row[0], row[1], content)
            f.seek(0)
            f.write(content)
            f.truncate()
            f.close()
    print('Replaced texts in files: ', files)

def ReplaceSpecialChars(word: str) -> str:
	replaceList =[	['\t','␉'],
                    ['\n','␤'],
				'''	['','␀'],
					['','␁'],
					['','␂'],
					['','␃'],
					['','␄'],
					['','␅'],
					['','␆'],
					['','␇'],
					['','␈'],
					['\n','␊'], # python uses universal newline to reduce OS dependency
					['','␋'],
					['','␌'],
					['\r','␍'], # python automatically converts \r\n to \n when reading file so this does nothing
					['','␎'],
					['','␏'],
					['','␐'],
					['','␑'],
					['','␒'],
					['','␓'],
					['','␔'],
					['','␕'],
					['','␖'],
					['','␗'],
					['','␘'],
					['','␙'],
					['','␚'],
					['','␛'],
					['','␜'],
					['','␝'],
					['','␞'],
					['','␟'],
					['','␠'],
					['','␡'],
					['','␣'],
					['','␤'],'''
					]
	for numrow, row in enumerate(replaceList, start = 1):
		word = re.sub(row[0], row[1], word)
	return word

def PreviewReplaceText(wordlist: 'list[list[str]]') -> 'list[list[str]]':
    files = ''
    matches = []
    for filename in glob.glob('*.txt'):
        files = files + ', ' + filename
        with open(os.path.join(CONTENT_LOC, filename), 'r', encoding = 'utf-8') as f:
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
                        matches.append( (filename, ReplaceSpecialChars('…'+foundtextb+foundtext+foundtexta+'…'), ReplaceSpecialChars('…'+foundtextb+changedtext+foundtexta+'…')) )
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
def Search(dirname: str):
    filelist = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        # full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(filename)[-1]
        if ext == '.txt': 
            filelist.append((dirname,filename))
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
        self.configure(height=10)   # number of minimum rows to show per tree
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
            newList.append(re.sub('[\t]+','\t',line))
        #print(newList)
        csvReader = csv.reader(newList, delimiter='\t', quoting=csv.QUOTE_NONE)
        REGEXDATA = list(csvReader)
        print('Loaded workbook: ',REGEXDATA)
    return REGEXDATA

################ Program Start ################

CreateSheet()
LoadSheet()

if __debug__:
    print(GetFileNames(WORKBOOK_LOC))

# Gui
rootwindow = Tk()
rootwindow.title('Bulk Replacer')
default_font = tkinter.font.nametofont("TkDefaultFont")
default_font.config(family='Noto Sans KR', size = 12)
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
#btn_reloadSheet.grid(row = 0, column = 2, pady = 5)
tv_keywords.grid(row =  1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = NSEW)

# frame2 (file browser for *.txt files)
tv_files = TreeBrowser(frame2, ('Path', 'Filename'), Search(CONTENT_LOC))
btn_files = Button(
    master = frame2,
    text = 'Refresh File List',
    command = lambda: tv_files.Update(Search(CONTENT_LOC))
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








