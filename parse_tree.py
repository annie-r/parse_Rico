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
from talkbackAccessible import talkback_accessible
from node import Node



def json_loader(filepath):
	file_descriptor = open(filepath, "r")
	data = json.load(file_descriptor)
	#data = yaml.load(file_descriptor)
	return data

# check if an item has text or content_desc
''' moved to talkbackAccessible
def has_label(child):
	'''
	
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
#TODO case where just root
def parse_child(node, ancestor_focusable, checks, level):
	#level 
	k = node.properties.keys()
	#if 'resource-id' in k:
	#	print("\n~~~~resource id: "+str(element["resource-id"]))
	#else:
	#	print("\n~~~~no resource id")
	children_visible = False
	# recursively go through children
	if 'children' in k:
		for child_prop in node.properties["children"]:
			# create node object with current node as parent
			child = Node(child_prop, node)
			# add child node to current node's children
			node.add_child(child)
			next_level = level + 1
			child_visible = parse_child(child, ancestor_focusable,checks, next_level)
			# only need one visible child to pass the test
			if child_visible:
				children_visible = child_visible
	for i in range(0,level):
		print("\t",end="")
	if 'resource-id' in k:
		print("resource id: "+str(node.properties["resource-id"]))
	else:
		print("no resource id")
	# only run checks on elements that talkback (and therefore switch?) would focus on
	if (talkback_accessible(node, ancestor_focusable, children_visible)):
		checks['num_talkback_accessible'] +=1
		print ("talkback_accessible")
		## has cont_desc or label
		#TODO : dif b/t non-speaking and bad labeling
		'''
		if(not has_label(node)):
			checks['num_unlabeled'] += 1
			print("no label")
		'''
	checks['num_elements'] +=1	

	return node.properties['visibility'] == 'visible'	
	
def initialize_checks(checks):
	checks['num_unlabeled']=0
	checks['num_talkback_accessible']=0
	checks['num_elements']=0
	checks['num_not_wide_enough']=0
	checks['num_not_tall_enough']=0

def parse_json(filepath):
	print ("file: "+filepath)
	checks = {}
	initialize_checks(checks)
	file_data = json_loader(filepath)
	#if no tree, data will be null
	if(file_data):
		checks.update({"has_file":True})
		root_prop = file_data["activity"]["root"]
		root = Node(root_prop, None)
		print("created node")
		parse_child(root, False, checks,0)
	else:
		checks.update({"has_file":False})
		#print("no tree")
	print("\n\n")
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

	''
	filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	filepath = "C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\com.google.android.gm\\trace_0\\view_hierarchies\\170.json"
	filepath="C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.google.android.gm\\trace_0\\view_hierarchies\\2.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.utorrent.client\\trace_0\\view_hierarchies\\3.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\com.utorrent.client\\trace_0\\view_hierarchies\\286.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\test.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\air.com.KalromSystems.SandDrawLite\\trace_0\\view_hierarchies\\197.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\com.google.android.gm\\trace_0\\view_hierarchies\\385.json"

	parse_json(filepath)
	#parse_directory("C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\example_apps")
	#parse_directory("C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/example_apps")
	'''filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	file_data = json_loader(filepath)
	root = file_data["activity"]["root"]
	parse_children(root)
'''