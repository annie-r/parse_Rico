
# each "screen" or "view" of an app (a heirarchy.json file from a single trace of a single app)
# creates view's set of Nodes from file
from view_checker import View_Checker
from node import Node
import node_checker
import json
class View:

	def __init__(self, id_arg, file_arg, app_id_arg):
		self.id = id_arg
		self.app_id =app_id_arg
		# json file of viewhierarchy
		self.filepath = file_arg
		self.has_valid_file = False
		# root node
		self.root = None
		# set of Node objects, representing the elements exposed by the view hierarchy	
		self.nodes = []

		#self.num_talkback_nodes = None
		self.num_type_nodes = {'TALKBACK': None, 'CLICKABLE': None, 'NON_CLICKABLE':None, 'EDITABLE_TEXTVIEW': None,
							   'ANDROID_DEFAULT':None, "HAVE_CONT_DESC": None, "WEBVIEW": None}
		#self.num_clickable_nodes = None
		#self.num_editable_textview_nodes = None

		self.__parse_view()
		if not self.has_valid_file:
			return

		self.__set_node_counts()

		# must check nodes from here not when making nodes
		# because need fully formed nodes, e.g. children sturct
		self.check_nodes()

		# to perform checks on this view's nodes
		# must be done last as dependant on the nodes
		self.checker = View_Checker(self)
		self.checker.perform_checks()

	def check_nodes(self):
		for node in self.nodes:
			node.checker.perform_checks()

	##### Gettings and Setters and 
	# checks if the coords land within any Node in the view 
	# coords: dict { "x":x_coord, "y":y_coord}
	# return: Node node if there exists a containing node
	#			else, returns None
	def get_node_containing_coords(self, coords):
		for node in self.nodes:
			if node.contains_coords(coords):
				return node
		return None


	def __add_node(self, node):
		self.nodes.append(node)



	##### PARSING VIEW FILE INTO NODES
	def __parse_view(self):
		#print ("file: "+self.filepath)
		file_data = self.json_loader(self.filepath)

		#if no tree, data will be null
		if(file_data):
			# if is Android home page or lock screen, not valid for the app
			## if beginning of activity name doesn't match app package, throw out
			# attempt to filter out Android home page, etc.
			#print(str(self.filepath))
			if not "activity_name" in file_data.keys():
				self.has_valid_file = False
			else:
				activity = file_data["activity_name"]
				if activity is None:
					self.has_valid_file = False
				else:
					activity_package = file_data["activity_name"].split("/")[0]
					if activity_package == self.app_id:
						self.has_valid_file = True
						root_prop = file_data["activity"]["root"]
						self.root = Node(root_prop, None, 0)
						# parse data
						self.__parse_node(self.root)
					else:
						self.has_valid_file = False
			#if file_data["activity_name"] == "com.android.launcher3/com.android.launcher3.Launcher" or \
			#	file_data["activity_name"] == "com.morrison.applocklite/com.morrison.applocklite.PasswordActivity":
			#	self.has_valid_file = False
			#else:
			#	self.has_valid_file = True
			#	root_prop = file_data["activity"]["root"]
			#	self.root = Node(root_prop, None, 0)
				# parse data
			#	self.__parse_node(self.root)


	# first build tree of children/parent
	# then set characteristics of each node
	def __parse_node(self, node):
		if node.raw_properties == None:
				print("file"+ self.filepath)
		k = node.raw_properties.keys()
		# recursively go through children
		if 'children' in k:
			child_level = node.level + 1
			for child_prop in node.raw_properties["children"]:
				if child_prop != None:
					# create node object with current node as parent
					child = Node(child_prop, node, child_level)
					# add child node to current node's children
					node.add_child(child)
					self.__parse_node(child)
		self.__add_node(node)	

		# determine if talkback focuses


	#### HELPERS ####

	def get_clickable_talkback_nodes(self):
		clickable_talkback_nodes = []
		for n in self.nodes:
			if n.is_clickable() and n.is_talkback_accessible():
				clickable_talkback_nodes.append(n)
		return clickable_talkback_nodes
	# this really needs more comments anyway
	# I have no idea what to type

	def get_num_type_nodes(self, type):
		# shouldn't be because it should set in beginning
		if self.num_type_nodes[type] == None:
			print ("TYPE: "+str(type)+" Is empty")
			self.__set_node_counts()
		return self.num_type_nodes[type]

	def __set_node_counts(self):

		for type in self.num_type_nodes.keys():
			self.num_type_nodes[type] = 0
		for n in self.nodes:

			if n.is_talkback_accessible():
				self.num_type_nodes["TALKBACK"] += 1
				if n.is_android_default_widget():
					self.num_type_nodes["ANDROID_DEFAULT"] += 1

				if n.is_clickable():
					self.num_type_nodes["CLICKABLE"] += 1
				else:
					self.num_type_nodes["NON_CLICKABLE"] += 1

				if n.is_editable_textview():
					self.num_type_nodes["EDITABLE_TEXTVIEW"] += 1

				if n.get_cont_desc() != None:
					self.num_type_nodes["HAVE_CONT_DESC"] += 1

				if n.is_webview():
					self.num_type_nodes["WEBVIEW"] += 1

	#### PRINTERS ####

	def print_table(self,table_type, fd,app_id, trace_id,talkback_focus_only = True):
		if table_type=="BY_NODE" or table_type=="IMAGE_NODE":
			for n in self.nodes:
				if (not talkback_focus_only) and (not n.is_talkback_accessible()):
					fd.write(str(app_id)+","+str(trace_id)+",")
					n.print_table(table_type,fd)
				if n.is_talkback_accessible():
					fd.write(str(app_id)+","+str(trace_id)+","+str(self.id)+",")
					n.print_table(table_type,fd)
		elif table_type == "BY_VIEW":
			self.checker.print_table(table_type,fd)


	# this is an internal function for printing
	# talkback_focus_only: bool if if to only print nodes that are "Talkback Focusable"

	def __print(self, node, fd, talkback_focus_only = True):
		if not talkback_focus_only:
			node.print(fd)
		elif talkback_focus_only and node.is_talkback_accessible():
			node.print(fd)
		for child in node.children:
			self.__print(child, fd, talkback_focus_only)

	# mostly debugging print statement
	def print_debug(self, fd, talkback_focus_only = True):
		fd.write("view ID: "+self.id+"\n")
		fd.write("num nodes: "+str(len(self.nodes))+"\n")
		self.checker.print_debug(fd)
		self.__print(self.root, fd, talkback_focus_only)

	def json_loader(self,filepath):
		file_descriptor = open(filepath, "r")
		#print("file: "+filepath)
		data = json.load(file_descriptor)
		file_descriptor.close()
		#data = yaml.load(file_descriptor)
		return data

