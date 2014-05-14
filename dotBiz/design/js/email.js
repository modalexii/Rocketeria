$(document).ready(function() {
    //global variables
    var form = $("#home-newsletter-signup-1");
 
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
			alert("Names cannot be empty!");
            return false;
        } else {

        }
 
        //validation for proper email formats
        //testing regular expression
        var a = $(".newsletter-email").val();
 
        var filter = /^[a-zA-Z0-9]+[a-zA-Z0-9_.-]+[a-zA-Z0-9_-]+@[a-zA-Z0-9]+[a-zA-Z0-9.-]+[a-zA-Z0-9]+.[a-z]{2,4}$/;
        //if it's valid email
        if (filter.test(a)) {
		    alert("Valid E-Mail");
            return true;
        }
        //if it's NOT valid
        else {
            alert("Invalid E-Mail");
            return false;
        }
    }
 
});