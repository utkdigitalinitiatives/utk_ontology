from rdflib import URIRef

class OntologyCleaner:
    def __init__(self, graph, namespace):
        self.full_ontology = graph
        self.namespace = namespace
        self.ontology_details = self.__get_details()
        self.properties_and_classes = self.__get_properties_and_classes()

    def __get_details(self):
        ontology_details = {
            'title': '',
            'definition': '',
            'namespace': self.namespace,
            'version': '',
            'last_modified': ''
        }
        for s, p, o in self.full_ontology:
            if str(s) == self.namespace and str(p) == "http://purl.org/dc/terms/title":
                ontology_details['title'] = o
            elif str(s) == self.namespace and str(p) == "http://www.w3.org/2000/01/rdf-schema#comment":
                ontology_details['definition'] = o
            elif str(s) == self.namespace and str(p) == "http://purl.org/dc/terms/modified":
                ontology_details['last_modified'] = o
            elif str(s) == self.namespace and str(p) == "http://purl.org/dc/terms/modified":
                ontology_details['last_modified'] = o
            elif str(s) == self.namespace and str(p) == "http://www.w3.org/2002/07/owl#versionInfo":
                ontology_details['version'] = o
        return ontology_details

    def __get_properties_and_classes(self):
        properties = {}
        for s, p, o in self.full_ontology:
            if self.__namespace_if_uri(s) is not self.namespace:
                if self.__namespace_if_uri(s) not in properties:
                    properties[self.__namespace_if_uri(s)] = {}
                    properties[self.__namespace_if_uri(s)][self.__namespace_if_uri(p)] = self.__namespace_if_uri(o)
                else:
                    properties[self.__namespace_if_uri(s)][self.__namespace_if_uri(p)] = self.__namespace_if_uri(o)
        return properties

    @staticmethod
    def __namespace_if_uri(potential_uri):
        namespaces = (
            {
                'namespace': 'http://purl.org/dc/elements/1.1/',
                'prefix': 'dc'
            },
            {
                'namespace': 'http://purl.org/dc/terms/',
                'prefix': 'dcterms'
            },
            {
                'namespace': 'http://www.w3.org/2002/07/owl#',
                'prefix': 'owl'
            },
            {
                'namespace': 'http://pcdm.org/models#',
                'prefix': 'pcdm'
            },
            {
                'namespace': 'http://pcdm.org/file-format-types#',
                'prefix': 'pcdmff'
            },
            {
                'namespace': 'http://pcdm.org/works#',
                'prefix': 'pcdmworks'
            },
            {
                'namespace': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'prefix': 'rdf'
            },
            {
                'namespace': 'http://www.w3.org/2000/01/rdf-schema#',
                'prefix': 'rdfs'
            },
            {
                'namespace': 'http://id.loc.gov/vocabulary/relators/',
                'prefix': 'relators'
            },
            {
                'namespace': 'http://www.w3.org/2004/02/skos/core#',
                'prefix': 'skos'
            },
            {
                'namespace': 'https://ontology.lib.utk.edu/roles#',
                'prefix': 'utk_roles'
            },
            {
                'namespace': 'https://ontology.lib.utk.edu/works#',
                'prefix': 'utk_works'
            },
            {
                'namepsace': 'http://www.w3.org/2001/XMLSchema#',
                'prefix': 'xsd'
            }
        )
        if type(potential_uri) == URIRef:
            for namespace in namespaces:
                if namespace['namespace'] in potential_uri and '#' in potential_uri:
                    return f"{namespace['prefix']}:{potential_uri.fragment}"
                elif namespace['namespace'] in potential_uri:
                    return f"{namespace['prefix']}:{str(potential_uri).split('/')[-1]}"
            return str(potential_uri)
        else:
            return str(potential_uri)
