"""
Set of util functions to manipulate the text
"""
import re

# Gets the entire text line at cursor position
def getLineAtCursorPosition(self, view):
	return (view.substr(view.line(view.sel()[0])))


# Gets the text of the line from the beginning to the cursor position
def getLineTextBeforeCursorPosition(self, view, sublime):
	pt = ''

	sels = view.sel()
	for s in sels:
		pt += " " + str(s.begin())


	region1 = sublime.Region(0, int(pt))
	selectionText = view.substr(region1)

	i = 0
	line = ''
	for c in selectionText:
		line += c
		if(c == '\n'):
			line = ''

	return line


# Gets the entire field at cursor positon
def getFieldAtCursorPosition(self, view, sublime):
	line = getLineAtCursorPosition(self, view)
	parcialLine = getLineTextBeforeCursorPosition(self, view, sublime)

	lineFieldList = re.split(r'(?<!\\)(?:\\\\)*\|', line)
	lineFieldCounter = len(lineFieldList)

	parcialLineFieldList = re.split(r'(?<!\\)(?:\\\\)*\|', parcialLine)
	parcialLineFieldCounter = len(parcialLineFieldList)

	return lineFieldList[parcialLineFieldCounter-1]

# Gets the entire component at cursor position
def getComponentAtCursorPosition(self, view, sublime):

	field = getFieldAtCursorPosition(self, view, sublime)

	parcialComponentList = re.split(r'(?<!\\)(?:\\\\)*\^', field)
	parcialComponentCounter = len(parcialComponentList)

	return parcialComponentList[parcialComponentCounter-1]




# Check if a field has components
def fieldHasComponents(self, field):
	componentsList = re.split(r'(?<!\\)(?:\\\\)*\^', field)
	if len(componentsList) > 1:
		return True
	else:
		return False


# Check if a field has sub-components
def fieldHasSubComponents(self, field):
	subComponentsList = re.split(r'(?<!\\)(?:\\\\)*\&', field)
	if len(subComponentsList) > 1:
		return True
	else:
		return False

