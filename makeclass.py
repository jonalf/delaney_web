#!/usr/bin/python
import cgi
import string
import time
import xmlrpclib
import curses.ascii

import cgitb
cgitb.enable()

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

def make_week_nav( num_weeks ):
    html = "<ul>"
    for i in range( num_weeks ):
        html+= "<li>Week " + `i+1` + "</li> "

    html+= "</ul><br>"
    return html

def make_card_html( sid ):
    cardHTML = '''<table class="card">
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="nickname-''' + `sid` + '''"></td>
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="firstname-''' + `sid` + '''" value="''' + `sid` + '''"></td>
      </tr>
      <tr>
	<td colspan="5"><input type="text" class="name" name="lastname-''' + `sid` + '''"></td></td>
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

def make_card_table(rows, cols, classname, startdate):
    html = """<form method="post" action="savenewclass.py">"""
    c = int(cols)
    for i in range( c ):
        html+= """<div class="cardcol">"""
        for j in range( int(rows) ):
            html+= make_card_html( c - i + j * c - 1 ) 
        if i == 0:
            html+= make_week_guide( startdate )
        html+= "</div>"

    html+= '''<br>
<input type="submit" value="save">
<input type="hidden" name="classname" value="''' + classname + '''">
<input type="hidden" name="rows" value="''' + rows + '''">
<input type="hidden" name="cols" value="''' + cols + '''">
<input type="hidden" name="startdate" value="''' + startdate  + '''">
</form>'''
    return html


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
        

form = cgi.FieldStorage()

print "\n"
print get_html_header()


if form.has_key("class") and form.has_key("rows") and form.has_key("cols") and form.has_key("startdate"):
#if True:
    if is_valid_date( form["startdate"].value ):
        print "<center><h1>" + form["class"].value + "</h1><h2>Enter Student Names</h2></center>"
        classname = form["class"].value.replace(" ", "_" )
        print make_card_table( form["rows"].value, form["cols"].value, classname, form["startdate"].value )
    else:
        print "<center><h1>Please enter a valid date on the previous page.</h1></center>"
else:
    print "<center><h1>Please Fill out all the information on the previous page.</h1></center>"


print "</body></html>"

