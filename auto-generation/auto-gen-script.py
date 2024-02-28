import argparse
import json
import os

from clang.cindex import CursorKind, Index, TokenKind
import clang

def get_class_tree(input_filenames):
    classes = {}
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
                    for param in method.get_children():
                        print(param.spelling, param.kind)
                    classes[cursor.spelling]["methods"][method.spelling] = [param.spelling for param in method.get_children() if param.kind == CursorKind.PARM_DECL]

        for cursor in translation_unit.cursor.get_children():
            search_namespace(cursor)
    return classes

def get_exporter_code(classes):
    code = ""
    
    extern = \
        ("#if defined(DYNAMIC_LINK)\n"
        "extern \"C\" __declspec(dllexport)\n"
        "#endif\n")
    
    for class_name, class_info in classes.items():
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

    classes = get_class_tree([input_filename])
    
    print(json.dumps(classes, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
