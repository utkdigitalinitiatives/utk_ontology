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
            if str(s) is not self.namespace:
                if str(s) not in properties:
                    properties[str(s)] = {}
                    properties[str(s)][str(p)] = str(o)
                else:
                    properties[str(s)][str(p)] = str(o)
        return properties

