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
	$('input.animate.policytosignsubmit').prop('type','image');
	$('input.animate.signaturesubmit').prop('src','/static/image/wait.gif');
	$('input.animate.policytosignsubmit').css('padding','12px, 45px');
	$('input[type="image"].policytosignsubmit').css('border','0');
	$('input.animate.policytosignsubmit').prop('disabled',true);

	// gmail interprets br as old message
	var policyContentHTMLNoBR = $('#policy_content').clone();
	policyContentHTMLNoBR.find('br').remove();

	$.post('/sendmail/policytosign', {
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
		comment1 : $('textarea[name="comment1"]').val(),
		no_chargeaccount : $('input[name="no_chargeaccount"]').is(':checked'),
		no_media_release : $('input[name="no_media_release"]').is(':checked'),
		digital_signature_name : $('input[name="digital_signature_name"]').val(),
		policy_content_text : $('#policy_content').text,
		policy_content_html : policyContentHTMLNoBR.html(),
		no_machines : $('input[name="no_machines"]').val(),
	})
	.done(function() {
		showPostSubmitMessage('submit_ok');
	})
	.fail(function(data, textStatus, xhr) {
		showPostSubmitMessage('submit_fail');
	})
	.always(function() {
		$('input.animate.policytosignsubmit').hide();
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
		alert('More then 3 students? Give us a call.')
	}
	else if ($('#student2').is(':visible')) {
		$('#student3').slideDown(function() {
			$('#add_student').addClass('gray');
		});
	} else {
		$('#student2').slideDown();
	}
}

function setReqdAsterisk(container) {
	$(container).html('<span class="reqd_asterisk">&ast;</span>');
}

function removeReqdAsterisk(container) {
	$(container).html('&nbsp;');
}


function scrollToBillTo() {
	$('html, body').animate({
		scrollTop: $("#billto_heading").offset().top
	}, 800);
}

function validatepolicytosign() {
	var validationError = false;


	var exp = /.*[,| ].*$/;
	if (exp.test($('input[name="billto_firstandlast"]').val())) {
		removeReqdAsterisk('#reqd_billto_firstandlast');
	}
	else {
		var fail = true;
		setReqdAsterisk('#reqd_billto_firstandlast');
		validationError = true;
	}

	var exp = /^.+\@.+\..+$/;
	if (exp.test($('input[name="billto_email"]').val())) {
		removeReqdAsterisk('#reqd_billto_email');
	}
	else {
		var fail = true;
		setReqdAsterisk('#reqd_billto_email');
		validationError = true;
	}

	var exp = /^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/;
	if (exp.test($('input[name="billto_mobilephone"]').val())) {
		removeReqdAsterisk('#reqd_billto_mobilephone');
	}
	else {
		var fail = true;
		setReqdAsterisk('#reqd_billto_mobilephone');
		validationError = true;
	}

	var exp = /^.* .*$/;
	if (exp.test($('input[name="billto_address1"]').val())) {
		removeReqdAsterisk('#reqd_billto_address1');
	}
	else {
		var fail = true;
		setReqdAsterisk('#reqd_billto_address1');
		validationError = true;
	}

	var exp = /^.* .*$/;
	if (exp.test($('input[name="billto_address2"]').val())) {
		removeReqdAsterisk('#reqd_billto_address2');
	}
	else {
		var fail = true;
		setReqdAsterisk('#reqd_billto_address2');
		validationError = true;
	}

	if (validationError) {
		alert('Sorry, some fields were not filled out correctly. Please correct all fields marked with an asterisk (*).');
		scrollToBillTo();
	}
	else {
		if ($('#digital_signature_name').val()) {
			submit();
		}
		else {
			alert('Please type your full name on the signature line to indicate that you have read and agree to abide by our Music Lessons Policies. Contact us before continuing if you have any questions or concerns.');
		}
	}

}

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
}

function addPolicyContent() {
	// fetch the Policy content 
	var uri = '/api/db?identifier=lessons/policies';
	$.getJSON(uri)
	.done(function( data ) {
		var content = $(data.content);
		content = content[2].innerHTML;
		// lame solution for emailing policy contents to client
		//window.policy_content_html = content;
		//window.policy_content_text = content.text;
		$('#policy_content').html(content);
	})
}

function activateComponentBillto() {}

function activateComponentStudent() {
	// show 2nd, 3rd student fields on click
	$('#add_student').on('click', function() {
		addStudent();
	});
}

function activateComponentStudents() {}

function activateComponentChargeAccount() {}

function activateComponentRelease() {}

function activateComponentNote() {
	// auto-expand comment area
	var comment1 = document.getElementById('comment1');
	var heightLimit = 200; /* Maximum height: 200px */

	comment1.oninput = function() {
		comment1.style.height = ""; /* Reset the height*/
		comment1.style.height = Math.min(comment1.scrollHeight, heightLimit) + "px";
	};
}

function activateComponentPolicy() {
	// fetch the Policy content from the API & add it to the page
	addPolicyContent();
}

function processActiveBlocks(activeBlocks) {
	/* 
	show/hide pieces of the form based on the URL parameter,
	and run any other schript needed by visible areas.

	possible active blocks:
	billto, student, programs, schedule, note, release, policy 
	*/

	if($.inArray('billto',activeBlocks) === -1) {
		$('.component_billto').remove();
	}
	else {
		activateComponentBillto();
	}

	if($.inArray('student',activeBlocks) === -1) {
		$('.component_student').remove();
	}
	else {
		activatecomponentStudent();

		// if Bill To is shown, disable Student inputs when Same as Bill To
		// is checked
		if($.inArray('billto',activeBlocks) === -1) {
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
		}
		else {
			// Bill To is not shown, so remove the Same as Bill To option
			$('.student_same_as_bill_to').remove();
		}
	}

	if($.inArray('note',activeBlocks) === -1) {
		$('.component_note').remove();
	}
	else {
		activateComponentNote();
	}

	if($.inArray('chargeaccount',activeBlocks) === -1) {
		$('.component_chargeaccount').remove();
	}
	else {
		activateComponentChargeAccount();
	}

	if($.inArray('release',activeBlocks) === -1) {
		$('.component_release').remove();
	}
	else {
		activateComponentRelease();
	}

	if($.inArray('policy',activeBlocks) === -1) {
		$('.component_policy').remove();
	}
	else {
		activateComponentPolicy();
	}

}

$(document).ready(function() {

	// if show param is given we MAY need to fetch policy content,
	// but if show isn't given, we MUST fetch policy content

	if (getURLParameter('show')) {
		activeBlocks = getURLParameter('show').split(',');
		processActiveBlocks(activeBlocks);
	}
	else {
		// actiate everything
		activateComponentBillto();
		activateComponentStudent();
		activateComponentNote();
		activateComponentChargeAccount();
		activateComponentRelease();
		activateComponentPolicy();
	}

});

WebFontConfig = {
	google: { families: [ 'Dawning+of+a+New+Day::latin' ] }
};
(function() {
	var wf = document.createElement('script');
	wf.src = ('https:' == document.location.protocol ? 'https' : 'http') +
	  '://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js';
	wf.type = 'text/javascript';
	wf.async = 'true';
	var s = document.getElementsByTagName('script')[0];
	s.parentNode.insertBefore(wf, s);
})();

// hold the active blocks (GET param) that we need to show/hide, run additional script on, and validate
var activeBlocks = [];