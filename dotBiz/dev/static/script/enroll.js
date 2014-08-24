function addStudent() {
	if ($('#student3').is(':visible')) {
		alert('More then 3 students? Enter additional information in the comment box below, or give us a call.')
	}
	else if ($('#student2').is(':visible')) {
		$('#student3').slideDown(function() {
			$('#add_student').addClass('gray');
		});
	} else {
		$('#student2').slideDown();
	}
}

function highlight(field) {
	$(field).css('background', '#f5ed14');
}

function unhighlightInputs(form) {
	$('input[type="text"].form-input').css('background','none');
	$('input[type="email"].form-input').css('background','none');
}

function scrollToBillTo() {
	$('html, body').animate({
		scrollTop: $("#billto_heading").offset().top
	}, 800);
}

function validateEnroll() {
	var validationError = false;

	var exp = /.*[,| ].*$/;
	if (!(exp.test($('input[name="billto_firstandlast"]').val()))) {
		var fail = true;
		highlight('input[name="billto_firstandlast"]');
		validationError = true;
	}

	var exp = /^.+\@.+\..+$/;
	if (!(exp.test($('input[name="billto_email"]').val()))) {
		var fail = true;
		highlight('input[name="billto_email"]');
		validationError = true;
	}

	var exp = /^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/;
	if (!(exp.test($('input[name="billto_mobilephone"]').val()))) {
		var fail = true;
		highlight('input[name="billto_mobilephone"]');
		validationError = true;
	}

	var exp = /^.* .*$/;
	if (!(exp.test($('input[name="billto_address1"]').val()))) {
		var fail = true;
		highlight('input[name="billto_address1"]');
		validationError = true;
	}

	if (validationError) {
		scrollToBillTo();
	}
}

$(document).ready(function() {

	$('#add_student').on('click', function() {
		addStudent();
	});

	// auto-expand comment areas
	var comment1 = document.getElementById('comment1');
	var heightLimit = 200; /* Maximum height: 200px */

	comment1.oninput = function() {{
		comment1.style.height = ""; /* Reset the height*/
		comment1.style.height = Math.min(comment1.scrollHeight, heightLimit) + "px";
	}};

	var student_same_as_bill_to = $('#student_same_as_bill_to')
	student_same_as_bill_to.change(function() {
		if (student_same_as_bill_to.is(':checked')) {
			$('#add_student').css('display','none')
			$('#student1').slideUp();
			$('#student2').slideUp();
			$('#student3').slideUp();
		}
		else {
			$('#add_student').removeClass('gray');
			$('#student1').slideDown(function() {
				$('#add_student').css('display','inherit');
			});
		}
	});

});