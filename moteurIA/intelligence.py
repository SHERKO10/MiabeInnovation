import os
import json
import re
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MODEL_IA = "openai/gpt-4o"

# ── Templates hardcodés ───────────────────────────────────────────────────────
REPONSES_HARDCODEES = {
    "Ewe": {
        "prête": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò Dzesidegbalẽ le klalo. "
            f"Va xɔe le Lomé dɔwɔƒe."
        ),
        "en cours": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò Dzesidegbalẽ le dɔ wɔm eŋu. "
            f"Gbo dzi ɖi."
        ),
        "non trouvé": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Míe mɔ wò gɔmedede nyawo o. "
            f"Yi dɔwɔƒe la me."
        ),
        "inconnu": lambda _: (
            "Míe mɔ ŋkɔ siwo wò ŋlɔ o. "
            "Ŋlɔ wò ID kple TG lɔlɔ̃ (example: TG012345)."
        ),
        "sante_ok": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò lãm ŋkɔ le dɔ me. "
            f"Vaccine gbɔgblɔ si wò xɔ : Polio. "
            f"Yi CSU Bè le Lomé."
        ),
        "sante_retard": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò lãm vaccine le emegbe. "
            f"Yi dɔwɔƒe lãm si le kɔtɔ."
        ),
        "impots_ok": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò taxatsi ŋkɔ le dɔ me. "
            f"Mɔ dzo le Dzove 2026."
        ),
        "impots_retard": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò taxatsi le emegbe. "
            f"Yi OTR dɔwɔƒe."
        ),
        "agriculture_ok": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò feŋɔ xɔ do. "
            f"CFA 75,000 — wò ɖo nu ko."
        ),
        "agriculture_nok": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Wò agble gɔmedede me kpɔ nyawo o. "
            f"Yi MASA dɔwɔƒe."
        ),
        "profil_complet": lambda nom: (
            f"Ŋdi na wò {nom}. "
            f"Míe kpɔ nyawo le dɔwɔƒe atɔ̃ame ŋu:\n"
            f"• Dzesidegbalẽ: Le klalo ✓\n"
            f"• Lãm: Dɔ me ✓\n"
            f"• Taxatsi: Dɔ me ✓"
        ),
    },
    "Kabye": {
        "prête": lambda nom: (
            f"Lafi {nom}. "
            f"Ña takayaɣ tɛma. "
            f"Kɔɔ ko-tɔ Lomé tʋmɩyɛ taa."
        ),
        "en cours": lambda nom: (
            f"Lafi {nom}. "
            f"Ña takayaɣ pɛwɛ pɩ-taa. "
            f"Danɩ pazɩ."
        ),
        "non trouvé": lambda nom: (
            f"Lafi {nom}. "
            f"Pɩtɩɩ naɣ ña tɔm taa. "
            f"Kɔ tʋmɩyɛ yɔ."
        ),
        "inconnu": lambda _: (
            "Mantɩ nɩɩ. "
            "Pʋlʋʋ ŋmɩ ña ID TG taa (example: TG012345)."
        ),
        "sante_ok": lambda nom: (
            f"Lafi {nom}. "
            f"Ña ɖɔkɔtɔ tɔm wɛ ɖeu. "
            f"Vaccine ña tɛma : Polio. "
            f"Kɔ CSU Lomé taa."
        ),
        "sante_retard": lambda nom: (
            f"Lafi {nom}. "
            f"Ña vaccine tɩɩ lɛ. "
            f"Kɔ ɖɔkɔtɔ tʋmɩyɛ taa nɛ pɩ-kɛdɛzaɣdɔ."
        ),
        "impots_ok": lambda nom: (
            f"Lafi {nom}. "
            f"Ña takɩtʋ tɔm wɛ ɖeu. "
            f"Ðɩɩ labɩ Dzove 2026."
        ),
        "impots_retard": lambda nom: (
            f"Lafi {nom}. "
            f"Ña takɩtʋ tɩɩ lɛ. "
            f"Kɔ OTR tʋmɩyɛ taa."
        ),
        "agriculture_ok": lambda nom: (
            f"Lafi {nom}. "
            f"Ña liidiye sɩɩnaa. "
            f"CFA 75,000 — pɛcɛlɩ-ɩ."
        ),
        "agriculture_nok": lambda nom: (
            f"Lafi {nom}. "
            f"Ña tɩ-tɩɩ tɔm tɩɩ ɖeu. "
            f"Kɔ MASA tʋmɩyɛ taa."
        ),
        "profil_complet": lambda nom: (
            f"Lafi {nom}. "
            f"Pɩnaɣ ña tɔm taa:\n"
            f"• Takayaɣ: Tɛma ✓\n"
            f"• Ɖɔkɔtɔ: Wɛ ɖeu ✓\n"
            f"• Takɩtʋ: Wɛ ɖeu ✓"
        ),
    },
    "Français": {
        "prête": lambda nom: (
            f"Bonjour {nom}. "
            f"Votre carte d'identité est prête. "
            f"Venez la récupérer au bureau de Lomé."
        ),
        "en cours": lambda nom: (
            f"Bonjour {nom}. "
            f"Votre demande est en cours de traitement. "
            f"Veuillez patienter."
        ),
        "non trouvé": lambda nom: (
            f"Bonjour {nom}. "
            f"Aucune demande trouvée. "
            f"Contactez le bureau concerné."
        ),
        "inconnu": lambda _: (
            "Désolé, je n'ai pas compris. "
            "Donnez votre numéro ID (ex: TG012345) et le service souhaité."
        ),
        "sante_ok": lambda nom: (
            f"Bonjour {nom}. "
            f"Votre dossier santé est à jour. "
            f"Dernier vaccin : Polio. Prochain rappel : Mars 2026."
        ),
        "sante_retard": lambda nom: (
            f"Bonjour {nom}. "
            f"Vos vaccinations sont en retard. "
            f"Rendez-vous au centre de santé le plus proche."
        ),
        "impots_ok": lambda nom: (
            f"Bonjour {nom}. "
            f"Votre situation fiscale est à jour. "
            f"Dernière déclaration : Janvier 2026."
        ),
        "impots_retard": lambda nom: (
            f"Bonjour {nom}. "
            f"Vous avez un retard fiscal. "
            f"Contactez l'OTR au +228 22 21 08 08."
        ),
        "agriculture_ok": lambda nom: (
            f"Bonjour {nom}. "
            f"Votre subvention agricole est approuvée. "
            f"Montant : 75 000 FCFA — versement en cours."
        ),
        "agriculture_nok": lambda nom: (
            f"Bonjour {nom}. "
            f"Votre dossier agricole est incomplet. "
            f"Contactez la DRAEP de votre région."
        ),
        "profil_complet": lambda nom: (
            f"Bonjour {nom}. Voici votre situation complète :\n"
            f"• Carte d'identité : Prête ✓\n"
            f"• Santé : À jour ✓\n"
            f"• Impôts : À jour ✓\n"
            f"• Agriculture : Subvention approuvée ✓\n"
            f"5 bases de données consultées."
        ),
    }
}


def analyse_demande_locale(question: str) -> dict:
    """
    Extrait l'ID national par regex et détecte langue + service par IA.
    """
    # 1. Extraction ID — regex, 100% fiable
    id_match = re.search(r'\bTG\d{5,}\b', question.upper())
    id_national = id_match.group(0) if id_match else None

    # 2. Détection langue + service par IA
    try:
        response = client.chat.completions.create(
            model=MODEL_IA,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyse ce message d'un citoyen togolais. "
                        "Réponds UNIQUEMENT avec ce JSON exact, sans markdown :\n"
                        '{"langue": "Ewe|Kabye|Français", "service": "carte|sante|impots|agriculture|profil_complet|inconnu"}\n\n'
                        "Règles pour service :\n"
                        "- carte : carte d'identité, CNI, pièce d'identité\n"
                        "- sante : vaccination, santé, médecin, lãm\n"
                        "- impots : NIF, taxes, fiscal, impôts, taxatsi\n"
                        "- agriculture : parcelle, subvention, champ, agble\n"
                        "- profil_complet : veut tout savoir, tous ses services, dossier complet\n"
                        "- inconnu : autre"
                    )
                },
                {"role": "user", "content": question}
            ]
        )
        texte = response.choices[0].message.content.strip()
        texte = texte.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(texte)
        langue  = parsed.get("langue", "Ewe")
        service = parsed.get("service", "inconnu")
        if langue not in ["Ewe", "Kabye", "Français"]:
            langue = "Ewe"
        if service not in ["carte", "sante", "impots", "agriculture", "profil_complet", "inconnu"]:
            service = "inconnu"
    except Exception as e:
        print(f"[Erreur IA] {e}")
        langue, service = "Ewe", "inconnu"

    return {
        "id_national":    id_national,
        "langue_detectee": langue,
        "intention":      service if id_national else "inconnu"
    }


def construire_reponse(nom: str | None, statut: str, langue: str) -> str:
    """
    Construit la réponse avec les templates hardcodés.
    Zéro IA — 100% déterministe et cohérent.
    """
    templates = REPONSES_HARDCODEES.get(langue, REPONSES_HARDCODEES["Français"])
    nom = nom or "Citoyen"

    # Mapping statut BD → clé template
    statut_lower = statut.lower()
    if statut in templates:
        return templates[statut](nom)
    elif "prête" in statut_lower or "prete" in statut_lower or "disponible" in statut_lower:
        return templates["prête"](nom)
    elif "cours" in statut_lower or "traitement" in statut_lower:
        return templates["en cours"](nom)
    elif "non trouvé" in statut_lower or "introuvable" in statut_lower or "aucun" in statut_lower:
        return templates.get("non trouvé", templates["inconnu"])(nom)
    else:
        return templates["inconnu"](nom)


# --- Tests ---
if __name__ == "__main__":
    tests = [
        "Nye carte d'identité TG012345 le klaloa?",
        "Man lãm TG067890 taa ñɩnɩɣ?",
        "Je veux tout savoir sur mon dossier TG012345",
        "Wò taxatsi TG012345",
        "Bonjour, statut agriculture TG067890",
    ]
    for t in tests:
        result = analyse_demande_locale(t)
        print(f"Input  : {t}")
        print(f"Result : {result}\n")