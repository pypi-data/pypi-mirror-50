"""A scanner generator that uses Jinja2 templates."""
import argparse
import sys
import jinja2
import rnd

scanners = []

def symbols(left: str, right: str = None) -> rnd.ExprSymbols:
    """Create range of symbols from characters."""
    if right is None:
        right = left
    left, right = ord(left), ord(right)
    return rnd.ExprSymbols(left, right)

def isymbols(left: int, right: int = None) -> rnd.ExprSymbols:
    """Create range of symbols from integers."""
    if right is None:
        right = left
    return rnd.ExprSymbols(left, right)

def optional(expr: rnd.ExprSymbols or rnd.Expr):
    """Return union of expr with empty symbol."""
    return expr.union(symbols('\0'))

def token(name):
    """Register scanner."""
    def decorator(func):
        def wrapper():
            expr = func()
            dfa = rnd.convert(expr)
            expr.destroy()
            dfa.token = name
            return dfa
        scanners.append(wrapper())
        return wrapper
    return decorator

def generate(entrypoint="", directory=""):
    """Generate code from templates."""
    def get_args(args):
        description = "Generate scanner using jinja2 templates."
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("entrypoint", help="filename of template entrypoint")
        parser.add_argument("-d", default="", dest="directory",
                            help="path to templates directory")
        return parser.parse_args(args)

    def generate_code():
        loader = jinja2.FileSystemLoader(directory)
        env = jinja2.Environment(loader=loader, line_statement_prefix="##")
        template = env.get_template(entrypoint)
        return template.render(scanners=scanners)

    args = sys.argv[1:]
    if entrypoint:
        args.append(entrypoint)
    if directory:
        args.extend(["-d", directory])
    args = get_args(args)
    if args.entrypoint:
        entrypoint = args.entrypoint
    if args.directory:
        directory = args.directory

    try:
        output = generate_code()
        print(output)
    except jinja2.exceptions.TemplateNotFound:
        print("scangen: Template not found:", entrypoint)

name = "scangen"

if __name__ == "__main__":
    generate()
