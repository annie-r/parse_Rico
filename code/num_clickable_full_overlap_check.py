from view_check_base import View_Check_Base 
import talkback_accessible

class Num_Clickable_Full_Overlap_Check(View_Check_Base):

	def __init__(self, id_arg, view_arg):
		View_Check_Base.__init__(self,id_arg, view_arg)

		# result is number of clickable nodes that fully overlap


	def perform(self):
		self.result = 0
		clickable_talkback_nodes = self.view.get_clickable_talkback_nodes()
		for n in self.view.nodes:
			# only important for clicable and accessibility important nodes
			# in testing framework, uses isImportantForAccessibility
			# TODO: try to implement that
			# but right now appears most of the checks aren't doable with our data (aka check listeners and
			# other View properites not in RICO
			# for now use our test of talkback accessible
			if n in clickable_talkback_nodes:
				num_overlap = self.__full_overlap_clickable_talkback(n)
				n.checker.view_set_checks["Num_Nodes_Overlap_With"] = num_overlap
				if num_overlap > 0:
					self.result += 1
			else:
				n.checker.view_set_checks["Num_Nodes_Overlap_With"] = "na"


		#####
	### Check exact overlap
	### checks if two clickable, talkback acessible nodes nodes occupy the exact same place on the screen
	#####

	def __full_overlap_clickable_talkback(self,node):
		num_full_overlap = 0
		for n in self.view.get_clickable_talkback_nodes():
			if n==node:
				continue
			else:
				if self.__full_overlap_compare(node, n):
					num_full_overlap += 1
		return num_full_overlap

	# check if two elements n1 and n2 occupy the exact same space
	def __full_overlap_compare(self, node1,node2):
		b1 = node1.get_bounds()
		b2 = node2.get_bounds()
		if(b1['top'] == b2['top'] and b1['bottom'] == b2['bottom'] and \
			b1['left'] == b2['left'] and b1['right'] == b2['right']):
			return True
		return False