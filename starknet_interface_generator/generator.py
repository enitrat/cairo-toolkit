import textwrap
from starkware.cairo.lang.compiler.ast.code_elements import CodeElementFunction, CodeBlock, CodeElementImport
from starkware.cairo.lang.compiler.ast.visitor import Visitor
from starkware.cairo.lang.compiler.ast.types import TypedIdentifier

from starknet_interface_generator.utils import to_camel_case


class Generator(Visitor):
    """
    Generates an interface from a Cairo contract.
    """

    def __init__(self, contract_name: str):
        super().__init__()
        self.contract_name = contract_name
        self.imports = {}
        self.required_import_paths = []
        self.functions = ""

    def generate_contract_interface(self, module):
        self.visit(module)
        interface = \
            "%lang starknet\n\n" + \
            "\n".join(self.required_import_paths) + "\n" \
            "@contract_interface\n" + \
            f"namespace I{to_camel_case(self.contract_name)}{{\n" \
            f"{self.functions} \n" \
            "}"
        return interface

    def parse_imports(self, elm: CodeBlock):
        # We want to keep track of the file imports so that we can import types inside the contract interface
        for x in elm.code_elements:
            if isinstance(x.code_elm, CodeElementImport):
                path = x.code_elm.path.name
                imported_items = x.code_elm.import_items
                for item in imported_items:
                    self.imports[item.orig_identifier.name] = path

    def parse_functions(self, elm: CodeElementFunction):
        # We only visit proper functions decorated with 'external' or 'view'.
        need_instrumentation = any(decorator.name in [
                                   "external", "view"] for decorator in elm.decorators)

        if not need_instrumentation:
            return

        # func name
        fn_signature = f"func {elm.name}("

        # func arguments
        for i, arg in enumerate(elm.arguments.identifiers):
            if arg.expr_type.format() != 'felt':
                self.add_import_path(arg)

            fn_signature += f"{arg.format()}"
            if i != len(elm.arguments.identifiers) - 1:
                fn_signature += ","
        fn_signature += ")"

        # func return values
        if elm.returns != None:
            fn_signature += " -> "
            fn_signature += elm.returns.format()
        fn_signature += "{\n}\n\n"

        self.functions += fn_signature

    def add_import_path(self, type: TypedIdentifier):
        # If we have imported types, we need to add the import path to our interface
        import_name = type.expr_type.format()
        import_path = self.imports[import_name]
        import_statement = f"from {import_path} import {type.expr_type.format()}\n"
        if import_statement in self.required_import_paths:
            return
        self.required_import_paths.append(import_statement)

    def _visit_default(self, obj):
        # top-level code is not generated
        return obj

    def visit_CodeElementFunction(self, elm: CodeElementFunction):
        self.parse_functions(elm)
        return super().visit_CodeElementFunction(elm)

    def visit_CodeBlock(self, elm: CodeBlock):
        self.parse_imports(elm)
        return super().visit_CodeBlock(elm)
