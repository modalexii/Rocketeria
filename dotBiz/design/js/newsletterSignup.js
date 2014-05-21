//
// OFFLINE/DESIGN environemnt
//

$(document).ready(function() {

	function submitNewsletterEmail(form) {
		var email = form.find('input[name="email"]').val();
		var container = form.parent()
		container.html('<div style="height:50%; margin-bottom:-6px;"></div><h3><img src="/static/image/wait.gif"></h3>');
		$.post('/api_proxy_pub/cc', {
			'email' : email
		})
		.done(function() {
			container.html('<h3><br/>Thanks :-)</h3>');
		})
		.fail(function(data, textStatus, xhr) {
			console.log(xhr); 
			switch (xhr) {
				// switch-case used to ease implementation of additional circumstantial return messages from ConCon API
				case 'Conflict':
					container.html('<h3>You\'re already<br/>on the list!</h3> <p style="text-align:center;">If you\'re not getting quarterly emails, check your Spam folder or click <u><a href="http://visitor.r20.constantcontact.com/manage/optin/ea?v=001Vzv-UqW3G56TS4HpjB5lNw%3D%3D" target="_blank">here</a></u> to update your profile.');
					break;
				default:
					container.html('<h3>Sorry, there was a problem :-/<br/><br/>Please click <a href="http://visitor.r20.constantcontact.com/manage/optin/ea?v=001Vzv-UqW3G56TS4HpjB5lNw%3D%3D" target="_blank"><u>here</u></a> to subscribe.</h3>');
			}
		});
		return false;
	}

	// auto-clear input
	$('input[name="email"]')
	.on('focus', function() {
		if (this.value == 'ENTER EMAIL') {
			this.value = '';
		}
	})
	.on('blur', function() {
		if (this.value == '') {
			this.value = 'ENTER EMAIL';
		}
	});

	$('form[name="newsletter"]').on('submit', function() {
		alert('Submit disabled in design environment.');
		// submitNewsletterEmail($(this)); // this is what would happen in an online environment
	});

});
