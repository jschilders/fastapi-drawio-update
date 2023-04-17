from fastapi import FastAPI, Request, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from xml.etree.ElementTree  import Element, SubElement, fromstring, tostring, dump
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

	# Return an XML response with updates
	return Response(
		content=XML.tostring(updates),
		media_type="application/xml"
	)


# -------------------------------

def make_random_style_changes(tree: dict) -> dict:
	updates = XML.Element('updates')
	for cell in tree.findall('.//mxCell[@id][@style]'):
		XML.SubElement(
    	updates, 
        'update', {
    		'id': cell.get('id'), 
      	'style': update_value(cell.get('style'), random_key(), random_color())
       }
     )
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
		'fontColor',
		'labelBackgroundColor',
		'labelBorderColor'
	])


def update_or_add_value(style: str, k: str, v: str) -> str:
	"""Naively update a key value pair. If it does not exists, it is added to the end of the string.

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


def update_value(style: str, k: str, v: str) -> str:
	"""Naively update a key value pair.

	Args:
		style (str): String to update a key-value pair in
		k (str): key to update
		v (str): new value

	Returns:
		str: updated string
	"""
	return f"{style}{k}={v};"
