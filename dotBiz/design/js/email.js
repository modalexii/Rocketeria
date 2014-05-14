$(document).ready(function() {
    //global variables
    var form = $("#billboard-newsletter-signup");
 
    var email = $(".newsletter-email"); //textbox being validated
 
    //first validation on form submit
    form.submit(function() {
        //alert("form submitted...!");
 
        // validation begin before submit
        if (validateEmail()) {
 
            return true;
        } else {
 
            return false;
        }
 
    });
    function validateEmail() {
        //validation for empty emails
        if (email.val() == "") {
			$("#lightbox-shadow").css("display", "block");
			$("#lightbox-1").css("display", "block");
            return false;
        } else {

        }
 
        //validation for proper email formats
        //testing regular expression
        var a = $(".newsletter-email").val();
 
        var filter = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        //if it's valid email
        if (filter.test(a)) {
            return true;
        }
        //if it's NOT valid
        else {
			$("#lightbox-shadow").css("display", "block");
			$("#lightbox-2").css("display", "block");
            return false;
        }
    }
 
});