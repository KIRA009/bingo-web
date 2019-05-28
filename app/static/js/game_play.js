function rgba2hex( color_value ) {
  if ( ! color_value ) return false;
  var parts = color_value.toLowerCase().match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/),
      length = color_value.indexOf('rgba') ? 3 : 2;
  delete(parts[0]);
  for ( var i = 1; i <= length; i++ ) {
    parts[i] = parseInt( parts[i] ).toString(16);
    if ( parts[i].length == 1 ) parts[i] = '0' + parts[i];
  }
  return '#' + parts.join('').toUpperCase();
}

$('.align-middle').hover(function() {
  if (rgba2hex($(this).css('background-color')) == '#FFFFFF')
    return
  else 
    $(this).css({'background-color': 'grey', 'color': 'black'});
}, function() {
  if (rgba2hex($(this).css('background-color')) == '#FFFFFF')
    return
  else
    $(this).css({'background-color': '', 'color': ''});
});

$('.align-middle').click(function() {
  $('.align-middle').each(function() {
    if (!$(this).hasClass('old')) {
      $(this).css({'background-color': '', 'color': ''});
      $(this).removeClass('new');
    }
  });
  if (!$(this).hasClass('old'))
    $(this).addClass('new');
});