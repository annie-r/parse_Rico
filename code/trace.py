import json
from collections import OrderedDict
import os # for directory parsing
from trace_checker import Trace_Checker
from talkback_accessible import window_bounds, window_height, window_width
from view import View
class Trace:
	def __init__(self, trace_dir_arg, app_arg):
		self.trace_dir = trace_dir_arg
		# assume trace dir of the form: <.....>\trace_<id>
		# split to trace_<id> then extract ID
		self.id = (self.trace_dir.split("\\")[-1]).split("_")[-1]
		self.app_id = app_arg
		# map view ID to View object
		self.views = {}
		self.num_null_views = 0
		self.__parse_views_dir()
		# ordered list of gestures performed
		# TODO swipe
		self.gestures = []
		self.__parse_gestures()

		self.checker = Trace_Checker(self)

	@staticmethod
	def print_header(fd):
		fd.write("app_id,trace_id,num_gestures,num_views,num_null_views,")

	def print_table(self, table_type, fd, talkback_focus_only = True):
		if table_type == "BY_TRACE":
			fd.write(str(self.app_id)+","+str(self.id)+","+str(len(self.gestures))+"," \
					 + str(len(self.views.keys()))+ "," +str(self.num_null_views)+",")
			self.checker.print_table(table_type, fd)
			fd.write("\n")

		elif table_type == "BY_NODE":
			# table format
			# app_name, <node info>, <node checks>
			for v in self.views.values():
				#fd.write(str(self.app_id)+","+str(self.id)+",")
				v.print_table(table_type, fd, self.app_id, self.id, talkback_focus_only)
		elif table_type == "BY_VIEW":
			for v in self.views.values():
				v.print_table(table_type, fd, self.app_id, talkback_focus_only)

	def print_debug(self):
		print("\t", end="")
		print("trace id: "+self.id)
		#print("\tGESTURES")
		#for g in self.gestures:
		#	print("\t\tgesture_id: "+str(g.view_id))
		print("\tVIEWS")
		for v in self.views.values():
			#print("\t\tview_id: "+str(v.id))
			v.print_debug()

	def __parse_views_dir(self):
		# go through trace directory and parse into Views
		# assume each file in view_hierarchy directory is of the form <view_id>.json
		view_directory = self.trace_dir + "\\view_hierarchies"
		for view_file in os.listdir(view_directory):
			view_id = view_file.split(".")[0]
			#print ("view ID: "+str(view_id))
			v = View(view_id, view_directory + "\\"+ view_file)
			# only count and consider valid non-null views
			if v.has_valid_file:
				self.views[int(view_id)] = v
			#print(str(view_id))
		#print(str(self.views.keys()))
		#return 0

	def __parse_gestures(self):
		## parse json
		ges_data = self.json_loader()
		k = ges_data.keys()
		for view_id, coords in ges_data.items():
			#ignore empty coords (e.g. com.google.android.gm, trace 2)
			if len(coords) > 0:
				self.gestures.append(Gesture(view_id, coords))

	def json_loader(self):
		gesture_filepath = self.trace_dir + "\\gestures.json"
		file_descriptor = open(gesture_filepath, "r")
		data = json.load(file_descriptor)
		file_descriptor.close()
		int_data = {}
		#print("file:"+str(gesture_filepath))
		for k,v in data.items():
			if k != '' and len(v)>0:
				int_data[int(k)]=v
		#data = {int(k):v for k,v in data.items()}


		# gestures need to be in order of view ID #
		# they are not in order in original file
		int_data = OrderedDict(sorted(int_data.items()))
		#data = yaml.load(file_descriptor)
		return int_data
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
			#print("view id: "+str(self.view_id)+ "coords "  +str(coords_arg))
			# coords come in as percentage down screen, so have to re-save as screen based coord

			self.coords = {"x":coords_arg[0][0]*window_width, "y":coords_arg[0][1]*window_height}
		
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