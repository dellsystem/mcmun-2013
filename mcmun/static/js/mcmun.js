$(document).ready(function() {
	var rotateTimeout = 3500;
	var firstDiv = $('#carousel-blocks div')[0];
	var timeout;

	$('#carousel-blocks div').click(function () {
		clearTimeout(timeout);
		$('.active').removeClass();
		$(this).addClass('active');
		$('#carousel-image').removeClass().addClass($(this).attr('data-image'));
		timeout = setTimeout(rotateCarousel, rotateTimeout);
	});


	var rotateCarousel = function () {
		var nextDiv = $('#carousel-blocks .active').next()[0] || firstDiv;
		timeout = setTimeout(rotateCarousel, rotateTimeout);
		$(nextDiv).click();
	};

	timeout = setTimeout(rotateCarousel, rotateTimeout);

	$('#sec-bios').delegate('.photo', 'click', function (event) {
		$('.active').removeClass('active');
		$('.bio').hide();
		$(this).addClass('active').next().show();
	});
});
