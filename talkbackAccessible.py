window_bounds = {"left": 0, "upper": 0, "right":1440, "lower": 2560}
window_width = window_bounds['right'] - window_bounds['left']
print("width: "+str(window_width))
window_height = window_bounds['lower'] - window_bounds['upper']
print("height: "+str(window_height))

#for get merge. delete

#TODO
def has_webAction(node):
	return False

#Role.java l213 2.14.2018 Talkback
def get_role(node):
	#print ("Getting role")

	if node == None:
		return "ROLE_NONE"
	k = node.raw_properties.keys()
	if not "class" in k:
		return "ROLE_NONE"

	node_class = node.raw_properties['class']
	#node_classes = node.raw_properties['ancestors']

    # When comparing node.getClassName() to class name of standard widgets, we should take care of
    # the order of the "if" statements: check subclasses before checking superclasses.
    # e.g. RadioButton is a subclass of Button, we should check Role RadioButton first and fall
    # down to check Role Button.

	# Inheritance: View->ImageView
	if (node_class == "android.widget.ImageView"):
		if (is_clickable(node)):
			return "ROLE_IMAGE_BUTTON"
		else:
			return "ROLE_IMAGE"

	##############################
	## Subclasses of TextView.

	## Inheritance: View->TextView->Button->CompoundButton->Switch
	if node_class == "android.widget.Switch":
		return "ROLE_SWITCH"

	if node_class == "android.widget.ToggleButton":
		return "ROLE_TOGGLE_BUTTON"

	if node_class == "android.widget.RadioButton":
		return "ROLE_RADIO_BUTTON"

	if node_class == "android.widget.CompoundButton":
		return "ROLE_CHECKBOX"

	if node_class == "android.widget.Button":
		return "ROLE_BUTTON"

	if node_class == "android.widget.CheckedTextView":
		return "ROLE_CHECKED_TEXT_VIEW"

	if node_class == "android.widget.EditText":
		return "ROLE_EDIT_TEXT"

	##################################
	## Subclasses of Progressbar

	if node_class == "android.widget.SeekBar":
		return "ROLE_SEEK_CONTROL"
	if node_class == "android.widget.ProgressBar":
		return "ROLE_PROGRESS_BAR"
	if node_class == "android.inputmethodservice.Keyboard.Key":
		return "ROLE_KEYBOARD_KEY"

	##############################
	## Subclasses of ViewGroup

	if node_class == "android.webkit.WebView":
		return "ROLE_WEB_VIEW"
	if node_class == "android.widget.TabWidget":
		return "ROLE_TAB_BAR"

	if node_class == "android.widget.HorizontalScrollView":
		return "ROLE_HORIZONTAL_SCROLL_VIEW"

	if node_class == "android.widget.ScrollView":
		return "ROLE_SCROLL_VIEW"
	# Inheritance: View->ViewGroup->ViewPager
	if node_class == "android.support.v4.view.ViewPager":
		return "ROLE_PAGER"

	if node_class == "android.widget.Spinner":
		return "ROLE_DROP_DOWN_LIST"
	if node_class == "android.widget.GridView":
		return "ROLE_GRID"
	if node_class == "android.widget.AbsListView":
		return "ROLE_LIST"

	# TODO!!! ln 339
	# CollectionInfoCompat collection = node.getCollectionInfo();
	# if (collection != null) {
	# # RecyclerView will be classified as a list or grid.
	# 	if (collection.getRowCount() > 1 && collection.getColumnCount() > 1) {
	# 		return ROLE_GRID;
	# 	} else {
	# 		return ROLE_LIST;
	# 	}
	# }

	if node_class == "android.view.ViewGroup":
		return "ROLE_VIEW_GROUP"

	return "ROLE_NONE"


# return if node is visible
# currently defined as the "visibile to user" property is "True"
def is_visible(node):
	#print("is visible test")
	k = node.raw_properties.keys()
	if ('visible-to-user' in k):
		# TODO: figure out all the meaning of the different
		# possible values of 'visibility' 
		node.log['talkback_accessible'].append('visible-to-user: ' + str(node.raw_properties['visible-to-user']))
		if (node.raw_properties['visible-to-user']):
			return True
	# if the node doesn't have a visibility property
	# or if that property is not set to "visible"
	# it is not a visible node
	else:
		node.log['talkback_accessible'].append('no visible-to-user tag')
	return False

def is_clickable(node):
	#print("is clickable test")
	k = node.raw_properties.keys()
	has_clickable ='clickable' in k
	has_long_clickable = 'content-desc' in k
	# is clickable
	if('clickable' in k):
		if(node.raw_properties["clickable"]):
			node.log['talkback_accessible'].append("node is clickable")
			return True
	# long clickable
	if('long-clickable' in k):
		if(node.raw_properties["long-clickable"]):
			node.log['talkback_accessible'].append("node is long clickable")
			return True
	return False

def is_focusable(node):
	#print("is focusable test")
	result = node.raw_properties["focusable"]
	if result:
		node.log['talkback_accessible'].append("focusable")
	else:
		node.log['talkback_accessible'].append("not focusable")
	return result

#TODO
# don't know what fields to look for
def is_checkable(node):
	return False

# don't know if right definition since in talkback specifies as "scroll forward" and "scroll backward"
# but in data only have "horizontal" and "vertical" scroll
def is_scrollable(node):
	k = node.raw_properties.keys()
	if "scrollable-vertical" in k:
		if node.raw_properties["scrollable-vertical"]:
			node.log['talkback_accessible'].append("scrollable-vertical")
			return True

	if "scrollable-horizontal" in k:
		if node.raw_properties["scrollable-horizontal"]:
			node.log['talkback_accessible'].append("scrollable-horizontal")
			return True
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
		node.log['talkback_accessible'].append("zero dimensions")
		return False
	return True

def bounds_within_window(node):
	bounds = node.get_bounds()
	within_window = True
	# if left is greater, right should be, but do both checks to be safe
	if bounds['right'] > window_width or bounds['left'] > window_width:
		within_window = False
		node.log['talkback_accessible'].append(str(bounds['right'])+" or "+str(bounds['left'])+ " positive outside width")
	elif bounds['lower'] > window_height or bounds['upper'] > window_height:
		within_window = False
		node.log['talkback_accessible'].append("positive outside height")
	# don't actually know if will ever be negative, but worth checking
	elif bounds['right'] < 0 or bounds['left'] < 0:
		within_window = False
		node.log['talkback_accessible'].append("neg outside width")
	elif bounds['lower'] < 0 or bounds['upper'] < 0:
		within_window = False
		node.log['talkback_accessible'].append("neg outside height")
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

def is_top_level_scrollable(node):
	if node == None:
		return False

	if node.parent == None:
		# not a child of anything
		return False

	if is_scrollable(node):
		return True

	# top-level items in a scrolling pager are actually two levels down since the first
	# level items in pagers are the pages themselves
	grandparent = node.parent.parent
	if get_role(grandparent) == "ROLE_PAGER":
		return True

	parent_role = get_role(node.parent)
	# Note that ROLE_DROP_DOWN_LIST(Spinner) is not accepted.
	# TODO: haven't RecyclerView is classified as a list or grid based on its CollectionInfo.
	result = (parent_role == "ROLE_LIST" or parent_role == "ROLE_GRID" or parent_role =="ROLE_SCROLL_VIEW" \
		or parent_role == "ROLE_HORIZONTAL_SCROLL_VIEW")
	node.log['talkback_accessible'].append("role: "+str(parent_role))
	return result




def non_actionable_speaking_children_text(node):
	#print("non actionable children test")
	for child in node.children:
		# ignore focusable children
		if is_focusable(child):
			continue
		# ignore invisible children
		if not is_visible(child):
			continue
		# check if this is a speaking child
		child_text = get_speaking_text(child)
		if child_text != None:
			node.log['talkback_accessible'].append("has nonactionable speaking children")
			#node.characteristics['has_non_actionable_speaking_children'] = True
			return child_text
		# recursively check
		if len(child.children) > 0:
			return non_actionable_speaking_children_text(child)
		# if leaf node and hasn't passed yet, false
	return None

def is_speaking(node):
	return (not get_speaking_text(node) == None)

'''
A node is speakable if:
	1. has text or content description
	2. is checkable (checkbox)
	3. has web content
	4. has non-actionable speaking children

	# will return text either from self or children, or None if no text
	# was is _speaking
'''
def get_speaking_text(node):
	#print("is speaking test")
	text = get_self_text(node)
	if text != None:
		return text
	#TODO
	#elif is_checkable(node):
	#	return True
	# TODO
	# if web thing
	text = non_actionable_speaking_children_text(node)
	if text != None:
		return text
	return text


def is_empty(str):
	if (str == None or len(str) == 0):
		return True
	else:
		return False

# def get_text(node):
# 	if not has_text(node):
# 		return None
# 	else:
# 		if has_non_empty_cont_desc(node):
# 			return node.raw_properties['content-desc']
# 		else:
# 			return node.raw_properties['text']

# defined as having none Null or zero length Text or Content Description
# TODO:
#      * For the purposes of this check, any node with a CollectionInfo is considered to not have
#     * text since its text and content description are used only for collection transitions.
# returns a node's text, or cont-descr, if available, else, returns None
def get_self_text(node):
	#print ("hast text")
	#pass_label = False
	text = None
	text = get_textfield(node)
	if text == None:
		text = get_cont_desc(node)


	
	# content_desc = has_non_empty_cont_desc(node)
	# if has_content_desc:
	# 	text = 
	# if (not has_text) and (not has_content_desc):
	# 	pass_label = False
	# else:
	# 	pass_label = True
	# return if has label
	node.log['talkback_accessible'].append("has own label: "+str(not text == None))
	return text

def get_textfield(node):
	text = None
	k = node.raw_properties.keys()
	# set to if the field exists
	has_text = 'text' in k
	if has_text:
		node.log['talkback_accessible'].append("has text: "+node.raw_properties['text'])
		has_text = not is_empty(node.raw_properties['text'])
		if has_text:
			text = node.raw_properties['text']
	else:
		node.log['talkback_accessible'].append("no text")
	return text

def get_cont_desc(node):
	cont_desc = None
	k = node.raw_properties.keys()
	has_content_desc = 'content-desc' in k
	if has_content_desc:
		node.log['talkback_accessible'].append("has cont desc: "+str(node.raw_properties['content-desc'][0]))
		has_content_desc = not is_empty(node.raw_properties["content-desc"][0])
		if has_content_desc:
			cont_desc = node.raw_properties["content-desc"][0]
	return cont_desc

def is_actionable(node):
	#print("is actionable test")
	if is_clickable(node):
		node.log['talkback_accessible'].append("is clickable")
		return True
	elif is_focusable(node):
		node.log['talkback_accessible'].append("is focusable")
		return True
	# TODO
	# elif web thing
	node.log['talkback_accessible'].append("not actionable")
	return False


def is_access_focus(node):
	#print("is access focus test")
	if not is_visible(node):
		node.log['talkback_accessible'].append("not visible")
		return False
	elif is_actionable(node):
		return True
	elif is_top_level_scrollable(node) and is_speaking(node):
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
		node.log['talkback_accessible'].append("is access focus")
		if not has_visible_children(node):
			node.log['talkback_accessible'].append("no visible children")
			return True
		elif is_speaking(node):
			node.log['talkback_accessible'].append("is_speaking")
			return True
		else:
			return False

	if (not has_focusable_ancestors(node)) and (get_self_text(node) != None):
		node.log['talkback_accessible'].append("no focusable ancestor and text")
		return True
	else:
		return False