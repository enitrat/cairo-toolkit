from starkware.cairo.lang.compiler.ast.code_elements import CodeBlock, CodeElementImport
from starkware.cairo.lang.compiler.ast.visitor import Visitor

class OrderImports(Visitor):
    """
    Orders imports in Cairo files
    """

    def __init__(self):
        super().__init__()

    def _visit_default(self, obj):
        # top-level code is not generated
        return obj
    
    def visit_CodeBlock(self, elm: CodeBlock):
        return self.extract_imports(elm)
    
    def extract_imports(self, elm):
        starkware = []
        oz = []
        rest = []
        for x in elm.code_elements:
            if isinstance(x.code_elm, CodeElementImport):
                if (len(x.code_elm.import_items) > 1):
                    import_names =  "".join(item.orig_identifier.name + ", " for item in x.code_elm.import_items)
                else:
                    import_names = x.code_elm.import_items[0].orig_identifier.name
                import_str = "from " + x.code_elm.path.name + " import " + import_names
                if ("starkware" in import_str):
                    starkware.append(import_str)
                elif ("openzeppelin" in import_str):
                    oz.append(import_str)
                else:
                    rest.append(import_str)
        all_import = starkware + oz + rest
        all_import_str = "".join(x + "\\n" for x in all_import)
        return all_import_str
    
    def create_ordered_imports(self, cairo_module):
        res = self.visit(cairo_module).cairo_file.code_block
        return res
