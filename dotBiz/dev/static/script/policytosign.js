function highlight(field) {
	$(field).css('background', '#f5ed14');
}

function unhighlightInputs(form) {
	$('input[type="text"].signature-input').css('background','none');
	$('input[type="email"].signature-input').css('background','none');
}

function showPostSubmitMessage(blockToShow) {
	$('#' + blockToShow).css('display','inherit');

	// scroll to top
	$('html, body').animate({
		scrollTop: $("body").offset().top
	}, 800);
}

function submit() {
	$('input.animate.signaturesubmit').prop('type','image');
	$('input.animate.signaturesubmit').prop('src','/static/image/wait.gif');
	$('input.animate.signaturesubmit').css('padding','12px, 45px');
	$('input[type="image"].signaturesubmit').css('border','0');
	$('input.animate.signaturesubmit').prop('disabled',true);
	$.post('/sendmail/policyacceptance', {
		photo_release : $('input[name="photo_release"]:checked').map(function() {
			return this.value;
		}).get().join(),
		signature_name : $('input[name="signature_name"]').val(),
		signature_email : $('input[name="signature_email"]').val(),
		policy_content_text : window.policy_content_text,
		policy_content_html : window.policy_content_html
	})
	.done(function() {
		$('#sign input').prop('disabled', true);
		showPostSubmitMessage('submit_ok');
		$('#policy_content').slideUp()
	})
	.fail(function(data, textStatus, xhr) {
		$('hr').hide();
		$('.hideonfail').hide();
		showPostSubmitMessage('submit_fail');
	})
	.always(function() {
		$('input.animate.signaturesubmit').hide();
	});
}

function validateSignature() {
	var validationError = false;

	var exp = /^.* .*$/;
	if (!(exp.test($('input[name="signature_name"]').val()))) {
		var fail = true;
		highlight('input[name="signature_name"]');
		validationError = true;
	}

	var exp = /^.*@.*\..*$/;
	if (!(exp.test($('input[name="signature_email"]').val()))) {
		var fail = true;
		highlight('input[name="signature_email"]');
		validationError = true;
	}

	if (validationError) {
		alert('Sorry, some fields were not filled out correctly. Please correct information in the highlighted areas.');
	}
	else {
		submit();
	}
}

function add_content(content) {

	// fill main policy content
	$('#policy_content').html(content);

	// insert form contents after summary
	var policy_summary = $('#policy_content ul')[0];
	var signature_form_content = $('#signature_form_content').html();
	$(signature_form_content).insertAfter(policy_summary);

	// clear contents of hidden div to remove duplicate inputs
	$('#signature_form_content').html('');
}

function enableform() {
	$('input.btn.signaturesubmit').css('background-color', '#58a326');
	$('#pleasewait').hide();
	$('#disclaimer').show();
	$('#form_table').show();
}

$(document).ready(function() {
	var uri = '/api/db?identifier=lessons/policies';
	$.getJSON(uri)
	.done(function( data ) {
		content = $(data.content);
		content = content[2].innerHTML;
		// lame solution for emailing policy contents to client
		window.policy_content_html = content;
		window.policy_content_text = content.text;
		add_content(content);
		enableform();
	})
	.fail(function() {
		$('hr').hide();
		$('.hideonfail').hide();
	});

});
