from enum import Enum

class DisplayStatus(Enum):
    VALID = 0
    INVALID = 1
    WARNING = 2
    
class PopupStatus(Enum):
    NO_POPUP = 0
    CSV_POPUP = 1
    NO_CSV_FILE_POPUP = 2
    
ANALYSING_TEXT = "Analyse en cours..."
NO_TEXT_FOUND = "Pas de texte valide détécté !\n"
NO_MATCH_FOUND = "Aucune correspondance trouvée !\n"
MOTION_DETECTED = "Mouvement détécté !\n"
CSV_POPUP_MESSAGE = "Mise à jour du csv.\n Merci de patienter, cette fenêtre se fermera automatiquement."
NO_CSV_FILE_POPUP_MESSAGE = "Aucun fichier csv détécté.\n Merci d'ajouter un fichier csv valide"