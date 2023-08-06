from types import ModuleType

import pandas as pd

from .. import _common

from ._model import Mixin


def instantiate(model, metadata):
    return pd.DataFrame(_instantiate(model, metadata))


def _instantiate(model, metadata):
    results = list()

    if 'Instance Path' not in metadata or 'Instance Asset' not in metadata or 'Instance Template' not in metadata:
        raise RuntimeError('"Instance Path", "Instance Asset", "Instance Template" are required columns')

    unique_assets = metadata[['Instance Path', 'Instance Asset', 'Instance Template']].drop_duplicates().dropna()

    for index, row in unique_assets.iterrows():
        if not _common.present(row, 'Instance Template') or \
                not _common.present(row, 'Instance Asset') or \
                not _common.present(row, 'Instance Path'):
            continue

        if isinstance(model, ModuleType):
            template = getattr(model, row['Instance Template'].replace(' ', '_'))
        else:
            template = model

        instance = template({
            'Name': row['Instance Asset'],
            'Asset': row['Instance Asset'],
            'Path': row['Instance Path']
        })

        instance_metadata = metadata[(metadata['Instance Asset'] == row['Instance Asset']) &
                                     (metadata['Instance Path'] == row['Instance Path'])]

        results.extend(instance.build(instance_metadata))

    return results
