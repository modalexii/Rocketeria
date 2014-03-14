$(document).ready(function(){

	(function($) {
		// .show() uses display:inline; we need inline-block
		$.fn.showinlineblock = function() {
			return this.css("display", "inline-block");
		};
	})(jQuery);

	// declare dict to hold the client's selections as we go
	var selection = {};

	// ----- services -----
	$('input:radio[name="service"]').change( // when service changes
		function() {
			if ($(this).is(':checked')) {
				// hide all other sections (does nothing on first run)
				$("#confirmation").slideUp("fast"); 
				$("#calendar").slideUp("fast");
				$("#employees").slideUp("fast");

				// update selection
				selection['service_name'] = $(this).val();
				selection['service_fs_id'] = $(this).attr('id');

				// uncheck employee button
				$("input[name='employee']").prop('checked', false); 

				// ask server who offers the selected service
				$.post("/api", { 
					'request' : 'whooffers',
					'serviceid' : selection['service_fs_id'],
				})
				.done(function(data) {
					// display relevant employees
					loademployees(data);
				})
				.fail(function(textStatus, errorThrown) {
					console.log(textStatus + ': ' + errorThrown);
				});
			}
		}
	);

	// ----- employees -----
	// called from services section
	function loademployees(data) {
		// all employee data was already downloaded, now display
		// only employees that offer the selected service
		$(".employee").each(function(index) {
			var employeeid = $(this).attr('id').substring(3)
			if (jQuery.inArray(parseInt(employeeid, 10), data) > -1
			|| parseInt(employeeid, 10) == 0) {
				$(this).showinlineblock();
			}
			else {
				$(this).hide();
			}
		});
		// open the employees section
		$("#employees").slideDown("slow");
		$('html,body').animate({ scrollTop: $('#employees').offset().top }, 'slow');
	}

	// ----- employees -----
	$('input:radio[name="employee"]').change(
		function () {
			// hide all following sections (does nothing on first run)
			$("#confirmation").slideUp("fast");
			$('#calendar').slideUp("fast");

			var selectedemployee = $("input[type='radio'][name='employee']:checked");
			if (selectedemployee.length > 0) {
				employee = selectedemployee.val();

				// update selection
				selection['employee_name'] = $(this).val(); 
				selection['employee_fs_id'] = selectedemployee.attr('id');
			}

			// ask the server for the selected employee's openings
			// currently this uses a backend-set range
			// later we will need to include a range parameter here
			// that can be used in ranges.getfsrange()
			$.post("/api", {
				'request' : 'getopenings',
				'serviceid' : selection['service_fs_id'],
				'employeeid' : selection['employee_fs_id'],
			})
			.done(function (data) {
				load_calendar(data);
			})
			.fail(function(xhr, textStatus, errorThrown) {
				alert(textStatus + ': ' + errorThrown);
			});
		}
	);

	// ----- calendar -----
	function load_calendar(html) {
		// data is html from events.makecal()
		$('#calendar').html(html);
		// spin up calendar script
		initMenu();
		// show #calendar
		$('#calendar').slideDown("slow");
		$('html,body').animate({ scrollTop: $('#calendar').offset().top }, 'slow');
	}

	// ----- calendar -----
	function initMenu() {
		var day = $('.day');
		day.hover(function() {
			window.status = $(this)
		}, 
		function() {
			window.status = ""
		});

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
				// update selection
				selection['event_readable'] = fsevent_button.val();
				// update selection
				selection['event_fs_at'] = fsevent_button.attr('id');
				// display the Book Now button and continue
				load_confirmation();
				$('html,body').animate({ scrollTop: $('#yourid').offset().top }, 'slow');
			}
		);
	}

	// ----- confirmation -----
	function load_confirmation() {
		// set up the details string using selection
		var appt_details = "<h3>" + selection["service_name"] + " with " 
		+ selection["employee_name"] + "<br />" + selection["event_readable"] 
		+ "</h3>";
		// insert the html in to #confirmation 
		// this is short, so there was no need to generate the html server-side
		// (hey look at us with our big boy jQuery pants on!)
		$('#confirmation').html(
			'<div id="event_info">' + appt_details + '</div><div id="booknow">Book Now</div><br /><br /><br /><hr />'
		);
		// show the confirmation section
		$("#confirmation").slideDown("slow");
		$('html,body').animate({ scrollTop: $('#confirmation').offset().top }, 'slow');
		//console.log(selection)

		stage_booknow();
	}

	// ----- confirmation -----
	function stage_booknow() {
		$('#booknow').click( function() {
			// ask the server to try to book the event
			$.post("/api", {
				'request' : 'book',
				'at' : selection['event_fs_at'],
				'service' : selection['service_fs_id'],
				'employee' : selection['employee_fs_id'],
				'right_to_contact' : $('input[name="right_to_contact"]').attr('checked'),
			})	
			.done(function(data) {
				if (data["status_code"] === 200) {
					// success
					alert('Confirmed! We\'ll see you ' + selection["event_readable"]);
					window.location.replace('/studentarea');
				}
				else {
					// fail
					// reason is _assumed_ to be that FullSlate bounced the
					// request on account of missing customer info, so fetch
					// the form to collect customer info
					load_client_info_form(data);
				}
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

	// ----- client info form  -----
	function load_client_info_form(html) {
		// prep the big submit button
		var submit = '<div id="#submit">Submit</div>'

		// add in form content from stage_booknow() & display the form section
		$('#book_response').html(html);
		$("#book_response").slideDown("slow");

		// Allow infinite additional student name fields to be added
		$('#add_student').click( function() {
			$('tr.student').after('\
				<tr>\
					<td class="label">\
						<label for="student">\
							Student Name\
						</label>\
					</td>\
					<td class="field">\
						<input type="text" class="student_name" value="" />\
					</td>\
				</tr>\
			');
		});

		stage_submit();
	}

	// ----- client info form  -----
	function stage_submit() {
		$('#submit').click( function() {
			// pack the contents of all Student Name fields into an array
			var children = [];
				$('.student').each(function(i, obj) { // add all students to array
					children.push(i);
				});

			// ask the server to try to book the event
			$.post("/api", {
				// this stuff is all still here, just hidden
				'request' : 'book',
				'at' : selection['event_fs_at'],
				'service' : selection['service_fs_id'],
				'employee' : selection['employee_fs_id'],
				'right_to_contact' : $('input[name="right_to_contact"]').attr('checked'),
				// new stuff from the form
				'children' : children,
				'holder1_first' : $('input[name="holder1_first"]').val(),
				'holder1_last' : $('input[name="holder1_last"]').val(),
				'holder2_first' : $('input[name="holder2_first"]').val(),
				'holder2_last' : $('input[name="holder2_last"]').val(),
				'phone_number' : $('input[name="phone_number"]').val(),
				'email' : $('input[name="email"]').val(),
				'street1' : $('input[name="street1"]').val(),
				'street2' : $('input[name="street2"]').val(),
				'city' : $('input[name="city"]').val(),
				'state' : $('input[name="state"]').val(),
				'postal_code' : $('input[name="postal_code"]').val(),
			})	
			.done(function(data) {
				if (data["status_code"] === 200) {
					// success
					alert('Confirmed! We\'ll see you ' + selection["event_readable"]);
					window.location.replace('/studentarea');
				}
				else {
					// fail
					// nothing useful is shown to the user if 
					// FullSlate bounces the request, so client-side
					// vallidation is important
					console.log("failed to book with POSTed data: ",data);
				}
			})
			.fail(function(textStatus, errorThrown) {
				console.log(textStatus + ': ' + errorThrown); // temp debugging measure
			});
		});
	}



	// this is for authstudentarea and should be moved when we break up the scripts
	$('#booknow_link').click( function() { window.location.replace('/lessons/book'); } )
});