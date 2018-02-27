class Trace:
	def __init__(self, filepath, app_arg):
		self.filepath = filepath
		self.app = app_arg
		# map view ID to View object
		self.views = {}
		# ordered list of gestures performed
		# TODO swipe
		self.gestures = []

	def __parse_directory(self):
		# go through trace directory and parse into Views

	def __parse_gestures(self):
		#STOPPED HERE!

	def json_loader(self,filepath):
		file_descriptor = open(filepath, "r")
		data = json.load(file_descriptor)
		#data = yaml.load(file_descriptor)
		return data
	class gesture:
		def __init__(self, id_arg):
			# view ID of gesture
			self.view_id = id_arg
			# only has one pair or coords is a tap
			# TODO swipe
			# swipe or tap
			if (len(coords_arg) == 1):
				self.type = "TAP"
				self.coords = {"x":coords_arg[0][0], "y":coords_arg[0][1]}