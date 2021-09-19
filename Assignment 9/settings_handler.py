import configparser


class SettingsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Settings:
    def __init__(self, settings_file):
        self._settings_file = settings_file
        self._reader = configparser.RawConfigParser()
        self._reader.read(self._settings_file)
        self._repo_type = self._reader['Settings']['repository']
        self._files = []
        self._gui = False
        self._set_ui()
        self._set_files()

    def _set_ui(self):
        ui_type = self._reader['Settings']['ui'].replace('"', '')
        if ui_type.lower() == 'gui':
            self._gui = True

    def _set_files(self):
        if self._repo_type == 'inmemory':
            return None
        elif self._repo_type == 'database':
            self._files.append('sql_data.db')
        elif self._repo_type in ('binaryfiles', 'textfiles', 'jsonfiles'):
            self._files.append(self._reader['Settings']['persons'].replace('"', ''))
            self._files.append(self._reader['Settings']['activities'].replace('"', ''))

    @property
    def repo_type(self):
        return self._repo_type

    @property
    def gui(self):
        return self._gui

    @property
    def files(self):
        return self._files


"""
All possible (accepted) settings:
repository - inmemory, textfiles, binaryfiles, jsonfiles, database
persons - "", "persons.txt", "persons.pickle", "persons.json", ""
activities - "", "activities.txt", "activities.pickle", "activities.json", ""
ui - "Console", "GUI"
"""