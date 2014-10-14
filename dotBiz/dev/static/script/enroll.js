function newsletterSignup() {
	if ($('input[name="billto_wants_newsletter"]').is(':checked')) {
		$.post('/api/external/cc', {
			'email' : $('input[name="billto_email"]').val(),
		})
	}
}

function showPostSubmitMessage(blockToShow) {
	$('#hide_on_submit').hide();
	$('#' + blockToShow).css('display','inherit');
	$('html, body').animate({
		scrollTop: $("body").offset().top
	}, 800);
}

function submit() {
	$('input.animate.enrollsubmit').prop('type','image');
	$('input.animate.signaturesubmit').prop('src','/static/image/wait.gif');
	$('input.animate.enrollsubmit').css('padding','12px, 45px');
	$('input[type="image"].enrollsubmit').css('border','0');
	$('input.animate.enrollsubmit').prop('disabled',true);
	$.post('/sendmail/enroll', {
		billto_firstandlast : $('input[name="billto_firstandlast"]').val(),
		billto_email : $('input[name="billto_email"]').val(),
		billto_mobilephone : $('input[name="billto_mobilephone"]').val(),
		billto_altphone : $('input[name="billto_altphone"]').val(),
		billto_address1 : $('input[name="billto_address1"]').val(),
		billto_address2 : $('input[name="billto_address2"]').val(),
		student_same_as_bill_to : $('input[name="student_same_as_bill_to"]').is(':checked'),
		student1_firstandlast : $('input[name="student1_firstandlast"]').val(),
		student1_email : $('input[name="student1_email"]').val(),
		student1_mobilephone : $('input[name="student1_mobilephone"]').val(),
		student1_altphone : $('input[name="student1_altphone"]').val(),
		student1_school : $('input[name="student1_school"]').val(),
		student1_grade : $('select[name="student1_grade"] option:selected').val(),
		student2_firstandlast : $('input[name="student2_firstandlast"]').val(),
		student2_email : $('input[name="student2_email"]').val(),
		student2_mobilephone : $('input[name="student2_mobilephone"]').val(),
		student2_altphone : $('input[name="student2_altphone"]').val(),
		student2_school : $('input[name="student2_school"]').val(),
		student2_grade : $('select[name="student2_grade"] option:selected').val(),
		student3_firstandlast : $('input[name="student3_firstandlast"]').val(),
		student3_email : $('input[name="student3_email"]').val(),
		student3_mobilephone : $('input[name="student3_mobilephone"]').val(),
		student3_altphone : $('input[name="student3_altphone"]').val(),
		student3_school : $('input[name="student3_school"]').val(),
		student3_grade : $('select[name="student3_grade"] option:selected').val(),
		lesson_environment : $('input[name="environment"]:checked').map(function() {
			return this.value;
		}).get().join(),
		instrument : $('input[name="instrument"]:checked').map(function() {
			return this.value;
		}).get().join(),
		expertise : $('input[name="expertise"]:checked').map(function() {
			return this.value;
		}).get().join(),
		teacher : $('input[name="teacher"]:checked').map(function() {
			return this.value;
		}).get().join(),
		recurrence : $('input[name="recurrence"]').val(),
		day_of_week : $('input[name="day_of_week"]:checked').map(function() {
			return this.value;
		}).get().join(),
		time_range : $('input[name="time_range"]:checked').map(function() {
			return this.value;
		}).get().join(),
		comment1 : $('textarea[name="comment1"]').val(),
		photo_release : $('input[name="photo_release"]:checked').map(function() {
			return this.value;
		}).get().join(),
	})
	.done(function() {
		showPostSubmitMessage('submit_ok');
	})
	.fail(function(data, textStatus, xhr) {
		showPostSubmitMessage('submit_fail');
	})
	.always(function() {
		$('input.animate.enrollsubmit').hide();
	});
	newsletterSignup();
}

function agreedToPolicies() {
	if ($('input[name="read_policies"]').is(':checked')) {
		return true;
	}
	else {
		return false;
	}
}

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
		alert('Sorry, some fields were not filled out correctly. Please correct information in the highlighted areas.');
		scrollToBillTo();
	}
	else {
		if (agreedToPolicies()) {
			submit();
		}
		else {
			highlight('.policy_checkbox');
			alert('Please confirm that you have read our Music Lessons Policies and are OK with them. Contact us before continuing if you have any questions or concerns.');
		}
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