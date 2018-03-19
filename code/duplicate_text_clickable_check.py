from view_check_base import View_Check_Base


#####
## Check identical speakable text
## item descriptions
# /** Accessitility-Test-framework-for-android DuplicateSpeakableTextViewHierarchyCheck
# If two Views in a hierarchy have the same speakable text, that could be confusing for users. Two
# Views with the same text, and at least one of them is clickable we warn in that situation. If we
# find two non-clickable Views with the same speakable text, we report that fact as info. If no
# Views in the hierarchy have any speakable text, we report that the test was not run.
#####

# if it's clickable, it's a warning
# if it's not, then it's just info
# so for now count as separate checks
# line 69, accessibility test framework, proto, duplicatespeakabletextviewhierarchycheck
# shares with clickable
class Duplicate_Text_Clickable_Check(View_Check_Base):

	def __init__(self, id_arg, view_arg):
		View_Check_Base.__init__(self,id_arg, view_arg)

		# result is number of clickable nodes that fully overlap


	def perform(self):
		self.result = 0
		# find all nodes that have text
		speakable_text_to_clickable_node_map = {}
		# collect all text and nodes associated with that
		for n in self.view.nodes:
			# todo: check is appropriate
			# only checking talkback accessible
			if n.is_talkback_accessible():
				text = n.get_speakable_text()
				if text != None and n.is_clickable():
					if text not in speakable_text_to_clickable_node_map.keys():
						speakable_text_to_clickable_node_map[text] = []
					speakable_text_to_clickable_node_map[text].append(n)
				# save non clickable with text for other check
				# if node has no text, test not applicable
				elif text == None:
					n.checker.view_set_checks['"Num_Nodes_Share_Label'] = "na"
			# todo: check is appropriate
			# only checking talkback accessible
			else:
				n.checker.view_set_checks['"Num_Nodes_Share_Label'] = "na"

		# check for more than one node with same text
		for speakable_text,clickable_nodes in speakable_text_to_clickable_node_map.items():
			# sanity check
			if (len(clickable_nodes) < 1):
				raise AssertionError("LABEL: "+str(speakable_text)+" SHOULD NOT BE IN MAP IF NO NODES")
			# catches all relevant cases. if only one node, then shares with 0 others, etc
			for n in clickable_nodes:
				n.checker.view_set_checks['Num_Nodes_Share_Label'] = len(clickable_nodes) - 1
			# duplicates cases
			# count number of elements involved in a case of duplication, not a count of how many
			# share any individual label
			if (len(clickable_nodes) > 1):
				self.result += len(clickable_nodes)

