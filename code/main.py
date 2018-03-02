from view import View
from app import App
if __name__ == "__main__":
	# cont desc editable textfield, 1 
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	#v = View(filepath)
	#v.print(talkback_focus_only = False)

	#trace test
	file = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.duolingo"
	a = App(file)
	a.print_check()
