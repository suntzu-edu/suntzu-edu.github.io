
import sys, os
from pathlib import Path

from flask import Flask, render_template, url_for
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from jinja2 import Environment, PackageLoader, select_autoescape

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

app.config['FREEZER_DESTINATION'] = './docs/'
freezer = Freezer(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/programs/')
def programs():
    return render_template('programs.html')

@app.route('/notes/')
def notes():
    return render_template('notes.html')

@app.route('/collection/')
def collection():
    return render_template('collection.html', pages=pages)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    if page['category'] == 'heartsutra':
        return render_template('page_zh.html', page=page)
    return render_template('page.html', page=page)

@freezer.register_generator
def pagelist():
    for page in pages:
        yield url_for('page', path=page.path)



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=5002)


