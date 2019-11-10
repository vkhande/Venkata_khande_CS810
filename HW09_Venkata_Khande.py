'''
Written by : Venkata Khande
'''

import os
from collections import defaultdict
from prettytable import PrettyTable

class Student():
    """Student class with details of the student and add course and pretty table function"""
    def __init__(self, CWID, Name, Major):
        """ Constructor to initialise the variables """
        self.CWID = CWID
        self.Name = Name
        self.Major = Major
        self.CoursesGradeInformation = defaultdict(str)

    def addCourseGrade(self,course, grade):
        """Add course grade to the course for this particular student instance"""
        self.CoursesGradeInformation[course] = grade

    def prettyTableStudent(self):
        """return the data for this student instance to the pretty table"""
        return [self.CWID, self.Name, sorted(self.CoursesGradeInformation.keys())]

class Instructor():
    """Instructor class with details of the Intructor and add course with no of students and pretty table function"""
    def __init__(self, CWID, Name, Dept):
        self.CWID = CWID
        self.Name = Name
        self.Dept = Dept
        self.Courses = defaultdict(int)
    
    def add_course_noofstudents (self, course):
        """Add number of students to the course for this instructor"""
        self.Courses[course] += 1

    def pretty_table_instructor(self):
        """Return data of this instructor to the pretty table"""
        return [self.CWID, self.Name, self.Dept], self.Courses

class Pack:
    def __init__(self, FilePath):

        self.FilePath = FilePath
        self.studentInfo ={}
        self.insructorsInfo = {}
        self.analyzeFiles()
        self.studentsSummary()
        self.instructor_summary()

    def analyzeFiles(self):
        """Analyse the files for getting the student, Instrctor, and grades data from the text file."""

        if not os.path.exists(self.FilePath):
            error_msg = f"File at {self.FilePath} Not Found"
            raise FileNotFoundError(error_msg)

        studentsFile = 'students.txt'
        instructorsFile = 'instructors.txt'
        gradesFile = 'grades.txt'

        pathJoinStudent = os.path.join(self.FilePath, studentsFile)
        pathJoinInstructor = os.path.join(self.FilePath, instructorsFile)
        filePathGrades = os.path.join(self.FilePath, gradesFile)
        
        if studentsFile in os.listdir(self.FilePath):
            
            for CWID, Name, Major in self.file_reading_gen(pathJoinStudent, 3, "\t", False): 
                self.studentInfo[CWID]=Student(CWID, Name, Major)
        else:
            raise FileNotFoundError(f"Can not open {studentsFile}")
        
        if instructorsFile in os.listdir(self.FilePath):
            
            for CWID, Name, Dept in self.file_reading_gen(pathJoinInstructor, 3, "\t", False): 
                self.insructorsInfo[CWID]=Instructor(CWID, Name, Dept)
        else:
            raise FileNotFoundError(f"Can not open {instructorsFile}")

        if gradesFile in os.listdir(self.FilePath):
            
            for studentCWID, course, grade, instructorCWID in  self.file_reading_gen(filePathGrades, 4, "\t", False):
                if studentCWID in self.studentInfo.keys():
                    self.studentInfo[studentCWID].addCourseGrade(course, grade)
                if instructorCWID in self.insructorsInfo.keys():
                    self.insructorsInfo[instructorCWID].add_course_noofstudents(course) 
        else:
            raise FileNotFoundError(f"Can't open {gradesFile}")

    def file_reading_gen(self, path, fields, sep=',', header=False):
        """File Reading Function"""
        try:
            File_Path = open(path, "r")

        except FileNotFoundError:
            raise FileNotFoundError(f"{path} Not Found")

        else:
            with File_Path:
                lineNum = 0
                if header and len(next(File_Path).split(sep)) != fields:
                    File_Path.seek(0)
                    raise ValueError(
                        f"{path} has has different fields than expected {fields}")

                if header:
                    lineNum += 1

                for ln in File_Path:
                    ln = ln.strip().split(sep)
                    lineNum += 1
                    if len(ln) != fields:
                        raise ValueError(
                            f"'{path}' has wrong fields on line {lineNum} but expected {fields}")
                    yield tuple(ln)

    def studentsSummary(self):
        """Printing pretty table for the student"""
        pretty = PrettyTable(field_Names = ['CWID', 'Name', 'Completed Courses'])
        print(f"Students")
        for student in self.studentInfo.values():
            pretty.add_row(student.prettyTableStudent())

        print(pretty)

    def instructor_summary(self):
        """Printing pretty table for the instructor"""
        Pretty = PrettyTable(field_Names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])
        print(f"Instructors")
        for instructor in self.insructorsInfo.values():
            instructorInformation, Courses = instructor.pretty_table_instructor()
            for course, noOfStudents in Courses.items():
                instructorInformation.extend([course, noOfStudents])
                Pretty.add_row(instructorInformation)
                instructorInformation = instructorInformation[0:3]
            
        print(Pretty)

def main():
    try:
        Pack('C:/Users/princ/OneDrive/Documents/stevens/810/')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()  # Main routine for priting the data in the code
