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
				load_confirmation();
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

	function load_confirmation() {
		var appt_details = "<h3>" + selection["service_name"] + " with " + selection["employee_name"] + "<br />" + selection["event_readable"] + "</h3>";
		$('#confirmation').html(
			'<div id="event_info">' + appt_details + '</div><div id="booknow">Book Now</div><br /><br /><br /><hr />'
			);
		$("#confirmation").slideDown("slow");
		//console.log(selection)

		$('#booknow').click( function() {
			$.post("/api", {
				'request' : 'book',
				'at' : selection['event_fs_at'],
				'service' : selection['service_fs_id'],
				'employee' : selection['employee_fs_id'],
				'right_to_contact' : $('input[name="right_to_contact"]').attr('checked'),
			})	
			.done(function(data) {
				// show whatever data was returned
				load_client_info_form(data);
			})
			.fail(function(textStatus, errorThrown) {
				console.log(textStatus + ': ' + errorThrown); // temp debugging measure
			});
			// hide everything thus far, in paralell with the POST request
			$("#services").slideUp("fast");
			$("#employees").slideUp("fast");
			$("#calendar").slideUp("fast");
			$("#confirmation").slideUp("fast");
			$("#book_response").slideUp("fast");
		});
	}

	function load_client_info_form(hmtl) {
		var heading = '<h2>Almost there!</h2><p>Please fill out all required (*) fields:</p>'
		var submit = '<div id="#submit">Submit</div>'
		$('#book_response').html(heading + html)
		$("#book_response").slideDown("slow");
		$('#add_student').click function() {
			$('#students').add('<tr><td class="label"><label for="student">Student Name</label></td><td class="field"><input type="text" class="student_name" value="%s" /></td></tr>')
		}
		$('#submit').click( function() {
			$.post("/api", {
				// this stuff is all still here, just hidden
				'request' : 'book',
				'at' : selection['event_fs_at'],
				'service' : selection['service_fs_id'],
				'employee' : selection['employee_fs_id'],
				'right_to_contact' : $('input[name="right_to_contact"]').attr('checked'),
				// new stuff from the form
				children = []
				$('.testimonial').each(function(i, obj) {
					children.push(i);
				});
				'holder1_first' : $('input[name="holder1_first"]').val(),
				'holder1_last' : $('input[name="holder1_last"]').val(),
				'holder2_first' : $('input[name="holder2_first"]').val(),
				'holder2_last' : $('input[name="holder2_last"]').val(),
				'phone' : $('input[name="phone"]').val(),
				'email' : $('input[name="email"]').val(),
				'street1' : $('input[name="street1"]').val(),
				'street2' : $('input[name="street2"]').val(),
				'city' : $('input[name="city"]').val(),
				'state' : $('input[name="state"]').val(),
				'postal_code' : $('input[name="postal_code"]').val(),
			})	
			.done(function(data) {
				console.log(data)
				//redirect to authstudentarea?
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