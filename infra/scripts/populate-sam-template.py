#!/usr/bin/env python3

import argparse
import os
import sys

CLOUDFRONT_FUNCTION_PLACEHOLDER = "__INLINE_CLOUDFRONT_CODE__"
INDENT = 8

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cf-auth-function", required=True)
    parser.add_argument("-t", "--template", default="template.yaml")
    parser.add_argument("-o", "--output", default="template.inlined.yaml")
    return parser.parse_args()

def main():
    args = get_arguments()

    if not os.path.exists(args.template):
        print(f"Error: Cannot find {args.template}")
        sys.exit(1)

    if not os.path.exists(args.cf_auth_function):
        print(f"Error: Cannot find {args.cf_auth_function}")
        sys.exit(1)

    with open(args.cf_auth_function, 'r') as js_file:
        js_code = js_file.readlines()

    indented_code = '\n'.join(
        (' ' * INDENT + line if line.strip() != '' and line != js_code[0] else line)
        for line in js_code
    )

    with open(args.template, 'r') as template_file:
        template = template_file.read()

    updated_template = template.replace(CLOUDFRONT_FUNCTION_PLACEHOLDER, indented_code)

    with open(args.output, 'w') as out_file:
        out_file.write(updated_template)

    print(f"Inlined template written to {args.output}")


if __name__ == "__main__":
    main()