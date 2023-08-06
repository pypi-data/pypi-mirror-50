import pytest

import pandas as pd

from seeq import spy

from . import test_common

from .. import _common


def setup_module():
    test_common.login()


@pytest.mark.system
def test_simple_search():
    search_results = spy.search({
        'Name': 'Area A_Temper'
    })

    assert len(search_results) == 1

    search_results = spy.search(pd.DataFrame([{
        'Name': 'Area A_Temper'
    }]))

    # Nothing will be returned because we use a equal-to comparison when a DataFrame is passed in
    assert len(search_results) == 0

    search_results = spy.search(pd.DataFrame([{
        'Name': 'Area A_Temperature'
    }]))

    assert len(search_results) == 1


@pytest.mark.system
def test_type_search():
    search_results = spy.search({
        'Datasource Class': 'Time Series CSV Files',
        'Type': 'Signal'
    })

    assert 150 < len(search_results) < 200

    datasource_names = set(search_results['Datasource Name'].tolist())
    assert len(datasource_names) == 1
    assert datasource_names.pop() == 'Example Data'

    types = set(search_results['Type'].tolist())
    assert len(types) == 1
    assert types.pop() == 'StoredSignal'

    search_results = spy.search({
        'Datasource Class': 'Time Series CSV Files',
        'Type': 'Condition'
    })

    assert len(search_results) == 0

    search_results = spy.search({
        'Datasource Class': 'Time Series CSV Files',
        'Type': 'Scalar'
    })

    assert len(search_results) == 0


@pytest.mark.system
def test_path_search():
    with pytest.raises(RuntimeError):
        spy.search({
            'Path': 'Non-existent >> Path'
        })

    search_results = spy.search({
        'Path': 'Example >> Cooling Tower 1'
    })

    assert 40 < len(search_results) < 60


@pytest.mark.system
def test_datasource_name_search():
    with pytest.raises(RuntimeError):
        spy.search({
            'Datasource Name': 'Non-existent'
        })

    search_results = spy.search({
        'Datasource Name': 'Example Data'
    })

    assert 150 < len(search_results) < 200


@pytest.mark.system
def test_search_pagination():
    original_page_size = _common.DEFAULT_SEARCH_PAGE_SIZE
    try:
        _common.DEFAULT_SEARCH_PAGE_SIZE = 2
        search_results = spy.search({
            'Name': 'Area A_*'
        })

        assert len(search_results) == 6

    finally:
        _common.DEFAULT_SEARCH_PAGE_SIZE = original_page_size
