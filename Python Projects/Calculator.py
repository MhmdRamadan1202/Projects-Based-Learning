"""
Calculator (safe, single-file)
--------------------------------
A simple calculator that evaluates math expressions safely (no eval).
- Supports: +, -, *, /, //, %, **, parentheses, unary +/-, and comparisons (==, !=, <, <=, >, >=)
- Functions: abs, round, sqrt, sin, cos, tan, log, log10, exp, pow, max, min
- Constants: pi, e, tau
- Variables: You can assign variables: x = 2, y = 3; then use x*y + 5
"""

import ast
import operator as op
import math
import sys
from typing import Any, Dict

# Supported operators mapping
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

_CMP_OPS = {
    ast.Eq: op.eq,
    ast.NotEq: op.ne,
    ast.Lt: op.lt,
    ast.LtE: op.le,
    ast.Gt: op.gt,
    ast.GtE: op.ge,
}

_ALLOWED_FUNCS = {
    "abs": abs,
    "round": round,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pow": pow,
    "max": max,
    "min": min,
}

_ALLOWED_CONSTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}

class SafeEval(ast.NodeVisitor):
    def __init__(self, variables: Dict[str, Any] | None = None):
        self.vars = {} if variables is None else dict(variables)

    def eval(self, expr: str) -> Any:
        try:
            tree = ast.parse(expr, mode="exec")
        except SyntaxError as e:
            raise ValueError(f"Syntax error: {e.msg}") from None
        # Allow either a single expression or assignment statements
        if not tree.body:
            return None
        if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
            return self._eval_expr(tree.body[0].value)
        else:
            # permit simple assignments: a = <expr>, possibly multiple lines separated by semicolons/newlines
            last_value = None
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    if len(node.targets) != 1:
                        raise ValueError("Only single-target assignment is allowed.")
                    target = node.targets[0]
                    if not isinstance(target, ast.Name):
                        raise ValueError("Can only assign to variable names.")
                    value = self._eval_expr(node.value)
                    self.vars[target.id] = value
                    last_value = value
                elif isinstance(node, ast.Expr):
                    last_value = self._eval_expr(node.value)
                else:
                    raise ValueError("Only expressions and simple assignments are allowed.")
            return last_value

    def _eval_expr(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):  # numbers, booleans
            if isinstance(node.value, (int, float, bool)):
                return node.value
            raise ValueError("Only numeric and boolean constants are allowed.")
        if isinstance(node, ast.Name):
            if node.id in self.vars:
                return self.vars[node.id]
            if node.id in _ALLOWED_CONSTS:
                return _ALLOWED_CONSTS[node.id]
            raise ValueError(f"Unknown variable or constant: {node.id}")
        if isinstance(node, ast.BinOp):
            left = self._eval_expr(node.left)
            right = self._eval_expr(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                return _BIN_OPS[op_type](left, right)
            raise ValueError(f"Operator not allowed: {op_type.__name__}")
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_expr(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                return _UNARY_OPS[op_type](operand)
            raise ValueError(f"Unary operator not allowed: {op_type.__name__}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct function calls are allowed.")
            func_name = node.func.id
            if func_name not in _ALLOWED_FUNCS:
                raise ValueError(f"Function not allowed: {func_name}")
            args = [self._eval_expr(a) for a in node.args]
            if node.keywords:
                raise ValueError("Keyword arguments are not allowed.")
            return _ALLOWED_FUNCS[func_name](*args)
        if isinstance(node, ast.Compare):
            if len(node.ops) != 1 or len(node.comparators) != 1:
                # Support chained comparisons by folding
                left_val = self._eval_expr(node.left)
                result = True
                current_left = left_val
                for op_node, comp_node in zip(node.ops, node.comparators):
                    right_val = self._eval_expr(comp_node)
                    op_type = type(op_node)
                    if op_type not in _CMP_OPS:
                        raise ValueError("Comparison operator not allowed.")
                    if not _CMP_OPS[op_type](current_left, right_val):
                        result = False
                        break
                    current_left = right_val
                return result
            # Simple binary comparison
            left = self._eval_expr(node.left)
            right = self._eval_expr(node.comparators[0])
            op_type = type(node.ops[0])
            if op_type in _CMP_OPS:
                return _CMP_OPS[op_type](left, right)
            raise ValueError("Comparison operator not allowed.")
        if isinstance(node, ast.BoolOp):
            # handle 'and'/'or'
            if isinstance(node.op, ast.And):
                for v in node.values:
                    if not self._eval_expr(v):
                        return False
                return True
            if isinstance(node.op, ast.Or):
                for v in node.values:
                    if self._eval_expr(v):
                        return True
                return False
            raise ValueError("Boolean operator not allowed.")
        if isinstance(node, ast.IfExp):
            return self._eval_expr(node.body) if self._eval_expr(node.test) else self._eval_expr(node.orelse)
        if isinstance(node, ast.Tuple):
            return tuple(self._eval_expr(elt) for elt in node.elts)
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

HELP_TEXT = __doc__

def repl() -> None:
    evaluator = SafeEval()
    print("Safe Calculator — type :help for help, :quit to exit.")
    while True:
        try:
            line = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not line:
            continue
        if line.startswith(":"):
            cmd = line[1:].strip().lower()
            if cmd == "help":
                print(HELP_TEXT)
            elif cmd == "quit":
                print("Bye!")
                break
            elif cmd == "vars":
                if evaluator.vars:
                    for k, v in sorted(evaluator.vars.items()):
                        print(f"{k} = {v}")
                else:
                    print("(no variables)")
            elif cmd == "clear":
                evaluator.vars.clear()
                print("Variables cleared.")
            else:
                print("Unknown command. Try :help")
            continue
        try:
            result = evaluator.eval(line)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Evaluate a single expression passed as argument
        expr = " ".join(sys.argv[1:])
        try:
            value = SafeEval().eval(expr)
            if value is not None:
                print(value)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        repl()
