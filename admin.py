from tkinter import *
from tkinter import ttk
from database import Database
from tkinter import messagebox
import login
import sessions

# creating a database object
db = Database("mainDatabase.db")


class AdminControls:
    def __init__(self, root):
        self.root = root

        # local variables
        self.insName = StringVar()
        self.insGender = StringVar()
        self.danceStyles = StringVar()
        self.insTelNo = StringVar()
        self.hrRate = DoubleVar()
        self.avail = StringVar()
        self.uName = StringVar()
        self.pw = StringVar()

        # Days of the week List
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Call the tkinter frames to the window
        self.adminControlsFrame()
        self.adminFrameButtons()
        self.tableOutputFrame()

    """Instructor Info Entries Frame"""

    def adminControlsFrame(self):
        # Admin Control Frame Configurations
        self.entriesFrame = Frame(self.root, bg="#5856a0")
        self.entriesFrame.pack(side=TOP, fill=X)
        self.admin_frame_title = Label(self.entriesFrame, text="Admin Control Panel", font=("Goudy old style", 35),
                                       bg="#5856a0",
                                       fg="white")
        self.admin_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

        # Instructor Name
        self.labelName = Label(self.entriesFrame, text="Name", font=("Times New Roman", 16, "bold"), bg="#5856a0",
                               fg="white")
        self.labelName.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtName = Entry(self.entriesFrame, textvariable=self.insName, font=("Times New Roman", 15), width=30)
        self.txtName.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Instructor Gender
        self.labelGender = Label(self.entriesFrame, text="Gender", font=("Times New Roman", 16, "bold"), bg="#5856a0",
                                 fg="white")
        self.labelGender.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.comboGender = ttk.Combobox(self.entriesFrame, textvariable=self.insGender, font=("Times New Roman", 15),
                                        width=28,
                                        state="readonly")
        self.comboGender['values'] = ("Male", "Female", "Other", "Prefer Not to Say")
        self.comboGender.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # Instructor Dance Style
        self.labelStyles = Label(self.entriesFrame, text="Dance Style", font=("Times New Roman", 16, "bold"),
                                 bg="#5856a0",
                                 fg="white")
        self.labelStyles.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.comboStyle = ttk.Combobox(self.entriesFrame, textvariable=self.danceStyles, font=("Times New Roman", 15),
                                       width=28,
                                       state="readonly")
        self.comboStyle['values'] = db.danceStylesValues()
        self.comboStyle.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Instructor Tel No
        self.labelTelNo = Label(self.entriesFrame, text="Contact Number", font=("Times New Roman", 16, "bold"),
                                bg="#5856a0",
                                fg="white")
        self.labelTelNo.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.txtTelNo = Entry(self.entriesFrame, textvariable=self.insTelNo, font=("Times New Roman", 15), width=30)
        self.txtTelNo.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Instructor Hourly Rate
        self.labelhrRate = Label(self.entriesFrame, text="Hourly Rate", font=("Times New Roman", 16, "bold"),
                                 bg="#5856a0",
                                 fg="white")
        self.labelhrRate.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.txthrRate = Entry(self.entriesFrame, textvariable=self.hrRate, font=("Times New Roman", 15), width=30)
        self.txthrRate.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Instructor Availability
        self.labelAvail = Label(self.entriesFrame, text="Availability", font=("Times New Roman", 16, "bold"),
                                bg="#5856a0",
                                fg="white")
        self.labelAvail.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.comboAvail = ttk.Combobox(self.entriesFrame, textvariable=self.avail, font=("Times New Roman", 15),
                                       width=28,
                                       state="readonly")
        self.comboAvail['values'] = ("AVAILABLE", "NOT AVAILABLE")
        self.comboAvail.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Instructor Working Days
        self.labelListDays = Label(self.entriesFrame, text="Choose Available Days",
                                   font=("Times New Roman", 16, "bold"),
                                   bg="#5856a0",
                                   fg="white")
        self.labelListDays.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.listDays = Listbox(self.entriesFrame, selectmode=MULTIPLE, font=("Times New Roman", 10), width=50,
                                height=7)
        self.listDays.grid(row=4, column=3, columnspan=3, rowspan=6, padx=10, pady=5, sticky="w")

        # Instructor Username
        self.labelUsername = Label(self.entriesFrame, text="Username", font=("Times New Roman", 16, "bold"),
                                   bg="#5856a0",
                                   fg="white")
        self.labelUsername.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.txtUsername = Entry(self.entriesFrame, textvariable=self.uName, font=("Times New Roman", 15), width=30,
                                 bg="#D3D3E7")
        self.txtUsername.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Instructor Password
        self.labelPassword = Label(self.entriesFrame, text="Password", font=("Times New Roman", 16, "bold"),
                                   bg="#5856a0",
                                   fg="white")
        self.labelPassword.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.txtPassword = Entry(self.entriesFrame, textvariable=self.pw, font=("Times New Roman", 15), width=30,
                                 bg="#D3D3E7")
        self.txtPassword.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    """Sub Methods to be used in primary CTA methods"""

    # event trigger Method to display the chosen data from the TreeView back in respective fields
    def getData(self, event):
        try:
            self.selectedRow = self.out.focus()
            self.selectedData = self.out.item(self.selectedRow)
            self.chosenRow = self.selectedData["values"]
            self.insName.set(self.chosenRow[1])
            self.insGender.set(self.chosenRow[2])
            self.danceStyles.set(self.chosenRow[3])
            self.insTelNo.set(self.chosenRow[4])
            self.hrRate.set(self.chosenRow[5])
            self.avail.set(self.chosenRow[6])
            self.selectDays(event)
            self.uName.set(self.chosenRow[8])
            self.pw.set(self.chosenRow[9])
        except IndexError as error:
            pass

    # Event trigger method to display the weekdays depending on the comboBox value
    def selectDays(self, event):
        if self.comboAvail.get() == "NOT AVAILABLE":
            self.listDays.delete(0, END)
        else:
            self.listDays.delete(0, END)  # clearing existing entries before inserting
            for day in self.weekdays:
                self.listDays.insert(END, day)

    # Method to get the selected (available) days from the ListBox Widget
    def getAvailableDays(self):
        self.availDays = []
        for day in self.listDays.curselection():
            # creating a string list from the chosen list indexes
            self.availDays.append(str(self.listDays.get(day)))
        return self.availDays

    """CTA Methods"""

    # Method to create a new Instructor
    def addInstructor(self):
        if self.txtName.get() == "" or self.txtTelNo.get() == "" or self.comboAvail.get() == "" or self.comboStyle.get() == "" or self.txthrRate.get() == "" or self.comboGender.get() == "" or self.txtUsername.get() == "" or self.txtPassword.get() == "":
            messagebox.showerror("Error!", "Please fill all the fields!")
            return

        self.tempAvailDays = ', '.join(self.getAvailableDays())  # converting the list of Days into a string

        db.insertInstructor(self.txtName.get(), self.comboGender.get(), self.comboStyle.get(), self.txtTelNo.get(),
                            self.txthrRate.get(), self.comboAvail.get(), self.tempAvailDays,
                            self.txtUsername.get(), self.txtPassword.get())
        messagebox.showinfo("Success!", "Record Successfully Insertered!")
        self.resetForm()
        self.viewInstructor()

    # Method to update selected Instructor details
    def assignInstructor(self):
        if self.txtName.get() == "" or self.txtTelNo.get() == "" or self.comboAvail.get() == "" or self.comboStyle.get() == "" or self.txthrRate.get() == "" or self.comboGender.get() == "" or self.txtUsername.get() == "" or self.txtPassword.get() == "":
            messagebox.showerror("Error!", "Choose an Instructor to Update Details!")
            return

        self.tempAvailDays = ', '.join(self.getAvailableDays())  # converting the list of Days into a string

        try:
            db.editInstructor(self.chosenRow[0], self.txtName.get(), self.comboGender.get(), self.comboStyle.get(),
                              self.txtTelNo.get(),
                              self.txthrRate.get(), self.comboAvail.get(), self.tempAvailDays,
                              self.txtUsername.get(), self.txtPassword.get())
            messagebox.showinfo("Success!", "Record Successfully Updated!")
            self.resetForm()
            self.viewInstructor()
        except AttributeError as error:
            messagebox.showerror("Error!", "Choose an existing Instructor to Update Details")

    # Method to remove selected instructor from the database
    def dltInstructor(self):
        try:
            db.removeInstructor(self.chosenRow[0])
            self.resetForm()
            self.viewInstructor()
        except AttributeError as error:
            messagebox.showerror("Error!", "Please Choose an Instructor Record to Remove!")

    # Method to display all instructors in the Treeview Frame
    def viewInstructor(self):
        self.out.delete(*self.out.get_children())  # emptying the table before reloading
        for row in db.viewInstructor():
            self.out.insert("", END, values=row)

    # Method to direct to the next Frame to Assign Instructors
    def manageSessions(self):
        self.entriesFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        sessions.AssignSession(self.root)

    # Method to reset all input widgets in the frame
    def resetForm(self):
        self.insName.set("")
        self.insGender.set("")
        self.danceStyles.set("")
        self.insTelNo.set("")
        self.hrRate.set("")
        self.avail.set("")
        self.listDays.delete(0, END)
        self.uName.set("")
        self.pw.set("")

    # Method to redirect to the login frame
    def logOut(self):
        self.entriesFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        login.Login(self.root)

    """CTA Buttons Frame"""

    def adminFrameButtons(self):
        # Button Frame Configurations
        self.buttonsFrame = Frame(self.entriesFrame, bg="#5856a0")
        self.buttonsFrame.grid(row=10, column=0, padx=10, pady=10, sticky="w", columnspan=8)

        # Add a new Record
        self.btnAdd = Button(self.buttonsFrame, command=self.addInstructor, text="Add Instructor", bd=0, cursor="hand2",
                             bg="#EADDF7",
                             fg="#5856a0", width=20, font=("Impact", 15))
        self.btnAdd.grid(row=0, column=0, padx=10)

        # Update Selected Record
        self.btnUpdate = Button(self.buttonsFrame, command=self.assignInstructor, text="Update Instructor", bd=0,
                                cursor="hand2",
                                bg="#EADDF7",
                                fg="#5856a0", width=20, font=("Impact", 15))
        self.btnUpdate.grid(row=0, column=1, padx=10)

        # Delete Selected Record
        self.btnDlt = Button(self.buttonsFrame, command=self.dltInstructor, text="Remove Instructor", bd=0,
                             cursor="hand2",
                             bg="#EADDF7",
                             fg="#5856a0", width=20, font=("Impact", 15))
        self.btnDlt.grid(row=0, column=2, padx=10)

        # Reset Widget Inputs
        self.btnReset = Button(self.buttonsFrame, command=self.resetForm, text="Reset Form", bd=0, cursor="hand2",
                               bg="#EADDF7", fg="#5856a0", width=20, font=("Impact", 15))
        self.btnReset.grid(row=0, column=3, padx=10)

        # Display List
        self.btnView = Button(self.buttonsFrame, command=self.viewInstructor, text="View Instructor List", bd=0,
                              cursor="hand2",
                              bg="#EADDF7",
                              fg="#5856a0", width=20, font=("Impact", 15))
        self.btnView.grid(row=0, column=4, padx=10)

        # Manage Sessions
        self.btnManageSess = Button(self.buttonsFrame, command=self.manageSessions, text="Manage Sessions", bd=0,
                                    cursor="hand2",
                                    bg="#EADDF7", fg="#5856a0", width=20, font=("Impact", 15))
        self.btnManageSess.grid(row=0, column=5, padx=10)

        # LogOut
        self.btnLogOut = Button(self.entriesFrame, command=self.logOut, text="Log Out", bd=0, cursor="hand2",
                                bg="#EADDF7",
                                fg="#5856a0", width=15, font=("Impact", 15))
        self.btnLogOut.grid(row=0, column=6, padx=15, sticky="e")

    """Table Frame using TreeView"""

    def tableOutputFrame(self):
        # Treeview Frame Configurations
        self.tableFrame = Frame(self.root, bg="#DADDE6")
        self.tableFrame.place(x=0, y=400, width=1400, height=560)
        self.yScroll = Scrollbar(self.tableFrame)
        self.yScroll.pack(side=RIGHT, fill=Y)

        # ttk style object to add configurations
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", font=('Calibri', 12),
                             rowheight=50)
        self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")

        # Formatting the output table view
        self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set,
                                columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), style="mystyle.Treeview")
        self.out.heading("1", text="Index")
        self.out.column("1", width=10)
        self.out.heading("2", text="Name")
        self.out.column("2", width=30)
        self.out.heading("3", text="Gender")
        self.out.column("3", width=5)
        self.out.heading("4", text="Dance Styles")
        self.out.column("4", width=8)
        self.out.heading("5", text="Tel Number")
        self.out.column("5", width=10)
        self.out.heading("6", text="Hourly Rate")
        self.out.column("6", width=6)
        self.out.heading("7", text="Availability")
        self.out.column("7", width=5)
        self.out.heading("8", text="Available Days")
        self.out.heading("9", text="Username")
        self.out.column("9", width=3)
        self.out.heading("10", text="Password")
        self.out.column("10", width=3)
        self.out['show'] = 'headings'

        # Virtual Events to trigger methods
        self.out.bind("<ButtonRelease-1>", self.getData)
        self.comboAvail.bind("<<ComboboxSelected>>", self.selectDays)

        # TreeView output layout configurations
        self.out.pack(fill=X)
        self.yScroll.config(command=self.out.yview)
