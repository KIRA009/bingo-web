$('.menu').click(function() {
	if ($(this).parent().prop("tagName") == 'HEADER')
		$('#sidebar').toggleClass('active');
});
$('.close').click(function() {
	$('#sidebar').removeClass('active');
});
$('#rules').click(function() {
	$('.row').html('');
	$('.rules').show();
});