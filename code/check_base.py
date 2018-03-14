

# abstract base class for checks to be run on a node
class Check_Base:
	def __init__(self, id_arg, node_arg):
		# the node this checker is checking
		self.node = node_arg
		self.id = id_arg
		# list of info that determined check
		self.log = []
		self.result = None

	# the ID should give sense of if the purpose, aka the name
	def get_id(self):
		return self.id


	def get_result(self):
		return self.result

	# must set self.result
	# all nodes must have perform function so that a list of checks can be called without knowing what's what
	# aka the purpose of inheritance
	def perform(self):
		raise NotImplementedError()


