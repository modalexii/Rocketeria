$(document).ready(function() {

	//
	// indent your script, you animal!
	//

	$(".arrow-next").mouseenter(function() {
		$(this).css("background", "url('images/a03.png') -186px -35px no-repeat");
	})
	.mouseleave(function(){
		$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
	});

	$(".arrow-next").mousedown(function() {
		$(this).css("background", "url('images/a03.png') -66px -35px no-repeat");
	})
	.mouseup(function(){
		$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
	});

	$(".arrow-previous").mouseenter(function() {
		$(this).css("background", "url('images/a03.png') -125px -35px no-repeat");
	})
	.mouseleave(function() {
		$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
	});

	$(".arrow-previous").mousedown(function(){
		$(this).css("background", "url('images/a03.png') -5px -35px no-repeat");
	})
	.mouseup(function(){
		$(this).css("background", "url('images/a03.png') 55px -35px no-repeat");
	});

	$("#lightbox-shadow").click(function() {
		$("#lightbox-1").css("display", "none");
		$("#lightbox-2").css("display", "none");
		$("#lightbox-3").css("display", "none");
		$("#lightbox-shadow").css("display", "none");
	});

});