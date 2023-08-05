import ast
import astor
import magma.ast_utils as ast_utils
import types
import collections


def flatten(l):
    """
    https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
    """
    for el in l:
        if isinstance(el, collections.Iterable) and \
                not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


class Channel:
    def __init__(self, type_):
        self.type_ = type_
        self.direction = None

    def qualify(self, direction):
        self.direction = direction
        return self


class Counter:
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step

    def __repr__(self):
        return f"Counter({self.start}, {self.end}, {self.step})"


def collect_IO(tree, defn_env):
    IO = {}
    for arg in tree.args.args:
        IO[arg.arg] = eval(astor.to_source(arg.annotation).rstrip(), defn_env)
    return IO


def transform_for_loops_to_counters(tree):
    counters = {}

    class Transformer(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            node = self.generic_visit(node)
            node.body = flatten(node.body)
            return node

        def visit_For(self, node):
            assert isinstance(node.iter, ast.Call) and \
                isinstance(node.iter.func, ast.Name) and \
                node.iter.func.id == "range" and \
                isinstance(node.target, ast.Name), \
                f"Found unsupported for loop {ast.dump(ndoe)}"
            assert not node.iter.keywords, "kwargs not implemented"
            if len(node.iter.args) == 1:
                counters[node.target.id] = Counter(0, node.iter.args[0].n, 1)
            else:
                assert False, "Case not implemented"
            node.body = flatten(self.visit(s) for s in node.body)
            return node.body

    return Transformer().visit(tree), counters



@ast_utils.inspect_enclosing_env
def coroutine(defn_env: dict, fn: types.FunctionType):
    tree = ast_utils.get_func_ast(fn)
    IO = collect_IO(tree, defn_env)
    tree, counters = transform_for_loops_to_counters(tree)
    print(IO)
    print(counters)
    print(astor.to_source(tree))
    assert False
