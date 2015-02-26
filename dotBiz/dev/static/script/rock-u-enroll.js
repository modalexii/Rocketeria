
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
	$.post('https://docs.google.com/a/rocketeria.biz/spreadsheet/formResponse?formkey=dEMyUHZ1cmx1cWcwQWhJaFNldEZzSVE6MQ&amp;theme=0AX42CRMsmRFbUy03NTAzM2Q4My03ODU1LTQ2NzItODI2YS1kZmU5YzdiMzZjOGQ&amp;ifq', {
		// 1st pref
		'entry.2.single' : $('select[name="entry.2.single"] option:selected').val(),
		// 2nd pref
		'entry.3.single' : $('select[name="entry.3.single"] option:selected').val(),
		// 3rd pref
		'entry.5.single' : $('select[name="entry.5.single"] option:selected').val(),
		// student name
		'entry.7.single' : $('input[name="entry.7.single"]').val(),
		// student age
		'entry.15.single' : $('input[name="entry.15.single"]').val(),
		// student instrument
		'entry.14.single' : $('input[name="entry.14.single"]').val(),
		// sutdent experience
		'entry.16.group' : $('input[name="entry.16.group"]:checked').val(),
		// parent name
		'entry.8.single' : $('input[name="entry.8.single"]').val(),
		// parent email
		'entry.11.single' : $('input[name="entry.11.single"]').val(),
		// parent mobile phone
		'entry.9.single' : $('input[name="entry.9.single"]').val(),
		// parent alt phone
		'entry.10.single' : $('input[name="entry.10.single"]').val(),
		// comment
		'entry.18.single' : $('textarea[name="entry.18.single"]').val(),
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
}

function setReqdAsterisk(container) {
	$(container).html('<span class="reqd_asterisk">&ast;</span>');
}

function removeReqdAsterisk(container) {
	$(container).html('&nbsp;');
}

function validateEnroll() {
	var validationError = false;

	// 1st pref
	if ($('select[name="entry.2.single"] option:selected').val() !== "") {
		removeReqdAsterisk('#entry_2_astr');
	}
	else {
		var fail = true;
		setReqdAsterisk('#entry_2_astr');
		validationError = true;
	}

	// student name
	var exp = /.*[,| ].*$/;
	if (exp.test($('input[name="entry.7.single"]').val())) {
		removeReqdAsterisk('#entry_7_astr');
	}
	else {
		var fail = true;
		setReqdAsterisk('#entry_7_astr');
		validationError = true;
	}

	// student age
	var exp = /[0-9].*$/;
	if (exp.test($('input[name="entry.15.single"]').val())) {
		removeReqdAsterisk('#entry_15_astr');
	}
	else {
		var fail = true;
		setReqdAsterisk('#entry_15_astr');
		validationError = true;
	}

	// student instrument
	var exp = /.*$/;
	if (exp.test($('input[name="entry.14.single"]').val())) {
		removeReqdAsterisk('#entry_14_astr');
	}
	else {
		var fail = true;
		setReqdAsterisk('#entry_14_astr');
		validationError = true;
	}

	// parent name
	var exp = /.*[,| ].*$/;
	if (exp.test($('input[name="entry.8.single"]').val())) {
		removeReqdAsterisk('#entry_8_astr');
	}
	else {
		var fail = true;
		setReqdAsterisk('#entry_8_astr');
		validationError = true;
	}

	// parent email
	var exp = /^.+\@.+\..+$/;
	if (exp.test($('input[name="entry.11.single"]').val())) {
		removeReqdAsterisk('#entry_11_astr');
	}
	else {
		var fail = true;
		setReqdAsterisk('#entry_11_astr');
		validationError = true;
	}

	// parent mobile phone
	var exp = /^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/;
	if (exp.test($('input[name="entry.9.single"]').val())) {
		removeReqdAsterisk('#entry_9');
	}
	else {
		var fail = true;
		setReqdAsterisk('#entry_9');
		validationError = true;
	}

	if (validationError) {
		alert('Sorry, some fields were not filled out correctly. Please correct all fields marked with an asterisk (*).');
	}
	else {
		submit();
	}

}

function activateComponentNote() {
	// auto-expand comment area
	var comment1 = document.getElementById('comment1');
	var heightLimit = 200; /* Maximum height: 200px */

	comment1.oninput = function() {
		comment1.style.height = ""; /* Reset the height*/
		comment1.style.height = Math.min(comment1.scrollHeight, heightLimit) + "px";
	};
}

$(document).ready(function() {

		activateComponentNote();

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