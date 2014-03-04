$(document).ready(function(){

	(function($) {
		// .show() uses display:inline; we need inline-block
		$.fn.showinlineblock = function() {
			return this.css("display", "inline-block");
		};
	})(jQuery);

	var selection = {};

	function initMenu() {
		var day = $('.day');
		day.hover(function() {window.status = $(this)}, function() {window.status = ""});
		
		$('.open').hide();

		day.click(
			function() {
				$(this).parents('div:eq(0)').find('.open').slideToggle('fast');	
			}
		);

		var fsevent = $('#calendar li.event');
		fsevent.click( // when calendar event is clicked
			function(open) { 
				var fsevent_button = $(this).children("input[type=radio]")
				fsevent_button.prop('checked',true);
				open.stopPropagation();
				selection['event_readable'] = fsevent_button.val(); // update selection
				selection['event_fs_at'] = fsevent_button.attr('id'); // update selection
				$.post("/api", {
					'request' : 'book',
				})
				.done(function(data) {
					load_confirmation(data);
				})
				.fail(function(textStatus, errorThrown) {
					console.log(textStatus + ': ' + errorThrown); // temp debugging measure
				});
			}
		);
	}

	$('input:radio[name="service"]').change( // when service changes
		function() {
			if ($(this).is(':checked')) {
				$("#confirmation").slideUp("fast"); // hide #confirmation (does nothing on first run)
				$("#calendar").slideUp("fast"); // hide #calendar (does nothing on first run)
				$("#employees").slideUp("fast"); // hide #employees (does nothing on first run)
				selection['service_name'] = $(this).val(); // update selection
				selection['service_fs_id'] = $(this).attr('id'); // update selection
				$("input[name='employee']").prop('checked', false); // uncheck employee button
				$.post("/api", { // get data from server
					'request' : 'whooffers',
					'serviceid' : selection['service_fs_id'],
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
			if (jQuery.inArray(parseInt(employeeid, 10), data) > -1 || parseInt(employeeid, 10) == 0) {
				$(this).showinlineblock();
			}
			else {
				$(this).hide();
			}
		});
		$("#employees").slideDown("slow");
	}

	function load_confirmation(data) {
		$('#confirmation').html('<div id="event_info">' + data + '</div><div id="booknow">Book Now</div>');
		var appt_details = "<h4>" + selection["service_name"] + " with " + selection["employee_name"] + "<br />" + selection["event_readable"] + "</h4>";
		$('#event_info').html(appt_details); // add confirmation information
		$("#confirmation").slideDown("slow");
		//console.log(selection)

		var submit = $('#book');
		submit.click( function() {
			$.post("/api", {
				'request' : 'book',
				'at' : selection['event_fs_at'],
				'service' : selection['service_fs_id'],
				'employee' : selection['employee_fs_id'],
				'right_to_contact' : $('input[name="right_to_contact"]').attr('checked'),
			})	
			.done(function(data) {
				alert(data);
			})
			.fail(function(textStatus, errorThrown) {
				console.log(textStatus + ': ' + errorThrown); // temp debugging measure
			});
		});
	}

	$('input:radio[name="employee"]').change(
		function () {
			$("#confirmation").slideUp("fast"); // hide #confirmation (does nothing on first run)
			$('#calendar').slideUp("fast"); // hide #calendar (does nothing on first run)
			var employee = "";
			var selectedemployee = $("input[type='radio'][name='employee']:checked");
			if (selectedemployee.length > 0) {
				employee = selectedemployee.val();
				selection['employee_name'] = $(this).val(); // update selection
				selection['employee_fs_id'] = selectedemployee.attr('id'); // update selection
			}
			//var service = "";
			//var selectedservice = $("input[type='radio'][name='service']:checked");
			//if (selectedservice.length > 0) {
			//	service = selectedservice.val();
			//}
			$.post("/api", {
				'request' : 'getopenings',
				'serviceid' : selection['service_fs_id'],
				'employeeid' : selection['employee_fs_id'],
			}, function (data) {
					$('#calendar').html(data);
					initMenu();
					$('#calendar').slideDown("slow"); // show #calendar)
			}, 'html')
			.fail(function(xhr, textStatus, errorThrown) {
				alert(textStatus + ': ' + errorThrown);
			});
		}
	);

	//$('input.notreschedulable').prop('disabled',true)
	//$('input.notreschedulable').attr('title', 'Sorry, this appointment cannot be rescheduled');

});
