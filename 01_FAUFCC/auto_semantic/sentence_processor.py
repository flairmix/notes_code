import spacy
from spacy import displacy
from IPython.display import display, HTML
import networkx as nx
import matplotlib.pyplot as plt

class SentenceProcessor:
    """
    A class for processing and visualizing sentences using spaCy.

    Features:
    - Loads text into a spaCy Doc object and splits into sentences
    - Allows reuse of loaded spaCy model across multiple texts
    - Provides named entities, syntactic dependencies, subject-modifier relations
    - Offers multiple visualizations (HTML lists, displacy trees, graphs)
    """

    def __init__(self, model: str = "ru_core_news_sm"):
        self.nlp = spacy.load(model)
        self.text = ""
        self.doc = None
        self.sentences = []

    def load_text(self, text: str):
        """Load new text into the processor and re-tokenize."""
        self.text = text
        self.doc = self.nlp(text)
        self.sentences = list(self.doc.sents)

    def get_entities(self):
        return [
            {"sentence": sent.text, "index": idx + 1, "entities": [(ent.text, ent.label_) for ent in self.nlp(sent.text).ents]}
            for idx, sent in enumerate(self.sentences)
        ]

    def get_dependencies(self):
        return [
            {"sentence": sent.text, "index": idx + 1, "dependencies": [(token.text, token.dep_, token.head.text) for token in self.nlp(sent.text)]}
            for idx, sent in enumerate(self.sentences)
        ]

    def render_dependencies(self, jupyter=False):
        for sent in self.sentences:
            displacy.render(self.nlp(sent.text), style="dep", jupyter=True)

    def render_entities(self, jupyter=False):
        for sent in self.sentences:
            displacy.render(self.nlp(sent.text), style="ent", jupyter=True)

    def get_doc(self):
        return self.doc

    def get_subjects_with_modifiers(self):
        all_subjects = []
        for sent in self.sentences:
            doc_sent = self.nlp(sent.text)
            subjects = []
            for token in doc_sent:
                if token.pos_ == "NOUN":
                    modifiers = [child.text for child in token.children if child.dep_ in ("amod", "acl", "advcl", "nmod", "compound")]
                    if modifiers:
                        phrase = " ".join(modifiers + [token.text])
                        if phrase not in subjects:
                            subjects.append(phrase)
            all_subjects.append(subjects)
        return all_subjects

    def render_subjects_with_modifiers(self):
        all_subjects = self.get_subjects_with_modifiers()
        html = "<h4>Subjects with Modifiers by Sentence:</h4>"
        for idx, subjects in enumerate(all_subjects):
            html += f"<b>Sentence {idx+1}:</b><ul>"
            for subj in subjects:
                html += f"<li>{subj}</li>"
            html += "</ul>"
        return HTML(html)

    def get_pos_groups(self):
        results = []
        for sent in self.sentences:
            doc_sent = self.nlp(sent.text)
            pos_groups = {"ADJ": [], "VERB": [], "ADV": [], "NOUN": []}
            for t in doc_sent:
                if t.pos_ in pos_groups:
                    pos_groups[t.pos_].append(t.text)
            results.append(pos_groups)
        return results

    def get_lemmatized_text(self):
        return [" ".join([t.lemma_ for t in self.nlp(sent.text)]) for sent in self.sentences]

    def get_subject_modifier_relations(self):
        all_relations = []
        for sent in self.sentences:
            doc_sent = self.nlp(sent.text)
            relations = []
            for token in doc_sent:
                if token.pos_ == "NOUN":
                    for child in token.children:
                        if child.dep_ in ("amod", "acl", "advcl", "nmod", "compound"):
                            relations.append((child.text, token.text))
            all_relations.append(relations)
        return all_relations

    def render_subject_modifier_relations(self):
        all_pairs = self.get_subject_modifier_relations()
        html = "<h4>Subject–Modifier Relations by Sentence:</h4>"
        for idx, pairs in enumerate(all_pairs):
            html += f"<b>Sentence {idx+1}:</b><ul>"
            for mod, head in pairs:
                html += f"<li><b>{mod}</b> → {head}</li>"
            html += "</ul>"
        return HTML(html)

    def plot_subject_modifier_graph(self):
        all_pairs = self.get_subject_modifier_relations()
        for idx, pairs in enumerate(all_pairs):
            if not pairs:
                continue
            G = nx.DiGraph()
            for mod, head in pairs:
                G.add_edge(mod, head)
            plt.figure(figsize=(8, 5))
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", arrows=True)
            plt.title(f"Subject–Modifier Graph (Sentence {idx+1})")
            plt.show()