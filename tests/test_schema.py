import typing

import pytest

import middle


def test_mixed_schema():
    class TestModel(middle.Model):
        __looks_reserved__: str
        name = {"type": str}
        surname: str = middle.field()
        age: int
        hobby = middle.field(type=typing.List[str])

    inst = TestModel(name="my", surname="model", age=1, hobby=["coding"])
    assert isinstance(inst, TestModel)


def test_init_not_available():
    class TestModel(middle.Model):
        __attr_s_kwargs__ = {"init": False, "cmp": True}
        name: str

    inst = TestModel(name="foo")
    inst2 = TestModel(name="foo")
    assert isinstance(inst, TestModel)
    assert isinstance(inst2, TestModel)
    assert inst == inst2

    class AnotherModel(middle.Model):
        name: str

    another_inst = AnotherModel(name="foo")
    another_inst2 = AnotherModel(name="foo")

    assert another_inst != another_inst2


def test_constructor():
    class TestObj:
        def __init__(self):
            self.name = "foo"
            self.age = 42
            self.result = 3.14

    class TestModel(middle.Model):
        name: str
        age: int

    with pytest.raises(TypeError):
        TestModel(None)

    with pytest.raises(TypeError):
        TestModel("name")

    with pytest.raises(TypeError):
        TestModel(42)

    with pytest.raises(TypeError):
        TestModel(4.2)

    with pytest.raises(TypeError):
        TestModel(True)

    with pytest.raises(TypeError):
        TestModel(["name", 42])

    inst = TestModel(TestObj())
    assert inst.name == "foo"
    assert inst.age == 42

    with pytest.raises(AttributeError):
        inst.result

    data = {"name": "bar", "age": 21}
    inst2 = TestModel(data)
    inst3 = TestModel(**data)

    assert isinstance(inst2, TestModel)
    assert inst2.name == "bar"
    assert inst2.age == 21

    assert isinstance(inst3, TestModel)
    assert inst3.name == "bar"
    assert inst3.age == 21


def test_invalid_models():
    with pytest.raises(TypeError):

        class TestModel(middle.Model):
            age = {"useless": "information"}

    # the following tests should not raise exceptions

    class AnotherModel(middle.Model):
        age: None

    class AndAnotherModel(middle.Model):
        age = {"type": None}

    class SomeAnotherModel(middle.Model):
        age: None = middle.field()
