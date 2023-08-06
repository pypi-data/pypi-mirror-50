import pytest

import pandas as pd

from seeq import spy

from . import test_common


@pytest.mark.system
def test_push_signal():
    test_common.login()

    push_df = pd.DataFrame(pd.Series([
        1,
        2,
        3
    ], index=[
        pd.to_datetime('2019-01-01'),
        pd.to_datetime('2019-01-02'),
        pd.to_datetime('2019-01-03')
    ]), columns=['My Signal'])

    spy.push(push_df)
