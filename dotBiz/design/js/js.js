// THIS FILE OBSOLETE AS-IS. 

$(document).ready(function() {

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
		$(this).css("background", "url('images/a03.png') -186px -35px no-repeat");
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
		$(this).css("background", "url('images/a03.png') -125px -35px no-repeat");
	});

	$("#slides").slidesjs({
		play: {
			active: false,
			// [boolean] Generate the play and stop buttons.
			// You cannot use your own buttons. Sorry.
			effect: "slide",
			// [string] Can be either "slide" or "fade".
			interval: 8000,
			// [number] Time spent on each slide in milliseconds.
			auto: true,
			// [boolean] Start playing the slideshow on load.
			swap: true,
			// [boolean] show/hide stop and play buttons
			pauseOnHover: false,
			// [boolean] pause a playing slideshow on hover
			restartDelay: 2500
			// [number] restart delay on inactive slideshow
		},
		pagination: {
		active: false,
		effect: "slide"
		},
		navigation: {
			active: true,
			// [boolean] Generates next and previous buttons.
			// You can set to false and use your own buttons.
			// User defined buttons must have the following:
			// previous button: class="slidesjs-previous slidesjs-navigation"
			// next button: class="slidesjs-next slidesjs-navigation"
			effect: "slide"
			// [string] Can be either "slide" or "fade".
		},
		width: 696,
		height: 285,
		start: 3  
	});

});