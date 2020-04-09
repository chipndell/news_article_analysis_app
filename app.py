from flask import Flask, render_template, url_for
from ctv import *
from cbc import *


app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html',agency = 'CTV & CBC')


@app.route('/cbc_view')
def cbc_view():
	x = cbc_scrap()
	return render_template('cbc.html', agency = 'CBC', vals = x)


@app.route('/ctv_view')
def ctv_view():
	x = ctv_scrap()
	return render_template('ctv.html', agency = 'CTV', vals = x)


# @app.route('/contact_us')
# def contact_us():
# 	return render_template('contact_us.html')



if __name__ == "__main__":
	app.run(debug=True)
