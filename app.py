# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, send_from_directory,jsonify,request
from transcriber_re_mg14 import TranscriberRegexp
import json


# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

def processWords(words):
    transcriber = TranscriberRegexp()    
    sphinx_dictionary = transcriber.transcribeDictionary(words)
    #app.logger.info(u'[processWords] first key: {}'.format(sphinx_dictionary.iterkeys().next()))
    return sphinx_dictionary

@app.route('/lieptas/api/v1.0/dictionary', methods=['GET'])
def resolve_dictionary():
    #return jsonify({'tasks': tasks})
    words = request.args.get('words', u"nėra žodžių")
    app.logger.info(u'[resolve_recognition] words: {}'.format(words))
    translatedMap = processWords(words)
    body = json.dumps(translatedMap)
    app.logger.info(u'[resolve_recognition] dictionary: {}'.format(body))
    #return body.encode('utf8')
    return jsonify(translatedMap)

# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')
# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
