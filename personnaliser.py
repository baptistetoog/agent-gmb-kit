"""Recopie les 14 prompts avec les valeurs d'une fiche de paramètres, pour une entreprise donnée.

python3 personnaliser.py                       ->  lit parametres.md
python3 personnaliser.py exemples/newjump.md   ->  lit une autre fiche

Sortie : mes-prompts/<entreprise>/ (les 14 prompts prêts à coller + le document HTML).
Une valeur peut citer une autre variable (ex. {SIGNATURE} = « L'équipe {ENTREPRISE} »).
"""
import re
import sys
from pathlib import Path

import build_doc

ICI = Path(__file__).parent
VARIABLE = re.compile(r"\{[A-Z_0-9]+\}")


def lire_parametres(fichier):
    valeurs = {}
    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) >= 2 and re.fullmatch(r"\{[A-Z_0-9]+\}", cellules[0]):
            valeurs[cellules[0]] = cellules[1]
    a_completer = [k for k, v in valeurs.items() if "à compléter" in v.lower()]
    # {DEPOT_BRUT} : l'adresse des fichiers bruts du dépôt GitHub (branche main)
    m = re.match(r"https://github\.com/([^/]+)/([^/\s]+?)/?$", valeurs.get("{DEPOT}", ""))
    if m:
        valeurs["{DEPOT_BRUT}"] = f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/main"
    # les valeurs qui citent d'autres variables
    for _ in range(5):
        for k, v in valeurs.items():
            valeurs[k] = VARIABLE.sub(lambda x: valeurs.get(x.group(0), x.group(0)), v)
    return valeurs, a_completer


def remplacer(texte, valeurs):
    return VARIABLE.sub(lambda x: valeurs.get(x.group(0), x.group(0)), texte)


def main():
    fiche = Path(sys.argv[1]) if len(sys.argv) > 1 else ICI / "parametres.md"
    valeurs, a_completer = lire_parametres(fiche)

    entreprise = valeurs.get("{ENTREPRISE}", "")
    nom = re.sub(r"[^a-z0-9]+", "-", entreprise.lower()).strip("-")
    if not nom or "compléter" in entreprise.lower():
        nom = "a-completer"
    sortie = ICI / "mes-prompts" / nom
    sortie.mkdir(parents=True, exist_ok=True)

    inconnues = set()
    for p in sorted((ICI / "prompts").glob("*.md")):
        texte = remplacer(p.read_text(encoding="utf-8"), valeurs)
        inconnues |= set(VARIABLE.findall(texte))
        (sortie / p.name).write_text(texte, encoding="utf-8")

    titre = f"Prompts - Agent fiche Google - {entreprise if nom != 'a-completer' else 'à compléter'}"
    doc = build_doc.construire(sortie, sortie / f"{titre}.html", valeurs)

    print(f"Prompts écrits dans {sortie}")
    print(f"Document : {doc}")
    if a_completer:
        print("\n⚠️  Encore à compléter dans", fiche.name, ":", ", ".join(a_completer))
    if inconnues:
        print("\n⚠️  Variables sans valeur dans les prompts :", ", ".join(sorted(inconnues)))


if __name__ == "__main__":
    main()
