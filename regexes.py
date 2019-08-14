import re

class_regex = r"class \w+:\n(\t| {4})+\"\"\"\n?(\w+|((\t| {4})+\w+\n*)+)\n?(\t| {4})*\"\"\""
function_regex = r"^def \w+\(.*\):\n(\t| {4})+\"\"\"\n?(\w+|((\t| {4})+\w+\n*)+)\n?(\t| {4})*\"\"\""
method_regex = r"^(\t| {4})+def \w+\(.*\):\n(\t| {4})+\"\"\"\n?(\w+|((\t| {4})+\w+\n*)+)\n?(\t| {4})*\"\"\""

def find_classes(string):
	classes = []
	match = re.match(class_regex, string)
	while match:
		classes += [match[0]]
		string = re.sub(class_regex, "", string, count=1)
		match = re.match(class_regex, string)
	return classes

def find_functions(stirng):
	functions = []
	match = re.match(function_regex, string)
	while match:
		functions += [match[0]]
		string = re.sub(function_regex, "", string, count=1)
		match = re.match(function_regex, string)
	return functions

def find_methods(stirng):
	methods = []
	match = re.match(method_regex, string)
	while match:
		methods += [match[0]]
		string = re.sub(method_regex, "", string, count=1)
		match = re.match(method_regex, string)
	return methods