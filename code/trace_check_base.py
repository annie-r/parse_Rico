from check_base import Check_Base

# abstract base class for checks to be run on a node
class Trace_Check_Base(Check_Base):
	def __init__(self, id_arg, trace_arg):
		Check_Base.__init__(self,id_arg)
		# the node this checker is checking
		self.trace = trace_arg



