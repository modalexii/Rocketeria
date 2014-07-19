$(document).ready(function() {
	$('head').append('<link rel="stylesheet" type="text/css" href="/static/script/datetimepicker/jquery.datetimepicker.css"/ >');
	var originalMakeup_diaclaimer = $('#makeup_disclaimer').html();
	jQuery('#datepicker').datetimepicker({
		timepicker:false,
			minDate:0,
			format:'m/d/Y',
			mask:true,
			yearStart:2014,
			yearEnd:2030,
			onClose:function(current_time,$input){
				if(current_time <= $.now()) {
					$('#makeup_disclaimer').html('I understand that under the terms of Rocketeria\'s <a href="/lessons/policy" target="_blank">Music Lessons Policies</a>, same-day cancellations are not elidgible for make-ups.');
				}
				else {
					$('#makeup_disclaimer').html(originalMakeup_diaclaimer);
				}
		}
	});
	jQuery('#timepicker').datetimepicker({
		datepicker:false,
			step:30,
			format:'H:i',
			mask:true,
			hours12:true,
	});

	// auto-clear input
	$('input[name="account_name"]')
	.on('focus', function() {
		if (this.value == 'Last, First') {
			this.value = '';
		}
	})
	.on('blur', function() {
		if (this.value == '') {
			this.value = 'Last, First';
		}
	});

	$('input[name="student_name"]')
	.on('focus', function() {
		if (this.value == 'Last, First') {
			this.value = '';
		}
	})
	.on('blur', function() {
		if (this.value == '') {
			this.value = 'Last, First';
		}
	});
	$('#change_one_btn').on('click', function() {
		$(this).css('background-color', '#96231f');
		$(this).css('border', '3px solid #0f0403');
		$('#change_all_btn').css('background-color', '#58a326');
		$('#change_all_btn').css('border', '3px solid #ddd');
		if ($('#change_one_form').css('display') == 'none') {
			$('#change_all_form').slideUp(function() {
				$('#change_one_form').slideDown();
			});
		}
	});
	$('#change_all_btn').on('click', function() {
		$(this).css('background-color', '#96231f');
		$(this).css('border', '3px solid #0f0403');
		$('#change_one_btn').css('background-color', '#58a326');
		$('#change_one_btn').css('border', '3px solid #ddd');
		if ($('#change_all_form').css('display') == 'none') {
			$('#change_one_form').slideUp(function() {
				$('#change_all_form').slideDown();
			});
		}
	});

});

function showPostSubmitNote(contextMessage) {
	$('#form_switch_buttons').slideUp();
	$('input.animate.changesubmit').slideUp();
	$('.validation_fail').slideUp();
	$('#' + contextMessage).slideDown();
}

function highlight(field) {
	$(field).css('background', '#f5ed14');
}

function unhighlightInputs(form) {
	$('#' + form + ' input[type="text"]').css('background','none');
	$('#' + form + ' input[type="text"]').css('background','none');
}

function sendChangeRequest(form) {
	$('input.animate.changesubmit').prop('type','image');
	$('input.animate.changesubmit').prop('src','/static/image/wait.gif');
	$('input[type="image"].changesubmit').css('padding','12px, 45px');
	$('input[type="image"].changesubmit').css('border','0');
	if (form === 'change_one_form'){
		$.post('/sendmail/changerequest', {
			account_name : $('input[name="account_name"]').val(),
			student_name : $('input[name="student_name"]').val(),
			lesson_day : $('input[name="lesson_date"]').val(),
			lesson_time : $('input[name="lesson_time"]').val(),
		})
		.done(function() {
			showPostSubmitNote('submit_ok_one');
		})
		.fail(function(data, textStatus, xhr) {
			showPostSubmitNote('fail');
		});
	}
	else if (form === 'change_all_form') {
		$.post('/sendmail/changerequest', {
			account_name : $('input[name="account_name"]').val(),
			student_name : $('input[name="student_name"]').val(),
			requested_action : $('input[name="requested_action"]').val(),
			pref_contact : $('input[name="pref_contact"]').val(),
		})
		.done(function() {
			showPostSubmitNote('submit_ok_all');
		})
		.fail(function(data, textStatus, xhr) {
			showPostSubmitNote('fail');
		});

	}
}

function validateChangeRequest(form) {
	unhighlightInputs(form);
	var exp = /^.*,.*$/;
	if (!(exp.test($('#' + form + ' input[name="account_name"]').val()))) {
		var fail = true;
		highlight('#' + form + ' input[name="account_name"]');
	}
	if (!(exp.test($('#' + form + ' input[name="student_name"]').val()))) {
		var fail = true;
		highlight('#' + form + 'input[name="student_name"]');
	}
	var exp = /^Last, First$/;
	if (exp.test($('#' + form + ' input[name="account_name"]').val())) {
		var fail = true;
		highlight('#' + form + ' input[name="account_name"]');
	}
	if (exp.test($('#' + form + ' input[name="student_name"]').val())) {
		var fail = true;
		highlight('#' + form + ' input[name="student_name"]');
	}
	if (form === 'change_one_form') {
		exp = /^[0-2][0-9]\/[0-3][0-9]\/20[1-2][0-9]$/;
		if (!(exp.test($('#' + form + ' input[name="lesson_date"]').val()))) {
			var fail = true;
			highlight('#' + form + ' input[name="lesson_date"]');
		}
		exp = /^[0-1][0-9]:[0-5][0-9]$/;
		if (!(exp.test($('#' + form + ' input[name="lesson_time"]').val()))) {
			var fail = true;
			highlight('#' + form + ' input[name="lesson_time"]');
		}

	}
	if (fail) {
		$('.validation_fail').html('<p style="color: #96231f; font-family: \'Quicksandbold\', sans-serif;">Some of the data above doesn\'t make sense. Please review the highlighted fields.</p><br/>');
	}
	else {
		console.log('moving to send request');
		sendChangeRequest(form);
	}
}
