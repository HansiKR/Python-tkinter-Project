from tkinter import *
from tkinter import ttk
from tkcalendar import *
from datetime import *
import admin
import instructor
from database import Database
from tkinter import messagebox

# creating a database object
db = Database("mainDatabase.db")


class BookSession:
    def __init__(self, root, stname):
        self.root = root
        self.tempName = stname

        # local variables
        self.studentName = StringVar()
        self.danceStyle = StringVar()
        self.sessDate = StringVar()
        self.sessDay = StringVar()
        self.maxRate = DoubleVar()

        # automatically set the student name when making bookings
        self.studentName.set(self.tempName)

        # Call the tkinter frames to the window
        self.instructorSessionsFrame()
        self.sessionsFrameButtons()
        self.tableOutputFrame()

    """Session Details Frame"""

    def instructorSessionsFrame(self):
        # Instructor Sessions Frame Configurations
        self.sessionFrame = Frame(self.root, bg="#5856a0")
        self.sessionFrame.pack(side=TOP, fill=X)
        self.session_frame_title = Label(self.sessionFrame, text="Session Control Panel", font=("Goudy old style", 35),
                                         bg="#5856a0",
                                         fg="white")
        self.session_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

        # Student Full Name
        self.labelStName = Label(self.sessionFrame, text="Student Name", font=("Times New Roman", 16, "bold"),
                                 bg="#5856a0",
                                 fg="white")
        self.labelStName.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtStName = Entry(self.sessionFrame, textvariable=self.studentName, font=("Times New Roman", 15), width=30,
                               state="readonly")
        self.txtStName.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Session Date
        self.labelSessDate = Label(self.sessionFrame, text="Session Date", font=("Times New Roman", 16, "bold"),
                                   bg="#5856a0",
                                   fg="white")
        self.labelSessDate.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entrySessDate = DateEntry(self.sessionFrame, setmode='day', date_pattern='dd/mm/yyyy',
                                       textvariable=self.sessDate, mindate=datetime.now(), font=("Times New Roman", 12),
                                       width=35)
        self.entrySessDate.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Session Day
        self.labelSessDay = Label(self.sessionFrame, text="Session Day", font=("Times New Roman", 16, "bold"),
                                  bg="#5856a0",
                                  fg="white")
        self.labelSessDay.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entrySessDay = Entry(self.sessionFrame, textvariable=self.sessDay, font=("Times New Roman", 15), width=30,
                                  state="readonly")
        self.entrySessDay.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Student Dance Style
        self.labelStyle = Label(self.sessionFrame, text="Dance Style", font=("Times New Roman", 16, "bold"),
                                bg="#5856a0",
                                fg="white")
        self.labelStyle.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.comboStyle = ttk.Combobox(self.sessionFrame, textvariable=self.danceStyle, font=("Times New Roman", 15),
                                       width=28,
                                       state="readonly")
        self.comboStyle['values'] = db.danceStylesValues()
        self.comboStyle.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Student's Max Rate Payable
        self.labelMaxRate = Label(self.sessionFrame, text="Max Rate", font=("Times New Roman", 16, "bold"),
                                  bg="#5856a0",
                                  fg="white")
        self.labelMaxRate.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.txtMaxRate = Entry(self.sessionFrame, textvariable=self.maxRate, font=("Times New Roman", 15), width=30)
        self.txtMaxRate.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    """Sub Methods to be used in primary CTA methods"""

    # event trigger Method to display the chosen data from the TreeView back in respective fields
    def getData(self, event):
        try:
            self.selectedRow = self.out.focus()
            self.selectedData = self.out.item(self.selectedRow)
            self.chosenRow = self.selectedData["values"]
            self.studentName.set(self.chosenRow[1])
            self.danceStyle.set(self.chosenRow[2])
            self.sessDate.set(self.chosenRow[3])
            self.sessDay.set(self.chosenRow[4])
            self.maxRate.set(self.chosenRow[5])
        except IndexError as error:
            pass

    # Method to redirect to the previous frame
    def GoBack(self):
        self.sessionFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        instructor.InstructorControls(self.root)

    # getting the selected weekday by creating a datetime object from the str variable
    def getDay(self, event):
        weekDayObj = datetime.strptime(self.entrySessDate.get(), '%d/%m/%Y')
        weekday = weekDayObj.strftime('%A')
        self.sessDay.set(weekday)

    """CTA Methods"""

    # Method to create a new session
    def addSession(self):
        if self.txtStName.get() == "" or self.comboStyle.get() == "" or self.entrySessDate.get() == "" or self.txtMaxRate.get() == "":
            messagebox.showerror("Error!", "Please fill all the fields!")
            return

        db.insertSession(self.txtStName.get(), self.comboStyle.get(), self.entrySessDate.get(), self.sessDay.get(),
                         self.txtMaxRate.get(), " ")
        messagebox.showinfo("Success!", "Session Successfully Booked!")
        self.viewSessions()

    # Method to view all sessions
    def viewSessions(self):
        self.out.delete(*self.out.get_children())  # emptying the treeview before reloading
        for row in db.viewSessionList():
            self.out.insert("", END, values=row)

    # Method to update the chosen Session Details
    def updateSession(self):
        if self.txtStName.get() == "" or self.comboStyle.get() == "" or self.entrySessDate.get() == "" or self.txtMaxRate.get() == "":
            messagebox.showerror("Error!", "Please a Session to Update Details!")
            return

        db.updateSession(self.chosenRow[0], self.txtStName.get(), self.comboStyle.get(), self.entrySessDate.get(),
                         self.sessDay.get(),
                         self.txtMaxRate.get(), " ")
        messagebox.showinfo("Success!", "Session Details Successfully Updated!")
        self.viewSessions()

    """CTA Buttons Frame"""

    def sessionsFrameButtons(self):
        # Session Buttons Frame Configurations
        self.buttonsFrame = Frame(self.sessionFrame, bg="#5856a0")
        self.buttonsFrame.grid(row=7, column=0, padx=10, pady=10, sticky="w", columnspan=8)

        # Add new session
        self.btnAddSession = Button(self.buttonsFrame, command=self.addSession, text="Add Session", bd=0,
                                    cursor="hand2",
                                    bg="#EADDF7",
                                    fg="#5856a0", width=20, font=("Impact", 15))
        self.btnAddSession.grid(row=0, column=0, padx=10)

        # View all existing session bookings
        self.btnViewSessions = Button(self.buttonsFrame, command=self.viewSessions, text="View Sessions List", bd=0,
                                      cursor="hand2",
                                      bg="#EADDF7",
                                      fg="#5856a0", width=20, font=("Impact", 15))
        self.btnViewSessions.grid(row=0, column=1, padx=10)

        # Update selected session details
        self.btnUpdateSessions = Button(self.buttonsFrame, command=self.updateSession, text="Update Session Details",
                                        bd=0,
                                        cursor="hand2",
                                        bg="#EADDF7",
                                        fg="#5856a0", width=20, font=("Impact", 15))
        self.btnUpdateSessions.grid(row=0, column=2, padx=10)

        # GoBack
        self.btnGoBack = Button(self.sessionFrame, command=self.GoBack, text="Go Back", bd=0, cursor="hand2",
                                bg="#EADDF7",
                                fg="#5856a0", width=15, font=("Impact", 15))
        self.btnGoBack.grid(row=0, column=2, padx=10, sticky="e")

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
        self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, columns=(1, 2, 3, 4, 5, 6, 7),
                                style="mystyle.Treeview")
        self.out.heading("1", text="Session Index")
        self.out.column("1", width=5)
        self.out.heading("2", text="Student Name")
        self.out.heading("3", text="Dance Style")
        self.out.column("3", width=20)
        self.out.heading("4", text="Session Date")
        self.out.column("4", width=5)
        self.out.heading("5", text="Booked Day")
        self.out.column("5", width=5)
        self.out.heading("6", text="Max Rate")
        self.out.column("6", width=5)
        self.out.heading("7", text="Instructor Name")
        self.out.column("7", width=15)
        self.out['show'] = 'headings'

        # Virtual Events to trigger methods
        self.out.bind("<ButtonRelease-1>", self.getData)
        self.entrySessDate.bind("<<DateEntrySelected>>", self.getDay)

        # TreeView output layout configurations
        self.out.pack(fill=X)
        self.yScroll.config(command=self.out.yview)


# Assignining Instructors
class AssignSession:
    def __init__(self, root):
        self.root = root

        # local variables
        self.studentName = StringVar()
        self.danceStyle = StringVar()
        self.sessDate = StringVar()
        self.sessDay = StringVar()
        self.maxRate = DoubleVar()
        self.instructorName = StringVar()

        # Call the tkinter frames to the window
        self.sessionsFrame()
        self.sessionFrameButtons()
        self.tableOutputFrame()

    """Session Details Frame"""

    def sessionsFrame(self):
        # Admin Sessions Frame Configurations
        self.sessionFrame = Frame(self.root, bg="#5856a0")
        self.sessionFrame.pack(side=TOP, fill=X)
        self.session_frame_title = Label(self.sessionFrame, text="Session Control Panel", font=("Goudy old style", 35),
                                         bg="#5856a0",
                                         fg="white")
        self.session_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

        # Student Full Name
        self.labelStName = Label(self.sessionFrame, text="Student Name", font=("Times New Roman", 16, "bold"),
                                 bg="#5856a0",
                                 fg="white")
        self.labelStName.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtStName = Entry(self.sessionFrame, textvariable=self.studentName, font=("Times New Roman", 15), width=30,
                               state="readonly")
        self.txtStName.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Session Date
        self.labelSessDate = Label(self.sessionFrame, text="Session Date", font=("Times New Roman", 16, "bold"),
                                   bg="#5856a0",
                                   fg="white")
        self.labelSessDate.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.txtSessDate = Entry(self.sessionFrame, textvariable=self.sessDate, font=("Times New Roman", 15), width=30,
                                 state="readonly")
        self.txtSessDate.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Session Day
        self.labelSessDay = Label(self.sessionFrame, text="Session Day", font=("Times New Roman", 16, "bold"),
                                  bg="#5856a0",
                                  fg="white")
        self.labelSessDay.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entrySessDay = Entry(self.sessionFrame, textvariable=self.sessDay, font=("Times New Roman", 15), width=30,
                                  state="readonly")
        self.entrySessDay.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Student Dance Style
        self.labelStyle = Label(self.sessionFrame, text="Dance Style", font=("Times New Roman", 16, "bold"),
                                bg="#5856a0",
                                fg="white")
        self.labelStyle.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.comboStyle = ttk.Combobox(self.sessionFrame, textvariable=self.danceStyle, font=("Times New Roman", 15),
                                       width=28, state="disabled")
        self.comboStyle.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Student's Max Rate Payable
        self.labelMaxRate = Label(self.sessionFrame, text="Max Rate", font=("Times New Roman", 16, "bold"),
                                  bg="#5856a0",
                                  fg="white")
        self.labelMaxRate.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.txtMaxRate = Entry(self.sessionFrame, textvariable=self.maxRate, font=("Times New Roman", 15), width=30,
                                state="readonly")
        self.txtMaxRate.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Available Instructor List
        self.labelInsName = Label(self.sessionFrame, text="Instructor Name", font=("Times New Roman", 16, "bold"),
                                  bg="#5856a0",
                                  fg="white")
        self.labelInsName.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.comboInsName = ttk.Combobox(self.sessionFrame, textvariable=self.instructorName,
                                         font=("Times New Roman", 15), width=28,
                                         state="readonly")
        self.comboInsName['values'] = ("-")
        self.comboInsName.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Label to Display Instructor Details when assigning
        self.labelDetails = Label(self.sessionFrame, text="Instructor Details:", font=("Times New Roman", 16, "bold"),
                                  bg="#5856a0",
                                  fg="white")
        self.labelDetails.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.labelTxtDetails = Label(self.sessionFrame, text=" ",
                                     font=("Helvetica", 15), justify=LEFT,
                                     bg="white",
                                     fg="#5856a0", width=75, height=10, anchor="w")
        self.labelTxtDetails.grid(row=2, column=3, padx=10, pady=5, sticky="w", columnspan=4, rowspan=6)

    """Sub Methods to be used in primary CTA methods"""

    # event trigger Method to display the chosen data from the TreeView back in respective fields
    def getData(self, event):
        try:
            self.selectedRow = self.out.focus()
            self.selectedData = self.out.item(self.selectedRow)
            self.chosenRow = self.selectedData["values"]
            self.studentName.set(self.chosenRow[1])
            self.danceStyle.set(self.chosenRow[2])
            self.sessDate.set(self.chosenRow[3])
            self.sessDay.set(self.chosenRow[4])
            self.maxRate.set(self.chosenRow[5])
            self.instructorName.set(self.chosenRow[6])
            self.displayInsDetails(event)
        except IndexError as error:
            pass

    # Method to display instructor names depending on the chosen session details
    def comboBoxValues(self, event):
        self.selected = self.out.focus()
        self.chosenData = self.out.item(self.selected, 'values')
        global instructorList
        # Parsing the style, maxRate, session Day values for querying the db
        instructorList = db.selectInstructor(self.chosenData[2], float(self.chosenData[5]), self.chosenData[4])
        self.comboInsName['values'] = instructorList

    # Method to Display Instructor Details when assigning
    def displayInsDetails(self, event):
        detailRecord = db.getInstructor(self.comboInsName.get())
        if detailRecord == " ":
            self.labelTxtDetails.config(text=" ")
        else:
            recordString = '  Name: {} \n  Gender: {} \n  Dance Style: {}\n  Contact No: {}\n  Hourly Rate: {}\n  Available Days: {}'.format(
                *detailRecord)
            self.labelTxtDetails.config(text=recordString)

    # Method to redirect to the previous frame
    def GoBack(self):
        self.sessionFrame.destroy()
        self.buttonsFrame.destroy()
        self.tableFrame.destroy()
        admin.AdminControls(self.root)

    """CTA Methods"""

    # Method to view all sessions
    def viewSessions(self):
        self.out.delete(*self.out.get_children())  # emptying the table before reloading
        for row in db.viewSessionList():
            self.out.insert("", END, values=row)

    # Method to assign an instructor to the chosen session
    def assignInstructor(self):
        if self.txtStName.get() == "" or self.comboStyle.get() == "" or self.txtSessDate.get() == "" or self.txtMaxRate.get() == "" or self.comboInsName.get() == "":
            messagebox.showerror("Error!", "Please choose an instructor!")
            return

        db.updateSession(self.chosenRow[0], self.txtStName.get(), self.comboStyle.get(), self.txtSessDate.get(),
                         self.sessDay.get(),
                         self.txtMaxRate.get(),
                         self.comboInsName.get())
        messagebox.showinfo("Success!", "Instructor Successfully Assigned!")
        self.viewSessions()

    """CTA Buttons Frame"""

    def sessionFrameButtons(self):
        # Session Buttons Frame Configurations
        self.buttonsFrame = Frame(self.sessionFrame, bg="#5856a0")
        self.buttonsFrame.grid(row=7, column=0, padx=10, pady=10, sticky="w", columnspan=8)

        # Assign Instructor to chosen session
        self.btnAssignInstructor = Button(self.buttonsFrame, command=self.assignInstructor, text="Assign Instructor",
                                          bd=0,
                                          cursor="hand2",
                                          bg="#EADDF7",
                                          fg="#5856a0", width=20, font=("Impact", 15))
        self.btnAssignInstructor.grid(row=0, column=0, padx=10)

        # View all existing session bookings
        self.btnViewSessions = Button(self.buttonsFrame, command=self.viewSessions, text="View Sessions List", bd=0,
                                      cursor="hand2",
                                      bg="#EADDF7",
                                      fg="#5856a0", width=20, font=("Impact", 15))
        self.btnViewSessions.grid(row=0, column=1, padx=10)

        # GoBack
        self.btnGoBack = Button(self.sessionFrame, command=self.GoBack, text="Go Back", bd=0, cursor="hand2",
                                bg="#EADDF7",
                                fg="#5856a0", width=15, font=("Impact", 15))
        self.btnGoBack.grid(row=0, column=6, padx=10, sticky="e")

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
        self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, columns=(1, 2, 3, 4, 5, 6, 7),
                                style="mystyle.Treeview")
        self.out.heading("1", text="Session Index")
        self.out.column("1", width=5)
        self.out.heading("2", text="Student Name")
        self.out.heading("3", text="Dance Style")
        self.out.column("3", width=20)
        self.out.heading("4", text="Session Date")
        self.out.column("4", width=5)
        self.out.heading("5", text="Booked Day")
        self.out.column("5", width=5)
        self.out.heading("6", text="Max Rate")
        self.out.column("6", width=5)
        self.out.heading("7", text="Instructor Name")
        self.out.column("7", width=7)
        self.out['show'] = 'headings'

        # Virtual Events to trigger methods
        self.out.bind("<ButtonRelease-1>", self.getData)
        self.out.bind("<<TreeviewSelect>>", self.comboBoxValues)
        self.comboInsName.bind("<<ComboboxSelected>>", self.displayInsDetails)

        # TreeView output layout configurations
        self.out.pack(fill=X)
        self.yScroll.config(command=self.out.yview)
