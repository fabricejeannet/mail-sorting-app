REGEX_DATE = r"\b(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[0-2])[./-](\d{2}|\d{4})\b"
REGEX_BRACKET = r"\[|\]"
REGEX_CONSECUTIVE_NUMBERS = r'\d\s*\d\s*\d\s*\d\s*\d\s*\d(?:\s*\d)*'
REGEX_SAS = r'\b[sS][.]?[aA][.]?[sS][.]?\b'
REGEX_SARL = r'\b[sS][.]?[aA][.]?[rR][.]?[lL][.]?\b'
REGEX_SASU = r'\b[sS][.]?[aA][.]?[sS][.]?[uU]\b'
REGEX_EURL = r'\b[eE][.]?[uU][.]?[rR][.]?[lL]\b'
REGEX_SCI = r'\b[sS][.]?[cC][.]?[iI]\b'
REGEX_SNC = r'\b[sS][.]?[nN][.]?[cC]\b'
REGEX_EI = r'\b[eE][.]?[iI]\b'
REGEX_EIRL = r'\b[eE][.]?[iI][.]?[rR][.]?[lL]\b'
REGEX_CABINET = r'\b[cC][aA][bB][iI][nN][eE][tT]\b'
REGEX_STE = r'\b[sS][tT][eE]\b'
REGEX_SOCIETE = r'\b[sS][oO][cC][iI][eE][tT][eE]\b'

BANNED_WORDS_LIST = ["33000 bordeaux", "recommande", "coolworking","representant legal", "le dirigeant de l'entreprise" "9 r de conde", "rue de conde","9 rue conde","titulaire du compte", "representant legal", "retour à", "a l'attention du dirigeant" ,"bureau 3", "destinataire", "ecopli", "etage 3", "numero de ", "\\x0c"]

LEGAL_STATUS = [REGEX_SAS, REGEX_SARL, REGEX_SASU, REGEX_EURL, REGEX_SCI, REGEX_SNC, REGEX_EI, REGEX_EIRL, REGEX_CABINET, REGEX_STE, REGEX_SOCIETE]
