##########################################
##### Python Documentation Generator #####
#####         by Chris Pyles         #####
##########################################

import runpy
import inspect
import sys
import glob
import argparse
import re

# create CLI argument parser and extract arguments
parser = argparse.ArgumentParser(description="generate Markdown documentation for Python files")
parser.add_argument("-a", "--append", dest="append", help="file to which to append generated Markdown")
parser.add_argument("-o", "--output", dest="out", help="file to save generated Markdown to")
parser.add_argument("-s", "--sub", dest="sub", help="file with ::DOCUMENTATION:: tag to replace Markdown")
parser.add_argument("-t", "--template", dest="temp", help="template file with ::DOCUMENTATION:: tag, needs OUT argument")
parser.add_argument(dest="files", nargs=argparse.REMAINDER, help="files to be documented")
namespace = vars(parser.parse_args())

docstrings, classes, methods = {}, [], []
for file in namespace["files"]:
	environment = runpy.run_path(file)
	objects = {name : environment[name] for name in environment if name[0] != "_"}
	for name in objects:
		obj = objects[name]
		string = inspect.getdoc(obj)
		docstrings[file[:-3] + "." + name] = string
		if inspect.isclass(obj):
			classes += [file[:-3] + "." + name]
			class_methods = [m for m in dir(obj) if callable(getattr(obj, m)) and m[0] != "_"]
			for method_name in class_methods:
				method = getattr(obj, method_name)
				docstrings[file[:-3] + "." + name + "." + method_name] = inspect.getdoc(method)
				methods += [file[:-3] + "." + name + "." + method_name]

markdown = ""
prevClass = False
for obj in docstrings:
	string = docstrings[obj]
	if obj in classes:
		if markdown != "":
			markdown += "---\n\n"
		name = "**_class_ `" + obj + "`**"
		prevClass = True
	elif obj in methods:
		name = "**_method_ `" + obj + "`**"
		prevClass = True
	else:
		if prevClass:
			markdown += "---\n\n"
		name = "**_function_ `" + obj + "`**"
		prevClass = False

	markdown += name + "\n\n" + string + "\n\n"

markdown = markdown[:-1]

if namespace["temp"]:
	if namespace["out"]:
		with open(namespace["temp"]) as f:
			contents = f.read()

		with open(namespace["out"], "w+") as f:
			f.write(re.sub("::DOCUMENTATION::", markdown, contents))

	else:
		print("You did not pass an OUT argument.")

elif namespace["sub"]:
	with open(namespace["sub"]) as f:
		contents = f.read()
		contents = re.sub("::DOCUMENTATION::", markdown, contents)
		f.write(contents)

elif namespace["append"]:
	with open(namespace["append"], "a+") as f:
		f.write(markdown)

elif namespace["out"]:
	with open(namespace["out"], "w+") as f:
		f.write(markdown)

else:
	print(markdown)