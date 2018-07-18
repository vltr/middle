import sys
from datetime import datetime
from datetime import timezone

import pytest

# ------------------------- #
# fixtures


@pytest.fixture
def local_tz():
    return datetime.now(timezone.utc).astimezone().tzinfo


# ------------------------- #
# ignores for Python 3.5


collect_ignore = []
if sys.version_info[:2] == (3, 5):  # noqa
    collect_ignore.extend(
        [
            "test_middle_simplistic_no_py35.py",
            "test_middle_verbose_no_py35.py",
            "test_model_no_py35.py",
        ]
    )
