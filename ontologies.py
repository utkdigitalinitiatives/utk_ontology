#!/usr/bin/env python
from rdflib import Graph, BNode, Literal, URIRef
from flask import Flask, request, render_template
from flask_rdf.flask import returns_rdf
import flask_rdf
from htmlify import htmlify
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/')
@app.route('/index')
def index():
    all_ontologies = []
    for p, d, f in os.walk('ontologies'):
        for ontology in f:
            g = Graph()
            g.parse(f"ontologies/{ontology}", format='ttl')
            ontology_info = htmlify.OntologyCleaner(
                graph=g,
                namespace=f"https://ontology.lib.utk.edu/{ontology.replace('.ttl', '')}#"
            )
            all_ontologies.append(
                {
                    'url': f'/{ontology.replace(".ttl", "")}',
                    'title': ontology_info.ontology_details['title']
                }
            )
    return render_template(
        'index.html',
        details={
            'title': 'UTK Digital Initiatives Ontologies'
        },
        ontologies=all_ontologies
    )


@app.route('/<path:path>')
@returns_rdf
def roles(path=''):
  g = Graph()
  g.parse("ontologies/roles.ttl", format='ttl')
  return g


@app.route('/works')
@returns_rdf
def files(path=''):
  g = Graph()
  g.parse("ontologies/works.ttl", format='ttl')
  return g


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
