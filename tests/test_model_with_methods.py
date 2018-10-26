import inspect
import typing

import middle


def test_model_with_methods_and_properties():
    class TestModel(middle.Model):
        name = middle.field(type=str)
        surname = middle.field(type=str)
        age = middle.field(type=int)
        hobby = middle.field(type=typing.List[str])

        def test(self):
            return "test"

        @property
        def age_plus_10(self):
            return self.age + 10

        @age_plus_10.setter
        def age_plus_10(self, value):
            self.age = value - 10

        @classmethod
        def something(cls):
            return 20

        @staticmethod
        def anotherthing():
            return 42

        async def hello(self):  # noqa
            return "world"

    inst = TestModel(name="my", surname="model", age=1, hobby=["coding"])
    assert isinstance(inst, TestModel)
    assert inst.test() == "test"
    assert inst.age_plus_10 == 11
    assert inst.something() == 20
    assert inst.anotherthing() == 42
    assert inspect.isawaitable(inst.hello())

    inst.age_plus_10 = 20

    assert inst.age_plus_10 == 20
