$(document).ready(function(){

	function enterEditingMode(newPath) {
		$('#editthis').removeClass('admin_link');
		$('#editthis').html(
			'Save to: ' + window.location.hostname + '/' +
			'<input type="text" name="resource" value="' + newPath + '" />' +
			'<div id="save" class="admin_link">Save</div><div id="cancel" class="admin_link">Cancel</div>'
		);
		$('#save').click(function(){
			var resource = $('input[name="resource"]').prop('value');
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
		});
		$('#cancel').click(function(){
			window.location.replace(window.location.pathname);
		});
	}

	if(editable_existing){
		$('#editthis').click(function() {
			$('#editable').prop('contenteditable',true);
			enterEditingMode(newPath = window.location.pathname.replace('/',''));
		});
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
	}
	else if(new_editor) {
		$('#editable').prop('contenteditable',true);
		enterEditingMode(newPath = ' ');
		$('#deletethis').addClass('disabled');
		$('#cancel').html('Start Over');
	}
	else {
		$('#editthis').addClass('disabled');
		$('#deletethis').addClass('disabled');
	}

	$('#newpage').click(function() {
		window.location.replace('/modify/new');
	});
	$('#signout').click(function() {
		window.location.replace('/_ah/login?continue=/&action=logout');
	});
	$('#upload').click(function() {
		window.open('/modify/upload', 'upload', 'left=20,top=20,width=500,height=500,toolbar=1,resizable=0');
	})
});