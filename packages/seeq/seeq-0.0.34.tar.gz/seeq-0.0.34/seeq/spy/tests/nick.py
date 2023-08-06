from seeq import spy
import pandas as pd

from seeq.spy.assets import Asset

pd.set_option('display.max_colwidth', -1)

spy.login(username="nicholas.gigliotti@seeq.com", password="Seeq2019!", url="https://birlacarbon.seeq.site",
          auth_provider="Seeq")


class Site(Asset):
    @Asset.Component()
    def Units(self, metadata):
        unit_names = metadata['Unit'].dropna().drop_duplicates().tolist()
        units = list()
        for unit_name in unit_names:
            unit = Unit({
                'Name': unit_name,
                'Type': 'Asset',
                'Asset': unit_name,
                'Path': self.asset_definition['Path'] + ' >> ' + self.asset_definition['Name']
            })
            units.append(unit)
        return units


class Unit(Asset):
    def select_my_metadata(self, metadata):
        return metadata[metadata['Unit'] == self.asset_definition['Name']]

    @Asset.Component()
    def Reactors(self, metadata):
        metadata = self.select_my_metadata(metadata)
        reactor_names = metadata['Reactor'].dropna().drop_duplicates().tolist()
        reactors = list()
        print(self.asset_definition)
        for reactor_name in reactor_names:
            reactor_metadata = metadata[metadata['Reactor'] == reactor_name]
            reactor = Reactor({
                'Type': 'Asset',
                'Name': reactor_name,
                'Asset': reactor_name,
                'Path': self.asset_definition['Path'] + ' >> ' + self.asset_definition['Name']
            }).build(reactor_metadata)
            reactors.extend(reactor)
        return reactors


class Reactor(Asset):
    def select_my_metadata(self, metadata):
        return metadata[metadata['Reactor'] == self.asset_definition['Name']]

    @Asset.Attribute()
    def Make_Oil_Flow_Rate(self, metadata):
        metadata = self.select_my_metadata(metadata)
        return metadata[metadata['Description'].str.contains('MAKE OIL|MAKEOIL')]

    @Asset.Attribute()
    def Blast_Air_Flow_Rate(self, metadata):
        metadata = self.select_my_metadata(metadata)
        metadata1 = metadata[metadata['Description'].str.contains('BLAST AIR')]
        metadata2 = metadata1[metadata1['Description'].str.contains('VENTURI') == False]
        if metadata2.iloc[0]['Value Unit Of Measure'] != 'ft³/h':
            return {
                'Name': 'Blast Air Flow Rate',
                'Type': 'Signal',
                'Formula': "($tag * 1000).setUnits('ft³/h')",
                'Formula Parameters': {
                    '$tag': metadata2
                },
            }
        else:
            return metadata2

    @Asset.Attribute()
    def Blast_Gas_Flow_Rate(self, metadata):
        metadata = self.select_my_metadata(metadata)
        metadata1 = metadata[metadata['Description'].str.contains('BLAST GAS')]
        return metadata1[metadata1['Description'].str.contains('AUXILIARY') == False]

    @Asset.Attribute()
    def Oil_Status(self, metadata):
        metadata = self.select_my_metadata(metadata)
        metadata2 = metadata[metadata['Name'].str.contains('AN')]
        return {
            'Type': 'Signal',
            'Formula': "$tag.validValues().toStep().setmaxInterpolation(30 days)",
            'Formula Parameters': {
                '$tag': metadata2
            },
        }


unit1_vars = spy.search({'Name': '/^FIC1[1-4]+0[2-4]+\.PV.*/', 'Type': 'StoredSignal'})
oil_status_1 = spy.search({'Name': '/^XS1[1-5]+02C_AN$/', 'Description': '/OIL/'})
unit1_df = unit1_vars.append(oil_status_1)
other_units = spy.search({'Name': '/^FIC[2-5]+10[1-4]+.\.PV./'})
all_units = unit1_df.append(other_units)
all_units['Reactor'] = 'RX' + all_units['Name'].str.extract(pat='\w{2,3}(.).*')
all_units['Unit'] = 'Unit ' + all_units['Name'].str.extract(pat='\w{2,3}.(.).*')
all_units['Site'] = 'North Bend'
all_units['Instance Path'] = 'Nick Dev'
all_units['Instance Asset'] = 'North Bend'
all_units['Instance Template'] = 'Site'
all_units[['Name', 'Description', 'Reactor', 'Unit', 'Site']]
spy.assets.instantiate(Site, all_units)
# reactor = all_units[all_units['Reactor'] == 'RX1']
# reactor[['Name', 'Description', 'Reactor', 'Unit', 'Site']]
