#!/usr/bin/python
import cgi
import string
import time
import xmlrpclib
import curses.ascii
import os

import cgitb
cgitb.enable()

datadir = "data/"

I_ABSENT = 0
I_LATE = 1
I_EXCUSED = 2

def set_mark( sid, classname, mark, date ):
    student_file = datadir + classname + "/students/" + sid 
    f = open( student_file, "r" )
    data = f.readlines()
    f.close()
    if mark == "a":
        if not (date in data[I_ABSENT]):
            data[I_ABSENT] = data[I_ABSENT][:-1] + "," + date + "\n"
        laList = data[I_LATE][2:-1].split(",")
        if date in laList:
            laList.remove(date)
            s = "L"
            for d in laList:
                s+= "," + d
            s+= "\n"
            data[I_LATE] = s
        exList = data[I_EXCUSED][2:-1].split(",")
        if date in exList:
            exList.remove(date)
            s = "E"
            for d in exList:
                s+= "," + d
            s+= "\n"
            data[I_EXCUSED] = s

    elif mark == "l":
        if not (date in data[I_LATE]):
            data[I_LATE] = data[I_LATE][:-1] + "," + date + "\n"
        abList = data[I_ABSENT][2:-1].split(",")
        if date in abList:
            abList.remove(date)
            s = "A"
            for d in abList:
                s+= "," + d
            s+= "\n"
            data[I_ABSENT] = s
        exList = data[I_EXCUSED][2:-1].split(",")
        if date in exList:
            exList.remove(date)
            s = "E"
            for d in exList:
                s+= "," + d
            s+= "\n"
            data[I_EXCUSED] = s

    elif mark == "v":
        if not (date in data[I_EXCUSED]):
            data[I_EXCUSED] = data[I_EXCUSED][:-1] + "," + date + "\n"
        abList = data[I_ABSENT][2:-1].split(",")
        if date in abList:
            abList.remove(date)
            s = "A"
            for d in abList:
                s+= "," + d
            s+= "\n"
            data[I_ABSENT] = s
        laList = data[I_LATE][2:-1].split(",")
        if date in laList:
            laList.remove(date)
            s = "L"
            for d in laList:
                s+= "," + d
            s+= "\n"
            data[I_LATE] = s
            
    f = open( student_file, "w" )
    for d in data:
        f.write( d )
    f.close

def get_excused_date( sid, classname, name, mark ):

    html ="""
Select date to excuse absence/lateness<br>
<button onclick="mark_absent('""" + sid + """', '""" + classname + """', 'v', '""" + name + """')">Use Today</button><br>
Month: <select id="month">"""
    for i in range(12):
        html+= '''<option value="''' + `i+1` + '''">''' + `i+1` + "</option>"
    html+= '''</select>Day: <select id="day">'''
    for i in range(31):
        html+= '''<option value="''' + `i+1` + '''">''' + `i+1` + "</option>"
    html+= """</select><br>
<button onclick="mark_absent('""" + sid + """', '""" + classname + """', 'u', '""" + name + """')">Use Entered Date</button>"""

    if mark == "u":
        html = '<font color="FF0000">Invalid Date, please try again.</font></br>' + html
    print html



form = cgi.FieldStorage()

sid = form["sid"].value
classname = form["classname"].value
mark = form["mark"].value
date = form["date"].value

print "\n\n"

if mark == "e" or mark == "u":
    get_excused_date(sid, classname, form["name"].value, mark )
else:
    set_mark( sid, classname, mark, date )
