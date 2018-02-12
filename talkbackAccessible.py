window_bounds = {"left": 0, "upper": 0, "right":1440, "lower": 2560}
window_width = window_bounds['right'] - window_bounds['left']
print("width: "+str(window_width))
window_height = window_bounds['lower'] - window_bounds['upper']
print("height: "+str(window_height))

def has_webAction(node):
	return False

# return if node is visible
# currently defined as the "visibile to user" property is "True"
def is_visible(node):
	#print("is visible test")
	k = node.raw_properties.keys()
	if ('visible-to-user' in k):
		# TODO: figure out all the meaning of the different
		# possible values of 'visibility' 
		node.log.append('visible-to-user: ' + str(node.raw_properties['visible-to-user']))
		if (node.raw_properties['visible-to-user']):
			return True
	# if the node doesn't have a visibility property
	# or if that property is not set to "visible"
	# it is not a visible node
	else:
		node.log.append('no visible-to-user tag')

	'''
	if ('visibility' in k):
		# TODO: figure out all the meaning of the different
		# possible values of 'visibility' 
		node.log.append('visibility: ' + str(node.raw_properties['visibility']))
		if (node.raw_properties['visibility'] == "visible"):
			return True
	# if the node doesn't have a visibility property
	# or if that property is not set to "visible"
	# it is not a visible node
	else:
		node.log.append('no visibility tag')
	'''
	return False

def is_clickable(node):
	#print("is clickable test")
	k = node.raw_properties.keys()
	has_clickable ='clickable' in k
	has_long_clickable = 'content-desc' in k
	# is clickable
	if('clickable' in k):
		if(node.raw_properties["clickable"]):
			node.log.append("node is clickable")
			return True
	# long clickable
	if('long-clickable' in k):
		if(node.raw_properties["long-clickable"]):
			node.log.append("node is long clickable")
			return True
	return False

def is_focusable(node):
	#print("is focusable test")
	result = node.raw_properties["focusable"]
	if result:
		node.log.append("focusable")
	else:
		node.log.append("not focusable")
	return result

#TODO
# don't know what fields to look for
def is_checkable(node):
	return False

#TODO
def bounds_same_as_window(node):
	node_bounds = node.get_bounds()
	if window_bounds['left'] == node_bounds['left'] and window_bounds['right'] == node_bounds['right'] and \
		window_bounds['upper'] == node_bounds['upper']and window_bounds['lower'] == node_bounds['lower']:
		return True 
	return False

def has_non_zero_dimensions(node):
	bounds = node.get_bounds()
	# not sure of case where it's only zero in one dimension
	if bounds['left'] == bounds['right'] and bounds['upper'] == bounds['lower']:
		return False
	return True

def bounds_within_window(node):
	bounds = node.get_bounds()
	within_window = True
	# if left is greater, right should be, but do both checks to be safe
	if bounds['right'] > window_width or bounds['left'] > window_width:
		within_window = False
		node.log.append(str(bounds['right'])+" or "+str(bounds['left'])+ " positive outside width")
	elif bounds['lower'] > window_height or bounds['upper'] > window_height:
		within_window = False
		node.log.append("positive outside height")
	# don't actually know if will ever be negative, but worth checking
	elif bounds['right'] < 0 or bounds['left'] < 0:
		within_window = False
		node.log.append("neg outside width")
	elif bounds['lower'] < 0 or bounds['upper'] < 0:
		within_window = False
		node.log.append("neg outside height")
	return within_window

# 
def has_visible_children(node):
	#print("has visible children test")
	for child in node.children:
		if is_visible(child):
			return True
	return False


def has_focusable_ancestors(node):
	#print("has focusable ancestor test")
	ancestor = node.parent
	while ancestor:
		if talkback_focus(ancestor, check_children=False):
			return True
		ancestor = ancestor.parent
	return False

def has_non_actionable_speaking_children(node):
	#print("non actionable children test")
	for child in node.children:
		# ignore focusable children
		if is_focusable(child):
			continue
		# ignore invisible children
		if not is_visible(child):
			continue
		# check if this is a speaking child
		if is_speaking(child):
			node.log.append("has nonactionable speaking children")
			return True
		# recursively check
		if len(child.children) > 0:
			return has_non_actionable_speaking_children(child)
		# if leaf node and hasn't passed yet, false
	return False

'''
A node is speakable if:
	1. has text or content description
	2. is checkable (checkbox)
	3. has web content
	4. has non-actionable speaking children
'''
def is_speaking(node):
	#print("is speaking test")
	if has_text(node):
		return True
	elif is_checkable(node):
		return True
	# TODO
	# if web thing
	elif has_non_actionable_speaking_children(node):
		return True
	return False



def is_empty(str):
	if (str == None or len(str) == 0):
		return True
	else:
		return False

# defined as having none Null or zero length Text or Content Description
# TODO:
#      * For the purposes of this check, any node with a CollectionInfo is considered to not have
#     * text since its text and content description are used only for collection transitions.
def has_text(node):
	#print ("hast text")
	pass_label = False
	k = node.raw_properties.keys()
	# set to if the field exists
	has_text = 'text' in k
	if has_text:
		node.log.append("has text: "+node.raw_properties['text'])
	if (has_text):
		has_text = not is_empty(node.raw_properties['text'])
	#node.log.append("has text: ")
	has_content_desc = 'content-desc' in k
	if has_content_desc:
		has_content_desc = not is_empty(node.raw_properties["content-desc"][0])

	# check if existing fields have content
	'''
	if has_content_desc:
		if(node.raw_properties["content-desc"] == [None]):
			has_content_desc = False
			node.log.append("has none cont desc")
		else:
			node.log.append("has non-none cont desc"+str(node.raw_properties['content-desc']))
	# must have non-empty/null text or cont_desc to pass
	'''
	if not has_text and not has_content_desc:
		pass_label = False
		#print ("inaccessible")
	else:
		pass_label = True
		#print("accessible")
	# return if has label 
	return pass_label

def is_actionable(node):
	#print("is actionable test")
	if is_clickable(node):
		node.log.append("is clickable")
		return True
	elif is_focusable(node):
		node.log.append("is focusable")
		return True
	# TODO
	# elif web thing
	node.log.append("not actionable")
	return False

#TODO
def is_top_level_scroll(node):
	return False

def is_access_focus(node):
	#print("is access focus test")
	if not is_visible(node):
		node.log.append("not visible")
		return False
	elif is_actionable(node):
		return True
	elif is_top_level_scroll(node) and is_speaking(node):
		return True

# Should Focus

def talkback_focus(node, check_children=True):
	# if is 0 px
	if not has_non_zero_dimensions(node):
		return False

	# if outside of bounds, not of interest
	if not bounds_within_window(node):
		return False

	if (has_webAction(node)):
		return True
	elif (not is_visible(node)):
		return False
	# only allow node with same bounds as window if it is clickable or a leaf
	elif (bounds_same_as_window(node) and not is_clickable(node) and len(node.children)>0):
		return False

	access_focus = is_access_focus(node)

	if not check_children:
		return access_focus


	if(access_focus):
		node.log.append("is access focus")
		if not has_visible_children(node):
			node.log.append("no visible children")
			return True
		elif is_speaking(node):
			node.log.append("is_speaking")
			return True
		else:
			return False

	if (not has_focusable_ancestors(node)) and has_text(node):
		node.log.append("no focusable ancestor and text")
		return True
	else:
		return False