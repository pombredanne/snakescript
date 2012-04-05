#!/usr/bin/env python

import snakescript

from flask import Flask, make_response, url_for
app = Flask(__name__)

@app.route("/<path:modules>")
def serve(modules):
	js = ""
	for name in modules.split("+"):
		js += snakescript.module(name).to_javascript()
	rs = make_response(js)
	rs.headers["Content-Type"] = "application/javascript"
	return rs

if __name__ == "__main__":
	app.run(debug=True)

