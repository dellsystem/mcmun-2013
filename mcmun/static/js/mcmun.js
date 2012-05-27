$(document).ready(function() {
	$('#carousel-blocks div').click(function () {
		$('#carousel-image').removeClass().addClass($(this).attr('data-image'));
	});
});
