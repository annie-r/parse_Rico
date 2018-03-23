from trace_check_base import Trace_Check_Base

class Num_Nodes_Accessible_In_Trace_Check(Trace_Check_Base):

	def __init__(self,id_arg,trace_arg):
		Trace_Check_Base.__init__(self,id_arg,trace_arg)


	# result is the num of clicks in trace that don't land on an
	# accessible node
	def perform(self):
		self.result = 0
		#print("trace: "+str(self.trace.id)+" "+str( self.trace.app_id))
		for g in self.trace.gestures:
			# only interested in clicks
			if g.type == "TAP":
				potential_nodes = []
				#print("app_id: "+self.trace.app_id +" trace: "+self.trace.id)

				v = self.trace.views[g.view_id]
				if v.has_valid_file:

					for n in v.nodes:
						if n.contains_coords(g.coords):
							potential_nodes.append(n)
					has_accessible_node = False
					# a coordinate may land on many uninterested, layered nodes (layout) that shouldn't be accessible
					# but if there are NO nodes that are at this coordinate and accessible, consider a problem
					for n in potential_nodes:
						if n.is_talkback_accessible():
							has_accessible_node = True
							break
					if not has_accessible_node:
						print("app_id: "+self.trace.app_id +" trace: "+self.trace.id)
						print(g.view_id)
						self.result += 1
				else:
					self.trace.num_null_views += 1



