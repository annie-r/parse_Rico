## IS NOT PARSING ALL CHILDREN!!
# see Sand 3.json as example 

#import com.android.provider.Settings
import time, sys, os.path, os
import subprocess #for running monkey command to start app with package name alone
#print sys.path
sys.path.append(os.path.join('/usr/lib/python2.7/dist-packages/'))
#print sys.path
import yaml
import json



def json_loader(filepath):
	file_descriptor = open(filepath, "r")
	data = json.load(file_descriptor)
	#data = yaml.load(file_descriptor)
	return data

# check if an item has text or content_desc
def has_label(child):
	pass_label = False
	k = child.keys()
	# set to if the field exists
	hasText = 'text' in k
	hasContentDesc = 'content-desc' in k
	# check if existing fields have content
	if hasContentDesc:
		if(child["content-desc"] == [None]):
			hasContentDesc = False
		#print("content desc: ")
		#print(child["content-desc"])
	if hasText:
		#print ("Text:" + str(child["text"]))
		if child["text"] == "" :
			#print("empty text")
			hasText = False
	#print("RESULT: ")
	# must have non-empty/null text or cont_desc to pass
	if not hasText and not hasContentDesc:
		pass_label = False
		print ("inaccessible")
	else:
		pass_label = True
		print("accessible")
	# return if has label 
	return pass_label

# recursively parse all children 
# only actually parse leaf elements
#TODO case where just root
def parse_children(root, checks):
	#num_focusable = 0
	for child in root["children"]:
		k = child.keys()
		# if has children, analyze them
		if 'children' in k:
			print("has children")
			#num_focusable += parse_children(child, checks)
			parse_children(child,checks)
		# test all elements, run tests
		
		# TODO: is right to only check focusable elements?
		# only focusable elements need to be tested
		if 'resource-id' in k:
			print("\nresource id: "+str(child["resource-id"]))
		else:
			print("no resource id")
		if not 'focusable' in k:
			print("not focus")
			print('not tagged focusable')
		elif child['focusable'] == True:
			print ("focus")
			checks['num_focusable'] += 1
			
			
			if 'resource-id' in k:
				print("\nresource id: "+str(child["resource-id"]))
			else:
				print("no resource id")
			#if 'class' in k:
				#print("class:")
				#print(child['class'])
			#else:
				#print("no class")


			########### PER ELEMENT CHECK LIST

			## Check for existance of label 
			print ("updating")
			if(not has_label(child)):
				checks['unlabeled_elements'] += 1
		else:
			print ("focus false")

	#return num_focusable
	'''
		if 'class' in k:
			if(child['class'] == "android.support.design.widget.FloatingActionButton" or
				child['class'] == "android.widget.ImageButton" or
				child['class'] == "android.widget.ImageView" 
				):
				print("class: ")
				print(child['class'])
				if 'content-desc' in k:
					print("content desc: ")
					print(child["content-desc"])

				else:
					print("no content desc\n")
				if 'resource-id' in k:
					print(child["resource-id"])
				else:
					print("no resource id")
					'''

def initialize_checks(checks):
	checks['unlabeled_elements']=0
	checks['num_focusable']=0

def parse_json(filepath):
	checks = {}
	initialize_checks(checks)
	file_data = json_loader(filepath)
	#if no tree, data will be null
	if(file_data):
		checks.update({"has_file":True})
		root = file_data["activity"]["root"]
		parse_children(root, checks)
		if checks['num_focusable'] == 0:
			checks.update({"has_focusable":False})
			#print ("none focusable")
		else:
			checks.update({"has_focusable":True})
	else:
		checks.update({"has_file":False})
		#print("no tree")
	print ("file: "+filepath)
	for check, val in checks.items():
		print(check +" : "+ str(val))

def parse_directory(apps_dir):
	for subdir, app_dirs, app_files in os.walk(apps_dir):
		for file in app_files:
			if(file.endswith(".json") and file != "gestures.json"):
				full_path = str(subdir)+"/"+str(file)
				print("+++++++++++++++++++")
				#print("\npath: " + full_path)
				parse_json(str(subdir)+"/"+str(file))
				print("-------------------")
		#for trace_subdir, trace_dirs, trace_files in os.walk(subdir):
		#	print ("trace: "+str(trace_subdir))



if __name__ == "__main__":
	filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	filepath = "C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\com.google.android.gm\\trace_0\\view_hierarchies\\170.json"
	filepath="C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.google.android.gm\\trace_0\\view_hierarchies\\2.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.utorrent.client\\trace_0\\view_hierarchies\\3.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\com.utorrent.client\\trace_0\\view_hierarchies\\46.json"
	parse_json(filepath)
	#parse_directory("C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\example_apps")
	#parse_directory("C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/example_apps")
	'''filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	file_data = json_loader(filepath)
	root = file_data["activity"]["root"]
	parse_children(root)
'''