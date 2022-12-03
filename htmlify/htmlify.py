class OntologyCleaner:
    def __init__(self, graph, namespace):
        self.full_ontology = graph
        self.namespace = namespace

    def get_title(self):
        for s, p, o, in self.full_ontology:
            if str(s) == self.namespace and str(p) == "http://purl.org/dc/terms/title":
                return o
        return "Unknown"
