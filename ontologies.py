#!/usr/bin/env python
from rdflib import Graph, BNode, Literal, URIRef
from flask import Flask, request, render_template
from flask_rdf.flask import returns_rdf
import flask_rdf
from htmlify import htmlify

app = Flask(__name__)


@app.route('/roles')
@app.route('/<path:path>')
@returns_rdf
def roles(path=''):
    g = Graph()
    g.parse("ontologies/roles.ttl", format='ttl')
    if flask_rdf.wants_rdf(request.headers['Accept']) is False:
        ontology = htmlify.OntologyCleaner(graph=g, namespace="https://ontology.lib.utk.edu/roles#")
        return render_template('index.html', title=ontology.get_title())
    else:
        return g


@app.route('/works')
@returns_rdf
def files(path=''):
    g = Graph()
    g.parse("ontologies/files.ttl", format='ttl')
    return g


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
