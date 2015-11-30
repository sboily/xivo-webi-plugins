$(function(){
  $('a.icon').on('click', function(){
    return confirm('Are you sure?');
  });

  $('#popover').popover('show');

});
