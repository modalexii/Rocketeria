window.onload = function() {

	var head = document.getElementsByTagName('head')[0];
	setTimeout(function() {
		// image
		new Image().src = '/static/image/wait.gif';
		new Image().src = '/static/image/header-blue.png';
		new Image().src = '/static/image/header-green.png';
		new Image().src = '/static/image/header-red.png';
		new Image().src = '/static/image/header-purple.png';
		new Image().src = '/static/image/header-yellow.png';
	}, 1000);

	if (document.location.pathname !== '/') {
		// preload billboard 
		setTimeout(function() {
			var slides  = document.createElement('script');
			slides.type = 'text/javascript';
			slides.src  = '/static/script/jquery.slides.js';
			new Image().src = '/static/image/billboard-home.png';
		}, 2000);

		setTimeout(function() {
			// preload home tiles
			new Image().src = '/static/image/bg-newsletter-red.png';
			new Image().src = '/static/image/bg-social-yellow.png';
			new Image().src = '/static/image/bg-store.png';
			new Image().src = '/static/image/bg-lessons.png';
			new Image().src = '/static/image/bg-rentals.png';
			new Image().src = '/static/image/bg-events.png';
			new Image().src = '/static/image/bg-testimonials.png';
		}, 3000);
	}
	else if (document.location.pathname === '/') {
		setTimeout(function() {
			// preload sidebar
			new Image().src = '/static/image/bg-testimonials-2.png';
		}, 2000);
	}

};