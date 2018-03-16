from check_base import Check_Base

# abstract base class for checks to be run on a node
class View_Check_Base(Check_Base):
	def __init__(self, id_arg, view_arg):
		Check_Base.__init__(self,id_arg)
		# the node this checker is checking
		self.view = view_arg



