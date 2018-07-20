import attr


@attr.s(slots=True, hash=True)
class BaseValidator:
    def __call__(self, inst, attr, value):  # noqa
        raise Exception("this method needs to be implemented in a subclass")

    @property
    def descriptor(self):
        return {
            field.name: getattr(self, field.name)
            for field in filter(
                lambda f: f.default != getattr(self, f.name)
                and not f.name.startswith("_"),
                attr.fields(self.__class__),
            )
        }

    @classmethod
    def validator_keys(cls):
        return [f.name for f in attr.fields(cls) if not f.name.startswith("_")]
