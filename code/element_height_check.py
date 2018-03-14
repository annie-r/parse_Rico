from check_base import Check_Base 
import talkback_accessible

class Element_Height_Check(Check_Base):

	def __init__(self, id_arg, node_arg):
		Check_Base.__init__(self,id_arg, node_arg)

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None

	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		self.result = self.__tall_enough()

	#####
	### Check Height
	#####

	def __tall_enough(self):
		# bounds is 4 node array
		# 0 = left, 1 = top, 2 = right, 3 = bottom
		# google dev guidelines, needs to be 48 dp
		bounds = self.node.get_bounds()
		px_height = bounds['bottom'] - bounds['top']
		# must convert pixel to dp
		dp_height = px_to_dp(px_height)
		dp_height_threshold = 48
		tall_enough = None
		if (dp_height < dp_height_threshold ):
			tall_enough = False
		else:
			tall_enough = True
		return tall_enough

#Helpers
def px_to_dp(px):
		# TODO: figure out dpi/phyical device of RICO
		# conversion of dp units to screen pixels is simple: px = dp * (dpi / 160).
		# https://developer.android.com/guide/practices/screens_support.html
		# calculated from what Google Scanner gave as DP of an element on 
		# the current version of app on Nexus 6P physical device and the 
		# pixel width based on that element's representation in RICO data
		# use dpi = 560
		dpi = 560
		return (px * 160)/dpi