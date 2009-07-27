$(document).ready(function() {
	$('.deleteLink').click(deleteTodo);
		
	$('.completeLink').click(toggleCompleteTodo);
	
	$('.projectDescription, .categoryDescription').editable({'submit': 'Update', 'cancel': 'Cancel', 'editClass': 'descriptionEdit', 'onSubmit': function(content) {
			if(content.current != content.previous) {
				var parent = $(this).parent();
				var type = parent.attr('class');
				$.post('/pm/update'+type+'/'+parent.attr('rel')+'/', { 'description': content.current }, function() {}, 'json');
			}
		} });
		
	$('.todos').sortable({
			handle: '.handle',
			update: function(event, ui) {
				var categoryParent = $(ui.item).parents('.category');
				var order = $.makeArray(
								$.map(
									$('li', categoryParent), 
										function(n) { return $(n).attr('rel'); }
									));

				$.post('/pm/prioritize/'+categoryParent.attr('rel')+'/', { 'order': order.join(',') }, function() {}, 'json');
			}
		});
			
	$('.showAddTodoLink').click(showAddTodo);
		
	$('.addProjectContainer :button').click(function() {
			var f = $(this.form);
			$.post('/pm/addproject/', f.serialize(), function(response) {
					$('<div>')
						.addClass('project')
						.attr('id', 'project'+response.id)
						.attr('rel', response.id)
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

var toggleCompleteTodo = function() {
		var parent = $(this).parents('.todo');
		var complete = (+$(this).is(':checked'));
		var category = parent.parents('.category');
		$.post('/pm/completetodo/'+parent.attr('rel')+'/'+complete+'/', {}, function() {
				debugger;
				if(complete) {
					$('.handle', parent).remove();
					parent.addClass('complete').appendTo($('.todos_completed', category));
				} else {
					$('.icons', parent).prepend($('<span>').addClass('handle').append($('<img>').attr('src', '/site_media/images/list_ordered.gif')));
					parent.removeClass('complete').appendTo($('.todos_active', category));
				}
			}, 'json');
	};

var deleteTodo = function() {
		var parent = $(this).parents('.todo');
		$.post('/pm/deltodo/'+parent.attr('rel')+'/', {}, function () {
				parent.slideUp('fast', function() {
					parent.remove();
				});
			}, 'json');
	};

var addTodo = function(f) {
		f = $(f);
		var category_id = $(f).parents('.category').attr('rel');
		
		$.post('/pm/addtodo/', f.serialize(), function(response) {
				$('<li>')
					.attr('id', 'todo'+response.id)
					.attr('rel', response.id)
					.addClass('todo')
					.append($('<div>').addClass('control')
								.append($('<div>').addClass('icons')
									.append($('<span>').addClass('handle').append($('<img>').attr('src', '/site_media/images/list_ordered.gif')))
									.append(' ')
									.append($('<a>').attr('href', 'javascript:;').addClass('deleteLink').append($('<img>').attr('src', '/site_media/images/trash.gif').click(deleteTodo)))
									.append(' '))
								.append($('<div>').addClass('completeInput')
									.append($('<input>').attr({ 'type': 'checkbox', 'autocomplete': 'off' }).addClass('completeLink').click(toggleCompleteTodo))
									)
								)
					.append($('<div>').addClass('item').append(response.item).append(' ').append($('<span>').addClass('created').text('('+response.created+')')))
					.appendTo('#category'+category_id+' .todos:first');
				
				f.get(0).reset();
			}, 'json');
			
		return false;
	};
	
var showAddTodo = function() {
		var f = $('#addTodoTemplateContainer > form').clone();
		var div = $(this).parent();
		var category_id = $(this).parents('.category').attr('rel');
		
		div.html(f).append(
			$('<a>').attr('href', 'javascript:;').text('All Done!').appendTo(div).click(function() {
				div.html($('<a>').attr('href', 'javascript:;').addClass('showAddTodoLink').text('Add Todo').click(showAddTodo));
			}));
		
		$(':input[name=category]', f).val(category_id);
		$(':input[name=priority]', f).val($('.todo', $(this).parents('.category')).length);
		$(':button', f).click(function() { addTodo(f); });
	};

function onKeyPress(e, keycode, fnc, param) {
	var pK = e.charCode || e.keyCode;

	if(pK == keycode) {
		fnc(param);
		return false;
	}

	return true;
}

function entFunc(e, fnc, param) {
	return onKeyPress(e, 13, fnc, param);
}

function entSub(e, frm) {
	return entFunc(e, function() { frm.submit(); });
}