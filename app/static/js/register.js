$email_reg = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;

$('#name input, #password input').keyup(function() {
	if ($(this).val() != '')
		{
			$(this).removeClass('incorrect');
			$(this).addClass('correct');
		}
	else
		{
			$(this).removeClass('correct');
			$(this).addClass('incorrect');
		}
})
$('#email input').keyup(function() {
	if ($email_reg.test($(this).val()))
		{
			$(this).removeClass('incorrect');
			$(this).addClass('correct');
		}
	else
		{
			$(this).removeClass('correct');
			$(this).addClass('incorrect');
		}
});
$('#cnfmpassword input').keyup(function() {
	if ($(this).val() == $('#password input').val() && $(this).val() != '')
		{
			$(this).removeClass('incorrect');
			$(this).addClass('correct');
		}
	else
		{
			$(this).removeClass('correct');
			$(this).addClass('incorrect');
		}
});