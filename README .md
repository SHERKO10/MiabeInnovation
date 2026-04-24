# MiabéInnovation 🇹🇬

> **Bot WhatsApp IA multilingue pour les services publics du Togo**  
> *Un citoyen envoie un message en Ewé. En 3 secondes, il reçoit sa situation auprès de 5 ministères.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-F22F46?style=flat-square&logo=twilio&logoColor=white)](https://twilio.com)
[![GPT-4o](https://img.shields.io/badge/GPT--4o-GitHub%20Models-181717?style=flat-square&logo=openai&logoColor=white)](https://github.com/marketplace/models)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Hackathon](https://img.shields.io/badge/D--CLIC-Hackathon%202026-orange?style=flat-square)](https://dclic.org)

---

## 📺 Démo live

[![Voir la démo](https://img.shields.io/badge/▶_Voir_la_démo-Google_Drive-4285F4?style=flat-square&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1U7i_dZSETN_XU8huZX-y9_ixfZvCFGHp/view?usp=drive_link)
---

## 🎯 Problème résolu

| Problème | Notre solution |
|----------|---------------|
| 60% des Togolais ne parlent pas français | Détection automatique de la langue (Ewé, Kabiyè, Mina, Français) |
| Les ministères ont des bases de données isolées | Interopérabilité — 5 bases croisées en une seule requête |
| Accès aux services nécessite alphabétisation | WhatsApp accessible sur tout téléphone, sans application |

---

## 🛠️ Stack technique

```
Backend          FastAPI (Python 3.11)
IA / NLP         GPT-4o via GitHub Models (gratuit)
Messaging        Twilio WhatsApp Business API
Tunnel dev       Ngrok
Données          CSV + JSON (simulation interopérabilité)
Langues          Ewé · Kabiyè · Mina · Français
```

---

## 🏛️ Services publics intégrés

```
┌─────────────────────────────────────────────────────────┐
│                   Miabe Innovation — MiabéBot                     │
├──────────────┬──────────────┬────────────┬──────────────┤
│  Carte CNI   │    Santé     │   Impôts   │ Agriculture  │
│   (RAVEC)    │   (DHIS2)    │   (OTR)    │   (MASA)     │
├──────────────┴──────────────┴────────────┴──────────────┤
│            Profil Complet — 5 bases simultanées         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Architecture du flux

```
Citoyen (WhatsApp)
      │
      │  Message en Ewé / Kabiyè / Français
      ▼
Twilio (WhatsApp Business API)
      │
      │  HTTP POST → URL publique
      ▼
Ngrok (Tunnel localhost ↔ internet)
      │
      ▼
FastAPI  ──► Regex extraction ID (TGxxxxxx)
      │
      ├──► GPT-4o (détection langue + intention)
      │
      ├──► Bases de données (CSV + JSON)
      │         ├── citoyens.csv       (État Civil)
      │         ├── statut_cartes.json (CNI / RAVEC)
      │         ├── services_sante.json (DHIS2)
      │         ├── services_impots.json (OTR)
      │         └── services_agriculture.json (MASA)
      │
      └──► Template hardcodé → Réponse dans la langue du citoyen
                │
                ▼
      Twilio → Citoyen ✓
```

---

## 📁 Structure du projet

```
miabe_innovation/
├── main.py                    # Serveur FastAPI + routing WhatsApp           
├── requirements.txt
├── .env                       # Variables d'environnement (non versionné)
├── .gitignore
│
├── databases/
│   ├── citoyens.csv
│   ├── database.py             # Accès aux données + interopérabilité
│   ├── statut_cartes.json
│   ├── services_sante.json
│   ├── services_impots.json
│   └── services_agriculture.json
│
├── moteurIA/
│   └── intelligence.py         # IA : détection langue, intention, templates 
```

---

## ⚡ Installation & lancement

### Prérequis

- Python 3.11+
- Compte [Twilio](https://twilio.com) (gratuit)
- Compte [GitHub](https://github.com) pour l'API GPT-4o
- [Ngrok](https://ngrok.com) installé

### 1. Cloner le repo

```bash
git clone https://github.com/SHERKO10/MiabeInnovation.git
cd MiabeInnovation
```

### 2. Environnement virtuel

```bash
# Créer
python -m venv venv

# Activer (Windows)
.\venv\Scripts\activate

# Activer (Linux / macOS)
source venv/bin/activate
```

### 3. Dépendances

```bash
pip install -r requirements.txt
```

### 4. Variables d'environnement

Créer un fichier `.env` à la racine :

```env
OPENAI_API_KEY=ghp_votre_clé_github_models
OPENAI_API_BASE=https://models.inference.ai.azure.com
```

> 💡 L'API GPT-4o est **gratuite** via [GitHub Models](https://github.com/marketplace/models) — aucune carte bancaire requise.

### 5. Lancer le serveur

```bash
uvicorn main:app --reload --port 8000
```

### 6. Exposer avec Ngrok

```bash
ngrok http 8000
```

Copier l'URL générée (ex: `https://abc123.ngrok.io`) et la coller dans Twilio :

```
Twilio Console → Messaging → Sandbox Settings
→ "When a message comes in" : https://abc123.ngrok.io/demande_ewe
```

---

## 💬 Exemples de conversations

### Ewé — Carte d'identité
```
Utilisateur : Nye carte d'identité TG012345 le klaloa?
MiabéBot    : Ŋdi na wò Akouvi KOMBATE. Wò Dzesidegbalẽ le klalo.
              Va xɔe le Lomé dɔwɔƒe.
```

### Kabiyè — Santé
```
Utilisateur : Man lãm TG067890 taa ñɩnɩɣ?
MiabéBot    : Lafi Koffi AGBO. Ña ɖɔkɔtɔ tɔm wɛ ɖeu.
              Kɔ CSU Lomé taa.
```

### Français — Profil complet (interopérabilité)
```
Utilisateur : Je veux tout savoir sur mon dossier TG012345
MiabéBot    : Bonjour Akouvi KOMBATE. Voici votre situation complète :
              • Carte d'identité : Prête ✓
              • Santé : À jour ✓
              • Impôts : À jour ✓
              • Agriculture : Subvention approuvée ✓
              5 bases de données consultées.
```

---

## 🗺️ Roadmap

- [x] Prototype WhatsApp fonctionnel
- [x] Détection automatique Ewé / Kabiyè / Français
- [x] Interopérabilité 5 bases de données simulées
- [x] 4 services publics intégrés
- [ ] Connexion aux vraies APIs gouvernementales
- [ ] Ajout Mina et Tem
- [ ] Fine-tuning modèle sur corpus togolais (partenariat Université de Lomé)
- [ ] Déploiement sur serveur cloud (AWS / OVH Togo)
- [ ] Interface web dashboard pour les agents administratifs

---

## 👥 Équipe HESTIA — D-CLIC 2026

| Nom | Rôle |
|-----|------|
| **POZOU Ewaba Emmanuel (SHERKO)** | Lead Technique · Architecture IA |
| **Atsoo ami Françoise** | Communication · Présentation |
| **Amélé Dorcas ADADE** | Data · Tests utilisateurs |
| **KPEGLO Esther** | Coordination · Livrables |

---

## 📄 Licence

MIT © 2026 Équipe HESTIA — MiabéInnovation

---

<div align="center">
  <sub>Construit avec ❤️ à Lomé, Togo — Hackathon D-CLIC 2026</sub>
</div>
