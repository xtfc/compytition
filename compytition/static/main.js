$(window).bind('hashchange', function() {
	$('#questions .question').hide();
	$('#questions .question-button').removeClass('pure-menu-selected');
	$(window.location.hash).show();
	$(window.location.hash + 'b').addClass('pure-menu-selected');
});

$(function() {
	var id = '#q1';
	if(window.location.hash) {
		id = window.location.hash;
	}
	$(id).show();
	$(id + 'b').addClass('pure-menu-selected');
});
