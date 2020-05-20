/*! jQuery v3.3.1 | (c) JS Foundation and other contributors | jquery.org/license */


function validate(){
alert("m here");
var sname = $("#txt_name").val();
alert(sname);
if (sname == null || sname == ' '){
    alert('Please Enter Name');
    return false;
    }

var sadd = $("#txt_add").val();
if (sadd == null || sadd == ' '){
    alert('Please Enter Address');
    return false;
    }

var sage = $("#txt_age").val();
if (sage == null || sage == ' '){
    alert('Please Enter Age');
    return false;
    }
}

