from view import View
from app import App
from node_checker import print_checker_header

import os
def print_header():
	print("app_id,node_id,class,android_widget,ad,",end="")
	print_checker_header()
	print("")

if __name__ == "__main__":
	# cont desc editable textfield, 1 
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	#v = View(filepath)
	#v.print(talkback_focus_only = False)

	#test single view
	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	v = View("74",view_dir)
	print_header()
	v.print_views_table("skype")

	#trace test
	# file = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.duolingo"
	
	# ## Traverse all apps in directory, assume directory only has apps directories
	# apps_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps"
	# print_header()
	# for a_dir in os.listdir(apps_dir):
	# 	a = App(apps_dir + "\\" + a_dir)
	# 	a.print_views_table()
	#a = App(file)
	#print_header()
		
