function overlay( name, s, c ) {

    el = document.getElementById("overlay");    

    if (el.style.visibility == "visible") {
	el.style.visibility = "hidden";
	box = document.getElementById("modalbox");
	box.innerHTML = "";
    }
    else {
	jQuery.get("show_student.py", { n: name, sid: s, classname: c }, function(data, status) {
	    box = document.getElementById("modalbox");
	    box.innerHTML = data;
	});
	el.style.visibility = "visible";		
    }        
}

function get_excused_choice(s, c, n, m) {

    jQuery.get("update_record.py", { sid: s, classname: c, mark: m, date: "d", name:n }, function(data, status) {
	box = document.getElementById("modalbox");
	box.innerHTML = data;
    });    
}


function days_in_month( month ) {

    if ( month == 4 || month == 6 || month == 9 || month == 11 ) {
	return 30;
    }
    else if ( month != 2 ) {
	return 31;
    }
    else {
	return 28;
    }
}
function verify_date( month, day ) {
    return day <= days_in_month( month );
}



function mark_absent( s, c, m, name) {

    var today = "";
    var early = false;

    if ( m == "u" ) {
	var mo = document.getElementById("month");
	var da = document.getElementById("day");    	
	var month = mo.options[mo.selectedIndex].value;
	var day = da.options[da.selectedIndex].value;

	if ( verify_date( month, day ) ) {
	    console.log( "date verified" + month + " " + day);
	    m = "v";	    
	}
	else {
	    get_excused_choice( s, c, name, m );
	    return;
	}
	
	today = month + "/" + day;
	early = true;
    }
    
    else {
	var d = new Date();
	today = (d.getMonth() + 1) + "/" + d.getDate();
    }
    
    console.log( today );

    jQuery.get("update_record.py", { sid: s, classname: c, mark: m, date: today});
    jQuery.get("show_student.py", { n: name, sid: s, classname: c }, function(data, status) {
	box = document.getElementById("modalbox");
	box.innerHTML = data;
    });

    if ( ! early ) {
	card = document.getElementById( s );
	line = card.innerHTML;
	
	if ( line.indexOf( "<font" ) != -1 ) {
	    var i = line.indexOf( "<br><br>" );
	    console.log("in a " + line + " i = " + i);
	    line = line.slice(0, i + 8 );
	}
	
	else {
	    line = "<font color=\"FF0000\">" + line + "<br><br>";
	}
	if (m == "a") {
	    line = line +  "Absent</font>";
	}
	else if ( m == "l" ) {
	    line = line + "Late</font>";
	}
	else if ( m == "v" ) {
	    line = line + "Excused</font>";
	}
	card.innerHTML = line;
    }
}