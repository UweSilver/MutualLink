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

    comments = {}
    for token in translation_unit.cursor.get_tokens():
        if token.kind == TokenKind.COMMENT:
            line_number = token.location.line
            comment = token.spelling

            comments[line_number] = comment

    functions = []
    for child in translation_unit.cursor.get_children():

        if child.kind == CursorKind.CLASS_DECL:
            filepath = child.location.file.name
            filename = os.path.basename(filepath)

            if filename != input_filename:
                continue

            class_name = child.spelling
            print(class_name)
            print(child.get_fields().spelling)
            continue

        if child.kind != CursorKind.FUNCTION_DECL:
            continue

        if child.location.file is None:
            continue

        filepath = child.location.file.name
        filename = os.path.basename(filepath)

        if filename != input_filename:
            continue

        function_name = child.spelling
        return_type = child.result_type.spelling

        line_number = child.location.line
        comment = comments.get(line_number, "")

        params = []
        for param in child.get_arguments():
            param_name = param.spelling
            param_type = param.type.spelling

            params.append({
                "name": param_name,
                "type": param_type
            })

        functions.append({
            "name": function_name,
            "return_type": return_type,
            "params": params,
            "filename": filename,
            "line_number": line_number,
            "comment": comment
        })

    print(json.dumps(functions, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
