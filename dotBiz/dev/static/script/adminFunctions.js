$(document).ready(function(){

	$('head').append('<link rel="stylesheet" type="text/css" href="/static/style/admin_bar.css">');

	function enterEditingMode(newPath) {
		$('#editthis').removeClass('admin_link');
		$('#editthis').html(
			'Save to: ' + window.location.hostname + '/' +
			'<input type="text" name="resource" value="' + newPath + '" />' +
			'<div id="save" class="admin_link">Save</div>' +
			'<div id="cancel" class="admin_link">Cancel</div>'
		);

		$('#editable').addClass('green_border');
		$('#editthis').addClass('yellow_bg');
		$('#cancel').removeClass('yellow_bg').addClass('red_bg');
		$('#deletethis').addClass('disabled');
		$('#deletethis').off('click');
		$('#newpage').addClass('disabled');
		$('#newpage').off('click');

		$('#save').on('click', function() {
			var resource = $.trim($('input[name="resource"]').prop('value'));
			if(resource == '') {
				alert('Please enter a URI for this page!');
				$('input[name="resource"]').addClass('highlight');
			}
			else {
				$.post('/modify/publish', {
					'content' : $('#editable').html(),
					'resource' : resource,
				})
				.done(function() {
					window.location.replace('/' + $.trim(resource));
				})
				.fail(function() {
					alert('Sorry, the save didn\'t go through. Check your internet connection, refresh and try again. If this condition persists, please file a bug.');
				});
			}
		});
		$('#admin_bar').append('<script type="text/javascript" src="/static/script/ckeditor/ckeditor.js"></script>');
		$('#cancel').on('click', function() {
			if(window.location.pathname === '/modify/new') {
				window.location.replace('/');
			}
			else {
				window.location.replace(window.location.pathname);
			}
		});
	}

	$('#newpage').on('click', function() {
		window.location.replace('/modify/new');
	});
	$('#signout').on('click', function() {
		window.location.replace('/modify/logout');
	});
	$('#bannersettings').on('click', function() {
		window.open('/modify/banner', 'banner', 'left=20,top=20,width=960,height=500,toolbar=1,resizable=0');
	})
	$('#upload').on('click', function() {
		window.open('/modify/upload', 'upload', 'left=20,top=20,width=500,height=500,toolbar=1,resizable=0');
	})


	if(editable_existing){
		$('#deletethis').click(function() {
			$.post('/modify/delete', {
				'resource' : window.location.pathname,
			})
			.done(function() {
				window.location.replace('/');
			})
			.fail(function() {
				alert('Sorry, the delete request didn\'t go through. Check your internet connection, refresh and try again. If this condition persists, please file a bug.');
			});
		});
		$('#editthis').on('click', function() {
			$('#editable').prop('contenteditable',true);
			enterEditingMode(newPath = window.location.pathname.replace('/',''));
		});
	}
	else if(new_editor) {
		$('#editable').prop('contenteditable',true);
		enterEditingMode(newPath = ' ');
		$('#deletethis').addClass('disabled');
	}
	else {
		$('#editthis').addClass('disabled');
		$('#deletethis').addClass('disabled');
	}

});