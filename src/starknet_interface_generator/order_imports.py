from multiprocessing import allow_connection_pickling
from symbol import import_name
from typing import List, Dict
from collections import OrderedDict
from numpy import isin
from starkware.cairo.lang.compiler.ast.code_elements import CodeBlock, CodeElementImport, CodeElementEmptyLine, CommentedCodeElement, CodeElementDirective
from starkware.cairo.lang.compiler.ast.visitor import Visitor

class OrderImports(Visitor):
    """
    Orders imports in Cairo files
    """

    def __init__(self, import_order_names: List[str]):
        super().__init__()
        self.import_order_names=import_order_names

    def _visit_default(self, obj):
        # top-level code is not generated
        return obj
    
    def visit_CodeBlock(self, elm: CodeBlock):
        return self.extract_imports(elm)
    
    def extract_imports(self, elm):
        code_elements = elm.code_elements
        all_imports: Dict[str, List] = OrderedDict()
        all_imports = {x: [] for x in self.import_order_names}
        first_occurance_of_import = -1
        for i, x in enumerate(code_elements):
            if isinstance(x.code_elm, CodeElementImport):
                if first_occurance_of_import == -1:
                    first_occurance_of_import = i
                # order the import_items
                x.code_elm.import_items.sort(key=lambda x: x.orig_identifier.name)
                import_first_word = x.code_elm.path.name.split(".")[0]
                # group additional elements if not specified in initial list
                if import_first_word not in self.import_order_names:
                    self.import_order_names.append(import_first_word)
                    all_imports[import_first_word] = []
                for import_order_name in self.import_order_names:
                    if (import_order_name == x.code_elm.path.name.split(".")[0]):
                        all_imports[import_order_name].append(x)
                        break
        code_elements = list(filter(lambda x: not(isinstance(x.code_elm, CodeElementImport)), code_elements))
        all_imports = {x: all_imports[x] for x in self.import_order_names}
        
        ordered_imports = []
        for _, v in all_imports.items():
            v.sort(key=lambda x: x.code_elm.path.name)
            ordered_imports += [self.get_empty_element()] + v
        elm.code_elements = code_elements[:first_occurance_of_import] + ordered_imports + code_elements[first_occurance_of_import:]
    
    def get_empty_element(self):
        return CommentedCodeElement(code_elm=CodeElementEmptyLine(), comment=None, location=None)
    

    def create_ordered_imports(self, cairo_module):
        res = self.visit(cairo_module)
        return res
