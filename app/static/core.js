$(function() {
	
	$('#images').sortable({
		
		start: function(event, ui) {
			ui.item.addClass('active');
		},
		stop: function(event, ui) {
			ui.item.removeClass('active').effect(
				'highlight', 
				{ color : '#000' }, 1000, function() {
				$.each($('#images li'), function(index, event) {
					$(this).children('.order').val(parseInt(index, 10)+1);
				});
			});
		}
		
	});
	$('#images').disableSelection();
	
});







