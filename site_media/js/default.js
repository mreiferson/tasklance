var sortableOptions_tasks = {
			handle: '.handle',
			connectWith: '.tasks_active',
			receive: function(event, ui) {
				var project = $(ui.item).parents('.project');
				$.post('/pm/updatetask/'+$(ui.item).attr('rel')+'/', { 'project_id': project.attr('rel') }, function() {}, 'json');
				checkForPlaceholder($('.tasks_active', project));
			},
			remove: function(event, ui) {
				checkForPlaceholder($(this));
			},
			update: function(event, ui) {
				var project = $(ui.item).parents('.project');
				var activeTasks = $('.tasks_active', project);
				var order = $.makeArray($.map($('li', activeTasks), 
									function(n) { return $(n).attr('rel'); }
								));
				$.post('/pm/prioritize/task/'+project.attr('rel')+'/', { 'order': order.join(',') }, function(response) {}, 'json');
			}
		};
		
var sortableOptions_reorder = {
		handle: '.handle',
		receive: function(event, ui) {
		},
		remove: function(event, ui) {
		},
		update: function(event, ui) {
			var parent = $(ui.item).parent();
			var type = parent.attr('rel');
			var order = $('.'+type+'Link', parent);
			
			$.each(order, function(i, el) {
				var match = $('#'+type+$(el).attr('rel'));
				$(match).parent().append(match);
			});
			
			order = $.makeArray($.map(order, 
							function(n) { return $(n).attr('rel'); }
						));
			
			if(type == 'category') {
				var parentId = $('#account').attr('rel');
			} else if(type == 'project') {
				var parentId = $(ui.item).parents('.categoryLink').attr('rel');
			}
			
			$.post('/pm/prioritize/'+type+'/'+parentId+'/', { 'order': order.join(',') }, function(response) {}, 'json');
		}
	};
		
var editableOptions = { 'editBy': 'dblclick', 'submit': 'Update', 'cancel': 'Cancel', 'editClass': 'descriptionEdit', 'onSubmit': function(content) {
		if(content.current != content.previous) {
			var parent = $(this).parents('div');
			var type = parent.attr('class');
			var params = {};
			params[$(this).attr('rel')] = content.current;
			$.post('/pm/update'+type+'/'+parent.attr('rel')+'/', params, function() {}, 'json');
		}
	} };

var checkForPlaceholder = function(target) {
		if($('.task', target).length) {
			$('.placeholder', target).fadeOut('fast', function() { $(this).remove(); });
		} else {
			$('<li>').addClass('placeholder').text('Add some tasks!').appendTo(target);
		}
	};

var toggleCompleteTask = function() {
		var parent = $(this).parents('.task');
		var complete = (+$(this).is(':checked'));
		var project = parent.parents('.project');
		$.post('/pm/completetask/'+parent.attr('rel')+'/'+complete+'/', {}, function(response) {
				if(complete) {
					parent.slideUp('fast', function() {
						$(this).hide();
						$('.created', this).text('('+response.date+')');
						$('.handle', this).remove();
						$(this).addClass('complete').appendTo($('.tasks_completed', project)).fadeIn('fast');
					});
				} else {
					parent.slideUp('fast', function() {
						$(this).hide();
						$('.created', this).text('('+response.age+' days)');
						$('.icons', this).prepend($('<span>').addClass('handle').append($('<img>').attr('src', '/site_media/images/list_ordered.gif')));
						$(this).removeClass('complete').appendTo($('.tasks_active', project)).fadeIn('fast');
					});
				}
			}, 'json');
	};

var deleteTask = function() {
		var parent = $(this).parents('.task');
		var tasks = parent.parent();
		$.post('/pm/deletetask/'+parent.attr('rel')+'/', {}, function () {
				parent.slideUp('fast', function() { parent.remove(); checkForPlaceholder(tasks); });
			}, 'json');
	};

var addTask = function(f) {
		f = $(f);
		var project = $(f).parents('.project');
		var project_id = project.attr('rel');
		
		$.post('/pm/addtask/', f.serialize(), function(response) {
				$('<li>')
					.attr('id', 'task'+response.id)
					.attr('rel', response.id)
					.addClass('task')
					.addClass('task')
					.append(
						$('<div>').addClass('floatContainer')
							.append($('<div>').addClass('control')
										.append($('<div>').addClass('icons')
											.append($('<span>').addClass('handle').append($('<img>').attr('src', '/site_media/images/list_ordered.gif')))
											.append(' ')
											.append($('<a>').attr('href', 'javascript:;').addClass('deleteLink').append($('<img>').attr('src', '/site_media/images/trash.gif')).click(deleteTask))
											.append(' '))
										.append($('<div>').addClass('completeInput')
											.append($('<input>').attr({ 'type': 'checkbox', 'autocomplete': 'off' }).addClass('completeLink').click(toggleCompleteTask))
											))
							.append($('<div>').addClass('item').append(response.item).append(' '))
							.append($('<div>').addClass('created').text('(0 days)'))
					)
					.hide()
					.appendTo('#project'+project_id+' .tasks:first')
					.fadeIn('fast');
				
				f.get(0).reset();
				
				checkForPlaceholder($('.tasks_active', project));
			}, 'json');
			
		return false;
	};
	
var showAddTask = function() {
		var f = $('#addTaskTemplateContainer > form').clone();
		var div = $(this).parent();
		var project_id = $(this).parents('.project').attr('rel');
		
		div.html(f).append('<br/>').append(
			$('<a>').attr('href', 'javascript:;').text('All Done!').appendTo(div).click(hideAddTask));
		
		$(':input[name=project]', f).val(project_id);
		$(':input[name=priority]', f).val($('.task', $(this).parents('.project')).length);
		$(':button', f).click(function() { addTask(f); });
		
		$(':input[type=text]', f).focus();
	};

var hideAddTask = function() {
		$(this).parents('.addTaskContainer').html($('<a>').attr('href', 'javascript:;').addClass('showAddTaskLink').text('Add Task').click(showAddTask));
	};

var onKeyPress_addTask = function(e, target) {
		switch(e.charCode || e.keyCode) {
			case 13:
				addTask(target);
				return false;
				break;
			case 27:
				$('a', $(target).parents('.addTaskContainer')).click();
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
	$('.deleteLink').click(deleteTask);
		
	$('.completeLink').click(toggleCompleteTask);
	
	$('.showAddTaskLink').click(showAddTask);
	
	$('.projectDescription, .categoryDescription, .projectName, .categoryName').editable(editableOptions);
	
	$('.projectLinks, .categoryLinks').sortable(sortableOptions_reorder);
		
	$('.tasks').sortable(sortableOptions_tasks);
	
	$('.addMilestoneContainer :button').click(function() {
			var f = $(this.form);
			$(':input[name=priority]', f).val($('.milestone').length);
			$.post('/pm/milestone/add/', f.serialize(), function(response) {
					f.get(0).reset();
				}, 'json');
		});
		
	$('.addProjectContainer :button').click(function() {
			var f = $(this.form);
			$(':input[name=priority]', f).val($('.project', $('#category'+$(':input[name=category]', f).val())).length);
			$.post('/pm/addproject/', f.serialize(), function(response) {
					var headline = $('<h2>')
										.append(
											$('<a>')
												.attr('href', '/pm/delproject/'+response.id)
												.append(
													$('<img>')
														.attr('src', '/site_media/images/folder_delete.gif')))
										.append(' ')
										.append(
											$('<span>')
												.addClass('projectName')
												.attr('rel', 'name').text(response.name));
					var project = $('<div>')
						.addClass('project')
						.attr('id', 'project'+response.id)
						.attr('rel', response.id)
						.append(headline)
						.append($('<div>').addClass('projectDescription').attr('rel', 'description').text(response.description).editable(editableOptions))
						.append($('<div>').addClass('tasks').addClass('tasks_active').sortable(sortableOptions_tasks))
						.append($('<div>').addClass('addTaskContainer').append($('<a>').attr('href', 'javascript:;').addClass('showAddTaskLink').text('Add Task').click(showAddTask)))
						.append($('<div>').addClass('tasks').addClass('tasks_completed'))
						.appendTo('.projects');
						
					checkForPlaceholder($('.tasks_active', project));
					
					f.get(0).reset();
				}, 'json');
		});
		
	$('.addCategoryContainer :button').click(function() {
			var f = $(this.form);
			$(':input[name=priority]', f).val($('.category').length);
			$.post('/pm/addcategory/', f.serialize(), function(response) {
					var headline = $('<h1>')
										.append(
											$('<a>')
												.attr('href', '/pm/delcategory/'+response.id)
												.append(
													$('<img>')
														.attr('src', '/site_media/images/report_delete.gif')))
										.append(' ')
										.append(
											$('<a>')
												.attr('href', '/pm/category/view/'+response.id).text(response.name));
					var cat = $('<div>')
						.addClass('category')
						.attr('id', 'category'+response.id)
						.attr('rel', response.id)
						.append(headline)
						.append($('<div>').addClass('categoryDescription').text(response.description))
						.appendTo('#categories');
						
					f.get(0).reset();
				}, 'json');
		});
});
