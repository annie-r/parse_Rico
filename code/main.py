from view import View
from app import App
from node_checker import Node_Checker
from view_checker import View_Checker
from app_checker import App_Checker
from trace import Trace
from trace_checker import Trace_Checker
from node import Node
import os
import csv

def print_header(table_type,fd):
	
	if (table_type == "BY_NODE"):
		Node.print_header(table_type,fd)
		Node_Checker.print_header(fd)
	elif (table_type=="IMAGE_NODE"):
		Node.print_header(table_type,fd)
		Node_Checker.print_header(fd)
	elif table_type == "BY_APP":
		App.print_header(fd, table_type)
		App_Checker.print_header(fd)
	elif table_type == "APP_INFO_ONLY":
		App.print_header(fd,table_type)
	elif table_type == "BY_TRACE":
		Trace.print_header(fd)
		Trace_Checker.print_header(fd)
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

def get_app_info(app_info_file_path):
	with open(app_info_file_path, 'r', encoding='utf-8') as f:
		app_info_dict = {}
		#print(str(f))
		reader = csv.reader(f)
		row_count = 0
		for row in reader:
			if row_count == 0:
				row_count += 1
				continue
			row_count += 1
			# map pacakge: { category: '', rating: #,
			# num_ratings: #, num_downloads: <range>
			# #, date_updated: <M d, y>}
			app_info_dict[row[0]] = {"name":row[1], "category":row[2], "rating":float(row[3]),
							"num_ratings":int(row[4]), "num_downloads":row[5],
							"date_updated":row[6]}
		return app_info_dict
if __name__ == "__main__":

	# with open('app_details.csv', 'r', encoding='utf-8') as f:
	# 	dict = {}
	# 	#print(str(f))
	# 	reader = csv.reader(f)
	# 	row_count = 0
	# 	for row in reader:
	# 		if row_count == 0:
	# 			row_count += 1
	# 			continue
	# 		row_count += 1
	# 		try:
	# 			# map pacakge: { category: #, rating: #,
	# 			# num_ratings: #, num_downloads: #
	# 			# #, date_updated: #}
	# 			dict[row[0]] = {"category":row[2], "rating":row[3],
	# 							"num_ratings":row[4], "num_downloads":row[5],
	# 							"date_updated":row[6]}
	# 			#print(str(row))
	# 		except UnicodeDecodeError:
	# 			print("error")
	# 	print(str(dict))
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

	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.waze\\trace_0\\view_hierarchies\\6527.json"
	#v = View("1246",view_dir)
	#v.print_debug()

	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.imo.android.imoim\\trace_0\\view_hierarchies\\662.json"
	#v = View("662",view_dir)
	#v.print_debug()


	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps_test\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	#v = View("662",view_dir)
	#v.print_debug()

	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps_test\com.skype.raider\\trace_1\\view_hierarchies\\677.json"
	#v = View("662",view_dir)
	#v.print_debug()

	view_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps_test\co.petcoach\\trace_0\\view_hierarchies\\8.json"
	#v = View("8",view_dir)
	#v.print_debug()

	view_dir ="C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps_test\sample\\trace_0\\view_hierarchies\\190.json"
	#v = View("190",view_dir)
	#fd = open("testview.txt",'w',encoding="utf-8")
	#v.print_debug(fd)
	#fd.close()

	#print("\n############################################\n")
	#trace test
	#file = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider.test\\trace_1"
	#t = Trace(file,"skype_test")
	#t.print_debug()

	#apps_dir = "E:\\Work\\Research\\Mobile_App_Accessibility\\filtered_traces"



	############## MAIN #################
	# ## Traverse all apps in directory, assume directory only has apps directories
	#apps_dir = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\example_apps_test"
	apps_dir = "E:\\Work\\Research\\Mobile_App_Accessibility\\filtered_traces"
	# all table types to run:
	# maps table type to [file name, file_descriptor===None to start]
	table_types = {"IMAGE_NODE":["node_drop_package.csv",None], "BY_APP":["app_drop_package.csv",None]}#"APP_INFO_ONLY":["app_info.csv",None]}#"BY_APP":["all_app.csv",None]}#,}
	#!!!!! THERE IS AN APP NAMED LOVE QUOTE", MUST GO INTO CSV AND DELETE THE " at the end of the app name!!!! app_id == net.ayudaporfavor.Love


	# table type options: BY_NODE, BY_APP, (under constructon) BY_VIEW, NODE_CLASS_COUNTS
	app_info_filepath = "rico_app_details.csv"
	app_info = get_app_info(app_info_filepath)

	#f =open('rating.csv','w',encoding="utf-8")
	#for a in app_info.values():
	#	f.write(str(a['rating'])+'\n')
	#f.write("\n")
	#f.close()
	if True:
		#table_type = "NODE_CLASS_COUNTS"
		for type,table_info in table_types.items():
			# set file objects
			if os.path.exists(table_info[0]):
				# don't accidently write over old data
				raise FileExistsError("file exists: "+table_info[0])
			table_info[1] = open(table_info[0],'w',encoding="utf-8")
			print_header(type,table_info[1])
		print("Beginning cycle")
		#only want to go through raw dataset once and create all tables from it

		counter = 0
		## aggregating variables:

		# for NODE_CLASS_COUNTS
		node_class_counts = {}


		for a_dir in os.listdir(apps_dir):
			if counter%100 == 0:
				print(str(counter))
			counter += 1
			info_only = False
			if len(table_types.keys()) == 1 and "APP_INFO_ONLY" in table_types.keys():
				info_only = True
			a = App(apps_dir + "\\" + a_dir, app_info, info_only=info_only)


			# any aggregate updates from app
			if "NODE_CLASS_COUNTS" in table_types.keys():
				update_classes_count(node_class_counts,a)

			# print row of appropriate tables
			if "BY_APP" in table_types.keys():
				a.print_table("BY_APP", table_types["BY_APP"][1])
			if "APP_INFO_ONLY" in table_types.keys():
				a.print_table("APP_INFO_ONLY", table_types["APP_INFO_ONLY"][1])
			if "BY_NODE" in table_types.keys():
				a.print_table("BY_NODE", table_types["BY_NODE"][1])
			if "BY_TRACE" in table_types.keys():
				a.print_table("BY_TRACE", table_types["BY_TRACE"][1])
			if "IMAGE_NODE" in table_types.keys():
				a.print_table("IMAGE_NODE", table_types["IMAGE_NODE"][1])


		if "NODE_CLASS_COUNTS" in table_types.keys():
			for node_class,count in node_class_counts.items():
				table_types["NODE_CLASS_COUNTS"][1].write(str(node_class)+","+str(count)+"\n")
		#
		# if table_type=="BY_APP" or table_type == "BY_NODE":
		# 	for a_dir in os.listdir(apps_dir):
		# 		a = App(apps_dir + "\\" + a_dir)
		# 		a.print_table(table_type,fd)
		# elif table_type == "NODE_CLASS_COUNTS":
		# 	node_class_counts = {}
		# 	counter = 0
		# 	for a_dir in os.listdir(apps_dir):
		# 		if counter%100==0:
		# 			print(str(counter))
		# 		a = App(apps_dir + "\\" + a_dir)
		# 		update_classes_count(node_class_counts,a)
		# 		counter += 1
		# 	for node_class,count in node_class_counts.items():
		# 		fd.write(str(node_class)+","+str(count)+"\n")

		#close files
		#fd.close()
		for table_info in table_types.values():
			table_info[1].close()


