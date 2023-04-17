from fastapi import FastAPI, Request, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from xml.etree.ElementTree  import Element
from xml.etree import ElementTree as XML

import re
import random


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"]
)


@app.get("/")
async def root():
	return {"message": "Hello World"}


@app.post("/")
async def root(xml: str = Form()) -> Response:
	# Create an XML documenttree from posted XML string
	tree = XML.fromstring(xml)

	# Randomly change colors
	updates = make_random_style_changes(tree)

	# Return an XML response:
	# <updates>
	#   <update id='...' style = '...'/>
	#   <update id='...' style = '...'/>
	#   <update id='...' style = '...'/>
	# </updates>
	return Response(
		content=f"<updates>{updates}</updates>",
		media_type="application/xml"
	)


def make_random_style_changes(tree: dict) -> dict:
	updates = ''
	for id, style in make_style_dict(tree).items():
		new_style=update_value(style, random_key(), random_color())
		updates += f"<update id='{id}' style='{new_style}'/>"
	return updates


def random_color() -> str:
	"""Randomly return one of the listed strings

	Returns:
		str: Randomly selected string from list
	"""
	return random.choice([
		'red',
		'green',
		'yellow',
		'blue',
		'black'
	])


def random_key() -> str:
	"""Randomly return one of the listed strings

	Returns:
		str: Randomly selected string from list
	"""
	return random.choice([
	'fillColor',
	'strokeColor',
	'fontColor'
	])


def update_value(style: str, k: str, v: str) -> str:
	"""Naivly update a key value pair. If it does not exists, it is added to the end of the string.

	Args:
		style (str): String to update a key-value pair in
		k (str): key to update
		v (str): new value

	Returns:
		str: updated string
	"""
	if re.search(f"{k}=", style):
			# if 'key=' exists in string, replace current value
			return re.sub(f'(?<={k}=)(\w+?)(?=;)', v, style)
	else:
		# add key=value; to the end
		return f"{style}{k}={v};"


def make_style_dict(xmlroot: Element) -> dict[str, str]:
	"""Make a dictionary: for each mxCell that has an "ID" and a "style", add an entry "{ 'ID': 'Style' }" to the dict

	Args:
		xmlroot (ElementTree): XML tree to search

	Returns:
		dict: Dict containing entries { 'ID': 'Style' }
	"""
	return {
		cell.attrib['id']: cell.attrib['style']
		for cell in xmlroot.iter('mxCell')
		if  cell.attrib.__contains__('id')
		and cell.attrib.__contains__('style')
		}

