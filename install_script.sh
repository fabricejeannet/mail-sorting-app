#!/bin/bash

# Fonction pour afficher un message en surbrillance
highlight_message() {
  echo -e "\033[1m$1\033[0m"
}

# Affiche un message d'accueil
highlight_message "Bienvenue dans l'assistant d'installation de l'application Mail Sorting!"

# Clone le dépôt GitHub
highlight_message "Clonage du dépôt GitHub..."
git clone https://github.com/fabricejeannet/mail-sorting-app.git

# Se déplace dans le répertoire du projet
highlight_message "Accès au répertoire du projet..."
cd mail-sorting-app

# Installe les dépendances système
highlight_message "Installation des dépendances système..."
sudo apt-get install python3-opencv
sudo apt-get install libatlas-base-dev
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-fra

# Installe les dépendances Python
highlight_message "Installation des dépendances Python..."
pip install pytesseract
pip install fuzzywuzzy
pip install python-Levenshtein
pip install pandas
pip install pillow --upgrade
pip install watchdog

# Configure la variable d'environnement PYTHONPATH
highlight_message "Configuration de la variable d'environnement PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:/

# Affiche un message de fin
highlight_message "L'installation est terminée. Profitez de votre application Mail Sorting!"
