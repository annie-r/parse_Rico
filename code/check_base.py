

# abstract base class for checks to be run on a node
class Check_Base:
	def __init__(self, node_arg, id_arg):
		# the node this checker is checking
		self.node = node_arg
		self.id = id_arg
		# list of info that determined check
		self.log = []
		self.result = None

	def get_id(self):
		return self.id

	def get_result(self):
		return self.result
	def perform(self):
		raise NotImplementedError()


