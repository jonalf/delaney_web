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
<script src="jquery-1.8.3.min.js"></script>
</head>
<body>""" 
    return h

def make_card_html( sid, first, last, nick, classname ):
    cardHTML = '''<div class="card" id="''' + `sid` + '''" ''' + """onclick="overlay('""" + first + " " + last + "', " + `sid` + ",'" + classname + """')">""" + nick + "<br>" + first + "<br>" + last + '''</div>'''
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

    cardHTML = '''<table class="card">
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


def make_card_table(rows, cols, classname, students):
    html = ""
    c = int(cols)

    for i in range( c ):
        html+= """<div class="cardcol">"""
        for j in range( int(rows) ):
            sid = c - i + j * c - 1
            student = find_sid( students, sid )
            if student != -1:               
                html+= make_card_html( sid, students[student][R_FIRST], students[student][R_LAST], students[student][R_NICK], classname )
            else:
                html+= '''<div class="spacer"></div>'''
        html+= "</div>"

    return html

def find_sid( students, sid ):
    for i in range(len(students)):
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
    #get student info
    students = []
    f = open( datadir + classname + "/roster", "r" )
    for line in f:
        line = line[:-1]
        students.append( line.split(",") )
    
    html = make_card_table( rows, cols, classname,  students )
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

    print get_class_html( classname, rows, cols ) +  '''
<div id="overlay">
<div id="modalbox">
</div>
</div>
<script type="text/javascript" src="scripts.js"></script>'''

else:
    print"<center><h1>" + classname + ": Does not exist.</h1></center>"

print "</body></html>"

