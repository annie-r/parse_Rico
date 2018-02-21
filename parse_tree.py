
## not sure if making right inferences based on visible elements who get their text from invisible children\
# see gmail 385 


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
	has_text = 'text' in k
	has_content_desc = 'content-desc' in k
	# check if existing fields have content
	if has_content_desc:
		if(child["content-desc"] == [None]):
			has_content_desc = False
		#print("content desc: ")
		#print(child["content-desc"])
	if has_text:
		#print ("Text:" + str(child["text"]))
		if child["text"] == "" :
			#print("empty text")
			has_text = False
	#print("RESULT: ")
	# must have non-empty/null text or cont_desc to pass
	if not has_text and not has_content_desc:
		pass_label = False
		#print ("inaccessible")
	else:
		pass_label = True
		#print("accessible")
	# return if has label 
	return pass_label

def px_to_dp(px):
	# TODO: figure out dpi/phyical device of RICO
	# conversion of dp units to screen pixels is simple: px = dp * (dpi / 160).
	# assuming mdpi device, so dpi = 160
	# https://developer.android.com/guide/practices/screens_support.html
	# assuming mdpi device, so dpi = 160
	dpi = 160
	return (px * 160)/dpi

def wide_enough(element):
	k = element.keys()
	# bounds is 4 element array
	# 0 = left, 1 = top, 2 = right, 3 = bottom
	# google dev guidelines, needs to be 48 dp
	bounds = element["bounds"]
	px_width = bounds[2] - bounds[0]
	# must convert pixel to dp

	dp_width = px_to_dp(px_width)
	dp_width_threshold = 48
	wide_enough = None
	if (dp_width < dp_width_threshold ):
		wide_enough = False
	else:
		wide_enough = True
	return wide_enough

def tall_enough(element):
	k = element.keys()
	# bounds is 4 element array
	# 0 = left, 1 = top, 2 = right, 3 = bottom
	# google dev guidelines, needs to be 48 dp
	bounds = element["bounds"]
	px_height = bounds[3] - bounds[1]
	# must convert pixel to dp
	dp_height = px_to_dp(px_height)
	dp_height_threshold = 48
	tall_enough = None
	if (dp_height < dp_height_threshold ):
		tall_enough = False
	else:
		tall_enough = True
	return tall_enough




# recursively parse all children 
# only actually parse leaf elements
#TODO case where just root
def parse_children(root, checks):
	#num_focusable = 0
	for child in root["children"]:
		k = child.keys()
		# if has children, analyze them
		if 'children' in k:
			#print("has children")
			#num_focusable += parse_children(child, checks)
			parse_children(child,checks)
		# test all elements, run tests
		
		# TODO: is right to only check focusable elements?
		# only focusable elements need to be tested
		'''if 'resource-id' in k:
			print("\nresource id: "+str(child["resource-id"]))
		else:
			print("no resource id")
		'''
		if not 'focusable' in k:
			#print("not focus")
			print('not tagged focusable')
		elif child['focusable'] == True or child["clickable"] == True:
			#print ("focus")
			if(child['focusable']):
				checks['num_focusable'] += 1
			if(child['clickable']):
				checks['num_clickable'] += 1
			if child['focusable'] and child['clickable']:
				checks['num_foc_and_click'] +=1
			
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
			#print ("updating")
			if(not has_label(child)):
				print ("no label")
				checks['unlabeled_elements'] += 1

			## Check element is wide enough
			if(not wide_enough(child)):
				print ("not wide")
				checks['num_not_wide_enough'] += 1
			## Check element is tall enough
			if not tall_enough(child):
				print ("not tall")
				checks['num_not_tall_enough'] += 1
		#else:
		#	print ("focus false")

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
	checks['num_clickable']=0
	checks['num_not_wide_enough']=0
	checks['num_not_tall_enough']=0
	checks['num_foc_and_click']=0

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
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\com.utorrent.client\\trace_0\\view_hierarchies\\286.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\com.imo.android.imoim\\trace_0\\view_hierarchies\\485.json"
	
	parse_json(filepath)
	#parse_directory("C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\example_apps")
	#parse_directory("C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/example_apps")
	'''filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	file_data = json_loader(filepath)
	root = file_data["activity"]["root"]
	parse_children(root)
'''