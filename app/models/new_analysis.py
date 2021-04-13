class NewAnalysisParametrization(object):
    TRANSITORY = 'TRANSITORY'
    WAVES = 'WAVES'
    SPARKS = 'SPARKS'

    NO_FILES_SELECTED = 'NO_FILES_SELECTED'
    NO_TYPE_SELECTED = 'NO_TYPE_SELECTED'

    def __init__(self, filenames, analysis_type):
        self.__filenames = filenames
        self.__analysis_type = analysis_type

    def is_valid(self):
        return len(self.errors()) == 0

    def errors(self):
        errors = []
        if len(self.__filenames) <= 0:
            errors.append(self.NO_FILES_SELECTED)
        if self.__analysis_type is None:
            errors.append(self.NO_TYPE_SELECTED)
        return errors