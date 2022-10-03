from starkware.cairo.lang.compiler.ast.code_elements import CodeElementFunction, CodeBlock, CodeElementImport
from starkware.cairo.lang.compiler.ast.visitor import Visitor

from starknet_interface_generator.utils import to_camel_case


class Generator(Visitor):
    """
    Generates an interface from a Cairo contract.
    """

    def __init__(self, contract_dir: str, contract_name: str):
        super().__init__()
        self.contract_dir = contract_dir
        self.contract_name = contract_name
        self.imports = {}
        self.required_import_paths = []
        self.functions = ""

    def generate_contract_interface(self, module):
        self.visit(module)
        interface = \
            "%lang starknet\n\n" + \
            "\n".join(self.required_import_paths) + "\n\n" \
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

    def parse_function_signature(self, elm: CodeElementFunction):
        # We only visit proper functions decorated with 'external' or 'view'.
        need_instrumentation = any(decorator.name in [
                                   "external", "view"] for decorator in elm.decorators)

        if not need_instrumentation:
            return

        # func name
        fn_signature = f"func {elm.name}("

        # func arguments
        for i, arg in enumerate(elm.arguments.identifiers):
            arg_type = arg.expr_type.format().replace('*', '')
            # non-felt types need to be imported
            if arg_type != 'felt':
                self.add_import_path(arg_type)

            fn_signature += f"{arg.format()}"
            if i != len(elm.arguments.identifiers) - 1:
                fn_signature += ","
        fn_signature += ")"

        # func return values
        if elm.returns != None:
            fn_signature += " -> "
            fn_signature += elm.returns.format()

            # non-felt return types need to be imported
            return_elems = elm.returns.get_children()
            for elem in return_elems:
                type = elem.typ.format().replace('*', '')
                if type != 'felt':
                    self.add_import_path(type)

        fn_signature += "{\n}\n\n"

        self.functions += fn_signature

    def add_import_path(self, arg_type: str):
        # If we have imported types, we need to add the import path to our interface
        # If we use namespace, we want to import the namespace and not the type itself.
        # if the type comes from a namespace, we only import the namespace
        import_name = arg_type.split('.')[0]
        import_path = self.imports.get(
            import_name) or f"{self.contract_dir.replace('/', '.')}.{self.contract_name}"  # this is a bad practice, when the type is directly declared in the contract.
        import_statement = f"from {import_path} import {import_name}"
        if import_statement in self.required_import_paths:
            return
        self.required_import_paths.append(import_statement)

    def _visit_default(self, obj):
        # top-level code is not generated
        return obj

    def visit_CodeElementFunction(self, elm: CodeElementFunction):
        self.parse_function_signature(elm)
        return super().visit_CodeElementFunction(elm)

    def visit_CodeBlock(self, elm: CodeBlock):
        self.parse_imports(elm)
        return super().visit_CodeBlock(elm)
