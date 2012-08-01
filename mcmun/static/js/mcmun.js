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

	// Show the person's title upon hovering over the photo
	$('#sec-bios').delegate('.photo', 'mouseenter', function (event) {
		var title = $(this).next().find('h3').text();
		$(this).append('<div class="title-hover">' + title + '</div>');
		$('.title-hover').fadeIn(300);
	});

	$('#sec-bios').delegate('.photo', 'mouseleave', function (event) {
		$('.title-hover').remove();
	});

	$('#sec-bios').delegate('.photo', 'click', function (event) {
		$('.active').removeClass('active');
		$('.bio').hide();
		$(this).addClass('active').next().show();
	});

	var delegationFee = 75;

	$('#fee-calculator').delegate('select', 'change', function (event) {
		var numDelegates = parseInt($('#num-delegates option:checked').val(), 10);
		var registrationType = $('#registration-type option:checked').val();

		// Only show the fee information stuff when everything has been selected
		if (numDelegates > 0 && registrationType !== '') {
			var delegateFee, totalFee, deposit, remainder;

			switch (registrationType) {
				case 'priority':
					delegateFee = 80;
				break;
				case 'regular':
					delegateFee = 95;
				break;
				case 'international':
					delegateFee = 50;
				break;
			}

			if (delegateFee) {
				totalFee = numDelegates * delegateFee + delegationFee;
				deposit = delegationFee + (numDelegates * delegateFee) * 0.5;
				remainder = totalFee - deposit;
				$('#fee-information').text('Your total fee, for ' + numDelegates + ' delegates and ' + registrationType + ' registration, is $' + totalFee.toFixed(2) + '. If you wish to pay using the tiered system, your deposit would be $' + deposit.toFixed(2) + ', and the remainder would be $' + remainder.toFixed(2) + '.');
			} else {
				// Someone is mucking about with the form
				$('#fee-information').text("Please stop messing with the form. There's nothing interesting here.");
			}
			$('#fee-information').show();
		}
	});

	// Handle stuff for the registration form
	var priorityOption = $('#priority-dt');
	if (priorityOption.length) {
		// Has to be done this way for now because dl only allows dt, dd (fix later)
		priorityOption.hide().next().hide();
		$('#id_country').change(function () {
			var country = $(this).val();

			// The priority registration option is only valid for North America
			if (country === 'CA' || country === 'US') {
				priorityOption.show().next().show();
			} else {
				priorityOption.hide().next().hide();
			}
		});
	}
});
