import pytest

import pandas as pd

from seeq import spy

from . import test_common


@pytest.mark.system
def test_pull_signal():
    test_common.login()

    search_results = spy.search({
        "Path": "Example >> Cooling Tower 1 >> Area A"
    })

    search_results = search_results.loc[
        search_results['Name'].isin(['Compressor Power', 'Temperature', 'Relative Humidity'])]

    spy.pull(search_results, start='2019-01-01', end='2019-03-07', grid='5min', header='Name')


@pytest.mark.system
def test_pull_condition_as_capsules():
    test_common.login()

    search_results = spy.search({
        'Name': 'Area A_Temperature'
    })

    push_result = spy.push(metadata=pd.DataFrame([{
        'Type': 'Condition',
        'Name': 'Hot',
        'Formula': '$a.validValues().valueSearch(isGreaterThan(80))',
        'Formula Parameters': {
            '$a': search_results.iloc[0]
        }
    }]))

    spy.pull(push_result.iloc[0], start='2019-01-01T00:00:00.000Z', end='2019-06-01T00:00:00.000Z')


@pytest.mark.system
def test_pull_condition_as_signal():
    test_common.login()

    search_results = spy.search({
        'Name': 'Area A_Temperature'
    })

    push_result = spy.push(metadata=pd.DataFrame([{
        'Type': 'Condition',
        'Name': 'Hot',
        'Formula': '$a.validValues().valueSearch(isGreaterThan(80))',
        'Formula Parameters': {
            '$a': search_results.iloc[0]
        }
    }]))

    spy.pull(push_result.iloc[0], start='2019-01-01T00:00:00.000Z', end='2019-06-01T00:00:00.000Z',
             capsules_as='signals')
