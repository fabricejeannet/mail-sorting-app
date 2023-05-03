# StreetFacteur 📬

StreetFacteur est une application d'aide au tri du courrier, conçue pour aider les entreprises de domiciliation à trier rapidement et efficacement leur courrier. 

## État actuel du projet
StreetFacteur est encore en développement et n'est pas encore fonctionnel. Actuellement, nous travaillons sur les fonctionnalités de base telles que la numérisation d'enveloppes et l'extraction de l'adresse postale. Nous prévoyons d'ajouter des fonctionnalités supplémentaires telles que la recherche de l'adresse dans un

## Fonctionnalités principales
- Numérisation d'enveloppes à l'aide d'une caméra Raspberry Pi
- Extraction de l'adresse postale à l'aide d'OpenCV et de Pytesseract
- Recherche de l'adresse dans un fichier CSV contenant les adresses des clients
- Affichage du statut de l'abonnement du client correspondant à l'adresse
- Affichage des informations de tri de l'enveloppe (acceptée ou non)

## Installation

### Prérequis
- Python 3.x
- Bibliothèques Python : opencv-python, pytesseract, fuzzywuzzy, picamera2

### Instructions
1. Clonez le projet depuis le dépôt GitHub
2. Installez les bibliothèques Python requises en exécutant la commande `pip install -r requirements.txt`
3. Lancez l'application avec la commande `python main.py`

## Utilisation
1. Connectez votre Raspberry Pi à la caméra et exécutez l'application
2. Placez l'enveloppe dans le cadre de la caméra
3. L'adresse postale sera extraite automatiquement de l'enveloppe et comparée à la liste des clients
4. Le statut de l'abonnement du client sera affiché à l'écran, ainsi que les informations de tri de l'enveloppe

## Auteur
Créé par Loïc LEVEQUE et Fabrice JEANNET
