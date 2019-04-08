import ast


def build_exception_message(msg, *value_ast):
    return ast.Raise(
        exc=ast.Call(
            func=ast.Name(id="ValidationError", ctx=ast.Load()),
            args=[
                ast.Call(
                    func=ast.Attribute(
                        value=ast.Str(s=msg), attr="format", ctx=ast.Load()
                    ),
                    args=[
                        ast.Attribute(
                            value=ast.Name(id="attr", ctx=ast.Load()),
                            attr="name",
                            ctx=ast.Load(),
                        ),
                        *value_ast,
                    ],
                    keywords=[],
                )
            ],
            keywords=[],
        ),
        cause=None,
    )


def build_base_body():
    return [
        ast.If(
            test=ast.BoolOp(
                op=ast.And(),
                values=[
                    ast.Compare(
                        left=ast.Attribute(
                            value=ast.Name(id="attr", ctx=ast.Load()),
                            attr="default",
                            ctx=ast.Load(),
                        ),
                        ops=[ast.Is()],
                        comparators=[ast.NameConstant(value=None)],
                    ),
                    ast.Compare(
                        left=ast.Name(id="value", ctx=ast.Load()),
                        ops=[ast.Is()],
                        comparators=[ast.NameConstant(value=None)],
                    ),
                ],
            ),
            body=[ast.Return(value=None)],
            orelse=[],
        )
    ]
