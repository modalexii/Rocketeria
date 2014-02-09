$(document).ready(function(){

	(function($) {
		$.fn.displayinlineblock = function() {
			return this.css("display", "inline-block");
		};
	})(jQuery);

	$('input:radio[name="service"]').change(
		function() {
			if ($(this).is(':checked')) {
				$("#employees").slideUp("slow");
				$.post("/lessons/api", {
					'request' : 'whooffers',
					'serviceid' : $(this).val(),
				})
				.done(function (data) {
					$(".employee").each(function(index) {
						var employeeid = $(this).attr('id').substring(3)
						console.log('!>>' + employeeid);
						if (jQuery.inArray(parseInt(employeeid, 10), data) > -1 || parseInt(employeeid, 10) == 0) {
							$(this).displayinlineblock();
						}
						else {
							$(this).hide();
						}
					});
					$("#employees").slideDown("slow");
				})
				.fail(function(xhr, textStatus, errorThrown) {
					alert(textStatus + ': ' + errorThrown);
				});
			}
		}
	);

	$('input:radio[name="employee"]').change(
		function () {
			var employee = "";
			var selectedemployee = $("input[type='radio'][name='employee']:checked");
			if (selectedemployee.length > 0) {
				employee = selectedemployee.val();
			}
			var service = "";
			var selectedservice = $("input[type='radio'][name='service']:checked");
			if (selectedservice.length > 0) {
				service = selectedservice.val();
			}
			$.post("/lessons/api", {
				'request' : 'getopenings',
				'serviceid' : service,
				'employeeid' : employee,
			})
			.done(function (xhr, data) {
					alert(xhr.responseText + data);
			})
			.fail(function(xhr, textStatus, errorThrown) {
				alert(textStatus + ': ' + errorThrown);
			});
		}
	);
});