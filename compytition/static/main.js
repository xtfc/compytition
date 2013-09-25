function update_question(event) {
	if(event) event.preventDefault();
	if(this.hash) window.location.hash = this.hash;

	$('#questions .question').hide();
	$('#questions .question-button').removeClass('pure-menu-selected');
	$(window.location.hash + '-body').show();
	$(window.location.hash + '-button').addClass('pure-menu-selected');
}

function set_hash(event) {
	$('#submit_for')[0].value = window.location.hash.substr(1);
	return true;
}

function update_scoreboard() {
	$('#scoreboard').load('/scoreboard');
}
function update_status() {
	$('#status').load('/status');
}

$(function() {
	if($('#questions').length) {
		if(!window.location.hash) {
			window.location.hash = '#q1';
		}
		update_question();
		$('#questions .question-button a').click(update_question);
	}

	if($('#messages').length) {
		$('#messages').fadeOut(5000, function() {
			$(this).hide();
		});
	}

	if($('#scoreboard').length) {
		setInterval('update_scoreboard()', 5000);
	}
	if($('#status').length) {
		setInterval('update_status()', 5000);
	}
});
