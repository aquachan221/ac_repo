# run_caramel.py
import sys
from parser_lexer import tokenize, Parser, Context, evaluate

def run_cml_file(filename):
    ctx = Context()
    try:
        with open(filename, 'r') as f:
            code = f.read()
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse_all()
        for stmt in ast:
            evaluate(stmt, ctx)

        print("\n✨ Variables after execution:")
        for k, v in ctx.vars.items():
            if not k.startswith('_'):
                print(f"  {k} = {v}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print("Runtime Error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_caramel.py <file.cml>")
    else:
        run_cml_file(sys.argv[1])