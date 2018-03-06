from view import View
from app import App
from node_checker import print_checker_header
def print_header():
	print("app_id,node_id,class,android_widget,ad,",end="")
	print_checker_header()
	print("")

if __name__ == "__main__":
	# cont desc editable textfield, 1 
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	#v = View(filepath)
	#v.print(talkback_focus_only = False)

	#trace test
	file = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.duolingo"
	a = App(file)
	print_header()
	a.print_views_table()
