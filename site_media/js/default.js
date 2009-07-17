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
	
	var showAddTodo = function() {
			var f = $('#addTodoTemplateContainer > form').clone();
			f.appendTo($(this).parent());
			var category_id = $(this).parents('.category').attr('rel');
			$(':input[name=category]', f).val(category_id);
			$(':input[name=priority]', f).val($('.todo', $(this).parents('.category')).length);
			$(':button', f).click(function() {
				$.post('/pm/addtodo/', f.serialize(), function(response) {
						$('<li>')
							.attr('id', 'todo'+response.id)
							.attr('rel', response.id)
							.addClass('todo')
							.append($('<div>').addClass('control')
										.append($('<span>').addClass('handle').append($('<img>').attr('src', '/site_media/images/list_ordered.gif')))
										.append(' ')
										.append($('<a>').attr('href', 'javascript:;').addClass('deleteLink').append($('<img>').attr('src', '/site_media/images/trash.gif')))
										.append(' ')
										.append($('<input>').attr({ 'type': 'checkbox', 'autocomplete': 'off' }).addClass('completeLink'))
										)
							.append($('<div>').addClass('item').append(response.item).append(' ').append($('<span>').addClass('created').text(response.created)))
							.appendTo('#category'+category_id+' .todos:first');
						
						f.get(0).reset();
					}, 'json');
			});
		};
		
	$('.showAddTodoLink').click(showAddTodo);
		
	$('.addProjectContainer :button').click(function() {
			var f = $(this.form);
			$.post('/pm/addproject/', f.serialize(), function(response) {
					$('<div>')
						.addClass('project')
						.attr('id', 'project'+response.id)
						.append($('<h1>').append($('<a>').attr('href', '/pm/delproject/'+response.id).text('X')).append(' '+response.name))
						.append($('<div>').addClass('categories'))
						.appendTo('#projects');
					
					$('.addCategoryContainer select').append($('<option>').attr('value', response.id).text(response.name));
					
					f.get(0).reset();
				}, 'json');
		});
		
	$('.addCategoryContainer :button').click(function() {
			var f = $(this.form);
			$.post('/pm/addcategory/', f.serialize(), function(response) {
					$('<div>')
						.addClass('category')
						.attr('id', 'category'+response.id)
						.attr('rel', response.id)
						.append($('<h2>').append($('<a>').attr('href', '/pm/delcategory/'+response.id).text('X')).append(' '+response.name))
						.append($('<div>').addClass('todos'))
						.append($('<div>').addClass('addTodoContainer').append($('<a>').attr('href', 'javascript:;').addClass('showAddTodoLink').text('Add Todo').click(showAddTodo)))
						.append($('<div>').addClass('todos').addClass('todos_completed'))
						.appendTo('#project'+response.project_id+' .categories');
						
						f.get(0).reset();
				}, 'json');
		});
});