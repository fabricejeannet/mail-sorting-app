REGEX_DATE = r"\b(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[0-2])[./-](\d{2}|\d{4})\b"
REGEX_BRACKET = r"\[|\]"
REGEX_CONSECUTIVE_NUMBERS = r'\d\s*\d\s*\d\s*\d\s*\d\s*\d(?:\s*\d)*'
REGEX_SAS = r'\b[sS]\.?[aA]\.?[sS]\b\.?'
REGEX_SARL = r'\b[sS]\.?[aA]\.?[rR]\.?[lL]\b\.?'
REGEX_SASU = r'\b[sS]\.?[aA]\.?[sS]\.?[uU]\b\.?'
REGEX_EURL = r'\b[eE]\.?[uU]\.?[rR]\.?[lL]\b\.?'
REGEX_SCI = r'\b[sS]\.?[cC]\.?[iI]\b\.?'
REGEX_SNC = r'\b[sS]\.?[nN]\.?[cC]\b\.?'
REGEX_EI = r'\b[eE]\.?[iI]\b\.?'
REGEX_EIRL = r'\b[eE]\.?[iI]\.?[rR]\.?[lL]\b\.?'
REGEX_CABINET = r'\b[cC][aA][bB][iI][nN][eE][tT]\b'
REGEX_STE = r'\b[sS][tT][eE]\b'
REGEX_SOCIETE = r'\b[sS][oO][cC][iI][eE][tT][eE]\b'
REGEX_CIE = r'\b[cC][iI][eE]\b'
REGEX_GENDER_MARKERS = r'\b(m\b\.?|mme\b\.?|mr\b\.?|madame\b|monsieur\b|mmemr\b|m\(me\)\b)'

BANNED_WORDS_LIST = ["33000 bordeaux", "recommande","9 rue de conde bureau 3", "france","adresse de livraison", "le representant legal","9 r de condé", "9 rue de condé" ,"coolworking","representant legal", "le dirigeant de l'entreprise" "9 r de conde", "rue de conde","9 rue conde","titulaire du compte", "representant legal", "retour à", "a l'attention du dirigeant" ,"bureau 3", "destinataire", "ecopli", "etage 3", "numero de ", "\\x0c"]

# Put the substrings regex at the end of the list to avoid matching a substring before the full string
LEGAL_STATUS = [REGEX_SARL, REGEX_SASU, REGEX_EURL, REGEX_SCI, REGEX_SNC, REGEX_EIRL, REGEX_CABINET, REGEX_STE, REGEX_SOCIETE, REGEX_SAS, REGEX_EI, REGEX_CIE]
