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
# os.path.dirname(os.path.abspath(__file__)) gives you location of python script EX)  d:\Users\Favmir\Documents\GitHub\BulkTextReplace\src
# __file__ doesn't work when you run python script from IDLE


CONTENT_LOC = os.path.dirname(os.path.abspath(__file__))
WORKBOOK_LOC = os.path.dirname(os.path.abspath(__file__))
WORKBOOK_FILENAME = 'BulkReplacer_List.csv'
WORKBOOK_PATH =  os.path.join(WORKBOOK_LOC, WORKBOOK_FILENAME)
REGEXDATA = []
EXTENSION = 'txt'
FILELIST = []


# dialect: delimiter='\t', quotechar = '\x07', quoting = csv.QUOTE_NONE

def GetFilesFull():
    list = glob.glob('*.' + EXTENSION)
    for filename in list:
        filename = os.path.join(CONTENT_LOC, filename)
    return list

def GetFilesSeparate() -> list[list[str]]:
    global FILESLIST
    FILELIST.clear()
    for dirpath, dnames, fnames in os.walk(CONTENT_LOC):
        for f in fnames:
            if f.endswith("."+EXTENSION):
                FILELIST.append([dirpath+'\\', f])
                #EXTENSION(os.path.join(dirpath, f))
    return FILELIST

# returns list of full path for all .EXTENSION files in current folder
def GetFileNames(mypath: str):
    # filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    filenames = glob.glob(mypath + '\*.'+EXTENSION)
    return filenames

# returns list of (dirname, filname) for all .EXTENSION files in dirname
def GetPathAndName():
    global EXTENSION
    filelist = []
    filenames = os.listdir(CONTENT_LOC)
    for filename in filenames:
        # full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(filename)[-1]
        if ext == '.'+EXTENSION:
            filelist.append((CONTENT_LOC,filename))
            print(filelist)
    return filelist

def CreateSheet():
    if(os.path.exists(WORKBOOK_PATH)):
        print(WORKBOOK_FILENAME,' already exists, skipping file creation')
        pass
    else:
        f = open(WORKBOOK_PATH, 'w', newline = '', encoding='utf-8-sig')
        writer = csv.writer(f, delimiter='\t', quoting = csv.QUOTE_NONE)
        #writer.writerow(('sep=',''))   # this line is for excel to recognize the file as tab delimited;
        writer.writerow(('hell', 'heck','hell will be replaced with heck(not capitalized)'))
        writer.writerow(('([hH])ell', '\\1eck','using RegEx to turn \'hell\' into \'heck\', and \'Hell\' into \'Heck\''))
        writer.writerow(('안녕하세요','Hello','Korean to English'))
        f.close

def OpenSheet():
    os.startfile(WORKBOOK_PATH)

def ReplaceText(wordlist: 'list[list[str]]'):
    files = ''
    for filename in GetFilesFull():
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
    replaceList = [
        ['\t','␉'],
        ['\n','␤'],
        [' ',' ␣ ']  # also could use ⎵  ⌫  ␠
        ]
    for row in replaceList:
        word = re.sub(row[0], row[1], word)
    return word

def PreviewReplaceText(wordlist: list[list[str]]) -> list[list[str]]:
    files = ''
    matches = []
    ellipsisLen = 5
    for filename in GetFilesFull():
        print('Previewing file: ', filename)
        files = files + ', ' + filename
        with open(filename, 'r', encoding = 'utf-8') as f:
            content = f.read()
            for row in wordlist:
                restofcontent = content
                while(restofcontent != None):
                    # <re.Match object; span=(374, 377), match='는….'>
                    found = re.search(row[0], restofcontent)
                    if found:
                        print("found: ", found)
                        foundtext = restofcontent[found.span()[0]: found.span()[1]]
                        foundtextb = restofcontent[max(0,found.span()[0]-ellipsisLen): min(len(restofcontent),
                            found.span()[0])]
                        foundtexta = restofcontent[max(0,found.span()[1]): min(len(restofcontent),
                            found.span()[1]+ellipsisLen)]
                        changedtext = re.sub(row[0], row[1], foundtext)
                        matches.append( (filename, ReplaceSpecialChars('… '+foundtextb+foundtext+foundtexta+' …'), ReplaceSpecialChars('… '+foundtextb+changedtext+foundtexta+' …'), row[2]) )
                        
                        #content = restofcontent[0:found.span()[0]] + changedtext + restofcontent[found.span()[1]:] # apply change for next regex

                        restofcontent = restofcontent[found.span()[1]:]
                        
                    else:
                        print("found no more ", row[0])
                        restofcontent = None
                        content = re.sub(row[0], row[1], content) # apply change for next regex
                        
            f.close()
    return matches

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
        
    def on_double_click(self, event):
        region = self.tree.identify('region', event.x, event.y)

        if region != 'heading':
            #print('column ' + str(self.tree.identify_column(event.x)))
            # print content of cell for copy&paste
            print( self.tree.item(self.tree.focus())['values'][int(self.tree.identify_column(event.x)[1:])-1])
            
            
        

class DataTreeview(Treeview):
    # datalist is a list of rowlists
    def __init__(self, master, columnslist: 'list[str]', datalist: 'list'):
        super().__init__(master)
        self.data = datalist
        self.configure(height=10)   # height: number of minimum rows to show per tree
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
        regList = list()
        #next(f) #skip the first line with 'sep= '
        
        for line in f:
            #check if the current line has no tabs
            #if so, ignore the line
            if(line.count('\t') == 0):
                print('No tab found, ignoring following line: ',line)
                continue
            line = re.sub('[\t]+','\t',line)
            #insert third column when there's only two columns
            line = re.sub('^([^\t]+)\t([^\r\n\t]+)([\r\n]+)$', '\\1\t\\2\t\\3', line)
            regList.append(line)
        #print(newList)
        csvReader = csv.reader(regList, delimiter='\t', quoting=csv.QUOTE_NONE)
        REGEXDATA = list(csvReader)
        print('Loaded workbook: ',REGEXDATA)
    return REGEXDATA

def UpdateExt():
    global EXTENSION
    EXTENSION = ext_input.get()
    print('Updated extension: ', EXTENSION)

################ Program Start ################

CreateSheet()
LoadSheet()

# Gui
rootwindow = Tk()
rootwindow.title('Bulk Replacer')
default_font = tkinter.font.nametofont("TkDefaultFont")
default_font.config(family= 'Noto Sans', size = 10)
rootwindow['bg'] = 'grey'
rootwindow.rowconfigure(0,weight = 0)   # title frame
rootwindow.rowconfigure(1,weight = 3)
rootwindow.rowconfigure(2,weight = 0)
rootwindow.rowconfigure(3,weight = 0)   # bottom frame
rootwindow.columnconfigure(0,weight = 0)
rootwindow.columnconfigure(1,weight = 2)

TreesStyle=Style()
TreesStyle.configure("Treeview", font=('Noto Sans', 15), rowheight=30)

# frame1 (csv file view)
# frame2 (file browser for *.EXTENSION files)
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

def refreshTV():
    tv_keywords.Update(REGEXDATA)
    tv_files.Update(GetFilesSeparate())
    tv_preview.Update(PreviewReplaceText(REGEXDATA))

# top frame
lbl_title = Label(
    master = frametitle,
    text = 'RegEx Bulk Replacer',
    font = ("Verdana", 20, "bold"),
    background = 'grey')
lbl_title.pack()

# frame1 (csv file view)
tv_keywords = TreeBrowser(frame1, ('RegEx1', 'RegEx2', 'Comment'), REGEXDATA)
tv_keywords.tree.bind("<Double-1>", tv_keywords.on_double_click)
btn_createSheet = Button(
    master = frame1,
    text = 'Create ' + WORKBOOK_FILENAME,
    command = CreateSheet
)
btn_openSheet = Button(
    master = frame1,
    text = 'Open RegEx Sheet',
    command = OpenSheet
)
def refresh_sheet():
    LoadSheet()
    refreshTV()
btn_reloadSheet = Button(
    master = frame1,
    text = 'Reload RegEx Sheet',
    command = refresh_sheet
)
btn_createSheet.grid(row = 0, column = 0, pady = 5)
btn_openSheet.grid(row = 0, column = 1, pady = 5)
btn_reloadSheet.grid(row = 0, column = 2, pady = 5)
tv_keywords.grid(row =  1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = NSEW)

# frame2 (file browser for *.EXTENSION files)
def character_limit(entry_text):
    if len(entry_text.get()) > 4:
        entry_text.set(entry_text.get()[:5])
tv_files = TreeBrowser(frame2, ('Path', 'Filename'), GetFilesSeparate())
tv_files.tree.bind("<Double-1>", tv_files.on_double_click)
ext_desc = Label(frame2, text = 'Input File Extension:')
entry_text = StringVar()
ext_input = Entry(frame2, width = 10, textvariable=entry_text)
ext_input.insert(END, 'txt')
def refresh_file():
    UpdateExt()
    refreshTV()
btn_files = Button(
    master = frame2,
    text = 'Refresh File List',
    command = refresh_file
)

tv_files.grid(row =  0, column = 0, columnspan=3, padx = 10, pady = 5, sticky = EW)
tv_files.tree.column(0, anchor=W, width=400)
tv_files.tree.column(1, anchor=E)

ext_desc.grid(row = 1, column = 0, sticky = E)
ext_input.grid(row =  1, column = 1, padx = 10, pady = 5)
entry_text.trace("w", lambda *args: character_limit(entry_text))
btn_files.grid(row =  1, column = 2, padx = 10, pady = 5)


# frame3 (preview changes, run)
lbl_preview = Label(
    master = frame3,
    text = 'What will be changed:')
tv_preview = TreeBrowser(frame3, ('Filename', 'Before', 'After', 'Comment'), PreviewReplaceText(REGEXDATA))
tv_preview.tree.bind("<Double-1>", tv_preview.on_double_click)
btn_preview = Button(
    master = frame3,
    text = 'Refresh preview window',
    command = lambda: LoadSheet and refreshTV()
)
btn_run = Button(
    master = frame3,
    text = 'Replace in every files selected',
    command = lambda: ReplaceText(REGEXDATA) and refreshTV()
)
lbl_preview.grid(row = 0, column = 0, pady = 5)
btn_preview.grid(row = 0, column = 1, padx = 5)
tv_preview.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 5, sticky = NSEW)
tv_preview.tree.column(0, width = 120, stretch=NO, anchor=W)
tv_preview.tree.column(1, width = 250, minwidth = 150)
tv_preview.tree.column(2, width = 250, minwidth = 150)
tv_preview.tree.column(3, width = 200, minwidth = 100)
btn_run.grid(row = 2, column = 0, pady = 5)


rootwindow.mainloop()
