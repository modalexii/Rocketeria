$(document).ready(function(){
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
}