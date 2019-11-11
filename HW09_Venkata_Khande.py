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
        return [self.CWID, self.Name, self.Major, self.CoursesGradeInformation]

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

class Majors():
    """Major class with details of the majors and their required and elective courses."""

    def __init__(self, major):
        self.major = major
        self.req = set()
        self.elec = set()

    def add_required(self, course):
        self.req = self.req.union(set(course))

    def add_elective(self, course):
        self.elec = self.elec.union(set(course))

class Pack:
    def __init__(self, FilePath):

        self.FilePath = FilePath
        self.studentInfo ={}
        self.insructorsInfo = {}
        self.majorsData = {}
        self.analyzeFiles()
        self.studentsSummary()
        self.instructor_summary()
        self.major_summary()

    def analyzeFiles(self):
        """Analyse the files for getting the student, Instrctor, and grades data from the text file."""

        if not os.path.exists(self.FilePath):
            error_msg = f"File at {self.FilePath} Not Found"
            print(error_msg)

        studentsFile = 'students.txt'
        instructorsFile = 'instructors.txt'
        gradesFile = 'grades.txt'
        majorFile = 'majors.txt'

        pathJoinStudent = os.path.join(self.FilePath, studentsFile)
        pathJoinInstructor = os.path.join(self.FilePath, instructorsFile)
        filePathGrades = os.path.join(self.FilePath, gradesFile)
        majorJoinFile = os.path.join(self.FilePath, majorFile)
        
        if studentsFile in os.listdir(self.FilePath):
            
            for CWID, Name, Major in self.file_reading_gen(pathJoinStudent, 3, ";", True): 
                self.studentInfo[CWID]=Student(CWID, Name, Major)
        else:
            print(f"Can not open {studentsFile}")
        
        if instructorsFile in os.listdir(self.FilePath):
            
            for CWID, Name, Dept in self.file_reading_gen(pathJoinInstructor, 3, "|", True): 
                self.insructorsInfo[CWID]=Instructor(CWID, Name, Dept)
        else:
            print(f"Can not open {instructorsFile}")

        if gradesFile in os.listdir(self.FilePath):
            
            for studentCWID, course, grade, instructorCWID in  self.file_reading_gen(filePathGrades, 4, "|", True):
                if studentCWID in self.studentInfo.keys():
                    self.studentInfo[studentCWID].addCourseGrade(course, grade)
                else:
                    print(f"Grade not found for student with {studentCWID}")
                if instructorCWID in self.insructorsInfo.keys():
                    self.insructorsInfo[instructorCWID].add_course_noofstudents(course)
                else:
                    print(f"Grade not found for Instructor with {instructorCWID}") 
        else:
            print(f"Can't open {gradesFile}")

        if majorFile in os.listdir(self.FilePath):
            tmp_dic = defaultdict(lambda: defaultdict(set))
            for dept, flag, course in self.file_reading_gen(majorJoinFile, 3, "\t", True):
                tmp_dic[dept][flag].add(course)

            for dept, courses in tmp_dic.items():
                
                new_major = Majors(dept)
                
                for flag, course in courses.items():
                    if flag == 'R':
                        new_major.add_required(course)
                    if flag == 'E':
                        new_major.add_elective(course)
                self.majorsData[dept] = new_major
        else:
            print(f"Can't open {majorFile}")

    def file_reading_gen(self, path, fields, sep=',', header=False):
        """File Reading Function"""
        try:
            File_Path = open(path, "r")

        except FileNotFoundError:
            print(f"{path} Not Found")

        else:
            with File_Path:
                lineNum = 0
                if header and len(next(File_Path).split(sep)) != fields:
                    File_Path.seek(0)
                    print(f"{path} has has different fields than expected {fields}")

                if header:
                    lineNum += 1

                for ln in File_Path:
                    ln = ln.strip().split(sep)
                    lineNum += 1
                    if len(ln) != fields:
                        print(
                            f"'{path}' has wrong fields on line {lineNum} but expected {fields}")
                    yield tuple(ln)

    def studentsSummary(self):
        """Printing pretty table for the student"""
        PassGrades = ['A','A-','B+','B','B-','C+','C']
        pretty = PrettyTable(field_names = ['CWID', 'Name', 'Major','Completed Courses','Remaining Required','Remaining Electives'])
        print(f"Students")
        for student in self.studentInfo.values():
            temp = student.prettyTableStudent()
            completedCourses = set([Course for Course, grade in temp[3].items() if grade in PassGrades])
            if temp[2] in self.majorsData:
                temp[3] = sorted(completedCourses)
                remain_require = self.majorsData[temp[2]].req.difference(temp[3])
                if len(self.majorsData[temp[2]].elec.intersection(temp[3]))>0:
                    remain_elective = None
                else:
                    remain_elective = self.majorsData[temp[2]].elec - completedCourses
            else:
                temp[3] = sorted(completedCourses)
                remain_elective, remain_require = None, None
                print(f"Major cannot be found {temp[2]} for student {temp[0]}")
            temp.append(remain_require)
            temp.append(remain_elective)
            pretty.add_row(temp)
            
        
        print(pretty)

    def instructor_summary(self):
        """Printing pretty table for the instructor"""
        Pretty = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])
        print(f"Instructors")
        for instructor in self.insructorsInfo.values():
            instructorInformation, Courses = instructor.pretty_table_instructor()
            for course, noOfStudents in Courses.items():
                instructorInformation.extend([course, noOfStudents])
                Pretty.add_row(instructorInformation)
                instructorInformation = instructorInformation[0:3]
            
        print(Pretty)

    def major_summary(self):
        """Printing Pretty table of majors info"""
        table = PrettyTable(field_names = ['Dept', 'Required', 'Elective'])
        for dept, major in self.majorsData.items():
            table.add_row([dept, major.req, major.elec])
        print(f"Majors")
        print(table)

def main():
    try:
        Pack('C:/Users/princ/OneDrive/Documents/stevens/810/')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()  # Main routine for priting the data in the code
