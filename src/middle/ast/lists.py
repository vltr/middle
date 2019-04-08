import ast
import binascii
import os

from functools import lru_cache

from ..exceptions import ValidationError
from .utils import build_base_body, build_exception_message


def _build_min_items(min_items):
    msg = "'{}' has no enough items of {}"
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id="total_size", ctx=ast.Load()),
            ops=[ast.Lt()],
            comparators=[ast.Num(n=min_items)],
        ),
        body=[build_exception_message(msg, ast.Num(n=min_items))],
        orelse=[],
    )


def _build_max_items(max_items):
    msg = "'{}' has more items than the limit of {}"
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id="total_size", ctx=ast.Load()),
            ops=[ast.Gt()],
            comparators=[ast.Num(n=max_items)],
        ),
        body=[build_exception_message(msg, ast.Num(n=max_items))],
        orelse=[],
    )


def _build_unique_items():
    msg = "'{}' must only have unique items"
    return ast.If(
        test=ast.Call(
            func=ast.Name(id="isinstance", ctx=ast.Load()),
            args=[
                ast.Name(id="value", ctx=ast.Load()),
                ast.Name(id="list", ctx=ast.Load()),
            ],
            keywords=[],
        ),
        body=[
            ast.For(
                target=ast.Name(id="v", ctx=ast.Store()),
                iter=ast.Name(id="value", ctx=ast.Load()),
                body=[
                    ast.If(
                        test=ast.Compare(
                            left=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="value", ctx=ast.Load()),
                                    attr="count",
                                    ctx=ast.Load(),
                                ),
                                args=[ast.Name(id="v", ctx=ast.Load())],
                                keywords=[],
                            ),
                            ops=[ast.Gt()],
                            comparators=[ast.Num(n=1)],
                        ),
                        body=[build_exception_message(msg)],
                        orelse=[],
                    )
                ],
                orelse=[],
            )
        ],
        orelse=[],
    )


@lru_cache(maxsize=2048, typed=True)
def build_list_validator(min_items=None, max_items=None, unique_items=False):
    fn_name = "validate_list_{}".format(
        str(binascii.hexlify(os.urandom(6)), "utf-8")
    )
    fn_body = build_base_body()
    if min_items is not None or max_items is not None:
        fn_body.append(
            ast.Assign(
                targets=[ast.Name(id="total_size", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="len", ctx=ast.Load()),
                    args=[ast.Name(id="value", ctx=ast.Load())],
                    keywords=[],
                ),
            )
        )
    if min_items is not None:
        fn_body.append(_build_min_items(min_items))
    if max_items is not None:
        fn_body.append(_build_max_items(max_items))
    if unique_items:
        fn_body.append(_build_unique_items())
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
    scope = {"ValidationError": ValidationError}
    exec(compile(tree, filename="", mode="exec"), scope)
    return scope[fn_name]
