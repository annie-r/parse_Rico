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
	# 5 talkback accessible nodes, 
	# app_id,node_id,class,android_widget,ad,Speakable_Text_Present,,
	# skype,com.skype.raider:id/create_acct_btn,android.widget.RelativeLayout,True,False,True,
	# skype,com.skype.raider:id/sign_in_userid,com.skype.android.widget.AccessibleAutoCompleteTextView,False,False,True,
	# skype,com.skype.raider:id/sign_in_next_btn,com.skype.android.widget.SymbolView,False,False,True,
	# skype,com.skype.raider:id/sign_in_content,android.widget.LinearLayout,True,False,True,
	# skype,com.skype.raider:id/content_layout,android.widget.ScrollView,True,False,False,
	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	
	# 4 not wide enough, 7 not tall enough, 9 no speakable text, 2 ads, 5 non-android widgets (just using one library)
	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\example_apps\\com.imo.android.imoim\\trace_0\\view_hierarchies\\662.json"
	v = View("74",view_dir)
	#v.print()
	print_header()
	v.print_views_table("imo")

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
		
