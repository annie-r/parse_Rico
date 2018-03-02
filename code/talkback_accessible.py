window_bounds = {"left": 0, "top": 0, "right":1440, "bottom": 2560}
window_width = window_bounds['right'] - window_bounds['left']
#print("width: "+str(window_width))
window_height = window_bounds['bottom'] - window_bounds['top']
#print("height: "+str(window_height))

######################
##### TODO
######################


######################
##### PRIVATE FUNCTIONS
######################



# Not currently used
def __bounds_within_window(node):
	bounds = node.get_bounds()
	within_window = True
	# if left is greater, right should be, but do both checks to be safe
	if bounds['right'] > window_width or bounds['left'] > window_width:
		within_window = False
		node.log['talkback_accessible'].append(str(bounds['right'])+" or "+str(bounds['left'])+ " positive outside width")
	elif bounds['bottom'] > window_height or bounds['top'] > window_height:
		within_window = False
		node.log['talkback_accessible'].append("positive outside height")
	# don't actually know if will ever be negative, but worth checking
	elif bounds['right'] < 0 or bounds['left'] < 0:
		within_window = False
		node.log['talkback_accessible'].append("neg outside width")
	elif bounds['bottom'] < 0 or bounds['top'] < 0:
		within_window = False
		node.log['talkback_accessible'].append("neg outside height")
	return within_window

def __bounds_same_as_window(node):
	node_bounds = node.get_bounds()
	if window_bounds['left'] == node_bounds['left'] and window_bounds['right'] == node_bounds['right'] and \
		window_bounds['top'] == node_bounds['top']and window_bounds['bottom'] == node_bounds['bottom']:
		return True 
	return False


def __is_access_focus(node):
	#print("is access focus test")
	if not node.is_visible():
		node.log['talkback_accessible'].append("not visible")
		return False
	elif node.is_actionable():
		return True
	elif node.is_top_level_scrollable() and is_speaking(node):
		return True



######################
##### PUBLIC FUNCTIONS
######################


# Should Focus
def talkback_focus(node, check_children=True):
	# if is 0 px
	if not node.has_non_zero_dimensions():
		return False

	# if outside of bounds, not of interest
	if not __bounds_within_window(node):
		return False

	if (node.has_webAction()):
		return True
	elif (not node.is_visible()):
		return False
	# only allow node with same bounds as window if it is clickable or a leaf
	elif (__bounds_same_as_window(node) and not node.is_clickable() and len(node.children)>0):
		return False

	access_focus = __is_access_focus(node)

	if not check_children:
		return access_focus


	if(access_focus):
		node.log['talkback_accessible'].append("is access focus")
		if not node.has_visible_children():
			node.log['talkback_accessible'].append("no visible children")
			return True
		elif node.is_speaking():
			node.log['talkback_accessible'].append("is_speaking")
			return True
		else:
			return False

	if (not node.has_focusable_ancestors()) and (node.get_self_text() != None):
		node.log['talkback_accessible'].append("no focusable ancestor and text")
		return True
	else:
		return False