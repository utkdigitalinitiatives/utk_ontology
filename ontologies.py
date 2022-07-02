#!/usr/bin/env python
from rdflib import Graph, BNode, Literal, URIRef
from flask import Flask
from flask_rdf.flask import returns_rdf

app = Flask(__name__)


@app.route('/files')
@app.route('/<path:path>')
@returns_rdf
def files(path=''):
  g = Graph()
  g.parse("ontologies/files.ttl", format='ttl')
  return g


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)