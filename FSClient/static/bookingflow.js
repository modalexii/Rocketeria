$(document).ready(function(){

	(function($) {
		// .show() uses display:inline; we need inline-block
		$.fn.showinlineblock = function() {
			return this.css("display", "inline-block");
		};
	})(jQuery);

	$('input:radio[name="service"]').change( // when service changes
		function() {
			if ($(this).is(':checked')) {
				$("#employees").slideUp("fast"); // hide #employees (does nothing on first run)
				$("#calendar").slideUp("fast"); // hide #calendar (does nothing on first run)
				$("input[name='employee']").prop('checked', false); // uncheck employee button
				$.post("/api", { // get data from server
					'request' : 'whooffers',
					'serviceid' : $(this).val(),
				})
				.done(function(data) {
					loademployees(data);
				})
				.fail(function(textStatus, errorThrown) {
					alert(textStatus + ': ' + errorThrown); // temp debugging measure - alert() the error
				});
			}
		}
	);

	function loademployees(data) {
		$(".employee").each(function(index) {
			var employeeid = $(this).attr('id').substring(3)
			console.log('!>>' + employeeid);
			if (jQuery.inArray(parseInt(employeeid, 10), data) > -1 || parseInt(employeeid, 10) == 0) {
				$(this).showinlineblock();
			}
			else {
				$(this).hide();
			}
		});
		$("#employees").slideDown("slow");
	}

	$('input:radio[name="employee"]').change(
		function () {
			$('#calendar').slideUp("fast"); // hide #calendar (does nothing on first run)
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
			$.post("/api", {
				'request' : 'getopenings',
				'serviceid' : service,
				'employeeid' : employee,
			}, function (data) {
					$('#calendar').html(data);
					initMenu();
					$('#calendar').slideDown("slow"); // hide #calendar (does nothing on first run)
					$('#calendar').slideDown("slow");
					$("#calendar").animate({ scrollTop: $('#calendar')[0].scrollHeight}, 1000);
			}, 'html')
			.fail(function(xhr, textStatus, errorThrown) {
				alert(textStatus + ': ' + errorThrown);
			});
		}
	);
});
