#!/usr/bin/env python
from rdflib import Graph, BNode, Literal, URIRef
from flask import Flask, request, render_template
from flask_rdf.flask import returns_rdf
import flask_rdf
from htmlify import htmlify
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/roles')
@app.route('/<path:path>')
@returns_rdf
def roles(path=''):
    g = Graph()
    g.parse("ontologies/roles.ttl", format='ttl')
    if flask_rdf.wants_rdf(request.headers['Accept']) is False:
        ontology = htmlify.OntologyCleaner(graph=g, namespace="https://ontology.lib.utk.edu/roles#")
        return render_template(
            'index.html',
            details=ontology.ontology_details,
            classes_and_props=ontology.properties_and_classes,
            namespaces=ontology.all_namespaces
        )
    else:
        return g


@app.route('/works')
@returns_rdf
def files(path=''):
    g = Graph()
    g.parse("ontologies/works.ttl", format='ttl')
    if flask_rdf.wants_rdf(request.headers['Accept']) is False:
        ontology = htmlify.OntologyCleaner(graph=g, namespace="https://ontology.lib.utk.edu/works#")
        return render_template(
            'index.html',
            details=ontology.ontology_details,
            classes_and_props=ontology.properties_and_classes,
            namespaces=ontology.all_namespaces
        )
    else:
        return g


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
