import os
import json
from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

from database import (
    get_citoyen_info,
    get_statut_carte,
    get_statut_sante,
    get_statut_impots,
    get_statut_agriculture,
    get_profil_complet,
)
from intelligence import analyse_demande_locale, construire_reponse

app = FastAPI(title="MiabéInnovation API")


@app.post("/demande_ewe")
async def traiter_demande_whatsapp(request: Request):

    form_data = await request.form()
    question_utilisateur = form_data.get("Body", "").strip()

    print(f"\n{'='*60}")
    print(f"MESSAGE REÇU : {question_utilisateur}")

    reponse_finale = ""

    if not question_utilisateur:
        reponse_finale = "Message vide reçu."

    else:
        # ── ÉTAPE 1 : Analyse ─────────────────────────────────────
        print("1. Analyse (ID + langue + service)...")
        analyse   = analyse_demande_locale(question_utilisateur)
        id_trouve = analyse.get("id_national")
        langue    = analyse.get("langue_detectee", "Ewe")
        intention = analyse.get("intention", "inconnu")

        print(f"   ID: {id_trouve} | Langue: {langue} | Service: {intention}")

        # ── Pas d'ID trouvé ───────────────────────────────────────
        if not id_trouve or intention == "inconnu":
            reponse_finale = construire_reponse(None, "inconnu", langue)

        # ── Service : Carte d'identité ────────────────────────────
        elif intention == "carte":
            print("2. Requête → État Civil + Cartes d'identité")
            info  = get_citoyen_info(id_trouve)
            carte = get_statut_carte(id_trouve)
            reponse_finale = construire_reponse(
                info.get("nom"),
                carte.get("statut_demande", "non trouvé"),
                langue
            )

        # ── Service : Santé ───────────────────────────────────────
        elif intention == "sante":
            print("2. Requête → État Civil + Santé/DHIS2")
            info  = get_citoyen_info(id_trouve)
            sante = get_statut_sante(id_trouve)
            if sante:
                statut = "sante_ok" if sante["statut_vaccination"] == "À jour" else "sante_retard"
            else:
                statut = "non trouvé"
            reponse_finale = construire_reponse(info.get("nom"), statut, langue)

        # ── Service : Impôts ──────────────────────────────────────
        elif intention == "impots":
            print("2. Requête → État Civil + Impôts/OTR")
            info   = get_citoyen_info(id_trouve)
            impots = get_statut_impots(id_trouve)
            if impots:
                statut = "impots_ok" if impots["statut_fiscal"] == "À jour" else "impots_retard"
            else:
                statut = "non trouvé"
            reponse_finale = construire_reponse(info.get("nom"), statut, langue)

        # ── Service : Agriculture ─────────────────────────────────
        elif intention == "agriculture":
            print("2. Requête → État Civil + Agriculture/MASA")
            info = get_citoyen_info(id_trouve)
            agri = get_statut_agriculture(id_trouve)
            if agri:
                statut = "agriculture_ok" if agri["subvention_statut"] == "Approuvée" else "agriculture_nok"
            else:
                statut = "non trouvé"
            reponse_finale = construire_reponse(info.get("nom"), statut, langue)

        # ── Service : Profil complet — INTEROPÉRABILITÉ ───────────
        elif intention == "profil_complet":
            print("2. Requête → 5 BASES SIMULTANÉES (interopérabilité)")
            profil = get_profil_complet(id_trouve)
            nom    = profil["identite"].get("nom", "Citoyen")

            print(f"   Bases consultées : {profil['bases_consultees']}")

            reponse_finale = construire_reponse(nom, "profil_complet", langue)

            # Log interopérabilité visible dans le terminal
            print("\n   ╔══ INTEROPÉRABILITÉ ══════════════════════╗")
            for base in profil["bases_consultees"]:
                print(f"   ║  ✓ {base}")
            print("   ╚══════════════════════════════════════════╝\n")

    print(f"RÉPONSE ENVOYÉE : {reponse_finale}")
    print('='*60)

    twiml = MessagingResponse()
    twiml.message(reponse_finale)

    return Response(content=str(twiml), media_type="application/xml")


@app.get("/")
def read_root():
    return {
        "Projet": "MiabéInnovation",
        "Status": "Opérationnel",
        "Services": ["carte", "sante", "impots", "agriculture", "profil_complet"],
        "Langues": ["Ewe", "Kabye", "Français"]
    }


@app.get("/test/{id_national}")
def test_profil(id_national: str):
    """Route de test rapide pour vérifier l'interopérabilité"""
    from database import get_profil_complet
    return get_profil_complet(id_national)