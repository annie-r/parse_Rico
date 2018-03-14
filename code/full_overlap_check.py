from check_base import Check_Base 
import talkback_accessible

class Full_Overlap_Check(Check_Base):

	def __init__(self, id_arg, node_arg):
		Check_Base.__init__(self,id_arg, node_arg)

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None

	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		self.result = self.__has_label()


		#####
	### Check exact overlap
	### checks if two clickable nodes occupy the exact same place on the screen
	#####

	def __full_overlap_clickable(self,node):
		num_full_overlap = 0
		for n in self.clickable_nodes:
			if n==node:
				continue
			else:
				if self.full_overlap_compare(node, n):
					num_full_overlap += 1
		return num_full_overlap

	# check if two elements n1 and n2 occupy the exact same space 
	def __full_overlap_compare(self, node1,node2):
		b1 = node1.get_bounds()
		b2 = node2.get_bounds()
		if(b1['upper'] == b2['upper'] and b1['lower'] == b2['lower'] and \
			b1['left'] == b2['left'] and b1['right'] == b2['right']):
			return True
		return False