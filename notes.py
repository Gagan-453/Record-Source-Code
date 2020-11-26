from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pyperclip
from tkinter import font
import about
import sqlite3 as sq
import os
from datetime import *

class new_note:
    def __init__(self):
        self.root = Tk()
        self.root.resizable()
        self.root.title('Untitled - Record')
        self.root.iconbitmap('required/icon.ico')
        self.width = self.root.winfo_screenheight()
        self.height = self.root.winfo_screenwidth()
        self.font_text = open('required/font.txt')
        self.font_size = open('required/size.txt')
        self.font_style = open('required/style.txt')
        self.font_in_text = self.font_text.read()
        self.font_size_in_text = self.font_size.read()
        self.font_style_in_text = self.font_style.read()
        self.font_text.close()
        self.font_size.close()
        self.font_style.close()

        self.t = Text(self.root, width=100, height=30, wrap=NONE, undo=10, font=(self.font_in_text, int(self.font_size_in_text), self.font_style_in_text))
        self.t.propagate(0)
        self.t.pack(side=TOP, fill=X, expand=True)
        self.t.focus_set()
        self.lbl = Label(text='Untitled - Record')
        self.lbl1 = Label(text=0.0)
        self.status = Label(self.root, text='Chars: 0')

        self.s = Scrollbar(self.t, orient=VERTICAL, command=self.t.yview)
        self.t.configure(yscrollcommand=self.s.set)
        self.s.pack(side=RIGHT, fill=Y)

        self.s1 = Scrollbar(self.t, orient=HORIZONTAL, command=self.t.xview)
        self.t.configure(xscrollcommand=self.s1.set)
        self.s1.pack(side=BOTTOM, fill=X)

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.filemenu = Menu(self.root, tearoff=0)
        self.filemenu.add_command(label='New                                Ctrl+N', command=lambda: self.new_file('<Button-1>'))
        self.filemenu.add_command(label='Open                              Ctrl+O', command=lambda: self.open_file('<Button-1>'))
        self.filemenu.add_command(label='Save                               Ctrl+S', command=lambda:self.save_file('<Button-1>'))
        self.filemenu.add_command(label='Save As..', command=lambda: self.save_file('<Button-1>'))
        self.filemenu.add_command(label='Save Secret file             Ctrl+Shift+S', command=self.save_secret_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = Menu(self.root, tearoff=0)
        self.editmenu.add_command(label='Undo                       Ctrl+Z', state=DISABLED)
        self.editmenu.add_command(label='Redo                       Ctrl+Y', state=DISABLED)
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Cut                          Ctrl+X', command=self.cut)
        self.editmenu.add_command(label='Copy                       Ctrl+C', command=self.copy)
        self.editmenu.add_command(label='Paste                       Ctrl+V', command=self.paste)
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Find                         Ctrl+F', command=lambda: self.find('<Button-1>'))
        self.editmenu.add_command(label='Replace                   Ctrl+R', command=lambda: self.replace_text('<Button-1>'))
        self.editmenu.add_command(label='Select All                 Ctrl+A', command=self.select_all)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.formatmenu = Menu(self.root, tearoff=0)
        self.check = IntVar()
        self.formatmenu.add_checkbutton(label='Word Wrap', variable=self.check, command=self.word_wrap)
        self.formatmenu.add_command(label='Font', command=self.font_window)
        self.menubar.add_cascade(label="Format", menu=self.formatmenu)

        self.viewmenu = Menu(self.root, tearoff=0)
        self.status_bar = IntVar()
        self.viewmenu.add_checkbutton(label='Status Bar', variable=self.status_bar, command=self.count_chars)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)

        self.moremenu = Menu(self.root, tearoff=0)
        self.moremenu.add_command(label='Developer..', command=about.Gagan)
        self.moremenu.add_command(label='Encrypt..', command=self.secret_files)
        self.menubar.add_cascade(label='More', menu=self.moremenu)

        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-n>', self.new_file)
        self.root.bind('<Control-f>', self.find)
        self.root.bind('<Control-r>', self.replace_text)
        self.t.bind('<Key>', self.destroy_tags)
        self.t.bind('<Button-1>', self.destroy_tags)
        self.t.bind('<Control-Shift-s>', self.save_secret_file)

        if self.lbl['text'] == 'Untitled - Record':
            self.filemenu.entryconfig(4, state=DISABLED)
        else:
            self.filemenu.entryconfig(4, state=NORMAL)

    def word_wrap(self):
        if self.check.get() == 1:
            self.t.config(wrap=WORD)
        else:
            self.t.config(wrap=NONE)

    def destroy_tags(self, event):
        for tag in self.t.tag_names():
            self.t.tag_delete(tag)


    def open_file(self, event, filename=None):
        if str(self.t.get(0.0, END)).strip() != '':
            self.yesno = messagebox.askquestion('Save on Close', 'Do you want to save the file?')
            if self.yesno == 'yes':
                self.save_file('<Button-1>')
                self.filename = filedialog.askopenfilename(parent=self.root, title='Open',
                                                           filetypes=(('Text documents', '*.txt'), ('All files', '*')))
                if self.filename != None:
                    self.t.delete(0.0, END)
                    self.f = open(self.filename, 'r')
                    self.contents = self.f.read()
                    self.t.insert(END, self.contents)
                    self.f.close()
                    self.root.title(self.filename + ' - Record')
                    self.lbl.config(text=self.filename)

            else:
                self.filename = filedialog.askopenfilename(parent=self.root, title='Open',
                                                           filetypes=(('Text documents', '*.txt'), ('All files', '*')))
                if self.filename != None:
                    self.t.delete(0.0, END)
                    self.f = open(self.filename, 'r')
                    self.contents = self.f.read()
                    self.t.insert(END, self.contents)
                    self.f.close()
                    self.root.title(self.filename+' - Record')
                    self.lbl.config(text=self.filename)

        else:
            self.filename = filedialog.askopenfilename(parent=self.root, title='Open',
                                                       filetypes=(('Text documents', '*.txt'), ('All files', '*')))
            if self.filename != None:
                self.f = open(self.filename, 'r')
                self.contents = self.f.read()
                self.t.insert(END, self.contents)
                self.f.close()
                self.root.title(self.filename + ' - Record')
                self.lbl.config(text=self.filename)

        if filename != None:
            self.t.delete(0.0, END)
            self.file = open(filename, 'r')
            self.c = self.file.read()
            self.t.insert(END, self.c)
            self.file.close()
        else:
            pass

    def save_file(self, event):
        if self.lbl['text'] == 'Untitled - Record':
            self.file = filedialog.asksaveasfilename(parent=self.root, defaultextension='.txt', filetypes=(('Text documents', '*.txt'), ('All files', '*')))

            if self.file != '':
                self.f = open(self.file, 'w')
                self.contents = str(self.t.get(0.0, END))
                self.f.write(self.contents)
                self.f.close()
                self.t.delete(0.0, END)
                self.f = open(self.file, 'r')
                self.contents = self.f.read()
                self.t.insert(END, self.contents)
                self.f.close()
                self.root.title(self.file + ' - Record')
                self.lbl.config(text=self.file)

        else:
            self.loc = self.lbl['text']
            self.f1 = open(self.loc, 'w')
            self.content = str(self.t.get(0.0, END))
            self.f1.write(self.content)
            self.f1.close()

    def new_file(self, event):
        self.yesno = messagebox.askquestion('Save on Close', 'Do you want to save the file?')
        if self.yesno == 'yes':
            self.save_file('<Button-1>')
        self.t.delete(0.0, END)
        self.root.title('Untitled - Record')
        self.lbl.config(text='Untitled - Record')

    def copy(self):
        try:
            self.selected = self.t.get(SEL_FIRST, SEL_LAST)
            pyperclip.copy(self.selected)
        except:
            pass

    def cut(self):
        self.selected = self.t.selection_get()
        self.content = self.t.get(0.0, END)
        pyperclip.copy(self.selected)
        self.content = self.content.replace(self.selected, '')
        self.t.delete(0.0, END)
        self.t.insert(END, self.content)

    def select_all(self):
        self.select = self.t.tag_add("sel", 0.0, END)

    def paste(self):
        self.pos = self.t.index(INSERT)
        self.string = pyperclip.paste()
        self.t.insert(self.pos, self.string)

    def find(self, event):
        self.find_window = Toplevel(self.root, width=350, height=150)
        self.find_window.iconbitmap('required/icon.ico')
        self.find_window.resizable(False, False)
        self.find_window.propagate(0)
        self.find_window.title('Find')
        self.find_what = Entry(self.find_window, width=27)
        self.find_what.place(x=90, y=30)
        self.find_what_lbl = Label(self.find_window, text='Find What:', font=('Calibri', 10))
        self.find_what_lbl.place(x=10, y=30)
        self.find_what.focus()
        self.var = IntVar()
        self.var1 = IntVar()
        self.case = Checkbutton(self.find_window, text="Match Case", variable=self.var)
        self.case.place(x=10, y=120)
        self.find_all = Checkbutton(self.find_window, text="Find all", variable=self.var1)
        self.find_all.place(x=150, y=120)
        self.next = Button(self.find_window, bg='silver', text='Find', width=8, height=0, command=lambda: self.search_for_word(self.find_what, self.var, self.var1))
        self.next.place(x=280, y=40)
        self.cancel = Button(self.find_window, bg='silver', text='Cancel', width=8, height=0, command=self.find_window.destroy)
        self.cancel.place(x=280, y=80)
        self.replace_button = Button(self.find_window, relief=FLAT, cursor='hand2', text='Replace text', width=11, height=1, bg='light blue', fg='dark green', font=('Arial', 13, 'bold'), command=self.find_window.destroy)
        self.replace_button.bind('<Button-1>', self.replace_text)
        self.replace_button.place(x=100, y=80)

    def search_for_word(self, word, case, find_all):
        self.word = word.get()
        self.matchcase = case.get()
        self.find_all = find_all.get()

        for tag in self.t.tag_names():
            self.t.tag_delete(tag)

        self.idxv = self.lbl1['text']
        if self.matchcase == 0 and self.find_all == 0:
            self.find_word = self.t.search(self.word, index=self.idxv, stopindex=END)
            try:
                self.t.tag_add('found', self.find_word, self.find_word+str(len(self.word)))
                self.t.tag_config('found', background='yellow', foreground='dark green')
            except TclError:
                self.lbl1.config(text=0.0)
                self.t.tag_add('found', self.find_word, self.find_word + str(len(self.word)))
                self.t.tag_config('found', background='yellow', foreground='dark green')
            self.idxv = self.find_word + str(len(self.word))
            self.lbl1.config(text=self.idxv)
        elif self.matchcase == 1 and self.find_all == 0:
            self.find_word = self.t.search(self.word, index=0.0, stopindex=END, nocase=True)
            self.t.tag_add('found', self.find_word, self.find_word + str(len(self.word)))
            self.t.tag_config('found', background='yellow', foreground='dark green')
        elif self.matchcase == 0 and self.find_all == 1:
            self.pos = 0.0
            while True:
                self.find_word = self.t.search(self.word, index=self.pos, stopindex=END)
                if not self.find_word:
                    break
                self.a = '{}'.format(len(self.word))
                self.lastidx = self.find_word+self.a
                self.t.tag_add('found', self.find_word, self.lastidx)
                self.pos = self.lastidx
                self.t.tag_config('found', background='yellow', foreground='dark green')

        elif self.matchcase == 1 and self.find_all == 1:
            self.pos = 0.0
            while True:
                self.find_word = self.t.search(self.word, index=self.pos, stopindex=END, nocase=True)
                if not self.find_word:
                    break
                self.a = '{}'.format(len(self.word))
                self.lastidx = self.find_word+self.a
                self.t.tag_add('found', self.find_word, self.lastidx)
                self.pos = self.lastidx
                self.t.tag_config('found', background='yellow', foreground='dark green')

    def replace_text(self, event):
        self.replace_window = Toplevel(self.root, width=350, height=200)
        self.replace_window.propagate(0)
        self.replace_window.title('Replace')
        self.replace_window.iconbitmap('required/icon.ico')
        self.replace_window.resizable(False, False)
        self.find_text = Entry(self.replace_window, width=27)
        self.find_text.place(x=100, y=30)
        self.replace = Entry(self.replace_window, width=27)
        self.replace.place(x=100, y=80)
        self.find_text_lbl = Label(self.replace_window, text='Find text:', font=('Calibri', 12))
        self.find_text_lbl.place(x=10, y=25)
        self.replace_lbl = Label(self.replace_window, text='Replace:', font=('Calibri', 12))
        self.replace_lbl.place(x=10, y=80)
        self.next = Button(self.replace_window, text='Replace all', bg='light green', fg='dark blue', font=('Arial', 12), command=lambda: self.replace_method(self.find_text.get(), self.replace.get()))
        self.next.place(x=50, y=150)
        self.cancel = Button(self.replace_window, text='Cancel', bg='light green', fg='dark blue',
                           font=('Arial', 12), command=self.replace_window.destroy)
        self.cancel.place(x=190, y=150)

    def replace_method(self, find, replacing):
        s = find
        r = replacing
        if (s and r):
            idx = '1.0'
            while 1:
                # searches for desried string from index 1
                idx = self.t.search(s, idx, nocase=1,
                                  stopindex=END)
                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(s))

                self.t.delete(idx, lastidx)
                self.t.insert(idx, r)

                lastidx = '% s+% dc' % (idx, len(r))

                # overwrite 'Found' at idx
                self.t.tag_add('found', idx, lastidx)
                idx = lastidx

                # mark located string as red
            self.t.tag_config('found', foreground='green', background='yellow')

    def font_window(self):
        self.font = Toplevel(self.root, width=500, height=500)
        self.font.propagate(0)
        self.font.title('Font')
        self.font.iconbitmap('required/icon.ico')
        self.font.resizable(False, False)
        self.font_list = list(font.families())
        self.font_list.sort()
        self.lb = Listbox(self.font, font='Arial 10 bold', width=30, fg='black', bg='white', height=10, selectmode=BROWSE)
        self.lb.propagate(0)
        self.lb.place(x=20, y=50)
        self.sb = Scrollbar(self.lb, orient=VERTICAL, command=self.lb.yview)
        self.lb.configure(yscrollcommand=self.sb.set)
        self.sb.pack(side=RIGHT, fill=Y)
        self.view_font = Entry(self.font, width=30, bg='#D9F9EA', fg='dark blue', font=('Arial', 10, 'bold'))
        self.view_font.place(x=20, y=27)
        self.lb.bind('<<ListboxSelect>>', lambda eff: self.change_font(self.lb, self.view_font))

        self.bold = IntVar()
        self.italic = IntVar()
        self.bold_text = Checkbutton(self.font, text="Bold", variable=self.bold, font=('Arial', 12, 'bold'))
        self.bold_text.place(x=300, y=50)
        self.italic_text = Checkbutton(self.font, text="Italic", variable=self.italic, font=('Arial', 12, 'italic'))
        self.italic_text.place(x=300, y=80)

        self.size_var = IntVar()
        self.size = Spinbox(self.font, from_=8, to=30, textvariable=self.size_var, width=9, bg='white', fg='black', font=('Arial', 14, 'bold'))
        self.size.place(x=300, y=180)

        for i in self.font_list:
            self.lb.insert(END, i)

        self.font_var = Label(self.font, text='Font:', font=('Arial', 12, 'underline'))
        self.font_var.place(x=20, y=0)
        self.style_var = Label(self.font, text='Styles:', font=('Arial', 12, 'underline'))
        self.style_var.place(x=300, y=27)
        self.size_variable = Label(self.font, text='Size:', font=('Arial', 12, 'underline'))
        self.size_variable.place(x=300, y=150)


        self.test_font = Button(self.font, text='Test font', width=15, height=1, bg='light blue', fg='dark green', font=('Arial', 13, 'bold'), command=lambda: self.testing_font(self.font, self.view_font.get(), self.size_var.get(), self.bold, self.italic))
        self.test_font.place(x=50, y=450)
        self.save = Button(self.font, text='Save Changes', width=15, height=1, bg='light blue', fg='dark green',
                                font=('Arial', 13, 'bold'), command=lambda: self.save_changes_to_file(self.font, self.view_font.get(), self.size_var.get(), self.bold, self.italic))
        self.save.place(x=300, y=450)

    def change_font(self, box, entry):
        self.index = box.curselection()
        self.font_change = self.lb.get(self.index)
        entry.delete(0, END)
        entry.insert(END, self.font_change)
        f = open('required/font.txt', 'w')
        f.write(self.font_change)
        f.close()

    def testing_font(self, frame, font, size, bold, italic):
        self.bold = bold
        self.italic = italic
        if self.italic.get() == 0 and self.bold.get() == 1:
            self.z = 'bold'
        elif self.italic.get() == 1 and self.bold.get() == 0:
            self.z = 'italic'
        elif self.italic.get() == 1 and self.bold.get() == 1:
            self.z = 'bold italic'
        elif self.italic.get() == 0 and self.bold.get() == 0:
            self.z = ''
        self.test = Text(frame, width=100, height=1, font=(font, size, self.z))
        self.test.place(x=10, y=250)
        self.test.insert(END, 'This is a simple test...')
        self.test.config(state=DISABLED)

    def save_changes_to_file(self, f, font, size, bold, italic):
        self.italic = bold.get()
        self.bold = italic.get()
        self.styles = open('required/style.txt', 'w')
        if self.italic == 0 and self.bold == 1:
            self.styles.write('bold')
            self.xyz = 'bold'
        elif self.italic == 1 and self.bold == 0:
            self.styles.write('italic')
            self.xyz = 'italic'
        elif self.italic == 1 and self.bold == 1:
            self.styles.write('bold italic')
            self.xyz = 'bold italic'
        elif self.italic == 0 and self.bold == 0:
            self.styles.write('')
            self.xyz = ''
        self.styles.close()

        self.sizes = open('required/size.txt', 'w')
        self.sizes.write(str(size))
        self.sizes.close()
        f.destroy()
        self.t.config(font=(font, size, self.xyz))

    def count_chars(self):
        self.status.pack(side=BOTTOM)
        if self.status_bar.get() == 1:
            self._events = ('<KeyPress>',
                            '<KeyRelease>',
                            '<ButtonRelease-1>',
                            '<ButtonRelease-2>',
                            '<ButtonRelease-3>',
                            '<Delete>',
                            '<<Cut>>',
                            '<<Paste>>',
                            '<<Undo>>',
                            '<<Redo>>')
            self.update_char_len(event=None, label=self.status)
            self.bind_events_on_callback(self._events, self.t, lambda eff: self.update_char_len(event=None, label=self.status))
        else:
            self.status.pack_forget()

    def bind_events_on_callback(self, events, widget, callback):
        for _event in events:
            widget.bind(_event, callback)

    def update_char_len(self, event, label):
        self.lines = int(self.t.index('end-1c').split('.')[0])
        label['text'] = 'Chars: ' + str(len(self.t.get('1.0', 'end-1c'))) + '\t\tLines: ' + str(self.lines)

    def secret_files(self):
        self.secret_window = Toplevel(self.root, bg='white', width=500, height=450)
        self.secret_window.propagate(0)
        self.secret_window.title('Encrypt')
        self.secret_window.iconbitmap('required/icon.ico')
        self.heading = Label(self.secret_window, text='Encrypt your file with password', bg='white', fg='#DC3205', font=('Cambria', 15, 'bold'))
        self.heading.pack()
        self.save_as = Entry(self.secret_window, width=24, bg='#D9F9F6', font=('Arial', 13, 'bold'))
        self.save_as.place(x=150, y=80)
        self.save_as_name = Label(self.secret_window, text='Save file as..', bg='white', fg='#050DDC', font=('Times New Roman', 12, 'italic'))
        self.save_as_name.place(x=10, y=80)
        self.save_as.focus()

        self.password = Entry(self.secret_window, width=20, bg='#EDFF6C', fg='#99218D', font=('Arial', 14, 'bold'), show='*')
        self.password.place(x=150, y=150)
        self.password_lbl = Label(self.secret_window, text='Password:', bg='white', fg='#324FB8', font=('Cambria', 13, 'italic'))
        self.password_lbl.place(x=10, y=150)
        self.retype_password = Entry(self.secret_window, width=20, bg='#EDFF6C', fg='#99218D', font=('Arial', 14, 'bold'),
                              show='*')
        self.retype_password.place(x=150, y=230)
        self.retype_password_lbl = Label(self.secret_window, text='Retype Password:', bg='white', fg='#324FB8',
                                  font=('Cambria', 13, 'italic'))
        self.retype_password_lbl.place(x=10, y=230)

        self.remove = IntVar()
        self.remove_file = Checkbutton(self.secret_window, text='Remove file from device', bg='white', variable=self.remove, fg='#128E00', font=('Georgia', 13))
        self.remove_file.select()
        self.remove_file.place(x=220, y=280)

        if self.lbl['text'] == 'Untitled - Record':
            self.remove_file.config(state=DISABLED)
        else:
            self.remove_file.config(state=NORMAL)

        self.save_secret_file = Button(self.secret_window, text='Save File', width=13, bg='#58CBCF', fg='#A80808', font=('Arial', 14, 'bold'), command=lambda: self.save_to_database(self.remove, self.save_as.get(), self.password.get(), self.retype_password.get()))
        self.save_secret_file.place(x=50, y=330)
        self.cancel_save = Button(self.secret_window, text='Cancel', width=13, bg='#58CBCF', fg='#A80808',
                                       font=('Arial', 14, 'bold'), command=self.secret_window.destroy)
        self.cancel_save.place(x=300, y=330)

        self.note = Label(self.secret_window, text="""NOTE you can only open this file from this app using password..
        Click on Secret Files to view all these saved files..""", bg='white', fg='#FF3AFE', font=('Arial', 12, 'italic'))
        self.note.place(x=10, y=400)

        self.filemenu.entryconfig(4, state=NORMAL)


    def save_to_database(self, var, name, password, rpassword):
        if var.get() == 1 and self.lbl['text'] != 'Untitled - Record':
            if os.path.isfile(self.lbl['text']):
                os.remove(self.lbl['text'])
            else:
                pass
        else:
            pass

        if name.strip() == '':
            messagebox.showerror('Error in Saving..', 'Enter a file name')
        elif password.strip() == '':
            messagebox.showerror('Error in Saving..', 'Please enter a strong password')
        elif password != rpassword:
            messagebox.showerror('Error in Saving..', 'Passwords do not match. Try again!')
        else:
            self.conn = sq.connect('database.db')
            self.cursor = self.conn.cursor()
            self.now = datetime.now()
            self.date_and_time = '{}/{}/{} {}:{}'.format(self.now.day, self.now.month, self.now.year, self.now.hour, self.now.minute)
            self.cursor.execute(f'''INSERT INTO YOUR_FILES (FILE, PASSWORD, DATE, CONTENT) VALUES("{name}", "{password}", "{self.date_and_time}", "{self.t.get(0.0, END)}")''')
            self.conn.commit()
            self.conn.close()
            messagebox.showinfo('Success..', 'Successfully saved file..')
            self.secret_window.destroy()
            self.root.title(name + ' - Encrypted file')
            self.lbl.config(text=(name + ' - Encrypted file'))

    def save_secret_file(self):
        self.conn = sq.connect('database.db')
        self.cursor = self.conn.cursor()
        self.name_of_file = self.lbl['text']
        self.update_data = f'''UPDATE YOUR_FILES SET CONTENT = "{self.t.get(0.0, END)}" WHERE FILE = "{self.name_of_file}"'''
        self.cursor.execute(self.update_data)
        self.conn.commit()
        self.conn.close()


                                      
            
if __name__ == '__main__':
    note = new_note()
    note.root.mainloop()