## node is an element of the view hierarchy of an Android screen

import talkbackAccessible

class Node:
	# raw_properties are the dictionary of properties associated with the node 9(e.g. "focusable" "cont_desc")
	# characteristics are determined with heuristic tests (e.g. "is speakble" "is visible")
	# parent, pointer to parent node
	# children, empty list of children
	#test
	def __init__(self, properties, parent):
		self.raw_properties = properties
		self.characteristics = {}
		self.initialize_charactertistics()
		self.parent = parent
		self.children = []
		# collects results of check results for individual nodes
		self.checks = {}
		# log to track decisions about talkback accessibility and checks
		# logged by step
		self.log = {'talkback_accessible':[], 'checks':[]}

	def initialize_charactertistics(self):
		# will be focused and attempted read by Talkback
		# an array to add the cause of the decision
		self.characteristics['talkback_accessible'] = False


	def add_child(self,child):
		self.children.append(child)

	# so don't have to remember what order they are in in the json
	def get_bounds(self):
		bounds = self.raw_properties['bounds']
		# the coordinates start in upper left of screen so 0,0 is left, upper-most point
		return {"left":bounds[0], "upper":bounds[1], "right":bounds[2], "lower":bounds[3]}

	def get_px_dimensions(self):
		# bounds are in [left, upper, right, lower]
		bounds = self.raw_properties['bounds']
		px_width = bounds[2] - bounds[0]
		px_height = bounds [3] - bounds[1]
		return [px_width, px_height]

	def print_level(self,level):
		for i in range(0,level):
			print("\t ",end="")
		print("++ ",end="")

	def print(self,level):
		k = self.raw_properties.keys()
		self.print_level(level)
		print("##########")
		# resource id
		self.print_level(level)
		if 'resource-id' in k:
			print("id: " + str(self.raw_properties['resource-id']))
		else: 
			print("no resource id")
		# class
		self.print_level(level)
		if 'class' in k:
			print("class: "+str(self.raw_properties['class']))
		else:
			print('no class')
		# bounds
		self.print_level(level)
		print("bounds: "+str(self.get_bounds()))
		# text, if applicable, to help identify

		if 'text' in self.raw_properties.keys():
			self.print_level(level)
			try:
				print("text: " + str(self.raw_properties['text']))
			except UnicodeEncodeError:
				print("text: undefined unicode")

		self.print_level(level)
		print("label: " + str(talkbackAccessible.get_speaking_text(self)))

		# talkback accessible criteria
		self.print_level(level)
		print("talkback_accessible: " + str(self.characteristics['talkback_accessible']))

		# print talkback accessible log
		for entry in set(self.log['talkback_accessible']):
			self.print_level(level)
			try:
				print("- "+str(entry))
			except UnicodeEncodeError:
				print("-: undefined unicode")

		# print results of checks
		self.print_level(level)
		print("checks results")
		for check, result in self.checks.items():
			self.print_level(level)
			print(check + ": "+str(result))

		# print checks log
		for entry in set(self.log['checks']):
			self.print_level(level)
			print("- "+str(entry))
		print ('\n')

