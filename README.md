# 🎓 Coach PFE - Orchestrateur Multi-Agents

Une plateforme d'intelligence artificielle multi-agents conçue pour accompagner les étudiants en ingénierie dans la réalisation de leur Projet de Fin d'Études (PFE). 

Ce système repose sur une architecture d'orchestration **LangGraph**, propulsée par les modèles **Google Gemini**, et intègre un système **RAG** (Retrieval-Augmented Generation) adossé à **MongoDB Atlas/Local** pour la recherche documentaire vectorielle.

---

## 🏗️ Architecture du Système

L'application agit comme un "Routeur Intelligent" qui analyse l'intention de l'utilisateur et délègue la tâche au meilleur agent expert :

1. **Agent Méthodologue :** Un expert en gestion de projet (WBS, Gantt, planification). Il aide l'étudiant à structurer ses idées et à définir ses jalons.
2. **Agent Correcteur (RAG) :** Un expert académique connecté à une base vectorielle MongoDB. Il relit les productions, corrige la syntaxe et s'assure du respect des normes bibliographiques et typographiques de l'école.

## 🚀 Fonctionnalités Clés
* **Routage Dynamique :** Redirection automatique des requêtes vers le bon agent expert.
* **Mémoire de Session :** Historique conversationnel persistant (Window Buffer) isolé par ID utilisateur.
* **Intégration RAG :** Recherche sémantique locale ultra-rapide sur des documents PDF (Guides, Mémoires, Normes) via MongoDB Vector Search.
* **Interface Telegram :** Connecté via `python-telegram-bot` pour une interaction fluide depuis un smartphone.

---

## 🛠️ Technologies Utilisées
* **Langage :** Python 3.10+
* **Orchestration IA :** LangGraph & LangChain
* **LLM :** Google Gemini (gemini-2.0-flash)
* **Base de Données Vectorielle :** MongoDB (Vector Search)
* **API :** Telegram Bot API

---

## ⚙️ Prérequis et Installation

### 1. Cloner le dépôt
```bash
git clone [https://github.com/RedaH13/coach-pfe-langgraph.git](https://github.com/RedaH13/coach-pfe-langgraph.git)
cd coach-pfe-langgraph
```

### 2. Environnement Virtuel et Dépendances
Il est recommandé d'utiliser un environnement virtuel :

bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
pip install .              # Ou pip install -r requirements.txt

### 3. Configuration des Variables d'Environnement
Créez un fichier .env à la racine du projet et ajoutez vos clés d'API et identifiants de base de données :

# MongoDB (Local ou Atlas)
MONGODB_URI="mongodb://localhost:27017" # Ou host.docker.internal si sous Docker

# Telegram Bot
TELEGRAM_BOT_TOKEN="Telegram_Token_Access"

## 📂 Structure du Projet
Code
coach_pfe_langgraph/
├── main.py                 # Point d'entrée et intégration Telegram
├── state.py                # Définition de l'état global et de la mémoire LangGraph
├── router.py               # Logique de routage (Switch)
├── tools/                  
│   └── mongo_retrievers.py # Outils RAG
├── agents/                 
│   ├── methodologue.py     # Logique et Prompt du Méthodologue
│   └── correcteur.py       # Logique et Prompt du Correcteur
├── data/                   # Dossier ignoré contenant memory.json
├── requirements.txt        # Dépendances du projet
└── pyproject.toml          # Configuration du package Python

## 🚀 Exécution
Pour lancer l'orchestrateur et mettre le bot en écoute :

bash
python main.py
