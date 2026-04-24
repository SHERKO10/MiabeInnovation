import csv
import json
from pathlib import Path


def _load_json(filename: str) -> dict:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_citoyen_info(id_national: str) -> dict:
    """Base principale — État Civil (CSV)"""
    try:
        with open('citoyens.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_National'].strip() == id_national.strip():
                    return {
                        "nom": f"{row['Prenom']} {row['Nom']}",
                        "date_naissance": row.get('Date_Naissance', ''),
                        "trouve": True
                    }
    except FileNotFoundError:
        pass
    return {"nom": None, "trouve": False}


def get_statut_carte(id_national: str) -> dict:
    data = _load_json('statut_cartes.json')
    return data.get(id_national, {"statut_demande": "non trouvé"})


def get_statut_sante(id_national: str) -> dict:
    data = _load_json('services_sante.json')
    return data.get(id_national, None)


def get_statut_impots(id_national: str) -> dict:
    data = _load_json('services_impots.json')
    return data.get(id_national, None)


def get_statut_agriculture(id_national: str) -> dict:
    data = _load_json('services_agriculture.json')
    return data.get(id_national, None)


# ── INTEROPÉRABILITÉ ─────────────────────────────────────────────────────────
def get_profil_complet(id_national: str) -> dict:
    """
    Croise TOUTES les bases de données pour un citoyen.
    C'est ça l'interopérabilité — une seule requête, toutes les infos.
    """
    identite  = get_citoyen_info(id_national)
    carte     = get_statut_carte(id_national)
    sante     = get_statut_sante(id_national)
    impots    = get_statut_impots(id_national)
    agriculture = get_statut_agriculture(id_national)

    return {
        "id_national": id_national,
        "identite":    identite,
        "carte":       carte,
        "sante":       sante,
        "impots":      impots,
        "agriculture": agriculture,
        "bases_consultees": [
            "État Civil (CSV)",
            "Cartes d'identité (JSON)",
            "Santé/DHIS2 (JSON)",
            "Impôts/OTR (JSON)",
            "Agriculture/MASA (JSON)"
        ]
    }


if __name__ == "__main__":
    import pprint
    print("=== Test interopérabilité ===")
    pprint.pprint(get_profil_complet("TG012345"))