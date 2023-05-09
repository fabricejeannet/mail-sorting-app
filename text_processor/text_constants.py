REGEX_DATE = r"\b(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[0-2])[./-](\d{2}|\d{4})\b"
REGEX_BRACKET = r"\[|\]"
REGEX_CONSECUTIVE_NUMBERS = r'\d\s*\d\s*\d\s*\d\s*\d\s*\d(?:\s*\d)*'
REGEX_SAS = r'\b[sS]?[.]?[aA]?[.]?[sS]?[.]?\b'
REGEX_SARL = r'\b[sS]?[.]?[aA]?[.]?[rR]?[.]?[lL]?[.]?\b'
REGEX_SASU = r'\b[sS]?[.]?[aA]?[.]?[sS]?[.]?[uU]?\b'
REGEX_EURL = r'\b[eE]?[.]?[uU]?[.]?[rR]?[.]?[lL]?\b'
REGEX_SCI = r'\b[sS]?[.]?[cC]?[.]?[iI]?\b'
REGEX_SNC = r'\b[sS]?[.]?[nN]?[.]?[cC]?\b'
REGEX_EI = r'\b[eE]?[.]?[iI]?\b'
REGEX_EIRL = r'\b[eE]?[.]?[iI]?[.]?[rR]?[.]?[lL]?\b'

BANNED_WORDS_LIST = ["33000 bordeaux", "9 rue de conde", "rue de conde","9 rue conde","titulaire du compte", "representant legal", "facture n" , "retour à" ,"destinataire lettre","bureau 3", "destinataire", "numero de tva", "numero de siret", "ecopli", "etage 3", "niveau de garantie", "numero de police", "numero de contrat", "numero de telephone", "numero de fax", "numero de compte", "numero de client", "numero de facture", "numero de commande", "numero de dossier", "\\x0c"]

LEGAL_STATUS = [REGEX_SAS, REGEX_SARL, REGEX_SASU, REGEX_EURL, REGEX_SCI, REGEX_SNC, REGEX_EI, REGEX_EIRL]
