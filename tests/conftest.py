import sys

collect_ignore = []
if sys.version_info[:2] == (3, 5):  # noqa
    collect_ignore.extend(
        [
            "test_middle_simplistic_no_py35.py",
            "test_middle_verbose_no_py35.py",
            "test_model_no_py35.py",
        ]
    )
