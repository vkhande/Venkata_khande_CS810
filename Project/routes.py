'''
Written by : Venkata Khande
'''
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
dataBase_path = '810_startup.db'

@app.route('/instructors')
def instructors():
    """Instructors data render function to be excuted"""
    
    dataBase = sqlite3.connect(dataBase_path)

    query = """ select CWID, Name , Dept, Course, count(*) as students from instructors,grades
                where  instructors.CWID = grades.InstructorCWID GROUP BY Instructors.CWID,grades.Course order by  CWID asc;"""

    data = dataBase.execute(query)

    render_data = [{'CWID': Cwid, 'Name': Name, 'Department': Department, 'Course': Course, 'Students': Students}
                    for Cwid, Name, Department, Course, Students in data]
    
    dataBase.close()

    Template = render_template('instructors.html', Main_Title='Stevens Repository',
                            Table_title='Courses and Students count',
                            instructors=render_data)

    return Template

app.run(debug=True)