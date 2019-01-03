__author__ = 'ansross'
import csv
## takes in a CSV with at least a column names class
## using the mapping from Proguard (used by Android studio) downloaded Jan 2 2019 https://stuff.mit.edu/afs/sipb/project/android/sdk/android-sdk-linux/tools/proguard/docs/index.html#/afs/sipb/project/android/sdk/android-sdk-linux/tools/proguard/docs/downloads.html
## http://sourceforge.net/project/showfiles.php?group_id=54750
## adds column for de minified name or copy of original name if not in map
# and column indicating if the name was replaced

def parse_map(map_filename):
	f = open(map_filename,'r')
	mini_map = {}
	for line in f:
		# the top lines, i believe of classes, end in ':', if this is the case, strip it
		parsed_line = line
		if parsed_line[-2]==":":
			parsed_line = line[:-2]
		parsed_line = parsed_line.split(" ")
		# things that map variables, etc, instead of classes have more strings
		if len(parsed_line) == 3:
			# 0: unmutated class name
			# 1: ->
			# 2: mutated class name
			#for hiearachy reasons, I think, some are listed as not mutated
			if parsed_line[0] != parsed_line[2]:
				mini_map[parsed_line[0]] = parsed_line[2]
	return mini_map

def unminify(mini_map, node_filename, outfile_name):
	with open(node_filename) as node_csv_file:
		with open(outfile_name, 'w', newline='') as csv_outfile:
			header = ['app_id','trace_id','view_id',
					  'node_id', 'class', 'is_clickable',
					  'android_widget', 'ad', 'Speakable_Text_Present',
					  'Element_Wide_Enough', 'Element_Tall_Enough', 'Editable_Textview_With_Cont_Desc',
					  'Has_Redundant_Description', 'Num_Nodes_Overlap_With', 'Num_Nodes_Share_Label', '',
					 'unmutated_class','class_was_mutated' ]
			reader = csv.reader(node_csv_file)
			node_dict = []
			old_header = []
			is_header = True
			for row in reader:
				if is_header:
					old_header = row
					is_header =False
				else:
					dict = {}
					for i in range(len(row)):

						dict[old_header[i]] = row[i]
					node_dict.append(dict)

			#node_dict = csv.DictReader(node_csv_file, fieldnames = header)

			for row in node_dict:
				classname = row['class']
				# class matches mutation
				if classname in mini_map:
					row['unmutated_class'] = mini_map[classname]
					row['class_was_mutated'] = "TRUE"
				# not mutated, so copy original name
				else:
					row['unmutated_class'] = classname
					row['class_was_mutated'] = "FALSE"

			#write new csv
			writer = csv.DictWriter(csv_outfile, fieldnames=header, delimiter=",")
			writer.writeheader()
			header = True
			for row in node_dict:
				if header:
					header = False
					continue
				writer.writerow(row)
	exit()

if __name__ == "__main__":
	# read in mapping file
	minification_map_filename = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\de_minify_rico_data\proguard_minification_mapping_1.2.2019.txt"
	mini_map = parse_map(minification_map_filename)

	node_filename = "C:\\Users\\ansross\Documents\Research\Accessibility\parse_Rico\code\\unminify_test_1.2.19.4.14.csv"
	outfile_name = "test_unminified_1.2.2019.4.00.csv"
	unminify(mini_map, node_filename, outfile_name)
