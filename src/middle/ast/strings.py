import ast
import binascii
import os

from functools import lru_cache

from ..exceptions import ValidationError
from .utils import build_base_body, build_exception_message


def _build_min_length(min_length):
    msg = "'{}' must have a minimum length of {} chars"
    return ast.If(
        test=ast.Compare(
            left=ast.Call(
                func=ast.Name(id="len", ctx=ast.Load()),
                args=[ast.Name(id="value", ctx=ast.Load())],
                keywords=[],
            ),
            ops=[ast.Lt()],
            comparators=[ast.Num(n=min_length)],
        ),
        body=[build_exception_message(msg, ast.Num(n=min_length))],
        orelse=[],
    )


def _build_max_length(max_length):
    msg = "'{}' must have a maximum length of {} chars"
    return ast.If(
        test=ast.Compare(
            left=ast.Call(
                func=ast.Name(id="len", ctx=ast.Load()),
                args=[ast.Name(id="value", ctx=ast.Load())],
                keywords=[],
            ),
            ops=[ast.Gt()],
            comparators=[ast.Num(n=max_length)],
        ),
        body=[build_exception_message(msg, ast.Num(n=max_length))],
        orelse=[],
    )


def _build_pattern_match(pattern):
    msg = "'{}' did not match the given pattern: '{}'"
    return [
        ast.Assign(
            targets=[ast.Name(id="match", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="strp", ctx=ast.Load()),
                    attr="match",
                    ctx=ast.Load(),
                ),
                args=[ast.Name(id="value", ctx=ast.Load())],
                keywords=[],
            ),
        ),
        ast.If(
            test=ast.Compare(
                left=ast.Name(id="match", ctx=ast.Load()),
                ops=[ast.Is()],
                comparators=[ast.NameConstant(value=None)],
            ),
            body=[build_exception_message(msg, ast.Str(s=pattern))],
            orelse=[],
        ),
    ]


@lru_cache(maxsize=2048, typed=True)
def build_string_validator(min_length=None, max_length=None, re_instance=None):
    fn_name = "validate_string_{}".format(
        str(binascii.hexlify(os.urandom(6)), "utf-8")
    )
    fn_body = build_base_body()
    if min_length is not None:
        fn_body.append(_build_min_length(min_length))
    if max_length is not None:
        fn_body.append(_build_max_length(max_length))
    if re_instance is not None:
        fn_body.extend(_build_pattern_match(re_instance.pattern))
    fn_def = ast.FunctionDef(
        name=fn_name,
        args=ast.arguments(
            args=[
                ast.arg(arg="attr", annotation=None),
                ast.arg(arg="value", annotation=None),
            ],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=fn_body,
        decorator_list=[],
        returns=None,
    )

    tree = ast.Module(body=[fn_def])
    ast.fix_missing_locations(tree)
    scope = {"ValidationError": ValidationError, "strp": re_instance}
    exec(compile(tree, filename="", mode="exec"), scope)
    return scope[fn_name]
