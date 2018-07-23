import sublime
import sublime_plugin
import re
import webbrowser
from .lib.hl7Event import hl7Event
from .lib.hl7Segment import hl7Segment

hl7EventList = hl7Event("","")
hl7SegmentList = hl7Segment("","")

class doubleClickKeywordListener(sublime_plugin.EventListener):

	def on_text_command(self, view, cmd, args):
		if cmd == 'drag_select' and 'event' in args:
			event = args['event']

			isEvent = True
			pt = view.window_to_text((event['x'], event['y']))
			text = []
			if view.sel():
				for region in view.sel():
					if region.empty():
						text.append(view.substr(view.word(region)))

						def asyncMessagePopup():
							desc = ""
							for eventItem in hl7EventList.loadEventList():

								regex = "(\^)"
								filler = "_"
								codeWithoutCircunflex = re.sub(regex, filler, text[0])

								if (eventItem.code == codeWithoutCircunflex):
									desc = eventItem.description

							for segmentItem in hl7SegmentList.loadSegmentList():

								regex = "(\^)"
								filler = "_"
								codeWithoutCircunflex = re.sub(regex, filler, text[0])

								if (segmentItem.code == codeWithoutCircunflex):
									desc = segmentItem.description

							if (len(desc) > 0):
								view.show_popup('<b  style="color:#33ccff;">' + desc + '</b>', location=pt)
							
						sublime.set_timeout_async(asyncMessagePopup)
					else:
						 text.append(view.substr(region))


class hl7searchCommand(sublime_plugin.WindowCommand):
	def run(self):     
		
		window = self.window
		view = window.active_view()
		sel = view.sel()
		region1 = sel[0]
		selectionText = view.substr(region1)

		isValid = 0

		URL = "http://hl7-definition.caristix.com:9010/HL7%20v2.5.1/Default.aspx?version=HL7 v2.5.1&"


		for eventItem in hl7EventList.loadEventList():

			regex = "(\^)"
			filler = "_"
			codeWithoutCircunflex = re.sub(regex, filler, selectionText)

			if (eventItem.code == codeWithoutCircunflex):
				URL = URL + "triggerEvent=" + eventItem.code
				isValid = 1

		for segmentItem in hl7SegmentList.loadSegmentList():
			if (segmentItem.code == selectionText):
				URL = URL + "segment=" + segmentItem.code
				isValid = 1


		if (isValid == 1):
			webbrowser.open_new(URL)


class hl7inspectorCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		#Popup layout
		header = ""
		body = ""

		#Segment
		selectedSegment = self.view.substr(self.view.line(self.view.sel()[0]))


		fields = selectedSegment.split('|')

		for segmentItem in hl7SegmentList.loadSegmentList():
			if (segmentItem.code == fields[0]):
				header = segmentItem.code + " - " + segmentItem.description


		header = '<b style="color:#33ccff;">' + header + '</b>'


		fieldId = 0
		componentId = 1
		subComponentId = 1


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

								if(totalCircunflex > 0):
									for tillItem in till:
										body = body + '<br>' + str(fieldId) + "." + str(componentId) + " - " + tillItem
								else:
									for tillItem in till:
										body = body + '<br>' + str(fieldId) + " - " + tillItem

						componentId = componentId + 1

					componentId = 1

				else:
					body = body + '<br>' + str(1) + " - " + "^~\&" + "\n"


			fieldId = fieldId + 1

		message = header + body
		message = message.replace("\&", "\&amp;")

		self.view.show_popup(message, on_navigate=print)
		

		
class hl7cleanerCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		content = self.view.substr(sublime.Region(0, self.view.size()))

		for segmentItem in hl7SegmentList.loadSegmentList():
			regex = "(\^M)" + segmentItem.code
			filler = "\n" + segmentItem.code
			content = re.sub(regex, filler, content)

		for segmentItem in hl7SegmentList.loadSegmentList():
			regex = "(\^K)" + segmentItem.code
			filler = "\n" + segmentItem.code
			content = re.sub(regex, filler, content)

		#remove any empty space before each segment
		for segmentItem in hl7SegmentList.loadSegmentList():
			regex = "\ {1,}" + segmentItem.code
			filler = "" + segmentItem.code
			content = re.sub(regex, filler, content)

		#when there is no space before 
		for segmentItem in hl7SegmentList.loadSegmentList():
			regex = "(?<=[a-zA-Z0-9|])" + segmentItem.code
			filler = "\n" + segmentItem.code
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
