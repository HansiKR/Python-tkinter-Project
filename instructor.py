from tkinter import *
from tkinter import ttk
from database import Database
from tkinter import messagebox
import login
import sessions
from tkcalendar import *

# creating a database object
db = Database("mainDatabase.db")


class InstructorControls:
    def __init__(self, root):
        self.root = root

        # local variables
        self.stuFName = StringVar()
        self.stuSurName = StringVar()
        self.stuEmail = StringVar()
        self.stuGender = StringVar()
        self.stuDOB = StringVar()
        self.stuTelNo = StringVar()

        # Call the tkinter frames to the window
        self.instructorControlsFrame()
        self.instructorFrameButtons()
        self.tableOutputFrame()

    """Student Info Entries Frame"""

    def instructorControlsFrame(self):
        # Instructor Control Frame Configurations
        self.entriesFrame = Frame(self.root, bg="#5856a0")
        self.entriesFrame.pack(side=TOP, fill=X)
        self.instructor_frame_title = Label(self.entriesFrame, text="Instructor Control Panel",
                                            font=("Goudy old style", 35),
                                            bg="#5856a0",
                                            fg="white")
        self.instructor_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

        # Student First Name
        self.labelFName = Label(self.entriesFrame, text="First Name", font=("Times New Roman", 16, "bold"),
                                bg="#5856a0",
                                fg="white")
        self.labelFName.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtFName = Entry(self.entriesFrame, textvariable=self.stuFName, font=("Times New Roman", 15), width=30)
        self.txtFName.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Student Last Name
        self.labelSName = Label(self.entriesFrame, text="Surname", font=("Times New Roman", 16, "bold"), bg="#5856a0",
                                fg="white")
        self.labelSName.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.txtSName = Entry(self.entriesFrame, textvariable=self.stuSurName, font=("Times New Roman", 15), width=30)
        self.txtSName.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # Student Email
        self.labelEmail = Label(self.entriesFrame, text="Email", font=("Times New Roman", 16, "bold"), bg="#5856a0",
                                fg="white")
        self.labelEmail.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.txtEmail = Entry(self.entriesFrame, textvariable=self.stuEmail, font=("Times New Roman", 15), width=30)
        self.txtEmail.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Student Gender
        self.labelGender = Label(self.entriesFrame, text="Gender", font=("Times New Roman", 16, "bold"), bg="#5856a0",
                                 fg="white")
        self.labelGender.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.comboGender = ttk.Combobox(self.entriesFrame, textvariable=self.stuGender, font=("Times New Roman", 15),
                                        width=28,
                                        state="readonly")
        self.comboGender['values'] = ("Male", "Female", "Other", "Prefer Not to Say")
        self.comboGender.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Student Date of Birth
        self.labelDOB = Label(self.entriesFrame, text="Date of Birth", font=("Times New Roman", 16, "bold"),
                              bg="#5856a0",
                              fg="white")
        self.labelDOB.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entryDOB = DateEntry(self.entriesFrame, setmode='day', date_pattern='dd/mm/yyyy', textvariable=self.stuDOB,
                                  font=("Times New Roman", 12), width=35)
        self.entryDOB.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Student Contact Number
        self.labelTelNo = Label(self.entriesFrame, text="Contact Number", font=("Times New Roman", 16, "bold"),
                                bg="#5856a0",
                                fg="white")
        self.labelTelNo.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.txtTelNo = Entry(self.entriesFrame, textvariable=self.stuTelNo, font=("Times New Roman", 15), width=30)
        self.txtTelNo.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Student Address
        self.labelAddress = Label(self.entriesFrame, text="Address", font=("Times New Roman", 16, "bold"), bg="#5856a0",
                                  fg="white")
        self.labelAddress.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.txtAddress = Text(self.entriesFrame, font=("Times New Roman", 15), width=82, height=5)
        self.txtAddress.grid(row=4, column=1, padx=10, pady=5, sticky="w", columnspan=4)

    """Sub Methods to be used in primary CTA methods"""

    # event trigger Method to display the chosen data from the TreeView back in respective fields
    def getData(self, event):
        try:
            self.selectedRow = self.out.focus()
            self.selectedData = self.out.item(self.selectedRow)
            self.chosenRow = self.selectedData["values"]
            self.stuFName.set(self.chosenRow[1])
            self.stuSurName.set(self.chosenRow[2])
            self.stuEmail.set(self.chosenRow[3])
            self.stuDOB.set(self.chosenRow[4])
            self.stuGender.set(self.chosenRow[5])
            self.stuTelNo.set(self.chosenRow[6])
            self.txtAddress.delete(1.0, END)
            self.txtAddress.insert(END, self.chosenRow[7])
        except IndexError as error:
            pass

    """CTA Methods"""

    # Method to create a new Student
    def regStudent(self):
        if self.txtFName.get() == "" or self.txtTelNo.get() == "" or self.txtSName.get() == "" or self.entryDOB.get() == "" or self.txtEmail.get() == "" or self.comboGender.get() == "" or self.txtAddress.get(
                1.0, END) == "":
            messagebox.showerror("Error!", "Please fill all the fields!")
            return

        db.insertStudent(self.txtFName.get(), self.txtSName.get(), self.txtEmail.get(), self.entryDOB.get(),
                         self.comboGender.get(),
                         self.txtTelNo.get(), self.txtAddress.get(1.0, END))
        messagebox.showinfo("Success!", "Record Successfully Insertered!")
        self.resetForm()
        self.viewStudents()

    # Method to update selected student details
    def updateStudent(self):
        if self.txtFName.get() == "" or self.txtTelNo.get() == "" or self.txtSName.get() == "" or self.entryDOB.get() == "" or self.txtEmail.get() == "" or self.comboGender.get() == "" or self.txtAddress.get(
                1.0, END) == "":
            messagebox.showerror("Error!", "Choose a Student to Update Details!")
            return

        db.editStudent(self.chosenRow[0], self.txtFName.get(), self.txtSName.get(), self.txtEmail.get(),
                       self.entryDOB.get(),
                       self.comboGender.get(), self.txtTelNo.get(), self.txtAddress.get(1.0, END))
        messagebox.showinfo("Success!", "Record Successfully Updated!")
        self.resetForm()
        self.viewStudents()

    # Method to display all students in the Treeview Frame
    def viewStudents(self):
        self.out.delete(*self.out.get_children())  # emptying the table before reloading
        for row in db.viewStudents():
            self.out.insert("", END, values=row)

    # Method to direct to the next Frame to Book a Session
    def bookSession(self):
        try:
            self.tempName = db.selectStudent(self.chosenRow[0])
            self.entriesFrame.destroy()
            self.buttonsFrame.destroy()
            self.tableFrame.destroy()
            sessions.BookSession(self.root, self.tempName)
        except AttributeError as error:
            messagebox.showerror("Error!", "Please View and Select a Student to Book a Session!")

    # Method to reset all input widgets in the frame
    def resetForm(self):
        self.stuFName.set("")
        self.stuSurName.set("")
        self.stuGender.set("")
        self.stuDOB.set("")
        self.stuTelNo.set("")
        self.stuEmail.set("")
        self.txtAddress.delete(1.0, END)

    # Method to redirect to the login frame
    def logOut(self):
        self.entriesFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        login.Login(self.root)

    # CTA Buttons
    def instructorFrameButtons(self):
        # Button Frame Configurations
        self.buttonsFrame = Frame(self.entriesFrame, bg="#5856a0")
        self.buttonsFrame.grid(row=9, column=1, padx=10, pady=10, sticky="w", columnspan=8)

        # Add a new Record
        self.btnAdd = Button(self.buttonsFrame, command=self.regStudent, text="Register Student", bd=0, cursor="hand2",
                             bg="#EADDF7",
                             fg="#5856a0", width=15, font=("Impact", 15))
        self.btnAdd.grid(row=0, column=0, padx=10)

        # Update Selected Record
        self.btnUpdate = Button(self.buttonsFrame, command=self.updateStudent, text="Update Student", bd=0,
                                cursor="hand2",
                                bg="#EADDF7",
                                fg="#5856a0", width=15, font=("Impact", 15))
        self.btnUpdate.grid(row=0, column=1, padx=10)

        # Reset Widget Inputs
        self.btnReset = Button(self.buttonsFrame, command=self.resetForm, text="Reset Form", bd=0, cursor="hand2",
                               bg="#EADDF7", fg="#5856a0", width=10, font=("Impact", 15))
        self.btnReset.grid(row=0, column=3, padx=10)

        # Display List
        self.btnView = Button(self.buttonsFrame, command=self.viewStudents, text="View Students List", bd=0,
                              cursor="hand2",
                              bg="#EADDF7",
                              fg="#5856a0", width=15, font=("Impact", 15))
        self.btnView.grid(row=0, column=2, padx=10)

        # Book a Session
        self.btnBook = Button(self.buttonsFrame, command=self.bookSession, text="Book Session", bd=0, cursor="hand2",
                              bg="#EADDF7",
                              fg="#5856a0", width=15, font=("Impact", 15))
        self.btnBook.grid(row=0, column=4, padx=10)

        # LogOut
        self.btnLogOut = Button(self.entriesFrame, command=self.logOut, text="Log Out", bd=0, cursor="hand2",
                                bg="#EADDF7",
                                fg="#5856a0", width=15, font=("Impact", 15))
        self.btnLogOut.grid(row=0, column=5, padx=20, sticky="e")

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
                             rowheight=70)
        self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")

        # Formatting the output table view
        self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, columns=(1, 2, 3, 4, 5, 6, 7, 8),
                                style="mystyle.Treeview")
        self.out.column("0", width=30)
        self.out.heading("1", text="Index")
        self.out.heading("2", text="First Name")
        self.out.heading("3", text="Last Name")
        self.out.heading("4", text="Email")
        self.out.column("5", width=80)
        self.out.heading("5", text="DOB")
        self.out.column("5", width=100)
        self.out.heading("6", text="Gender")
        self.out.column("6", width=100)
        self.out.heading("7", text="Contact Number")
        self.out.heading("8", text="Address")
        self.out['show'] = 'headings'

        # Virtual Events to trigger methods
        self.out.bind("<ButtonRelease-1>", self.getData)

        # TreeView output layout configurations
        self.out.pack(fill=BOTH)
        self.yScroll.config(command=self.out.yview)
