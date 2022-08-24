import requests
from rdflib import Graph, URIRef, RDFS, Literal, XSD
from rdflib.namespace import RDF, SKOS, DC, RDFS, DCTERMS, OWL
import arrow


class RoleBuilder:
    def __init__(self, uri):
        self.headers = {
            "Accept": "text/turtle, application/turtle, application/x-turtle, application/json, text/json, text/n3,"
            "text/rdf+n3, application/rdf+n3, application/rdf+xml, application/n-triples"
        }
        self.uri = uri
        self.data = self.__get_content(uri)

    def __get_content(self, uri):
        r = requests.get(uri, headers=self.headers)
        return r.content.decode("utf-8")

    def build(self):
        full_graph = Graph().parse(data=self.data, format="json-ld")
        subject = f"https://utk-ontologies.herokuapp.com/roles#{self.uri.split('/')[-1]}"
        g = Graph()
        g.add((URIRef(subject), RDF.type, RDF.Property))
        for s, p, o in full_graph:
            if p.strip() == "http://www.w3.org/2004/02/skos/core#prefLabel" and s.strip() == self.uri:
                g.add((URIRef(subject), SKOS.prefLabel, Literal(f"Local {o}")))
            if p.strip() == "http://www.w3.org/2004/02/skos/core#definition" and s.strip() == self.uri:
                g.add((URIRef(subject), SKOS.definition, Literal(o)))
        g.add((URIRef(subject), SKOS.closeMatch, URIRef(self.uri)))
        g.add((URIRef(subject), RDFS.range, RDFS.Literal))
        g.add((URIRef(subject), RDFS.subPropertyOf, DC.contributor))
        g.add((URIRef(subject), RDFS.isDefinedBy, URIRef("https://utk-ontologies.herokuapp.com/roles#")))
        return g


class OntologyGenerator:
    def __init__(self, output):
        self.filename = output

    def write_ontology(self, input):
        g = Graph()
        g.bind("skos", SKOS)
        g.bind("utk", "https://utk-ontologies.herokuapp.com/roles#")
        g.bind("dc", "http://purl.org/dc/elements/1.1/")
        g.bind("dcterms", "http://purl.org/dc/terms/")
        g.bind("relators", "http://id.loc.gov/vocabulary/relators/")
        g.bind("xsd", "http://www.w3.org/2001/XMLSchema#")
        with open(input, 'r') as my_input:
            for line in my_input:
                role_graph = RoleBuilder(line.strip()).build()
                for role in role_graph:
                    g.add(role)
        ontology = self.add_ontology_information()
        for triple in ontology:
            g.add(triple)
        with open(f"ontologies/{self.filename}", "wb") as rdf:
            rdf.write(
                g.serialize(format='turtle', indent=4).encode("utf-8")
            )
        return

    def add_ontology_information(self):
        g = Graph()
        date = arrow.utcnow().format('YYYY-MM-DD')
        comment = "Ontology for the the University of Tennessee Libraries to state relationships between people and works.  This ontology exists because m3 profiles defined by Houndstooth cannot support both URIs and strings.  For that reason, this ontology exists and closely follows marcrelators.  The key difference is that this ontology is defined to work with values that are strings only."
        g.add((URIRef('https://utk-ontologies.herokuapp.com/roles#'), DCTERMS.modified, Literal(date, datatype=XSD.date)))
        g.add((URIRef('https://utk-ontologies.herokuapp.com/roles#'), RDFS.comment, Literal(comment, lang='en')))
        g.add((URIRef('https://utk-ontologies.herokuapp.com/roles#'), DCTERMS.publisher, URIRef('http://www.lib.utk.edu/')))
        g.add((URIRef('https://utk-ontologies.herokuapp.com/roles#'), DCTERMS.title, Literal('University of Tennessee Digital Initiatives Role Terms Ontology', lang='en')))
        g.add((URIRef('https://utk-ontologies.herokuapp.com/roles#'), RDFS.seeAlso, URIRef('https://github.com/utkdigitalinitiatives/utk_ontology/')))
        g.add((URIRef('https://utk-ontologies.herokuapp.com/roles#'), OWL.versionInfo, Literal(date, datatype=XSD.date)))
        return g


if __name__ == "__main__":
    OntologyGenerator('roles.ttl').write_ontology('tests/roles.txt')
