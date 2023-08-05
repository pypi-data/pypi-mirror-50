import json
from pathlib import Path

import holoviews


class HVManiaManager():
    def __init__(self, name: str, directory: Path, renderer: str = 'bokeh'):
        self.name = name
        self.directory = directory

        if not self.directory.is_dir():
            raise Exception(f'{self.directory} is not directory.')

        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)

        self.catalog_file = self.directory / f'{name}.json'
        if not self.catalog_file.exists():
            self.dump_catalog({})

        self.renderer = renderer

    def load_catalog(self):
        catalog = json.load(self.catalog_file.open('r'), encoding='utf-8')
        return catalog

    def dump_catalog(self, catalog):
        json.dump(catalog, self.catalog_file.open('w'), ensure_ascii=False, indent=4, sort_keys=True)

    def __getitem__(self, item: str) -> Path:
        return Path(self.load_catalog()[item]['path'])

    def __setitem__(self, key: str, value):
        renderer = holoviews.renderer('bokeh')
        renderer.save(value, str(self.directory / key))
        c = self.load_catalog()
        c[key] = {'path': str((self.directory / f'{key}.html').absolute())}
