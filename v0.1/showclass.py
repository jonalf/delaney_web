#!/usr/bin/python
import cgi
import string
import time
import xmlrpclib
import curses.ascii
import os

import cgitb
cgitb.enable()

I_NAME = 0
I_SIZE = 1
I_ROWS = 2
I_COLS = 3

R_ID = 0
R_FIRST = 1
R_LAST = 2
R_NICK = 3

datadir = "data/"

def get_html_header():
    h = """
<html>
<head>
<title>NEW CLASS</title>
<link rel="stylesheet"
      type="text/css"
      href="style.css" />
</head>
<body>""" 
    return h

def make_week_nav( weeklist, classname ):

    html = "<ul>"
    for w in weeklist:
        html+= "<li>" +  w + "</li> "

    html+= "</ul><br>"
    return html

def make_card_html( sid, first, last, nick ):
    cardHTML = """<table class="card">
      <tr>"""
    for i in range(5):
        cardHTML +="""
	<td><input type="text" class="data" name="attendance-""" + `sid` + "-" + `i` +""""></td>"""
    cardHTML+= """
      </tr>
      <tr>"""
    for i in range(5):
        cardHTML +="""
	<td><input type="text" class="data" name="work-""" + `sid` + "-" + `i` + """"></td>"""
    cardHTML+= """
      </tr>
      <tr>"""
    for i in range(5):
        cardHTML +="""
	<td><input type="text" class="data" name="work-""" + `sid` + "-" + `i+5` + """"></td>"""
    cardHTML+= '''
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="nickname-''' + `sid` + '''" value="''' + nick + '''"></td>
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="firstname-''' + `sid` + '''" value="''' + first + '''"></td>
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="lastname-''' + `sid` + '''" value="''' + last + '''"></td></td>
      </tr>
    </table>
    <input type="hidden" name="studentid-''' + `sid` + '''" value="''' + `sid` + '''">
'''
    return cardHTML

def make_week_guide( startdate ):
    date = startdate.split("/")
    month = int(date[0])
    day = int(date[1])
    year = int(date[2])
    end_day = day + 4
    end_month = month
    if end_day > days_in_month( month, year ):
        end_day = end_day - days_in_month( month, year )
        if month == 12:
            end_month = 1
        else:
            end_month = month + 1

    cardHTML = """<table class="card">
      <tr>"""
    for i in range(5):
        cardHTML +='''
	<td><input type="text" class="data" name="attendance-master-''' + `i` + '''"></td>'''
    cardHTML+= """
      </tr>
      <tr>"""
    for i in range(5):
        cardHTML +="""
	<td><input type="text" class="data" name="work-master-""" + `i` + """"></td>"""
    cardHTML+= """
      </tr>
      <tr>"""
    for i in range(5):
        cardHTML +="""
	<td><input type="text" class="data" name="work-master-""" + `i+5` + """"></td>"""
    cardHTML+= '''
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="start" value="''' + startdate[:-5] + '''"></td>
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="through" value="-"></td>
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="end" value="''' + `end_month` + "/" + `end_day` + '''"></td></td>
      </tr>
    </table>
    <input type="hidden" name="master" value="master">
'''
    return cardHTML


def make_card_table(rows, cols, classname, startdate, students):
    html = """<form method="post" action="savenewclass.py">"""
    c = int(cols)

    for i in range( c ):
        html+= """<div class="cardcol">"""
        for j in range( int(rows) ):
            sid = c - i + j * c - 1
            student = find_sid( students, sid )
            if student != -1:               
                html+= make_card_html( sid, students[student][R_FIRST], students[student][R_LAST], students[student][R_NICK] )
            else:
                html+= '''<div class="spacer"></div>'''
        if i == 0:
            sd = startdate.replace("-", "/")
            html+= make_week_guide( sd )
        html+= "</div>"

    html+= '''<br>
<input type="submit" value="save">
<input type="hidden" name="classname" value="''' + classname + '''">
<input type="hidden" name="rows" value="''' + rows + '''">
<input type="hidden" name="cols" value="''' + cols + '''">
<input type="hidden" name="startdate" value="''' + startdate  + '''">
</form>'''
    return html

def find_sid( students, sid ):
    for i in range(len(students)):
        #print "i = " + `i` + " sid = " + `sid` + " student = " + students[i][R_ID] + "<br>"
        if int(students[i][R_ID]) == sid:
            return i
    return -1

def is_leap_year( year ):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False

def days_in_month( month, year ):
    if month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    elif month != 2:
        return 31
    elif is_leap_year( year ):
        return 29
    else:
        return 28

def is_valid_date( date ):
    if date.find("/") != -1:
        l = date.split("/")
        if len(l) == 3 and l[0].isdigit() and l[1].isdigit() and l[2].isdigit():
            month = int(l[0])
            day = int(l[1])
            year = int(l[2])
            now = time.localtime()
            currentyear = now[0]
            if year >= currentyear - 1 and year <= currentyear + 1:
                if month >= 1 and month <= 12 and day >= 1:
                    return day <= days_in_month( month, year )
    return False

def get_class_html( classname, rows, cols ):
    #get weeks
    weeklist = os.listdir( datadir + classname + "/weeks/" )
    html = make_week_nav( weeklist, classname )    
    
    #get student info
    students = []
    f = open( datadir + classname + "/roster", "r" )
    for line in f:
        line = line[:-1]
        students.append( line.split(",") )
    
    html+= make_card_table( rows, cols, classname, weeklist[0], students )
    return html

def is_class( classname ):
    f = open( datadir + "classlist", "r" )
    for line in f:
        l = line.split(",")
        if l[0] == classname:
            return True
    return False

form = cgi.FieldStorage()

print "\n"
print get_html_header()

classname = form["classname"].value
classdir = datadir + classname + "/"

if is_class( classname ):
    f = open( datadir + "classlist", "r" )

    size = 0
    rows = 0
    cols = 0
    
    for line in f:
        entry = line.split(",")
        if entry[ I_NAME ] == classname:
            size = entry[ I_SIZE ]
            rows = entry[ I_ROWS ]
            cols = entry[ I_COLS ]
            break

    print get_class_html( classname, rows, cols )
else:
    print"<center><h1>" + classname + ": Does not exist.</h1></center>"

print "</body></html>"

