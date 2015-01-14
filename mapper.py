#!/usr/bin/env python

"""
Written by Steven Levine
"""

"""
Because Victor has too much fun with moira lists.

Hi, Victor! I bet you're reading my source code.
(Too bad it's not javascript LOL ;-)
"""
import subprocess
import argparse

class MoiraList():
	"""A class representing a moira list. Auto-constructs itself (recursively!)
	based on constructor root_name arg"""
	def __init__(self, root_name, lists_dict, terminals):
		self.name = root_name
		self.members = []
		# Continues only if we haven't seen this list before
		if not self.name in lists_dict:
			lists_dict[self.name] = self
			for m in self.get_members(self.name):
				name, is_list = self.interpret_member(m)
				if is_list:
					sublist = MoiraList(name, lists_dict, terminals)
					self.members.append(sublist)
				else:	
					self.members.append(name)
					terminals.add(name)
	
	def get_members(self, list_name):
		"Returns all strings in a list"
		#print "Checking list {}".format(list_name)
		try:
			return [x for x in subprocess.check_output(['blanche', list_name, '-noauth']).split('\n') if x != ""]
		except:
			return ['cant-blanche-this']
	def interpret_member(self, member):
		#"Returns a tuple (name, is_list)"
		if len(member) >= 5 and member[:5] == "LIST:":
			# It's a list!
			return (member[5:], True)
		else:
			return (member, False)


def to_dot(lists_dict, terminals, filename):
	# Write a dot file
	#print "Writing dot file to {}".format(filename)
	with open(filename, "w") as f:
		f.write("digraph G {\n")
		# Write terminals as boxes
		for m in terminals:
			f.write("    \"{}\" [shape=box]\n".format(m))
		# Write sublists as default circles
		f.write("\n")
		for list_name in lists_dict:
			f.write("    \"{}\"[fillcolor=\"#dfdfdf\", style=\"filled\"]\n".format(list_name))
		# Now, add in all the edges
		f.write("\n")
		for l in lists_dict.values():
			for m in l.members:
				f.write("    \"{}\" -> \"{}\"\n".format(l.name, m.name if isinstance(m, MoiraList) else m))	
		f.write("}")


def dot_to_pdf(dot_file, pdf_file):
	#print "Generating PDF"
	subprocess.call(["dot", "-Tpdf", dot_file, "-o", pdf_file])


# Starts here
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="A tool to help combat the ever-changing labyrinth that is Victor's moira lists")
	parser.add_argument("lists", nargs="+", help="A lists of moira lists to check")
	parser.add_argument("-d", "--dot_output", help="The output dot file", default="victor.dot")
	parser.add_argument("-o", "--output", help="The output PDF file", default="victor.pdf")
	args = parser.parse_args()

	lists_dict = {}
	terminals = set()
	for list_name in args.lists:
		m = MoiraList(list_name, lists_dict, terminals)
	to_dot(lists_dict, terminals, args.dot_output)
	dot_to_pdf(args.dot_output, args.output)
	subprocess.call(["rm", "victor.dot"])
	#print "Done, yee haw! Check out {}".format(args.output)
