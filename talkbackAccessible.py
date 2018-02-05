# TODO
def has_webAction(node):
	return False

# return if node is visible
# currently defined as the "visibility" property is "visible"
def is_visible(node):
	k = node.raw_properties.keys()

	if ('visibility' in k):
		# TODO: figure out all the meaning of the different
		# possible values of 'visibility' 
		node.characteristics['talkback_accessible'].append('visibility: ' + str(node.raw_properties['visibility']))
		if (node.raw_properties['visibility'] == "visible"):
			return True
	# if the node doesn't have a visibility property
	# or if that property is not set to "visible"
	# it is not a visible node
	else:
		node.characteristics['talkback_accessible'].append('no visibility tag')
	return False

def is_clickable(node):
	k = node.raw_properties.keys()
	has_clickable ='clickable' in k
	has_long_clickable = 'content-desc' in k
	# is clickable
	if('clickable' in k):
		if(node.raw_properties["clickable"]):
			node.characteristics['talkback_accessible'].append("node is clickable")
			return True
	# long clickable
	if('long-clickable' in k):
		if(node.raw_properties["long-clickable"]):
			node.characteristics['talkback_accessible'].append("node is long clickable")
			return True
	return False

def is_focusable(node):
	result = node.raw_properties["focusable"]
	if result:
		node.characteristics['talkback_accessible'].append("focusable")
	else:
		node.characteristics['talkback_accessible'].append("not focusable")
	return result

#TODO
# don't know what fields to look for
def is_checkable(node):
	return False

#TODO
def bounds_same_as_window(node):
	return False

# 
def has_visible_children(node):
	for child in node.children:
		if is_visible(child):
			return True
	return False


def has_focusable_ancestors(node):
	ancestor = node.parent
	while ancestor:
		#TODO 
		# don't use is_focusable
		# use should_focus without checking children
		# STOPPED HERE!
		if should_focus(ancestor, check_children=False):
			return True
		ancestor = ancestor.parent
	return False

def has_non_actionable_speaking_children(node):
	for child in node.children:
		# ignore focusable children
		if is_focusable(child):
			continue
		# ignore invisible children
		if not is_visible(child):
			continue
		# check if this is a speaking child
		if is_speakable(child):
			return True
		# recursively check
		if len(child.children) > 0:
			return has_nonactionable_speaking_children(child)
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
	if has_text(node):
		return True
	elif is_checkable(node):
		return True
	# TODO
	# if web thing
	elif has_non_actionable_speaking_children(node):
		return True
	return False



# defined as having none Null Text or Content Description
# TODO:
#      * For the purposes of this check, any node with a CollectionInfo is considered to not have
#     * text since its text and content description are used only for collection transitions.
def has_text(node):
	pass_label = False
	k = node.raw_properties.keys()
	# set to if the field exists
	has_text = 'text' in k
	node.characteristics['talkback_accessible'].append("has text")
	has_content_desc = 'content-desc' in k
	# check if existing fields have content
	if has_content_desc:
		if(node.raw_properties["content-desc"] == [None]):
			has_content_desc = False
			node.characteristics['talkback_accessible'].append("has none cont desc")
		else:
			node.characteristics['talkback_accessible'].append("has non-none cont desc")
	# must have non-empty/null text or cont_desc to pass
	if not has_text and not has_content_desc:
		pass_label = False
		#print ("inaccessible")
	else:
		pass_label = True
		#print("accessible")
	# return if has label 
	return pass_label

def is_actionable(node):
	if is_clickable(node):
		return True
	elif is_focusable(node):
		return True
	# TODO
	# elif web thing
	return False

#TODO
def is_top_level_scroll(node):
	return False

def is_access_focus(node):
	if not is_visible(node):
		return False
	elif is_actionable(node):
		return True
	elif is_top_level_scroll(node) and is_speaking(node):
		return True

# Should Focus

def should_focus(node, check_children=True):
	if (has_webAction(node)):
		return True
	elif (not is_visible(node)):
		return False
	elif (bounds_same_as_window(node)):
		return False

	access_focus = is_access_focus(node)

	if not check_children:
		return access_focus

	if(access_focus):
		if not has_visible_children(node):
			return True
		elif is_speaking(node):
			return True
		else:
			return False

	if (not has_focusable_ancestors(node)) and has_text(node):
		return True
	else:
		return False