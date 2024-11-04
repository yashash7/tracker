from typing import List, Optional

class Filter_Validation_Exception(Exception):
    
    def __init__(self, msg: Optional[str] = "Filter Validation Failed!", filters: Optional[List[str]] = None):
        self.msg = msg
        if filters is None:
            self.desc = "One or Many of the filters are invalid, please contact admin to add new filters!"
        else:
            self.desc = ",".join(filters) + " doesn't exist in valid filters, please contact admin to add them to valid filters!"
        super().__init__(self.msg, self.desc)
    