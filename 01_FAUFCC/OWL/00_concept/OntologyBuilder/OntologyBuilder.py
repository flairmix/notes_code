from owlready2 import get_ontology, Thing, ObjectProperty, DataProperty, types
from pyvis.network import Network

class OntologyBuilder:
    def __init__(self, base_uri="http://example.org/ontology#", gravity=-7000, spring_length=30):
        self.onto = get_ontology(base_uri)
        self.classes = {}
        self.object_properties = {}
        self.individuals = {}
        self.gravity = gravity
        self.spring_length = spring_length

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

        net = Network(width="100%", height="100vh", cdn_resources='in_line', notebook=False, directed=True)
        net.repulsion(node_distance=300, spring_length=200, central_gravity=0.1)

        # === Add class nodes ===
        for cls_name, cls_obj in self.classes.items():
            net.add_node(f"class_{cls_name}",
                        label=cls_name,
                        shape='box',
                        color='lightblue',
                        title=f"Class: {cls_name}",
                        group='class')

            for parent_cls in cls_obj.is_a:
                if isinstance(parent_cls, Thing.__class__) and parent_cls.name in self.classes:
                    net.add_edge(f"class_{parent_cls.name}", f"class_{cls_name}",
                                label="subclass_of",
                                arrows='to',
                                width=2,
                                color='gray',
                                group='edge_class')

        # === Add individuals ===
        for ind_name, ind_obj in self.individuals.items():
            cls_name = ind_obj.is_a[0].name
            net.add_node(f"ind_{ind_name}",
                        label=ind_name,
                        shape='dot',
                        color='yellow',
                        title=f"Individual of class: {cls_name}",
                        group='individual')
            net.add_edge(f"class_{cls_name}", f"ind_{ind_name}",
                        arrows='to',
                        color='black',
                        width=2,
                        group='edge_ind')

        # === Add unique properties as intermediate nodes ===
        prop_counter = 0
        for prop_name, _ in self.object_properties.items():
            for subj in self.individuals.values():
                for obj in getattr(subj, prop_name, []):
                    prop_counter += 1
                    prop_node_id = f"prop_{prop_name}_{prop_counter}"
                    net.add_node(prop_node_id,
                                label=prop_name,
                                shape='triangle',
                                color='tomato',
                                title=f"{prop_name}: {subj.name} → {obj.name}",
                                group='property')

                    net.add_edge(f"ind_{subj.name}", prop_node_id,
                                arrows='to',
                                color='orange',
                                width=2,
                                group='edge_prop')
                    net.add_edge(prop_node_id, f"ind_{obj.name}",
                                arrows='to',
                                color='orange',
                                width=2,
                                group='edge_prop')

        # === CSS: full screen and button overlay ===
        style_patch = """
        <style>
        html, body {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }

        #mynetwork {
            width: 100vw !important;
            height: 100vh !important;
            border: none;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 0;
        }

        .layer-controls {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 10;
            background: white;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        </style>
        """

        # === JS: layer toggles and auto-zoom ===
        controls_js = """
        <script>
        function toggleGroup(groupName) {
            let nodes = network.body.data.nodes.get();
            let edges = network.body.data.edges.get();

            nodes.forEach(n => {
                if (n.group === groupName) {
                    n.hidden = !n.hidden;
                    network.body.data.nodes.update(n);
                }
            });

            edges.forEach(e => {
                if (e.group === "edge_" + groupName) {
                    e.hidden = !e.hidden;
                    network.body.data.edges.update(e);
                }
            });
        }

        network.once("stabilizationIterationsDone", function () {
            network.fit({ animation: { duration: 1000, easingFunction: "easeInOutQuad" } });
        });
        </script>

        <div class="layer-controls">
        <button onclick="toggleGroup('class')">Toggle Classes</button>
        <button onclick="toggleGroup('individual')">Toggle Individuals</button>
        <button onclick="toggleGroup('property')">Toggle Properties</button>
        </div>
        """

        # === Final HTML assembly ===
        html_content = net.generate_html()
        final_html = html_content.replace("</head>", style_patch + "\n</head>")
        final_html = final_html.replace("</body>", controls_js + "\n</body>")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_html)


    def save_and_visualize(self, owl_filename="ontology.owl", html_filename="ontology.html"):
        self.save(owl_filename)
        self.visualize(html_filename)