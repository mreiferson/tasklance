$(document).ready(function() {
	$('.deleteLink').click(function() {
			var parent = $(this).parents('.todo');
			$.post('/pm/deltodo/'+parent.attr('rel')+'/', {}, function () {
					parent.slideUp('fast', function() {
						parent.remove();
					});
				});
		});
		
	$('.completeLink').click(function() {
			var parent = $(this).parents('.todo');
			var complete = (+$(this).is(':checked'));
			$.post('/pm/completetodo/'+parent.attr('rel')+'/'+complete+'/', {}, function() {
					if(complete) {
						parent.addClass('complete');
					} else {
						parent.removeClass('complete');
					}
				});
		});
		
	$('.todos').sortable({
		handle: '.handle',
		update: function(event, ui) {
			var categoryParent = $(ui.item).parents('.category');
			var order = $.makeArray(
							$.map(
								$('li', categoryParent), 
									function(n) { return $(n).attr('rel'); }
								));
			$.post('/pm/prioritize/'+categoryParent.attr('rel')+'/', { 'order': order.join(',') }, function() {});
		}
	});
	
	$('.showAddTodoLink').click(function() {
		var f = $('#addTodoTemplateContainer > form').clone();
		f.appendTo($(this).parent());
		$(':input[name=category]', f).val($(this).parents('.category').attr('rel'));
		$(':input[name=priority]', f).val($('.todo', $(this).parents('.category')).length);
		$(':button', f).click(function() {
			$.post('/pm/addtodo/', f.serialize(), function(response) {
					alert(response.id);
					
				}, 'json');
		});
	});
});