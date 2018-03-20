from view import View
from app import App
from node_checker import Node_Checker
from view_checker import View_Checker
from app_checker import App_Checker
from trace import Trace
import os
def print_header(table_type,fd):
	
	if (table_type == "BY_NODE"):
		fd.write("app_id,node_id,class,android_widget,ad,")
		Node_Checker.print_header(fd)
	elif table_type == "BY_APP":
		App.print_header(fd)
		App_Checker.print_header(fd)
	elif table_type == "NODE_CLASS_COUNTS":
		fd.write("class,count")
	fd.write("\n")

def update_classes_count(class_count_dict, app):
	for t in app.traces.values():
		for v in t.views.values():
			for n in v.nodes:
				if n.is_talkback_accessible():
					node_class = n.raw_properties['class']
					if node_class not in class_count_dict.keys():
						class_count_dict[node_class] = 0
					class_count_dict[node_class] +=1

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
	#v = View("677",view_dir)
	#v.print_debug()

	# 4 not wide enough, 7 not tall enough, 9 no speakable text, 2 ads, 5 non-android widgets (just using one library)
	#view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\example_apps\\com.imo.android.imoim\\trace_0\\view_hierarchies\\662.json"

	# # 5 nodes, cont desc editable textfield 1, 3 android widgets, 0 ads, 1 not speakable text, 0 not wide enough, 1 not tall enough
	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	
	#v = View("74",view_dir)
	#v.print_debug()
	#print(str(v.num_tba))
	#print_header("BY_NODE")
	
	#v.print_table("BY_NODE","skype")

	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps_test\com.waze.test\\trace_0\\view_hierarchies\\1540.json"
	#v = View("1540",view_dir)
	#v.print_debug()


	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps_test\com.quizlet.quizletandroid.test\\trace_0\\view_hierarchies\\1246.json"
	#v = View("1246",view_dir)
	#v.print_debug()
	#print("\n############################################\n")
	#trace test
	#file = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider.test\\trace_1"
	#t = Trace(file,"skype_test")
	#t.print_debug()
	# ## Traverse all apps in directory, assume directory only has apps directories
	#apps_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps"
	apps_dir = "E:\\Work\\Research\\Mobile_App_Accessibility\\filtered_traces"

	# all table types to run:
	# maps table type to [file name, file_descriptor]
	table_types = {"BY_APP":["error_by_app.csv",None]}
	# table type options: BY_NODE, BY_APP, (under constructon) BY_VIEW, NODE_CLASS_COUNTS
	if True:
		table_type = "NODE_CLASS_COUNTS"
		# for type,table_info in table_type.items():
		# 	# set file objects
		# 	table_info[1] = open(table_info[0],'w',encoding="utf-8")
		# 	print_header(type,table_info[1])

		fd_name = "node_class_count.csv"
		if os.path.exists(fd_name):
			raise FileExistsError("file exists: "+fd_name)
		fd = open(fd_name, 'w', encoding='utf-8')
		print_header(table_type,fd)
		print("Beginning cycle")
		if table_type=="BY_APP" or table_type == "BY_NODE":
			for a_dir in os.listdir(apps_dir):
				a = App(apps_dir + "\\" + a_dir)
				a.print_table(table_type,fd)
		elif table_type == "NODE_CLASS_COUNTS":
			node_class_counts = {}
			counter = 0
			for a_dir in os.listdir(apps_dir):
				if counter%100==0:
					print(str(counter))
				a = App(apps_dir + "\\" + a_dir)
				update_classes_count(node_class_counts,a)
				counter += 1
			for node_class,count in node_class_counts.items():
				fd.write(str(node_class)+","+str(count)+"\n")

		#close files
		fd.close()
		#for table_info in table_types.values():
		#	table_info[1].close()


