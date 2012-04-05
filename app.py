#!/usr/bin/env python

import snakescript

from flask import Flask, make_response, url_for
app = Flask(__name__)

@app.route("/<path:name>")
def get_module(name):
	rs = make_response(snakescript.module(name).to_javascript())
	rs.headers["Content-Type"] = "application/javascript"
	return rs

if __name__ == "__main__":
	app.run(debug=True)

