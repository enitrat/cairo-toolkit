from multiprocessing import allow_connection_pickling
from symbol import import_name
from typing import List, Dict
from collections import OrderedDict
from starkware.cairo.lang.compiler.ast.code_elements import CodeBlock, CodeElementImport, CodeElementEmptyLine
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
        empty_element = self.get_empty_element(elm)
        all_imports: Dict[str, List] = OrderedDict()
        temp_import_order_names = self.import_order_names + ["rest"]

        all_imports = {x: [empty_element] for x in temp_import_order_names}
        code_elements = elm.code_elements
            
        for i, x in enumerate(code_elements):
            if isinstance(x.code_elm, CodeElementImport):
                for import_order_name in temp_import_order_names:
                    if (import_order_name not in self.import_order_names):
                        all_imports["rest"].append(x)
                        break
                    elif (import_order_name in x.code_elm.path.name):
                        all_imports[import_order_name].append(x)
                        break
        code_elements = list(filter(lambda x: not(isinstance(x.code_elm, CodeElementImport)), code_elements))
        all_imports = {x: all_imports[x] for x in temp_import_order_names if len(all_imports[x]) > 1}
        
        ordered_imports = []
        for _, v in all_imports.items():
            ordered_imports += v
        elm.code_elements = [code_elements[0]] + ordered_imports + code_elements[1:]
        return elm.code_elements
    
    def get_empty_element(self, cairo_module):
        code_elements = cairo_module.code_elements
        for x in code_elements:
                if isinstance(x.code_elm, CodeElementEmptyLine):
                    res = x
                    break
        return res
    

    def create_ordered_imports(self, cairo_module):
        res = self.visit(cairo_module)
        return res
