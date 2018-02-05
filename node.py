## node is an element of the view hierarchy of an Android screen

class Node:
	# raw_properties are the dictionary of properties associated with the node 9(e.g. "focusable" "cont_desc")
	# characteristics are determined with heuristic tests (e.g. "is speakble" "is visible")
	# parent, pointer to parent node
	# children, empty list of children
	def __init__(self, properties, parent):
		self.raw_properties = properties
		self.characteristics = {}
		self.initialize_charactertistics()
		self.parent = parent
		self.children = []

	def initialize_charactertistics(self):
		# will be focused and attempted read by Talkback
		# an array to add the cause of the decision
		self.characteristics['talkback_accessible'] = [False,]
		# has characteristics of being speakable by Talkback
		self.characteristics['is_speakable'] = False 
		# has an actual non-null field to be read by Talkback
		self.characteristics['has_label'] = False

	def add_child(self,child):
		self.children.append(child)

	def print_level(self,level):
		for i in range(0,level):
			print("\t+ ",end="")

	def print(self,level):
		k = self.raw_properties.keys()
		self.print_level(level)
		print("##########")
		self.print_level(level)
		if 'resource_id' in k:
			print("id: " + str(self.raw_properties['resource_id']))
		else: 
			print("no resource id")
		self.print_level(level)
		print("talkback_accessible: " + str(self.characteristics['talkback_accessible'][0]))
		for reason in self.characteristics['talkback_accessible']:
			self.print_level(level)
			print(" - "+str(reason))
		print ('\n')

