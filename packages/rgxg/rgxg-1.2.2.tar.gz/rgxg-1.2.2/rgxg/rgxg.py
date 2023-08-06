from . import (
    alternation,
    exrex,
    _range
)
import argparse

_sorthand = {
    "generate": exrex.generate,
    "count": exrex.count,
    "getone": exrex.getone,
    "simplify": exrex.simplify,
    "alternation": alternation.match,
}

def main():
    parser = argparse.ArgumentParser(description="ReGular eXpression Generator")
    sub = parser.add_subparsers(dest="sub")

    gen = sub.add_parser("generate", help="Generates all matching strings to a given regular expression")
    gen.add_argument("s", metavar="regex", nargs="+", help="Regular Expression")

    count = sub.add_parser("count", help="Counts all matching strings to a given regular expression")
    count.add_argument("s", metavar="regex", nargs="+", help="Regular Expression")

    getone = sub.add_parser("getone", help="Returns a random matching string to a given regular expression")
    getone.add_argument("s", metavar="regex", nargs="+", help="Regular Expression")

    simplify = sub.add_parser("simplify", help="Simplify a regular expression")
    simplify.add_argument("s", metavar="regex", nargs="+", help="Regular Expression")

    alternation = sub.add_parser("alternation", help="Generates one regex from a list of strings")
    alternation.add_argument("s", metavar="strings", nargs="+", help="List of String")

    v_range = sub.add_parser("range", help="Split range to ranges that has its unique pattern")
    v_range.add_argument("--min", default=0, help="Minimal, default 0")
    v_range.add_argument("--max", help="Maximal", required=True)

    arg = parser.parse_args()

    if "s" in arg:
        arg.s = " ".join(arg.s)

    if arg.sub:
        try:
            if arg.sub == "range":
                print(_range.match(arg.min, arg.max))
            else:
                s = _sorthand[arg.sub](arg.s)
                if arg.sub == "generate":
                   for i in s:
                       print(i)
                else:
                    print(s)
        except Exception as e:
            print(str(e))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
