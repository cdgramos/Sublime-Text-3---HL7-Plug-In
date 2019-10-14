import sublime
import sublime_plugin
import re
import webbrowser
from .lib.hl7Event import *
from .lib.hl7Segment import *
from .lib.hl7TextUtils import *



hl7EventList = hl7Event("","")
hl7EventList = hl7EventList.loadEventList()
hl7SegmentList = hl7Segment("","")
hl7SegmentList = hl7SegmentList.loadSegmentList()

STATUS_BAR_HL7 = 'StatusBarHL7'

# On selection modified it will update the status bar
class selectionModifiedListener(sublime_plugin.EventListener):
	def on_selection_modified(self, view):


		line = getLineTextBeforeCursorPosition(self, view, sublime)
		fullLine = getLineAtCursorPosition(self, view)

		# Get the first 3 letters of the line
		segment = fullLine[:3]

		
		if hl7Segment.getSegmentByCode(self, segment, hl7SegmentList) != None:

			statusBarText = '[ ' + segment + ' '


			fieldList = re.split(r'(?<!\\)(?:\\\\)*\|', line)
			fieldCounter = len(fieldList)

			if segment != 'MSH':
				statusBarText +=  str(fieldCounter-1) 
			else:
				statusBarText +=  str(fieldCounter)

			isComponentRequired = False
			isSubComponentRequired = False

			fullField = getFieldAtCursorPosition(self, view, sublime)
			
			# Level of detail required
			if fieldHasComponents(self, fullField) == True:
				isComponentRequired = True

			if fieldHasSubComponents(self, fullField) == True:
				isComponentRequired = True
				isSubComponentRequired = True

			if isComponentRequired == True:
				field = fieldList[-1]
				componentList = re.split(r'(?<!\\)(?:\\\\)*\^', field)
				componentCounter = len(componentList)
				statusBarText += '.' + str(componentCounter)

			if isSubComponentRequired == True:
				subComponent = componentList[-1]
				subComponentList = re.split(r'(?<!\\)(?:\\\\)*\&', subComponent)
				subComponentCounter = len(subComponentList)
				statusBarText += '.' + str(subComponentCounter)


			statusBarText += ' ]' 
			#sublime.status_message('\t' + statusBarText + ' '*20)
			view.set_status(STATUS_BAR_HL7, statusBarText)

		else:
			#sublime.status_message('')
			view.erase_status(STATUS_BAR_HL7)




# Double click on keywords (segments / events)
class doubleClickKeywordListener(sublime_plugin.EventListener):

	def on_text_command(self, view, cmd, args):
		if cmd == 'drag_select' and 'event' in args:
			event = args['event']

			isEvent = True
			pt = view.window_to_text((event['x'], event['y']))
			text = []

			if view.sel():

				for region in view.sel():
					print(view.substr(view.word(region)))

					if region.empty():

						text.append(view.substr(view.word(region)))

						def asyncMessagePopup():
							desc = ""
							for eventItem in hl7EventList:

								regex = "(\^)"
								filler = "_"
								codeWithoutCircunflex = re.sub(regex, filler, text[0])

								if (eventItem.code == codeWithoutCircunflex):
									desc = eventItem.description

							for segmentItem in hl7SegmentList:

								regex = "(\^)"
								filler = "_"
								codeWithoutCircunflex = re.sub(regex, filler, text[0])

								if (segmentItem.code == codeWithoutCircunflex):
									desc = segmentItem.description

							if (len(desc) > 0):
								if(getComponentAtCursorPosition(self, view, sublime) == text[0]):
									view.show_popup('<b  style="color:#33ccff;">' + desc + '</b>', location=pt)
							
						sublime.set_timeout_async(asyncMessagePopup)
					else:
						text.append(view.substr(region))


# Searchs an event or segment on caristix web-site
class hl7searchCommand(sublime_plugin.WindowCommand):
	def run(self):  
		
		window = self.window
		view = window.active_view()
		sel = view.sel()
		region1 = sel[0]
		selectionText = view.substr(region1)

		isValid = 0

		URL = "http://hl7-definition.caristix.com:9010/HL7%20v2.5.1/Default.aspx?version=HL7 v2.5.1&"


		for eventItem in hl7EventList:

			regex = "(\^)"
			filler = "_"
			codeWithoutCircunflex = re.sub(regex, filler, selectionText)

			if (eventItem.code == codeWithoutCircunflex):
				URL = URL + "triggerEvent=" + eventItem.code
				isValid = 1

		for segmentItem in hl7SegmentList:
			if (segmentItem.code == selectionText):
				URL = URL + "segment=" + segmentItem.code
				isValid = 1


		if (isValid == 1):
			webbrowser.open_new(URL)

# Inspects an entire line
class hl7inspectorCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		#Popup layout
		header = ""
		body = ""
		segmentCode = ""

		#Segment
		selectedSegment = self.view.substr(self.view.line(self.view.sel()[0]))


		fields = selectedSegment.split('|')
		fields = re.split(r'(?<!\\)(?:\\\\)*\|', selectedSegment)


		fieldId = 0
		componentId = 1
		subComponentId = 1

		for segmentItem in hl7SegmentList:
			if (segmentItem.code == fields[0]):
				header = segmentItem.code + " - " + segmentItem.description
				segmentCode = segmentItem.code


		header = '<b style="color:#33ccff;">' + header + '</b>'

		for field in fields:

			if (field != ""):

				if(field != "^~\&"):
					components =  re.compile(r'(?<!\\)(?:\\\\)*\^').split(field)

					totalCircunflex = field.count("^")

					for component in components:
						if(component != ""):

							subComponents =  re.compile(r'(?<!\\)(?:\\\\)*&').split(component)

							if(len(subComponents) > 1):

								for subComponent in subComponents:
									if(subComponent != ""):

										regex = "(<)"
										filler = "&lt;"
										subComponent = re.sub(regex, filler, subComponent)
			
										regex = "(>)"
										filler = "&gt;"
										subComponent = re.sub(regex, filler, subComponent)
			
										body = body + '<br>' + str(fieldId) + "." + str(componentId) + "."+ str(subComponentId) + " - " + subComponent


									subComponentId = subComponentId + 1

								subComponentId = 1


							else: 

								regex = "(<)"
								filler = "&lt;"
								component = re.sub(regex, filler, component)
	
								regex = "(>)"
								filler = "&gt;"
								component = re.sub(regex, filler, component)
	
								till = re.compile(r'(?<!\\)(?:\\\\)*~').split(component)

								if segmentCode == 'MSH' and fieldId > 1:
									
									fieldCounter = fieldId + 1
								else:
									fieldCounter = fieldId


								if(totalCircunflex > 0):
									for tillItem in till:
										body = body + '<br>' + str(fieldCounter) + "." + str(componentId) + " - " + tillItem
								else:
									for tillItem in till:
										body = body + '<br>' + str(fieldCounter) + " - " + tillItem

						componentId = componentId + 1

					componentId = 1

				else:
					if len(selectedSegment) > 3:
						if selectedSegment[3] == '|':
							body = body + '<br>' + str(1) + " - " + selectedSegment[3] + "\n"
					if len(fields) > 0:
						body = body + '<br>' + str(2) + " - " + fields[1] + "\n"

			fieldId = fieldId + 1

		message = header + body
		message = message.replace("\&", "\&amp;")

		self.view.show_popup(message, on_navigate=print)
		

# Cleans an HL7 message from reduntant information and idents it
class hl7cleanerCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		content = self.view.substr(sublime.Region(0, self.view.size()))

		for segmentItem in hl7SegmentList:
			regex = "(\^M)" + segmentItem.code
			filler = "\n" + segmentItem.code
			content = re.sub(regex, filler, content)

		for segmentItem in hl7SegmentList:
			regex = "(\^K)" + segmentItem.code
			filler = "\n" + segmentItem.code
			content = re.sub(regex, filler, content)

		#remove any empty space before each segment
		for segmentItem in hl7SegmentList:
			regex = "\ {1,}" + segmentItem.code
			filler = "" + segmentItem.code
			content = re.sub(regex, filler, content)

		#when there is no space before 
		for segmentItem in hl7SegmentList:
			regex = "(\|){1,}(?<=[a-zA-Z0-9|])" + segmentItem.code + "(\|){1,}"
			filler = "|\n" + segmentItem.code + "|"
			content = re.sub(regex, filler, content)

		#last two ^M at the end of content followed by new line
		content = re.sub("(\^M\^\\\\\^M)\n", "\n", content)
		
		#last two ^M at the end of content followed by end of content
		content = re.sub("(\^M\^\\\\\^M)$", "\n", content)
			
		#last ^M with new line
		regex = "(\^M)\n" 
		filler = "\n"
		content = re.sub(regex, filler, content)
		
		#last ^M with end of content
		regex = "(\^M)$" 
		filler = "\n"
		content = re.sub(regex, filler, content)


		#last two ^M at the end of content followed by new line with empty space before
		content = re.sub("(\^M\^\\\\\^M)\ {1,}\n", "\n", content)
		
		#last two ^M at the end of content followed by end of content with empty space before
		content = re.sub("(\^M\^\\\\\^M)\ {1,}$", "\n", content)

		#last ^M with new line with empty space before
		regex = "(\^M)\ {1,}\n" 
		filler = "\n"
		content = re.sub(regex, filler, content)
		
		#last ^M with end of content with empty space before
		regex = "(\^M)\ {1,}$" 
		filler = "\n"
		content = re.sub(regex, filler, content)

		#extra circumflex ^
		content = re.sub("(\^{1,})[|]", "|", content)
		
		#extra pipes | followed by new lines
		content = re.sub("\|{2,}\n", "|\n", content)
		
		#extra pipes | followed by end of content
		content = re.sub("\|{2,}$", "|\n", content)
		
		#empty lines at the beginning of the text
		content = re.sub("^(\n){1,}", "", content)
		
		#blank spaces at the beginning of the text
		content = re.sub("^ {1,}", "", content)
		


		self.view.insert(edit, 0, content + "\n\n\n")
