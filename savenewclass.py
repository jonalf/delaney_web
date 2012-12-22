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

def get_names( fullsize, form ):
    names = []

    for i in range( fullsize ):        
        if form.has_key( "firstname-" + `i` ):
            fn = form["firstname-" + `i`].value 

            if not fn.isdigit():
                if form.has_key("lastname-" + `i` ):
                    ln = form["lastname-" + `i`].value
                else:
                    ln = ""
                if form.has_key("nickname-" + `i` ):
                    nn = form["nickname-" + `i`].value
                else:
                    nn = ""
                names.append( (i, fn, ln, nn) )
    return names

def update_files( classname, names, rows, cols, startdate ):
    f = open( datadir + "classlist", "r" )
    for line in f:
        s = line.split(",")[0]
        if s == classname:
            return -1
    f.close()
    f = open( datadir + "classlist", "a" )
    f.write( classname + "," + `len(names)` + "," + `rows` + "," + `cols` + "\n" );
    f.close()

    classdir = datadir + classname + "/"
    studentdir = classdir + "students/"
    if not os.path.exists( classdir ):    
        os.mkdir( classdir )
        os.chmod( classdir, 0775 )

        os.mkdir( studentdir )
        os.chmod( studentdir, 0775 )
        
        f = open( classdir + "roster", "w+" )
        for  name in names:
            f.write( `name[0]` + "," + name[1] + "," + name[2] + "," + name[3] + "\n" )
            s = open( studentdir + `name[0]`, "w+")
            s.write("A\nL\nE\n")
            s.close()
        f.close()

form = cgi.FieldStorage()

print "\n"
print get_html_header()

rows = int(form["rows"].value)
cols = int(form["cols"].value)
classname = form["classname"].value
names = get_names( rows * cols, form )
startdate = form["startdate"].value

i = update_files( classname, names, rows, cols, startdate )

if i == -1:
    print "<center> That Class Already Exists </center>"
else:
    print '''<center>Class created.<br> Click enter to go to the classe's site.<br>
<form method="post" action="showclass.py">
<input type="hidden" name="classname" value="''' + classname + '''">
<input type="submit" value="ENTER">
</form>
</center>'''

print "</body></html>"

