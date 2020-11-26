from tkinter import *
import sqlite3 as sq
import os
from notes import *

class view_files:
    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Quick Access')
        self.root.iconbitmap('required/icon.ico')
        self.f = Frame(self.root, width=550, height=350, bg='white')
        self.f.propagate(0)
        self.f.pack()

        self.secret = Button(self.f, text='Secret Files', width=15, height=1, cursor='hand2', bg='#B4FB84', fg='#2628F5', font=('Arial', 12, 'bold'), command=self.view_secret_files)
        self.secret.place(x=20, y=300)

        self.open_pad = Button(self.f, text='Open Notes', width=15, height=1, cursor='hand2', bg='#B4FB84',
                             fg='#2628F5', font=('Arial', 12, 'bold'), command=self.open_notes)
        self.open_pad.place(x=200, y=300)

        self.home = Button(self.f, text='Home', width=15, height=1, cursor='hand2', bg='#B4FB84',
                             fg='#2628F5', font=('Arial', 12, 'bold'))
        self.home.place(x=380, y=300)

        self.txt_files = []
        self.buttons = []


        self.current_dir = os.getcwd()
        d = self.current_dir
        for path in os.listdir(d):
            full_path = os.path.join(d, path)
            if os.path.isfile(full_path):
                if full_path.endswith(('.txt', '.py', '.htm', '.html')):
                    self.txt_files.append(full_path)

        self.lth = len(self.txt_files)

        if self.lth > 10:
            while self.lth != 10:
                self.txt_files.pop()
                self.lth -= 1

        for i in self.txt_files:
            self.files = Button(self.f, text=i, width=200, bg='white', activebackground='light blue',fg='black', relief=FLAT, anchor=W)
            self.files.pack(fill=Y)
            self.files['command'] = lambda btn=self.files, file=i: self.active_file(btn, file, self.buttons)
            self.buttons.append(self.files)

        if len(self.txt_files) == 0:
            self.no_files = Label(self.f, text='No files found or can\'t open files with "Record"..', bg='white', fg='black')
            self.no_files.pack()



    def active_file(self, button, file, buttons, db=None):
        self.buttons = buttons
        for i in self.buttons:
            i['bg'] = 'white'
        button['bg'] = 'light blue'

        if db == None:
            button.bind('<Double-Button>', lambda eff: self.opening(filename=file))
        else:
            button.bind('<Double-Button>', lambda eff: self.opening(dbfile=db))


    def opening(self, filename=None, dbfile=None):
        self.root.destroy()
        self.pad = new_note()
        if filename != None:
            self.f = open(filename, 'r')
            self.content = self.f.read()
            self.f.close()
            self.pad.t.insert(END, self.content)
            self.pad.root.title(filename)
            self.pad.lbl.config(text=filename)
        else:
            self.pad.t.bind('<Control-Shift-s>', self.pad.filemenu[0].invoke())
            self.conn = sq.connect('database.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute(f'''SELECT CONTENT FROM YOUR_FILES WHERE FILE = "{dbfile[0]}"''')
            self.sa = self.cursor.fetchall()
            self.sa = self.sa[0][0]
            self.pad.t.insert(END, self.sa)
            self.pad.root.title(dbfile[0] + ' - Encrypted File')
            self.pad.filemenu.entryconfig(4, state=NORMAL)
            self.pad.lbl.config(text=dbfile[0].strip())

    def open_notes(self):
        self.root.destroy()
        self.o = new_note()


    def view_secret_files(self):
        self.f1 = Text(self.root, width=68, height=17, bg='white', state=DISABLED, cursor='arrow')
        self.f1.propagate(0)
        self.f1.place(x=0, y=0)
        self.sb = Scrollbar(self.f1, orient=VERTICAL, command=self.f1.yview)
        self.f1.configure(yscrollcommand=self.sb.set)
        self.sb.pack(side=RIGHT, fill=Y)
        self.secret.config(text='Back', command=lambda: self.back_to_files(self.f1))

        self.conn = sq.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT FILE FROM YOUR_FILES')
        self.sa = self.cursor.fetchall()


        self.heading = Label(self.f1, text='Private Files', bg='white', fg='red', font=('Cambria', 14, 'bold'))
        self.heading.pack()

        self.sbuttons = []
        for i in self.sa:
            self.sfiles = Button(self.f1, text=i, width=200, cursor='hand2', bg='white', activebackground='light blue', fg='black',
                                relief=FLAT, anchor=W, font=('Calibri', 12))
            self.sfiles.pack(fill=Y)
            self.sbuttons.append(self.sfiles)
            self.sfiles['command'] = lambda btn=self.sfiles, file=i: self.active_file(btn, None, self.sbuttons, db=file)

    def back_to_files(self, f):
        f.destroy()
        self.secret.config(text='Secret Files', command=self.view_secret_files)


if __name__ == '__main__':
    a = view_files()
    a.root.mainloop()