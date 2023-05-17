

class MatchingResult:

    def __init__(self, matching_string, correspondance_ratio, status):
        self.matching_string = matching_string
        self.match_ratio = correspondance_ratio
        self.status = status
    
    def __str__(self) -> str:
        return "Matching string: " + self.matching_string + " - Match ratio: " + str(self.match_ratio) + " - Status: " + self.status