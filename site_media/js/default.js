var sortableOptions = {
			handle: '.handle',
			connectWith: '.todos_active',
			receive: function(event, ui) {
				var category = $(ui.item).parents('.category');
				$.post('/pm/updatetodo/'+$(ui.item).attr('rel')+'/', { 'category_id': category.attr('rel') }, function() {}, 'json');
				checkForPlaceholder($('.todos_active', category));
			},
			remove: function(event, ui) {
				checkForPlaceholder($(this));
			},
			update: function(event, ui) {
				var category = $(ui.item).parents('.category');
				var activeTodos = $('.todos_active', category);
				var order = $.makeArray(
								$.map(
									$('li', activeTodos), 
										function(n) { return $(n).attr('rel'); }
									));

				$.post('/pm/prioritize/'+category.attr('rel')+'/', { 'order': order.join(',') }, function() {}, 'json');
			}
		};
		
var editableOptions_description = { 'editBy': 'dblclick', 'submit': 'Update', 'cancel': 'Cancel', 'editClass': 'descriptionEdit', 'onSubmit': function(content) {
			if(content.current != content.previous) {
				var parent = $(this).parent();
				var type = parent.attr('class');
				$.post('/pm/update'+type+'/'+parent.attr('rel')+'/', { 'description': content.current }, function() {}, 'json');
			}
		} };

var checkForPlaceholder = function(target) {
		if($('.todo', target).length) {
			$('.placeholder', target).fadeOut('fast', function() { $(this).remove(); });
		} else {
			$('<li>').addClass('placeholder').text('Add some tasks!').appendTo(target);
		}
	};

var toggleCompleteTodo = function() {
		var parent = $(this).parents('.todo');
		var complete = (+$(this).is(':checked'));
		var category = parent.parents('.category');
		$.post('/pm/completetodo/'+parent.attr('rel')+'/'+complete+'/', {}, function() {
				if(complete) {
					parent.slideUp('fast', function() {
						$(this).hide();
						$('.handle', this).remove();
						$(this).addClass('complete').appendTo($('.todos_completed', category)).fadeIn('fast');
					});
				} else {
					parent.slideUp('fast', function() {
						$(this).hide();
						$('.icons', this).prepend($('<span>').addClass('handle').append($('<img>').attr('src', '/site_media/images/list_ordered.gif')));
						$(this).removeClass('complete').appendTo($('.todos_active', category)).fadeIn('fast');
					});
				}
			}, 'json');
	};

var deleteTodo = function() {
		var parent = $(this).parents('.todo');
		var todos = parent.parent();
		$.post('/pm/deletetodo/'+parent.attr('rel')+'/', {}, function () {
				parent.slideUp('fast', function() { parent.remove(); checkForPlaceholder(todos); });
			}, 'json');
	};

var addTodo = function(f) {
		f = $(f);
		var category = $(f).parents('.category');
		var category_id = category.attr('rel');
		
		$.post('/pm/addtodo/', f.serialize(), function(response) {
				$('<li>')
					.attr('id', 'todo'+response.id)
					.attr('rel', response.id)
					.addClass('todo')
					.append($('<div>').addClass('control')
								.append($('<div>').addClass('icons')
									.append($('<span>').addClass('handle').append($('<img>').attr('src', '/site_media/images/list_ordered.gif')))
									.append(' ')
									.append($('<a>').attr('href', 'javascript:;').addClass('deleteLink').append($('<img>').attr('src', '/site_media/images/trash.gif')).click(deleteTodo))
									.append(' '))
								.append($('<div>').addClass('completeInput')
									.append($('<input>').attr({ 'type': 'checkbox', 'autocomplete': 'off' }).addClass('completeLink').click(toggleCompleteTodo))
									)
								)
					.append($('<div>').addClass('item').append(response.item).append(' ').append($('<span>').addClass('created').text('('+response.created+')')))
					.hide()
					.appendTo('#category'+category_id+' .todos:first')
					.fadeIn('fast');
				
				f.get(0).reset();
				
				checkForPlaceholder($('.todos_active', category));
			}, 'json');
			
		return false;
	};
	
var showAddTodo = function() {
		var f = $('#addTodoTemplateContainer > form').clone();
		var div = $(this).parent();
		var category_id = $(this).parents('.category').attr('rel');
		
		div.html(f).append(
			$('<a>').attr('href', 'javascript:;').text('All Done!').appendTo(div).click(hideAddTodo));
		
		$(':input[name=category]', f).val(category_id);
		$(':input[name=priority]', f).val($('.todo', $(this).parents('.category')).length);
		$(':button', f).click(function() { addTodo(f); });
		
		$(':input[type=text]', f).focus();
	};

var hideAddTodo = function() {
		$(this).parents('.addTodoContainer').html($('<a>').attr('href', 'javascript:;').addClass('showAddTodoLink').text('Add Todo').click(showAddTodo));
	};

var onKeyPress_addTodo = function(e, target) {
		switch(e.charCode || e.keyCode) {
			case 13:
				addTodo(target);
				return false;
				break;
			case 27:
				$('a', $(target).parents('.addTodoContainer')).click();
				return false;
				break;
		}
		
		return true;
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

$(document).ready(function() {
	$('.deleteLink').click(deleteTodo);
		
	$('.completeLink').click(toggleCompleteTodo);
	
	$('.showAddTodoLink').click(showAddTodo);
	
	$('.projectDescription, .categoryDescription').editable(editableOptions_description);
		
	$('.todos').sortable(sortableOptions);
		
	$('.addProjectContainer :button').click(function() {
			var f = $(this.form);
			$.post('/pm/addproject/', f.serialize(), function(response) {
					$('<div>')
						.addClass('project')
						.attr('id', 'project'+response.id)
						.attr('rel', response.id)
						.append($('<h1>').append($('<a>').attr('href', '/pm/delproject/'+response.id).text('X')).append(' '+response.name))
						.append($('<div>').addClass('projectDescription').text(response.description).editable(editableOptions))
						.append($('<div>').addClass('categories'))
						.appendTo('#projects');
					
					$('.addCategoryContainer select').append($('<option>').attr('value', response.id).text(response.name));
					
					f.get(0).reset();
				}, 'json');
		});
		
	$('.addCategoryContainer :button').click(function() {
			var f = $(this.form);
			$.post('/pm/addcategory/', f.serialize(), function(response) {
					var cat = $('<div>')
						.addClass('category')
						.attr('id', 'category'+response.id)
						.attr('rel', response.id)
						.append($('<h2>').append($('<a>').attr('href', '/pm/delcategory/'+response.id).text('X')).append(' '+response.name))
						.append($('<div>').addClass('categoryDescription').text(response.description))
						.append($('<div>').addClass('todos').addClass('todos_active').sortable(sortableOptions))
						.append($('<div>').addClass('addTodoContainer').append($('<a>').attr('href', 'javascript:;').addClass('showAddTodoLink').text('Add Todo').click(showAddTodo)))
						.append($('<div>').addClass('todos').addClass('todos_completed'))
						.appendTo('#project'+response.project_id+' .categories');
						
					checkForPlaceholder($('.todos_active', cat));
						
					f.get(0).reset();
				}, 'json');
		});
});