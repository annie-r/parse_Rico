## not sure if making right inferences based on visible elements who get their text from invisible children\
# see gmail 385 
# for merge

#import com.android.provider.Settings
import time, sys, os.path, os
import subprocess #for running monkey command to start app with package name alone
#print sys.path
sys.path.append(os.path.join('/usr/lib/python2.7/dist-packages/'))
#print sys.path
import yaml
import json
from talkbackAccessible import talkback_focus, get_role
from node import Node
from checker import Checker



def json_loader(filepath):
	file_descriptor = open(filepath, "r")
	data = json.load(file_descriptor)
	#data = yaml.load(file_descriptor)
	return data

# recursively parse all children 
#TODO case where just root
def parse_node(node, ancestor_focusable, checker): 
	k = node.raw_properties.keys()
	children_visible = False
	# recursively go through children
	if 'children' in k:
		for child_prop in node.raw_properties["children"]:
			# create node object with current node as parent
			child = Node(child_prop, node)
			# add child node to current node's children
			node.add_child(child)
			parse_node(child, ancestor_focusable,checker)
	checker.add_node(node)	

	# determine if talkback focuses
	node.characteristics['talkback_accessible']= talkback_focus(node)



def parse_json(filepath):
	print ("file: "+filepath)
	checker = Checker(filepath)
	#checks = {}
	#initialize_checks(checks)
	file_data = json_loader(filepath)

	''' TO TEST
	if(file_data):
		checks.update({"has_file":True})
		root_prop = file_data["activity"]["root"]
		root = Node(root_prop, None)
		should_focus(root)
'''
	#if no tree, data will be null
	if(file_data):
		checker.add_overall_check('has_file',True)
		root_prop = file_data["activity"]["root"]
		root = Node(root_prop, None)
		print("created node")
		# parse data
		parse_node(root, False, checker)

		# run checks on all nodes
		# run relevant checks
		checker.perform_checks()

		print("\n\n TREE:")
		print_tree(root)#, talkback_focus_only=True)
	else:
		checks.add_overall_check("has_file", False)
		#print("no tree")
	
	checker.print_overall_checks()

	'''
	for check, val in checks.items():
		print(check +" : "+ str(val))
		'''

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

def print_node(node, level, talkback_focus_only):
	# print self
	if not talkback_focus_only:
		node.print(level)
	# if only want to print talkback focused, check that it's talkback accessible 
	# before printing
	elif talkback_focus_only and node.characteristics['talkback_accessible']:
		node.print(level)

	# increment level for children
	level += 1
	# print children
	for child in node.children:
		print_node(child, level, talkback_focus_only)

def print_tree(root, talkback_focus_only=False):
	level = 0
	print_node(root,level, talkback_focus_only)


if __name__ == "__main__":

	''
	filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	filepath = "C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\com.google.android.gm\\trace_0\\view_hierarchies\\170.json"
	filepath="C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.google.android.gm\\trace_0\\view_hierarchies\\2.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.utorrent.client\\trace_0\\view_hierarchies\\3.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\com.utorrent.client\\trace_0\\view_hierarchies\\240.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\test.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\air.com.KalromSystems.SandDrawLite\\trace_0\\view_hierarchies\\197.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\com.google.android.gm\\trace_0\\view_hierarchies\\385.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\example_apps\\com.imo.android.imoim\\trace_0\\view_hierarchies\\662.json"
	## Problem in imo 492 not identifying the search and hamburger button as accessibility focusable, likely because unlabeled but don't know what heuristic is failing
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\\test1.json"
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.duolingo\\trace_0\\view_hierarchies\\1571.json"
	# overlapping elements
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.waze\\trace_0\\view_hierarchies\\1540.json"
	# cont desc editable textfield
	filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.skype.raider\\trace_1\\view_hierarchies\\74.json"
	parse_json(filepath)
	#parse_directory("C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\example_apps")
	#parse_directory("C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/example_apps")
	'''filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	file_data = json_loader(filepath)
	root = file_data["activity"]["root"]
	parse_node(root)
'''