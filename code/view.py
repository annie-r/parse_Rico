
# each "screen" or "view" of an app (a heirarchy.json file from a single trace of a single app)
# creates view's set of Nodes from file
from view_checker import View_Checker
from node import Node
import json
class View:
	
	def __init__(self, file):
		# json file of viewhierarchy
		self.filepath = file
		self.has_valid_file = False
		# root node
		self.root = None
		# set of Node objects, representing the elements exposed by the view hierarchy	
		self.nodes = []
		# to perform checks on this view's nodes
		self.checker = View_Checker(self)

		self.num_nodes = 0

		self.__parse_view()


	##### Gettings and Setters
	def __add_node(self, node):
		self.nodes.append(node)
		self.num_nodes += 1

	def __print(self, node, talkback_focus_only = True):
		if not talkback_focus_only:
			node.print()
		elif talkback_focus_only and node.is_talkback_accessible():
			node.print()
		for child in node.children:
			self.__print(child, talkback_focus_only)

	def print(self, talkback_focus_only = True):
		print ("num nodes: "+str(len(self.nodes)))
		self.__print(self.root, talkback_focus_only)

	##### PARSING VIEW FILE INTO NODES
	def __parse_view(self):
		print ("file: "+self.filepath)
		file_data = self.json_loader(self.filepath)

		#if no tree, data will be null
		if(file_data):
			self.has_valid_file,True
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
	def json_loader(self,filepath):
		file_descriptor = open(filepath, "r")
		data = json.load(file_descriptor)
		#data = yaml.load(file_descriptor)
		return data
