import pytest

from seeq import spy
from seeq.spy.assets import Asset

from . import test_common


def setup_module():
    test_common.login()


class HVAC(Asset):

    @Asset.Attribute()
    def Temperature(self, metadata):
        # We use simple Pandas syntax to select for a row in the DataFrame corresponding to our desired tag
        return metadata[metadata['Name'].str.endswith('Temperature')]

    @Asset.Attribute()
    def Relative_Humidity(self, metadata):
        # All Attribute functions must take (self, metadata) as parameters
        return metadata[metadata['Name'].str.contains('Humidity')]


class Compressor(Asset):

    @Asset.Attribute()
    def Power(self, metadata):
        return metadata[metadata['Name'].str.endswith('Power')]


class HVAC_With_Calcs(HVAC):

    @Asset.Attribute()
    def Temperature_Rate_Of_Change(self, metadata):
        return {
            'Type': 'Signal',

            # This formula will give us a nice derivative in F/h
            'Formula': '$temp.lowPassFilter(150min, 3min, 333).derivative() * 3600 s/h',

            'Formula Parameters': {
                # We can reference the base class' Temperature attribute here as a dependency
                '$temp': self.Temperature(metadata),
            }
        }

    @Asset.Attribute()
    def Too_Hot(self, metadata):
        return {
            'Type': 'Condition',
            'Formula': '$temp.valueSearch(isGreaterThan($threshold))',
            'Formula Parameters': {
                '$temp': self.Temperature(metadata),

                # We can also reference other attributes in this derived class
                '$threshold': self.Hot_Threshold(metadata)
            }
        }

    @Asset.Attribute()
    def Hot_Threshold(self, metadata):
        return {
            'Type': 'Scalar',
            'Formula': '80F'
        }

    # Designating a function as a Component allows you to include a child asset with its own set of attributes
    @Asset.Component()
    def Compressor(self, metadata):
        return Compressor

    @Asset.Component()
    def Pump(self, metadata):
        return [
            {
                'Name': 'Pump Volume',
                'Type': 'Scalar',
                'Formula': '1000L'
            },
            {
                'Name': 'Pump Voltage',
                'Type': 'Scalar',
                'Formula': '110V'
            }
        ]


@pytest.mark.system
def test_instantiate():
    hvac_metadata_df = spy.search({
        'Name': 'Area ?_*'
    })

    hvac_metadata_df['Instance Template'] = 'HVAC'

    hvac_metadata_df['Instance Asset'] = hvac_metadata_df['Name'].str.extract('(Area .)_.*')

    hvac_metadata_df['Instance Path'] = 'My HVAC Units >> Facility #1'

    instances_df = spy.assets.instantiate(HVAC, hvac_metadata_df)

    # We'll get an error the first time because of Area F doesn't have the signals we need
    with pytest.raises(RuntimeError):
        spy.push(metadata=instances_df)

    # Now we'll catalog the errors instead of stopping on them
    spy.push(metadata=instances_df, errors='catalog')

    hvac_with_calcs_metadata_df = hvac_metadata_df.copy()
    hvac_with_calcs_metadata_df['Instance Template'] = 'HVAC_With_Calcs'

    instances_with_calcs_df = spy.assets.instantiate(HVAC_With_Calcs, hvac_with_calcs_metadata_df)

    spy.push(metadata=instances_with_calcs_df, errors='catalog')

    search_results_df = spy.search({
        'Path': 'My HVAC Units >> Facility #1'
    })

    areas = [
        'Area A',
        'Area B',
        'Area C',
        'Area D',
        'Area E',
        'Area F',
        'Area G',
        'Area H',
        'Area I',
        'Area J',
        'Area K',
        'Area Z',
    ]

    for area in areas:
        assertions = [
            ('My HVAC Units >> Facility #1', area, 'Temperature', 'CalculatedSignal'),
            ('My HVAC Units >> Facility #1', area, 'Temperature Rate Of Change', 'CalculatedSignal'),
            ('My HVAC Units >> Facility #1', area, 'Relative Humidity', 'CalculatedSignal'),
            ('My HVAC Units >> Facility #1', area, 'Too Hot', 'CalculatedCondition'),
            ('My HVAC Units >> Facility #1', area, 'Hot Threshold', 'CalculatedScalar'),
            ('My HVAC Units >> Facility #1', area, 'Pump Voltage', 'CalculatedScalar'),
            ('My HVAC Units >> Facility #1', area, 'Pump Volume', 'CalculatedScalar'),
            ('My HVAC Units >> Facility #1 >> ' + area, 'Compressor', 'Power', 'CalculatedSignal'),
        ]

        # Area F is special!
        if area == 'Area F':
            assertions = [
                ('My HVAC Units >> Facility #1', area, 'Hot Threshold', 'CalculatedScalar'),
                ('My HVAC Units >> Facility #1', area, 'Pump Voltage', 'CalculatedScalar'),
                ('My HVAC Units >> Facility #1', area, 'Pump Volume', 'CalculatedScalar'),
                ('My HVAC Units >> Facility #1 >> ' + area, 'Compressor', 'Power', 'CalculatedSignal'),
            ]

        for _path, _asset, _name, _type in assertions:
            assertion_df = search_results_df[
                (search_results_df['Path'] == _path) &
                (search_results_df['Asset'] == _asset) &
                (search_results_df['Name'] == _name) &
                (search_results_df['Type'] == _type)]

            assert len(assertion_df) == 1, \
                'Instantiated item not found: %s, %s, %s, %s' % (_path, _asset, _name, _type)
