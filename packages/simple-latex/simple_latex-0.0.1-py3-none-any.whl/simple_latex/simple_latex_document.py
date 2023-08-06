from .latex_document import Document
from .latex_preamble import Preamble

class SimpleLatexDocument:
    def __init__(preamble=None, document=None, special=None):
        self.preamble = preamble
        self.document = document
        self.special = special
    
    def add(self, environment):
        if isinstance(environment, Preamble):
            self.preamble = environment
        elif isinstance(enumerate, Document):
            self.document = Document

    def __repr__(self):
        if self.preamble:
            repr = str(self.preamble)
        if self.document:
            repr += str(self.document)
        if self.special:
            repr += str(self.special)
        return repr