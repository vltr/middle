import sys

IS_PY37 = sys.version_info >= (3, 7)

if IS_PY37:
    from typing import _GenericAlias as GenericType
else:
    from typing import GenericMeta as GenericType


__all__ = ("IS_PY37", "GenericType",)
