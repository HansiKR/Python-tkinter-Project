import sqlite3


class Database:
    def __init__(self, db):
        # creating database connection
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        # SQL queries to create tables
        sql = """
        CREATE TABLE IF NOT EXISTS instructors (
            instructorID Integer PRIMARY KEY,
            name text,
            gender text,
            danceStyles text,
            telNo text,
            hrRate real,
            availability text,
            availableDays text,
            username text,
            password text
        )
        """
        sql2 = """
        CREATE TABLE IF NOT EXISTS students (
            studentID Integer PRIMARY KEY,
            firstName text,
            surName text,
            email text,
            DOB text,
            gender text,
            telNo text,
            address text
        )
        """
        sql3 = """
                CREATE TABLE IF NOT EXISTS sessions (
                    sessionID Integer PRIMARY KEY,
                    studentName text,
                    danceStyle text,
                    sessDate text,
                    sessDay text,
                    maxRate real,
                    instructorName text
                )
                """
        # cursor executions
        self.cur.execute(sql)
        self.cur.execute(sql2)
        self.cur.execute(sql3)
        self.con.commit()

    # local method to hold the dance styles values used across the system
    def danceStylesValues(self):
        danceStyles = ("Salsa", "Waltz", "HipHop", "Zumba", "Ballet", "Ballroom", "Jazz", "Contemporary")
        return danceStyles

    """Admin Controls - Backend"""

    # Add Instructor record to the table
    def insertInstructor(self, name, gender, dStyles, telNo, hrRate, avail, days, username, password):
        self.cur.execute("INSERT INTO instructors VALUES (NULL,?,?,?,?,?,?,?,?,?)",
                         (name, gender, dStyles, telNo, hrRate, avail, days, username, password))
        self.con.commit()

    # Display Instructor List from table
    def viewInstructor(self):
        self.cur.execute("SELECT * FROM instructors")
        rows = self.cur.fetchall()
        return rows

    # Delete Instructor Entry from table
    def removeInstructor(self, insID):
        self.cur.execute("DELETE FROM instructors WHERE instructorID=?", (insID,))
        self.con.commit()

    # Edit Instructor Details in the table
    def editInstructor(self, insID, name, gender, dStyles, telNo, hrRate, avail, days, username, password):
        sql_insert_query = """UPDATE instructors SET name=?, gender=?, danceStyles=?, telNo=?, hrRate=?, availability=?, availableDays=?, username=?, password=? WHERE instructorID=?"""
        self.cur.execute(sql_insert_query,
                         (name, gender, dStyles, telNo, hrRate, avail, days, username, password, insID))
        self.con.commit()

    """instructor Controls - Backend"""

    # Add Student record to the table
    def insertStudent(self, firstName, surName, email, dob, gender, telNo, address):
        self.cur.execute("INSERT INTO students VALUES (NULL,?,?,?,?,?,?,?)",
                         (firstName, surName, email, dob, gender, telNo, address))
        self.con.commit()

    # Display Students list from table
    def viewStudents(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return rows

    # Edit data in the table
    def editStudent(self, stuID, firstName, surName, email, dob, gender, telNo, address):
        sql_update_query = """UPDATE students SET firstName=?, surName=?, email=?, DOB=?, gender=?, telNo=?, address=? WHERE studentID=?"""
        self.cur.execute(sql_update_query, (firstName, surName, email, dob, gender, telNo, address, stuID))
        self.con.commit()

    # Instructor Login Verification - used in the login.py file
    def instructorLogin(self, username, password):
        sql_select_query = "SELECT * FROM instructors WHERE username=? AND password=?"
        self.cur.execute(sql_select_query, (username, password))
        result = self.cur.fetchall()
        return result

    """Session Controls - Backend"""

    # Return the full name of the student
    def selectStudent(self, stuID):
        sql_select_query = "SELECT firstName, surName FROM students WHERE studentID=?"
        self.cur.execute(sql_select_query, (stuID,))
        data = self.cur.fetchone()
        result = data[0] + " " + data[1]
        return result

    # Add new session record to the table
    def insertSession(self, stname, dStyles, sessDate, sessDay, maxRate, insName):
        self.cur.execute("INSERT INTO sessions VALUES (NULL,?,?,?,?,?,?)",
                         (stname, dStyles, sessDate, sessDay, maxRate, insName))
        self.con.commit()

    # Display Session List from table
    def viewSessionList(self):
        self.cur.execute("SELECT * FROM sessions")
        rows = self.cur.fetchall()
        return rows

    # Update Session Record
    def updateSession(self, sessID, stname, dStyles, sessDate, sessDay, maxRate, insName):
        sql_update_query = """UPDATE sessions SET studentName=?, danceStyle=?, sessDate=?, sessDay=?, maxRate=?, instructorName=? WHERE sessionID=?"""
        self.cur.execute(sql_update_query, (stname, dStyles, sessDate, sessDay, maxRate, insName, sessID))
        self.con.commit()

    # Return suitable instructors list to set the comboBox values
    def selectInstructor(self, dStyle, maxRate, sessDay):
        sql_select_query = "SELECT name FROM instructors WHERE danceStyles=? AND hrRate<=? AND availableDays LIKE ?"
        self.cur.execute(sql_select_query, (dStyle, maxRate, '%' + sessDay + '%'))
        namesList = self.cur.fetchall()
        result = []
        for i in namesList:
            result.append(i[0])
        return result

    # Retrieve Instructor Details from table to display when assigning
    def getInstructor(self, insName):
        if insName == " ":
            return " "
        else:
            self.cur.execute(
                "SELECT name, gender, danceStyles, telNo, hrRate, availableDays FROM instructors WHERE name=?",
                (insName,))
            result = self.cur.fetchone()
            return result
