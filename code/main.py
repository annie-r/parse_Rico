from view import View
from app import App
from node_checker import Node_Checker
from view_checker import View_Checker
from trace import Trace
import os
def print_header(table_type):
	
	if (table_type == "BY_NODE"):
		print("app_id,node_id,class,android_widget,ad,",end="")
		Node_Checker.print_header()
	elif table_type == "BY_APP":
		App.print_header()
		View_Checker.print_header()
	print("")

if __name__ == "__main__":
	# cont desc editable textfield, 1 
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	#v = View(filepath)
	#v.print(talkback_focus_only = False)

	#test single view
	# 4 talkback accessible nodes,
	# app_id,node_id,class,android_widget,ad,Speakable_Text_Present,,
	# skype,com.skype.raider:id/create_acct_btn,android.widget.RelativeLayout,True,False,True,
	# skype,com.skype.raider:id/sign_in_userid,com.skype.android.widget.AccessibleAutoCompleteTextView,False,False,True,
	# skype,com.skype.raider:id/sign_in_next_btn,com.skype.android.widget.SymbolView,False,False,True,
	# skype,com.skype.raider:id/sign_in_content,android.widget.LinearLayout,True,False,True,
	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	

	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\677.json"
	v = View("677",view_dir)
	v.print_debug()

	# 4 not wide enough, 7 not tall enough, 9 no speakable text, 2 ads, 5 non-android widgets (just using one library)
	#view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\example_apps\\com.imo.android.imoim\\trace_0\\view_hierarchies\\662.json"

	# # 5 nodes, cont desc editable textfield 1, 3 android widgets, 0 ads, 1 not speakable text, 0 not wide enough, 1 not tall enough
	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	
	v = View("74",view_dir)
	v.print_debug()
	#print(str(v.num_tba))
	#print_header("BY_NODE")
	
	#v.print_table("BY_NODE","skype")

	#print("\n############################################\n")
	#trace test
	#file = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider.test\\trace_1"
	#t = Trace(file,"skype_test")
	#t.print_debug()
	# ## Traverse all apps in directory, assume directory only has apps directories
	apps_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps_test"
	print_header("BY_APP")
	for a_dir in os.listdir(apps_dir):
		a = App(apps_dir + "\\" + a_dir)
		a.print_table("BY_APP")

