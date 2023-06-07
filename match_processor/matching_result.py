

class MatchingResult:

    def __init__(self, status, company_match_ratio = None, person_match_ratio = None, matching_company = None, matching_person = None):
        self.matching_company = matching_company
        self.matching_person = matching_person
        self.company_match_ratio = company_match_ratio
        self.person_match_ratio = person_match_ratio
        self.status = status
    
    def __str__(self) -> str:
        return "MatchingResult: " + str(self.__dict__)
    
    def __repr__(self):
        return str(self)
    
    
    def get_max_match_ratio(self):
        if self.company_match_ratio is None:
            return self.person_match_ratio
        
        elif self.person_match_ratio is None:
            return self.company_match_ratio
        
        return max(self.company_match_ratio, self.person_match_ratio)