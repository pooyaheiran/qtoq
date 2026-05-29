import re
import json



def parse_input(string):
	pattern = r'^([\w\d]+)\s*-\s*([\w\d,]+|λ|ε|lambda)\s*->\s*([\w\d]+)\s*$'

	main_dict = {}
	string_list = string.split("\n")

	for string in string_list:
		if "start:" in string:
			main_dict["start"] = string[6:]
		if "finals:" in string:
			main_dict["finals"] = string[7:].split(",")

	transitions = []

	for line in string_list:
		line = line.strip()
		# if not line:
		# 	continue
			
		match = re.match(pattern, line)
		
		if match:
			state_from = match.group(1)
			inputs = match.group(2)
			state_to = match.group(3)
			
			if inputs in ['λ', 'ε', 'lambda']:
				input_list = [None]
			else:
				input_list = inputs.split(',')
			
			transition_obj = {
				"from": state_from,
				"on": input_list,
				"to": state_to
			}
			
			transitions.append(transition_obj)
	main_dict["transitions"] = transitions

	with open("db.json", "w") as f:
		json.dump(main_dict, f)

