from view_check_base import View_Check_Base 
import talkback_accessible

class Num_Full_Overlap_Clickable(View_Check_Base):

	def __init__(self, id_arg, view_arg):
		View_Check_Base.__init__(self,id_arg, view_arg)

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None
	# this is only applicable to talkback_accessible nodes
	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		clickable_nodes = self.view.clickable_nodes
		
		if self.node.is_talkback_accessible():
			self.result = self.__has_label()
		else:
			self.result = "na"