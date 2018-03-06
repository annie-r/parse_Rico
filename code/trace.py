import json
from collections import OrderedDict
import os # for directory parsing

from view import View
class Trace:
	def __init__(self, trace_dir_arg, app_arg):
		self.trace_dir = trace_dir_arg
		# assume trace dir of the form: <.....>\trace_<id>
		# split to trace_<id> then extract ID
		self.id = (self.trace_dir.split("\\")[-1]).split("_")[-1]
		self.app = app_arg
		# map view ID to View object
		self.views = {}
		self.__parse_views_dir()
		# ordered list of gestures performed
		# TODO swipe
		self.gestures = []
		self.__parse_gestures()

	def print_views_table(self):
		# table format
		# app_name, <node info>, <node checks>
		for v in self.views.values():
			v.print_views_table(self.app)

	def print_check(self):
		print("\t", end="")
		print("trace id: "+self.id)
		#print("\tGESTURES")
		#for g in self.gestures:
		#	print("\t\tgesture_id: "+str(g.view_id))
		print("\tVIEWS")
		for v in self.views.values():
			#print("\t\tview_id: "+str(v.id))
			v.print()

	def __parse_views_dir(self):
		# go through trace directory and parse into Views
		# assume each file in view_hierarchy directory is of the form <view_id>.json
		view_directory = self.trace_dir + "\\view_hierarchies"
		for view_file in os.listdir(view_directory):
			view_id = view_file.split(".")[0]
			self.views[view_id] = View(view_id, view_directory + "\\"+ view_file)
			#print(str(view_id))
		return 0

	def __parse_gestures(self):
		## parse json
		ges_data = self.json_loader()
		k = ges_data.keys()
		for view_id, coords in ges_data.items():
			self.gestures.append(Gesture(view_id, coords))

	def json_loader(self):
		gesture_filepath = self.trace_dir + "\\gestures.json"
		file_descriptor = open(gesture_filepath, "r")
		data = json.load(file_descriptor)
		file_descriptor.close()
		data = {int(k):v for k,v in data.items()}

		# gestures need to be in order of view ID #
		# they are not in order in original file
		data = OrderedDict(sorted(data.items()))
		#data = yaml.load(file_descriptor)
		return data
class Gesture:
	def __init__(self, id_arg, coords_arg):
		# view ID of gesture
		self.view_id = id_arg
		# only has one pair or coords is a tap
		# swipe or tap
		# from inspecting by hand on RICO site what
		# data appears to be a swipe action vs a tap
		# on duolingo, trace 0, 
		# taps have < 20 coords and swipes have > 20
		# taps have more than 1 b/c noone has a perfect touch without jiggling

		# for tap, treat first entry as "coordinate" because they should be close enough
		# that it's effective
		if (len(coords_arg) < 20 ):
			self.type = "TAP"
			self.coords = {"x":coords_arg[0][0], "y":coords_arg[0][1]}
		
		# TODO: SWIPE!!!!! determine if useful
		else:
			self.type="SWIPE"
			self.coords = coords_arg

	def print(self):
		#print("T,"+str(self.view_id)+","+str(len(self.coords)))
		print("id: "+str(self.view_id))
		print("num coords: "+str(len(self.coords)))
		print("type: " + self.type)
		#print("coords: "+str(self.coords))