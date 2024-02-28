import argparse
import json
import os

from clang.cindex import CursorKind, Index, TokenKind
import clang

def main():
    clang.cindex.Config.set_library_path('C:/Apps/Clang/LLVM/bin')

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Input file")
    args = parser.parse_args()

    input_filename = os.path.basename(args.filename)

    index = Index.create()

    translation_unit = index.parse(args.filename, args=['-x', 'c++'])

    namespace = []
    classes = {}
    def search_namespace(cursor):
        if cursor.kind == CursorKind.NAMESPACE:
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
                "public_methods": [method.spelling for method in cursor.get_children() if method.kind == CursorKind.CXX_METHOD and method.access_specifier == CursorKind.CXX_PUBLIC],
                "protected_methods": [method.spelling for method in cursor.get_children() if method.kind == CursorKind.CXX_METHOD and method.access_specifier == CursorKind.CXX_PROTECTED],
                "private_methods": [method.spelling for method in cursor.get_children() if method.kind == CursorKind.CXX_METHOD and method.access_specifier == CursorKind.CXX_PRIVATE],
            }


    for cursor in translation_unit.cursor.get_children():
        search_namespace(cursor)

    export_classes = {}
    for class_name, class_info in classes.items():
        if "ExportClass" in class_info["base_classes"]:
            export_classes[class_name] = class_info

    print(json.dumps(export_classes, indent=4, ensure_ascii=False))

    comments = {}
    for token in translation_unit.cursor.get_tokens():
        if token.kind == TokenKind.COMMENT:
            line_number = token.location.line
            comment = token.spelling

            comments[line_number] = comment

    # classes = {}
    # for child in translation_unit.cursor.get_children():
    #     if child.kind != CursorKind.CLASS_DECL:
    #         continue

    #     base_classes = []
    #     for base in child.get_children():
    #         if base.kind != CursorKind.CXX_BASE_SPECIFIER:
    #             continue

    #         base_classes.append(base.get_definition().spelling)

    #     classes[child.spelling] = {
    #         "filename": child.location.file.name,
    #         "line_number": child.location.line,
    #         "base_classes": base_classes,
    #         }

    # print(json.dumps(classes, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
