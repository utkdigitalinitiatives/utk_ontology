import requests
from rdflib import Graph, URIRef, RDFS, Literal
from rdflib.namespace import RDF, SKOS, DC, RDFS


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
        subject = f"https://ontology.lib.utk.edu/roles#{self.uri.split('/')[-1]}"
        g = Graph()
        g.bind("skos", SKOS)
        g.bind("utk", "https://ontology.lib.utk.edu/roles#")
        g.bind("dc", "http://purl.org/dc/elements/1.1/")
        g.bind("relators", "http://id.loc.gov/vocabulary/relators/")
        g.add((URIRef(subject), RDF.type, RDF.Property))
        for s, p, o in full_graph:
            if p.strip() == "http://www.w3.org/2004/02/skos/core#prefLabel" and s.strip() == self.uri:
                g.add((URIRef(subject), SKOS.prefLabel, Literal(o)))
            if p.strip() == "http://www.w3.org/2004/02/skos/core#definition" and s.strip() == self.uri:
                g.add((URIRef(subject), SKOS.definition, Literal(o)))
        g.add((URIRef(subject), SKOS.closeMatch, URIRef(self.uri)))
        g.add((URIRef(subject), RDFS.range, RDFS.Literal))
        g.add((URIRef(subject), RDFS.subPropertyOf, DC.contributor))
        return g


class OntologyGenerator:
    def __init__(self, output):
        self.filename = output

    def write_ontology(self, input):
        g = Graph()
        g.bind("skos", SKOS)
        g.bind("utk", "https://ontology.lib.utk.edu/roles#")
        g.bind("dc", "http://purl.org/dc/elements/1.1/")
        g.bind("relators", "http://id.loc.gov/vocabulary/relators/")
        with open(input, 'r') as my_input:
            for line in my_input:
                role = RoleBuilder(line.strip()).build()
                for thing in role:
                    g.add(thing)
        with open(f"ontologies/{self.filename}", "wb") as rdf:
            rdf.write(
                g.serialize(format='turtle', indent=4).encode("utf-8")
            )
        return


if __name__ == "__main__":
    OntologyGenerator('test.ttl').write_ontology('tests/roles.txt')
