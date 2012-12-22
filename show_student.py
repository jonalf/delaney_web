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

def get_attendance( key, classname, type ):

    html = '''<div style="text-align: left">'''
    if type == I_ABSENT:
        html+= "Absences: "
    elif type == I_LATE:
        html+= "Latenesses: "

    f = open( datadir + classname + "/students/" + key, "r")
    data = f.readlines()
    f.close()
    s = data[type][2:-1].split(",")
    for d in s:
        html+= d + " "
    return html + "</div>"

form = cgi.FieldStorage()
divider = "<br><hr>"

name = form["n"].value
sid = form["sid"].value
classname = form["classname"].value

print "\n\n"

print name + " " + sid  + divider
print get_attendance( sid, classname, I_ABSENT ) + divider
print get_attendance( sid, classname, I_LATE ) + divider
print """
<button onclick="mark_absent('""" + sid + "', '" + classname + """', 'a', '""" + name + """')">Mark Absent</button>
<button onclick="mark_absent('""" + sid + "', '" + classname + """', 'l', '""" + name + """')">Mark Late</button> 
<button onclick="get_excused_choice('""" + sid + "', '" + classname + """', '""" + name + """', 'e')">Mark Excused</button><hr>"""


print """<a onclick="overlay('hello')">Close Box</a>"""
