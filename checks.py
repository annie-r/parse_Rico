## checks for accessibility barriers on RICO dataset 



def px_to_dp(px):
	# TODO: figure out dpi/phyical device of RICO
	# conversion of dp units to screen pixels is simple: px = dp * (dpi / 160).
	# assuming mdpi device, so dpi = 160
	# https://developer.android.com/guide/practices/screens_support.html
	# assuming mdpi device, so dpi = 160
	dpi = 160
	return (px * 160)/dpi

def wide_enough(node):
	k = node.raw_properties.keys()
	# bounds is 4 node array
	# 0 = left, 1 = top, 2 = right, 3 = bottom
	# google dev guidelines, needs to be 48 dp
	bounds = node.raw_properties["bounds"]
	px_width = bounds[2] - bounds[0]
	# must convert pixel to dp

	dp_width = px_to_dp(px_width)
	dp_width_threshold = 48
	wide_enough = None
	if (dp_width < dp_width_threshold ):
		wide_enough = False
	else:
		wide_enough = True
	return wide_enough

def tall_enough(node):
	k = node.raw_properties.keys()
	# bounds is 4 node array
	# 0 = left, 1 = top, 2 = right, 3 = bottom
	# google dev guidelines, needs to be 48 dp
	bounds = node.raw_properties["bounds"]
	px_height = bounds[3] - bounds[1]
	# must convert pixel to dp
	dp_height = px_to_dp(px_height)
	dp_height_threshold = 48
	tall_enough = None
	if (dp_height < dp_height_threshold ):
		tall_enough = False
	else:
		tall_enough = True
	return tall_enough

#def has_label(node):
	# if it's not speakable, we're not interested in a label ?
	# TODO: check that this is right
#	if(isSpeakable(node)):
#		if node.characterisitcs['']
