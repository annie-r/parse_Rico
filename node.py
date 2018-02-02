## node is an element of the view hierarchy of an Android screen

class Node:
	# properties are the dictionary of properties associated with the node 9(e.g. "focusable" "cont_desc")
	# parent, pointer to parent node
	# children, empty list of children
	def __init__(self, properties, parent):
		self.properties = properties
		self.parent = parent
		self.children = []

	def add_child(self,child):
		self.children.append(child)

