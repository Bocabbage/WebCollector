from enum import Enum

class RSSRuleFileErrCode(Enum):
    r'''
        RSS file download/parse error enum
    '''
    YAML_FORMAT_ERROR = 1
    RSS_XML_REQUEST_ERROR = 2
    XML_PARSE_ERROR = 3
    RULE_VERSION_ERROR = 4

        
class RSSRuleFileError(Exception):
    r'''
        RSS file download/parse error
    '''
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
