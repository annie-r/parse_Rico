from speakable_text_present_check import Speakable_Text_Present_Check

class Node_Checker:
	def __init__(self, node_arg):
		# the node this checker is checking
		self.node = node_arg
		self.log = []


		# list of checks to perform on node
		# map id to CHECK object
		self.checks = {}
		self.__initialize_checks()

	def __initialize_checks(self):
		#some tests only to be performed on talkback accessible nodes
		if self.node.is_talkback_accessible():
			self.checks["Speakable_Text_Present"]= Speakable_Text_Present_Check(self.node)

	def perform_checks(self):
		for check in self.checks.values():
			check.perform()

	def print_views_table(self):
		# print order:
		# has_speakable_text_present, 
		if self.node.is_talkback_accessible():
			print(str(self.checks['Speakable_Text_Present'].result)+",",end="")

def print_checker_header():
	print("Speakable_Text_Present,",end="")

