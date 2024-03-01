import argparse
import json
import os

from clang.cindex import CursorKind, Index, TokenKind
import clang

def get_class_tree(input_filenames):
    classes = {}
    typealiases = {}
    for input_file in input_filenames:
        index = Index.create()
        translation_unit = index.parse(input_file, args=['-x', 'c++'])

        namespace = []
        def search_namespace(cursor):
            if cursor.kind == CursorKind.NAMESPACE:
                if cursor.spelling != "std":
                    namespace.append(cursor.spelling)
                    for child in cursor.get_children():
                        search_namespace(child)
                    namespace.pop()

            if cursor.kind == CursorKind.CLASS_DECL:
                classes[cursor.spelling] = {
                    "filename": cursor.location.file.name,
                    "line_number": cursor.location.line,
                    "namespace": namespace.copy(),
                    "base_classes": [base.spelling for base in cursor.get_children() if base.kind == CursorKind.CXX_BASE_SPECIFIER],
                    "methods": {},
                    "constructors": [method.spelling for method in cursor.get_children() if method.kind == CursorKind.CONSTRUCTOR],
                    "destructor": [method.spelling for method in cursor.get_children() if method.kind == CursorKind.DESTRUCTOR],
                }
                for method in cursor.get_children():
                    if not method.kind == CursorKind.CXX_METHOD:
                        continue
                    classes[cursor.spelling]["methods"][method.spelling] = {
                        "return_type": method.result_type.spelling,
                        "parameters": {},
                        "access_specifier": method.access_specifier.name,
                    }
                    
                    for c in method.get_children():
                        if c.kind == CursorKind.PARM_DECL:
                            classes[cursor.spelling]["methods"][method.spelling]["parameters"][c.spelling] = c.type.spelling

            if cursor.kind == CursorKind.TYPE_ALIAS_DECL:
                typealiases[cursor.spelling] = {
                    "filename": cursor.location.file.name,
                    "line_number": cursor.location.line,
                    "namespace": namespace.copy(),
                    "type": cursor.underlying_typedef_type.spelling,
                }
        for cursor in translation_unit.cursor.get_children():
            search_namespace(cursor)
    return classes, typealiases

def get_exporter_code(classes):
    code = ""
    
    extern = \
        ("#if defined(DYNAMIC_LINK)\n"
        "extern \"C\" __declspec(dllexport)\n"
        "#endif\n")
    
    
    
    for class_name, class_info in classes.items():
        full_namespace = "_".join(class_info["namespace"])
        # print(full_namespace)

        # constructor
        code += extern
        code += f"void* {full_namespace}_{class_name}_CONSTRUCTOR(\n"
        code += f"{full_namespace}_{class_name}** self\n"
        code += "){\n"
        # allocate memory
        # add reference count
        code += "}\n\n"

        # destructor
        code += extern
        code += f"void {full_namespace}_{class_name}_DESTRUCTOR(\n"
        code += f"{full_namespace}_{class_name}** self\n"
        code += "){\n"
        # release memory
        # subtract reference count
        code += "}\n\n"

        # methods
        for method_name, method_info in class_info["methods"].items():
            code += extern
            code += f"{method_info['return_type']} {full_namespace}_{class_name}_{method_name}(\n"
            self_param = {"self": f"{full_namespace}_{class_name}**"}
            params = self_param | method_info["parameters"]
            param_code = " ,".join([f"{param_type} {param_name}" for param_name, param_type in params.items()])
            code += f"{param_code}\n"
            code += "){\n"
            # call the method
            code += "}\n\n"
        pass
    return code

def get_importer_code(classes):
    
    pass

def main():
    # Set the path to the LLVM shared library
    clang.cindex.Config.set_library_path('C:/Apps/Clang/LLVM/bin')

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Input file")
    args = parser.parse_args()

    input_filename = os.path.basename(args.filename)

    classes, typealiases = get_class_tree([input_filename])
    
    # print(json.dumps(classes, indent=4, ensure_ascii=False))
    # print(json.dumps(typealiases, indent=4, ensure_ascii=False))
    print(get_exporter_code(classes))

if __name__ == "__main__":
    main()
