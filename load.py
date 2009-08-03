import sys
import settings
from django.core.management import setup_environ
from xml.etree import ElementTree as etree

setup_environ(settings)

def load(fileName):
    doc = etree.parse(fileName)
    projects = doc.findall('projects/project')
    for project in projects:
    	projectname = project.findtext('name')
    	print 'Project: %s' % (projectname,)
    	todolists = project.findall('todo-lists/todo-list')
    	for todolist in todolists:
    		todolistname = todolist.findtext('name')
    		print '    Todo-list: %s' % (todolistname,)
    		todoitems = todolist.findall('todo-items/todo-item')
    		for todoitem in todoitems:
    			todoitemname = todoitem.findtext('content')[:25]
    			print '        Todo-item: %s' % (todoitemname,)

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print 'usage: python load.py infile.xml'
        sys.exit(-1)
    load(args[0])

if __name__ == '__main__':
    main()
