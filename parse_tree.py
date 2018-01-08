
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

def parse_children(root):
	for child in root["children"]:
		k = child.keys()
		if 'children' in k:
			parse_children(child)
		#else:
		if not 'focusable' in k:
			print('not tagged focusable')
		elif child['focusable'] == True:
			hasText = 'text' in k
			hasContentDesc = 'content-desc' in k
			if 'resource-id' in k:
				print("\nresource id: "+str(child["resource-id"]))
			else:
				print("no resource id")
			if 'class' in k:
				print("class:")
				print(child['class'])
			else:
				print("no class")
			if hasContentDesc:
				if(child["content-desc"] == [None]):
					hasContentDesc = False
				print("content desc: ")
				print(child["content-desc"])
			if hasText:
				print ("Text:" + str(child["text"]))
				if child["text"] == "" :
					print("empty text")
					hasText = False
				'''if not child["text"]:
					print ("no text")
					hasText = False'''
			if not hasText and not hasContentDesc:
				print ("inaccessible")
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

def parse_json(filepath):
	file_data = json_loader(filepath)
	root = file_data["activity"]["root"]
	parse_children(root)

def parse_directory(apps_dir):
	for subdir, app_dirs, app_files in os.walk(apps_dir):
		for file in app_files:
			if(file.endswith(".json") and file != "gestures.json"):
				full_path = str(subdir)+"/"+str(file)
				print(full_path)
				parse_json(str(subdir)+"/"+str(file))
		#for trace_subdir, trace_dirs, trace_files in os.walk(subdir):
		#	print ("trace: "+str(trace_subdir))


if __name__ == "__main__":
	filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	filepath = "C:\\Users\\ansross\\Documents\\Research\\Accessibility\\parse_Rico\\com.google.android.gm\\trace_0\\view_hierarchies\\170.json"
	filepath="C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.google.android.gm\\trace_0\\view_hierarchies\\2.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\com.utorrent.client\\trace_0\\view_hierarchies\\3.json"
	#filepath = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\example_apps\\air.com.KalromSystems.SandDrawLite\\trace_0\\view_hierarchies\\197.json"
	parse_json(filepath)
	#parse_directory("C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/example_apps")
	'''filepath = "C:/Users/ansross/Documents/Research/Accessibility/parse_Rico/com.google.android.gm/trace_0/view_hierarchies/170.json"
	file_data = json_loader(filepath)
	root = file_data["activity"]["root"]
	parse_children(root)
'''