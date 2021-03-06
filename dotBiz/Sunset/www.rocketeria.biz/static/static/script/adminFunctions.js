function savePage() {
	var resource = $.trim($('input[name="resource"]').prop('value'));
	if(resource == '') {
		alert('Please enter a URI for this page!');
		$('input[name="resource"]').addClass('red_border');
	}
	else {
		$('#save').html('<img src="/static/image/wait.gif" style="padding-left:12px;padding-right:12px;"/>');
		$('#save').off('click');
		// the following assumes that all editable pages are identical
		// content has to be recreated
		// if it is captured with outerHTML, we get all the ckeditor junk too
		var content_template = '<div id="header-sub"><img class="bg-header-sub" src="{0}" width="705px" height="82px"/><h1>{1}</h1></div><!-- /header-sub --><div id="content_sub">{2}</div><!-- /content_sub -->'
		var CKEData = CKEDITOR.instances.content_sub.getData();
		var content = String.format(
			content_template,
			$('img.bg-header-sub').attr('src'),
			$('#header-sub h1').html(),
			CKEData
		);

		$.post('/modify/publish', {
			'content' : content,
			'resource' : resource,
		})
		.done(function() {
			window.location.replace('/' + $.trim(resource));
		})
		.fail(function() {
			alert('Sorry, the save didn\'t go through. Check your internet connection. If this condition persists, please file a bug.');
			$('#save').html('Save');
			$('#save').on('click', function() {
				savePage();
			});
		});
	}
}

function enterEditingMode(newPath) {
	$('#content_sub').prop('contenteditable',true);
	$('#header-sub h1').prop('contenteditable',true);
	$('#editthis').removeClass('admin_link');
	$('#editthis').html(
		'Save to: ' + window.location.hostname + '/' +
		'<input type="text" name="resource" value="' + newPath + '" />' +
		'<div id="save" class="admin_link">Save</div>' +
		'<div id="cancel" class="admin_link">Cancel</div>'
	);
	$('#editthis').addClass('yellow_bg');
	$('#cancel').removeClass('yellow_bg').addClass('red_bg');
	$('#deletethis').hide();
	$('#deletethis').off('click');
	$('#newpage').hide();
	$('#newpage').off('click');
	$('#bannersettings').hide();
	$('#bannersettings').off('click');
	$('#signout').hide();
	$('#signout').off('click');

	// Do not allow headers on these pages to change color
	var locked_header_color = ['/lessons','/store','/rentals','/events','/testimonials']
	if ($.inArray(window.location.pathname, locked_header_color) === -1) {
		$("img.bg-header-sub").on('click', function() {
			if ($("img.bg-header-sub").attr('src') === '/static/image/header-green.png') {
				$("img.bg-header-sub").attr('src','/static/image/header-blue.png');
			} 
			else if ($("img.bg-header-sub").attr('src') === '/static/image/header-blue.png') {
				$("img.bg-header-sub").attr('src','/static/image/header-yellow.png');
			}
			else if ($("img.bg-header-sub").attr('src') === '/static/image/header-yellow.png') {
				$("img.bg-header-sub").attr('src','/static/image/header-red.png');
			}
			else if ($("img.bg-header-sub").attr('src') === '/static/image/header-red.png') {
				$("img.bg-header-sub").attr('src','/static/image/header-purple.png');
			}
			else {
				$("img.bg-header-sub").attr('src','/static/image/header-green.png');
			}
		});
	}

	$('#save').on('click', function() {
		savePage();
	});

	$('#cancel').on('click', function() {
		if(window.location.pathname === '/modify/new') {
			window.location.replace('/');
		}
		else {
			window.location.replace(window.location.pathname);
		}
	});

	// Turn off automatic editor creation first.
	CKEDITOR.disableAutoInline = true;

	try {
		CKEDITOR.inline( 'content_sub' );
		//CKEDITOR.inline( 'content_sub' ); // + line for each div that should spawn a ck instance
	}
	catch(e) {
		console.log('Error attaching in-line editor: ' + e);
	}
}

$(document).ready(function(){

	// define pages that should have delete disabled
	var protectedPages = ["/lessons","/store","/rentals","/repairs","/events","/about","/contact","/testimonials"];

	if (!String.format) {
		// stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format
		String.format = function(format) {
			var args = Array.prototype.slice.call(arguments, 1);
			return format.replace(/{(\d+)}/g, function(match, number) { 
				return typeof args[number] != 'undefined'
					? args[number] 
					: match
				;
			});
		};
	}

	$('head').append('<link rel="stylesheet" type="text/css" href="/static/style/admin_bar.css">');
	$('head').append('<script type="text/javascript" src="/static/script/ckeditor/ckeditor.js"></script>');



	$('#newpage').on('click', function() {
		window.location.replace('/modify/new');
	});
	$('#signout').on('click', function() {
		window.location.replace('/modify/logout');
	});
	$('#bannersettings').on('click', function() {
		window.open('/modify/banner', 'banner', 'left=20,top=20,width=960,height=400,toolbar=0,menubar=0,resizable=0');
	});
	$('#upload').on('click', function() {
		window.open('/modify/upload', 'upload', 'left=20,top=20,width=500,height=500,toolbar=0,menubar=0,resizable=0');
	});
	$('.info').on('click', function() {
		window.open('/modify/info', 'info', 'left=20,top=20,width=500,height=500,toolbar=0,menubar=0,resizable=0');
	})
	$('.gcs_dir').on('click', function() {
		window.open('/dres/directory', 'directory', 'left=20,top=20,width=500,height=500,menubar=0,resizable=1');
	})

	if (editable_existing){
		if ($.inArray(window.location.pathname, protectedPages) === -1) {
			$('#deletethis').click(function() {
				if (confirm('Really delete ' + window.location.pathname + ' forever?')) {
					$.post('/modify/delete', {
						'resource' : window.location.pathname,
					})
					.done(function() {
						window.location.replace('/');
					})
					.fail(function() {
						alert('Sorry, the delete request didn\'t go through. Check your internet connection, refresh and try again. If this condition persists, please file a bug.');
					});
				}

			});
		}
		else {
			$('#deletethis').hide();
		}
		$('#editthis').on('click', function() {
			$('#editthis').off('click');
			enterEditingMode(newPath = decodeURIComponent(window.location.pathname.replace('/','')));
		});
	}
	else if (new_editor) {
		enterEditingMode(newPath = ' ');
	}
	else {
		$('#editthis').hide();
		$('#deletethis').hide();
	}

});