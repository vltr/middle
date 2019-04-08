import ast
import binascii
import os

from functools import lru_cache

from ..exceptions import ValidationError
from .utils import build_base_body, build_exception_message


def _build_min_properties(min_properties):
    msg = "'{}' has no enough properties of {}"
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id="total_size", ctx=ast.Load()),
            ops=[ast.Lt()],
            comparators=[ast.Num(n=min_properties)],
        ),
        body=[build_exception_message(msg, ast.Num(n=min_properties))],
        orelse=[],
    )


def _build_max_properties(max_properties):
    msg = "'{}' has more properties than the limit of {}"
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id="total_size", ctx=ast.Load()),
            ops=[ast.Gt()],
            comparators=[ast.Num(n=max_properties)],
        ),
        body=[build_exception_message(msg, ast.Num(n=max_properties))],
        orelse=[],
    )


@lru_cache(maxsize=2048, typed=True)
def build_dict_validator(min_properties=None, max_properties=None):
    fn_name = "validate_dict_{}".format(
        str(binascii.hexlify(os.urandom(6)), "utf-8")
    )
    fn_body = build_base_body()
    if_body = []
    if min_properties is not None or max_properties is not None:
        if_body.append(
            ast.Assign(
                targets=[ast.Name(id="total_size", ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="len", ctx=ast.Load()),
                    args=[ast.Name(id="value", ctx=ast.Load())],
                    keywords=[],
                ),
            )
        )
    if min_properties is not None:
        if_body.append(_build_min_properties(min_properties))
    if max_properties is not None:
        if_body.append(_build_max_properties(max_properties))
    if if_body:
        fn_body.append(
            ast.If(
                test=ast.Compare(
                    left=ast.Name(id="value", ctx=ast.Load()),
                    ops=[ast.IsNot()],
                    comparators=[ast.NameConstant(value=None)],
                ),
                body=if_body,
                orelse=[],
            )
        )
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
