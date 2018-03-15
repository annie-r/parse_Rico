from node_check_base import Node_Check_Base 
import talkback_accessible
from element_height_check import px_to_dp

class Element_Width_Check(Node_Check_Base):

	def __init__(self, id_arg, node_arg):
		Node_Check_Base.__init__(self,id_arg, node_arg)

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None

	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		if self.node.is_talkback_accessible():
			self.result = self.__wide_enough()
		else:
			self.result = "na"

	#####
	### Check Width
	#####

	def __wide_enough(self):
		#k = self.node.raw_properties.keys()
		# bounds is 4 node array
		# 0 = left, 1 = top, 2 = right, 3 = bottom
		# google dev guidelines, needs to be 48 dp
		bounds = self.node.get_bounds()
		px_width = bounds['right'] - bounds['left']
		# must convert pixel to dp

		dp_width = px_to_dp(px_width)
		dp_width_threshold = 48
		wide_enough = None
		if (dp_width < dp_width_threshold ):
			wide_enough = False
		else:
			wide_enough = True
		return wide_enough