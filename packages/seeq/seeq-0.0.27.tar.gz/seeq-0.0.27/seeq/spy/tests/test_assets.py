import pytest

from seeq import spy
from seeq.spy.assets import Asset

from . import test_common


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


@pytest.mark.system
def test_instantiate():
    test_common.login()

    hvac_metadata_df = spy.search({
        'Name': 'Area ?_*'
    })

    hvac_metadata_df['Instance Template'] = 'HVAC'

    hvac_metadata_df['Instance Asset'] = hvac_metadata_df['Name'].str.extract('(Area .)_.*')

    hvac_metadata_df['Instance Path'] = 'My HVAC Units >> Facility #1'

    instances_df = spy.assets.instantiate(HVAC, hvac_metadata_df)

    spy.push(metadata=instances_df)

    hvac_with_calcs_metadata_df = hvac_metadata_df.copy()
    hvac_with_calcs_metadata_df['Instance Template'] = 'HVAC_With_Calcs'

    instances_with_calcs_df = spy.assets.instantiate(HVAC_With_Calcs, hvac_with_calcs_metadata_df)

    spy.push(metadata=instances_with_calcs_df)
