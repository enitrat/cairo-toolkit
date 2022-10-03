from starkware.cairo.lang.compiler.ast.code_elements import CodeElementFunction, CodeBlock, CodeElementImport
from starkware.cairo.lang.compiler.ast.visitor import Visitor


class InterfaceParser(Visitor):
    """
    Parses a Cairo interface. Call `parse_interface` to return the interface as a dictionary.
    """

    def __init__(self, contract_name: str):
        super().__init__()
        self.contract_name = contract_name
        self.imports = {}  # map import_name => path
        # list of required import statements for the interface
        self.required_import_paths = []
        self.functions = {}  # TODO should be a list
        self.namespace_name = ''

    def parse_interface(self, module):
        self.visit(module)
        return {
            'name': self.namespace_name,
            'functions': self.functions,
            'imports': self.imports
        }

    def parse_imports(self, elm: CodeBlock):
        # We want to keep track of the file imports so that we can import types inside the contract interface
        for x in elm.code_elements:
            if isinstance(x.code_elm, CodeElementImport):
                path = x.code_elm.path.name
                imported_items = x.code_elm.import_items
                for item in imported_items:
                    self.imports[item.orig_identifier.name] = path

    def parse_code_elm_function(self, elm: CodeElementFunction):

        if elm.element_type == 'namespace':
            self.parse_namespace(elm)
            return

        # We only visit proper functions decorated with 'external' or 'view'.
        self.parse_function(elm)
        return

    def parse_namespace(self, elm):
        namespace_name = elm.name
        self.namespace_name = namespace_name

    def parse_function(self, elm: CodeElementFunction):

        fn_params = []
        fn_returns = []
        # func arguments
        for i, arg in enumerate(elm.arguments.identifiers):
            fn_params.append(arg.format())

        # func return values
        if elm.returns != None:
            fn_returns.append(elm.returns.format())

        self.functions[elm.name] = {'params': fn_params, 'returns': fn_returns}

    def _visit_default(self, obj):
        # top-level code is not generated
        return obj

    def visit_CodeElementFunction(self, elm: CodeElementFunction):
        self.parse_code_elm_function(elm)
        return super().visit_CodeElementFunction(elm)

    def visit_CodeBlock(self, elm: CodeBlock):
        self.parse_imports(elm)
        return super().visit_CodeBlock(elm)
