
$(document).ready(function(){
	$('#banner').addClass('red_bg');
	$('input[name="banner_color"]').change(function () {
		$('#banner').removeClass('red_bg yellow_bg green_bg blue_bg plain_bg').addClass($(this).val());
	});
	$('input[name="text_color"]').change(function () {
		$('#banner').removeClass('white_txt black_txt red_txt').addClass($(this).val());
	});

	jQuery('#datetimepicker').datetimepicker({
		timepicker : false,
		format : 'd/m/Y'
	});

	$('#post').click(function(){
		$.post('/modify/banner', {
			'state' : $('input[name="state"]:checked').val(),
			'banner_bg' : $('input[name="banner_color"]:checked').val(),
			'text_color' : $('input[name="text_color"]:checked').val(),
			'message' : $('#banner').html(),
			'expire' : $('input[name="expire"]').val(),
		})
		.done(function() {
			alert('Banner Updated. Refresh the home page to inspect it.');
			window.close();
		})
		.fail(function() {
			alert('Sorry, the update didn\'t go through. Check your internet connection and try again. If this condition persists, please submit a bug report.');
			window.close();
		});
	});
	$('#cancel').click(function(){
		window.close();
	});

	$('input[name="state"]').change(function () {
		if ($('input[name="state"]:checked').val() === 'off') {
			$('input[name="banner_color"]').each( function() {
				$(this).prop('disabled', true);
			});
			$('input[name="text_color"]').each( function() {
				$(this).prop('disabled', true);
			});
			$('input[name="expire"]').prop('disabled', true);
			$('#banner').addClass('disabled');
		}
		else {
			$('input[name="banner_color"]').each( function() {
				$(this).prop('disabled', false);
			});
			$('input[name="text_color"]').each( function() {
				$(this).prop('disabled', false);
			});
			$('input[name="expire"]').prop('disabled', false);
			$('#banner').removeClass('disabled');
		}
	});

});
