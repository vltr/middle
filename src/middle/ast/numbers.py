import ast
import binascii
import os

from decimal import Decimal
from functools import lru_cache

from ..exceptions import ValidationError
from .utils import build_base_body, build_exception_message


def _build_minimum(minimum, exclusive=False):
    msg = "'{}' must have a minimum value of {}"
    op = [ast.Lt()]
    if exclusive:
        msg = "'{}' must have a (exclusive) minimum value of {}"
        op = [ast.LtE()]
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id="value", ctx=ast.Load()),
            ops=op,
            comparators=[ast.Num(n=minimum)],
        ),
        body=[build_exception_message(msg, ast.Num(n=minimum))],
        orelse=[],
    )


def _build_maximum(maximum, exclusive=False):
    msg = "'{}' must have a maximum value of {}"
    op = [ast.Gt()]
    if exclusive:
        msg = "'{}' must have a (exclusive) maximum value of {}"
        op = [ast.GtE()]
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id="value", ctx=ast.Load()),
            ops=op,
            comparators=[ast.Num(n=maximum)],
        ),
        body=[build_exception_message(msg, ast.Num(n=maximum))],
        orelse=[],
    )


def _build_multiple_of_float(multiple_of, msg):
    return ast.If(
        test=ast.Compare(
            left=ast.Call(
                func=ast.Name(id="float", ctx=ast.Load()),
                args=[
                    ast.BinOp(
                        left=ast.Call(
                            func=ast.Name(id="Decimal", ctx=ast.Load()),
                            args=[
                                ast.Call(
                                    func=ast.Name(id="str", ctx=ast.Load()),
                                    args=[
                                        ast.Name(id="value", ctx=ast.Load())
                                    ],
                                    keywords=[],
                                )
                            ],
                            keywords=[],
                        ),
                        op=ast.Mod(),
                        right=ast.Call(
                            func=ast.Name(id="Decimal", ctx=ast.Load()),
                            args=[
                                ast.Call(
                                    func=ast.Name(id="str", ctx=ast.Load()),
                                    args=[ast.Num(n=multiple_of)],
                                    keywords=[],
                                )
                            ],
                            keywords=[],
                        ),
                    )
                ],
                keywords=[],
            ),
            ops=[ast.NotEq()],
            comparators=[ast.Num(n=0.0)],
        ),
        body=[build_exception_message(msg, ast.Num(n=multiple_of))],
        orelse=[],
    )


def _build_multiple_of_int(multiple_of, msg):
    return ast.If(
        test=ast.Compare(
            left=ast.BinOp(
                left=ast.Name(id="value", ctx=ast.Load()),
                op=ast.Mod(),
                right=ast.Num(n=multiple_of),
            ),
            ops=[ast.NotEq()],
            comparators=[ast.Num(n=0)],
        ),
        body=[build_exception_message(msg, ast.Num(n=multiple_of))],
        orelse=[],
    )


def _build_multiple_of(multiple_of):
    msg = "'{}' must be multiple of {}"
    if isinstance(multiple_of, float):
        return _build_multiple_of_float(multiple_of, msg)
    return _build_multiple_of_int(multiple_of, msg)


@lru_cache(maxsize=2048, typed=True)
def build_number_validator(
    minimum=None,
    maximum=None,
    multiple_of=None,
    exclusive_minimum=False,
    exclusive_maximum=False,
):
    fn_name = "validate_number_{}".format(
        str(binascii.hexlify(os.urandom(6)), "utf-8")
    )
    fn_body = build_base_body()
    if minimum is not None:
        fn_body.append(_build_minimum(minimum, exclusive_minimum))
    if maximum is not None:
        fn_body.append(_build_maximum(maximum, exclusive_maximum))
    if multiple_of is not None:
        fn_body.append(_build_multiple_of(multiple_of))
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
    scope = {"Decimal": Decimal, "ValidationError": ValidationError}
    exec(compile(tree, filename="", mode="exec"), scope)
    return scope[fn_name]
