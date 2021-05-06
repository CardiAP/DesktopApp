from app.models.analysis_parametrization import AnalysisParametrization


class AnalysisFile:
    UNSELECTED = 'UNSELECTED'
    ACCEPTED = 'ACCEPTED'
    SELECTED = 'SELECTED'

    def __init__(self, file):
        self.__file = file
        self.__status = self.UNSELECTED
        self.parametrization = AnalysisParametrization.default(file)

    @property
    def name(self):
        return self.__file.name

    @property
    def path(self):
        return self.__file

    @property
    def status(self):
        return self.__status

    def is_unselected(self):
        return self.__status == self.UNSELECTED

    def is_selected(self):
        return self.__status == self.SELECTED

    def is_accepted(self):
        return self.__status == self.ACCEPTED

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.path == other.path

    
class AnalysisFiles:

    @classmethod
    def for_file_paths(cls, files):
        return cls([AnalysisFile(file) for file in files])

    def __init__(self, files):
        self.__files = files

    def __iter__(self):
        return (file for file in self.__files)
