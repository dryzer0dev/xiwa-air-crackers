# XIWA Air Crackers

<!-- Bannière avec badges -->
<p align="center">
  <a href="https://github.com/dryzer0dev/xiwa-air-crackers" target="_blank">
    <img src="https://img.shields.io/github/stars/dryzer0dev/xiwa-air-crackers?style=for-the-badge&color=brightgreen&label=Stars" alt="Stars">
  </a>
  <a href="https://github.com/dryzer0dev/xiwa-air-crackers/fork" target="_blank">
    <img src="https://img.shields.io/github/forks/dryzer0dev/xiwa-air-crackers?style=for-the-badge&color=orange&label=Forks" alt="Forks">
  </a>
</p>

<!-- Titre principal -->
# XIWA Air Crackers

**XIWA Air Crackers** est un puissant toolkit d'information web et de cracking de mots de passe, conçu pour faciliter la collecte d'informations et les tests de sécurité de manière efficace et organisée.

---

## Fonctionnalités

### 🔍 Visionneuse de Source Web

- Visualiser le code source du site
- Obtenir l'IP du serveur et les infos SSL
- Extraire les emails des développeurs
- Sauvegarder le code source localement

> <a href="#" style="text-decoration: none; padding: 8px 16px; background-color: #007BFF; color: #fff; border-radius: 4px; font-weight: bold;">python main.py -v http://exemple.com</a>

---

### 🕷️ Web Spyder

- Exploration récursive de sites web
- Extraction d'emails et de numéros de téléphone
- Recherche de liens vers les réseaux sociaux
- Génération de plans du site

> <a href="#" style="text-decoration: none; padding: 8px 16px; background-color: #007BFF; color: #fff; border-radius: 4px; font-weight: bold;">python main.py -sp</a>

---

### 🔑 Cracker de Mots de Passe

- Crackage de comptes Instagram
- Crackage de comptes GitHub
- Configuration de la longueur des mots de passe
- Suivi en temps réel de la progression

> <a href="#" style="text-decoration: none; padding: 8px 16px; background-color: #007BFF; color: #fff; border-radius: 4px; font-weight: bold;">python main.py -crack instagram -u username -min 8 -max 12</a>

---

### 📡 Sniffeur Réseau

- Capture de paquets réseau
- Journalisation du trafic TCP/UDP
- Extraction des détails de paquets
- Sauvegarde au format CSV

> <a href="#" style="text-decoration: none; padding: 8px 16px; background-color: #007BFF; color: #fff; border-radius: 4px; font-weight: bold;">python main.py -s -f sniffed_data.csv</a>

---

### ⚡ Intégration Aircrack-ng

- Lancer une attaque avec aircrack-ng sur un réseau Wi-Fi

> <a href="#" style="text-decoration: none; padding: 8px 16px; background-color: #007BFF; color: #fff; border-radius: 4px; font-weight: bold;">python main.py -a</a>

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/yourusername/xiwa-air-crackers.git
cd xiwa-air-crackers

```

## 2. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

---

## USAGE

``` bash
# Visualiser le code source
python main.py -v http://exemple.com

# Sniffer le trafic
python main.py -s -f sortie.csv

# Cracker Instagram
python main.py -crack instagram -u username -min 8 -max 12

# Attaque Aircrack-ng
python main.py -a
```