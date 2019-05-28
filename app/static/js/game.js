$('input[type="file"]').change(function() {
  $(this).siblings('input[type="submit"]').show();
});

$('#key').keyup(function() {
  l = $(this).val().length;
  if (l == '10')
    {
      $(this).removeClass('incorrect').removeClass('notcorrect');
      $(this).addClass('correct');
      $('.message').hide();
    }
  else if (l == 0) {
      $('.message').hide();
      $(this).removeClass('correct');
      $(this).addClass('incorrect');
    }
  else
    {
      $(this).removeClass('correct');
      $(this).addClass('incorrect');
      $(this).addClass('notcorrect');
      $('.message').show();
      $('.message').html('Key should be 10 characters long');
    }
})

var currentClass = '';
var num = 0;
var data = '';

$('.head').click(function() {
	$('.head').removeClass('active');
	$(this).addClass('active');	
	var cube = $('.cube');	
  	var face = $(this).attr('id');
  	var showClass = 'show-' + face;
  	if (currentClass != '') {
    	cube.removeClass(currentClass);
  	}
  	cube.addClass(showClass);
  	currentClass = showClass;
});

$('.align-middle').hover(function() {
  if ($(this).html() > 0)
    return
  else
    $(this).css({'background-color': 'grey', 'color': 'black'});
}, function() {
  if ($(this).html() > 0)
    return
  else
    $(this).css({'background-color': '', 'color': ''});
});

$('.align-middle').click(function() {
  if ($(this).html() > 0)
    return
  $(this).html(++num).css({'background-color': 'white', 'color': 'black'});
});

$('.reset').click(function() {
  $('.align-middle').html(0).css({'background-color': '', 'color': ''});
  num = 0;
  data = '';
  $('.message').html('');
});

$('.submit').click(function(e) {
  $('.align-middle').each(function() {
    if ($(this).html() == 0)
      return false
    data += $(this).html() + '+';
  });
  if (data == '') {
    $('.message').html('Fill all boxes before submitting!');
    e.preventDefault();
  }
  else
    $('input[name="data"]').val(data);
});