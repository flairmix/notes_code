from owlready2 import get_ontology, Thing, ObjectProperty, DataProperty, types
from pyvis.network import Network

class OntologyBuilder:
    def __init__(self, base_uri="http://example.org/ontology#"):
        self.onto = get_ontology(base_uri)
        self.classes = {}
        self.object_properties = {}
        self.individuals = {}

    def add_class(self, class_name, parent_class=Thing):
        if class_name not in self.classes:
            with self.onto:
                new_class = types.new_class(class_name, (parent_class,))
            self.classes[class_name] = new_class
        return self.classes[class_name]

    def add_object_property(self, property_name, domain, range_):
        if property_name not in self.object_properties:
            with self.onto:
                new_property = types.new_class(property_name, (ObjectProperty,))
                new_property.domain = [self.classes[domain]]
                new_property.range = [self.classes[range_]]
            self.object_properties[property_name] = new_property
        return self.object_properties[property_name]

    def add_individual(self, class_name, individual_name):
        with self.onto:
            individual = self.classes[class_name](individual_name)
        self.individuals[individual_name] = individual
        return individual

    def relate_individuals(self, subject, predicate, obj):
        getattr(subject, predicate).append(obj)

    def save(self, filename):
        self.onto.save(file=filename, format="rdfxml")

    def visualize(self, filename="ontology.html"):
        net = Network(width="2500px", height="1100px", cdn_resources='in_line', notebook=False)
        net.barnes_hut(gravity=-7000, spring_length=30)

        # Adding classes
        for cls_name, cls_obj in self.classes.items():
            net.add_node(f"class_{cls_name}", label=cls_name, shape='ellipse', color='lightblue')
            for parent_cls in cls_obj.is_a:
                if isinstance(parent_cls, Thing.__class__) and parent_cls.name in self.classes:
                    net.add_edge(f"class_{parent_cls.name}", f"class_{cls_name}", label="subclass_of", length=400)

        # Adding individuals
        for ind_name, ind_obj in self.individuals.items():
            cls_name = ind_obj.is_a[0].name
            net.add_node(f"ind_{ind_name}", label=ind_name, shape='dot', color='lightgreen')
            net.add_edge(f"class_{cls_name}", f"ind_{ind_name}")

        # Adding properties as edges between individuals
        for prop_name in self.object_properties:
            for subj in self.individuals.values():
                for obj in getattr(subj, prop_name, []):
                    net.add_edge(f"ind_{subj.name}", f"ind_{obj.name}", label=prop_name, length=300)

        html_content = net.generate_html()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def save_and_visualize(self, owl_filename="ontology.owl", html_filename="ontology.html"):
        self.save(owl_filename)
        self.visualize(html_filename)