
# each "screen" or "view" of an app (a heirarchy.json file from a single trace of a single app)
# creates view's set of Nodes from file
from view_checker import View_Checker
from node import Node
import node_checker
import json
class View:

	def __init__(self, id_arg, file_arg):
		self.id = id_arg
		# json file of viewhierarchy
		self.filepath = file_arg
		self.has_valid_file = False
		# root node
		self.root = None
		# set of Node objects, representing the elements exposed by the view hierarchy	
		self.nodes = []

		self.__parse_view()

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
			self.has_valid_file = True
			root_prop = file_data["activity"]["root"]
			self.root = Node(root_prop, None, 0)
			# parse data
			self.__parse_node(self.root)


	# first build tree of children/parent
	# then set characteristics of each node
	def __parse_node(self, node):
		k = node.raw_properties.keys()
		# recursively go through children
		if 'children' in k:
			child_level = node.level + 1
			for child_prop in node.raw_properties["children"]:
				# create node object with current node as parent
				child = Node(child_prop, node, child_level)
				# add child node to current node's children
				node.add_child(child)
				self.__parse_node(child)
		self.__add_node(node)	

		# determine if talkback focuses
		node.set_characteristics()

	#### HELPERS ####

	def get_clickable_talkback_nodes(self):
		clickable_talkback_nodes = []
		for n in self.nodes:
			if n.is_clickable() and n.is_talkback_accessible():
				clickable_talkback_nodes.append(n)
		return clickable_talkback_nodes
	# this really needs more comments anyway
	# I have no idea what to type

	def get_num_talkback_nodes(self):
		num_nodes = 0
		for n in self.nodes:
			if n.is_talkback_accessible():
				num_nodes += 1
		return num_nodes

	def print_table(self,table_type,app_id):
		if table_type=="BY_NODE":
			for n in self.nodes:
				if n.is_talkback_accessible():
					print(str(app_id)+",",end="")
					n.print_table(table_type)
					# new line
					print("")
		elif table_type == "BY_VIEW":
			self.checker.print_table(table_type)

	# this is an internal function for printing
	# talkback_focus_only: bool if if to only print nodes that are "Talkback Focusable"

	def __print(self, node, talkback_focus_only = True):
		if not talkback_focus_only:
			node.print()
		elif talkback_focus_only and node.is_talkback_accessible():
			node.print()
		for child in node.children:
			self.__print(child, talkback_focus_only)

	# mostly debugging print statement
	def print_debug(self, talkback_focus_only = True):
		print("view ID: "+self.id)
		print ("num nodes: "+str(len(self.nodes)))
		self.checker.print_debug()
		self.__print(self.root, talkback_focus_only)

	def json_loader(self,filepath):
		file_descriptor = open(filepath, "r")
		#print("file: "+filepath)
		data = json.load(file_descriptor)
		file_descriptor.close()
		#data = yaml.load(file_descriptor)
		return data

