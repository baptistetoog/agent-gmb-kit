"""Compile le README et les 14 prompts en un document HTML, à importer dans Google Docs.

python3 build_doc.py  ->  livrable/Prompts - Agent fiche Google (kit générique).html  (variables entre accolades)
personnaliser.py s'en sert aussi pour le document d'une entreprise (valeurs remplacées, couleurs de sa charte).
"""
import html
import re
from pathlib import Path

ICI = Path(__file__).parent
SORTIE = ICI / "livrable" / "Prompts - Agent fiche Google (kit générique).html"
E = html.escape


def inline(t):
    t = E(t)
    t = re.sub(r"`([^`]+)`", r'<code>\1</code>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
    return t


def md(texte):
    """Markdown simple des fichiers de prompts : titres, listes, tableaux, blocs de code."""
    out, liste, tableau, code, lang = [], None, [], None, ""
    def fermer_liste():
        nonlocal liste
        if liste:
            out.append(f"</{liste}>")
            liste = None
    def fermer_tableau():
        nonlocal tableau
        if tableau:
            lignes = [l for l in tableau if not re.match(r"^\|\s*-", l)]
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in lignes]
            h = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f"<table><tr>{h}</tr>{b}</table>")
            tableau = []
    for ligne in texte.split("\n"):
        if code is not None:
            if ligne.strip() == "```":
                classe = "prompt" if not lang else "cmd"
                titre = "Prompt à coller dans Claude Code" if not lang else "Commande à lancer dans le terminal"
                out.append(f'<div class="{classe}"><div class="lab">{titre}</div><pre>{E(chr(10).join(code))}</pre></div>')
                code = None
            else:
                code.append(ligne)
            continue
        if ligne.startswith("```"):
            fermer_liste(); fermer_tableau()
            code, lang = [], ligne[3:].strip()
            continue
        if ligne.startswith("|"):
            fermer_liste(); tableau.append(ligne); continue
        fermer_tableau()
        if ligne.startswith("# "):
            fermer_liste(); out.append(f"<h1>{inline(ligne[2:])}</h1>")
        elif ligne.startswith("## "):
            fermer_liste(); out.append(f"<h2>{inline(ligne[3:])}</h2>")
        elif ligne.strip() == "---":
            fermer_liste()
        elif re.match(r"^\s*[-*] ", ligne):
            if liste != "ul":
                fermer_liste(); out.append("<ul>"); liste = "ul"
            item = re.sub(r'^\s*[-*] ', '', ligne)
            out.append(f"<li>{inline(item)}</li>")
        elif re.match(r"^\d+\. ", ligne):
            if liste != "ol":
                fermer_liste(); out.append(f'<ol start="{ligne.split(".")[0]}">'); liste = "ol"
            item = re.sub(r'^\d+\. ', '', ligne)
            out.append(f"<li>{inline(item)}</li>")
        elif ligne.strip():
            fermer_liste(); out.append(f"<p>{inline(ligne)}</p>")
        else:
            fermer_liste()
    fermer_liste(); fermer_tableau()
    return "\n".join(out)


CSS = """
body{font-family:'DM Sans',Arial,sans-serif;color:#1F242E;max-width:820px;margin:40px auto;line-height:1.5;font-size:11pt}
h1{font-family:'Lexend Deca',Arial,sans-serif;font-weight:600;font-size:20pt;color:#1F242E;margin:36px 0 6px;padding-top:10px;border-top:3px solid #FF5C2A}
h1.titre{border:none;font-size:26pt}
h2{font-family:'Lexend Deca',Arial,sans-serif;font-weight:600;font-size:13pt;color:#FF5C2A;margin:20px 0 6px}
.badge{display:inline-block;background:#FFDB21;color:#1F242E;font-weight:700;font-size:9pt;padding:3px 10px;border-radius:20px}
.prompt,.cmd{border-radius:10px;padding:12px 16px;margin:10px 0}
.prompt{background:#FFF4EF;border-left:5px solid #FF5C2A}
.cmd{background:#FFFFFF;border:2px solid #FF5C2A;color:#1F242E}
.lab{font-size:8.5pt;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;color:#FF5C2A}
pre{white-space:pre-wrap;font-family:'DM Mono',Consolas,monospace;font-size:9.5pt;margin:0}
code{font-family:Consolas,monospace;background:#F1EEE3;padding:0 4px;border-radius:4px}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:10pt}
th,td{border:1px solid #DEDACC;padding:6px 8px;text-align:left;vertical-align:top}
th{background:#F1EEE3}
a{color:#FF5C2A}
"""


def construire(dossier, sortie, valeurs=None):
    """dossier : les prompts à compiler ; valeurs : celles de personnaliser.py (None = kit générique)."""
    valeurs = valeurs or {}
    accent = valeurs.get("{COULEUR_ACCENT}", "#FF5C2A")
    css = CSS.replace("#FF5C2A", accent) if re.fullmatch(r"#[0-9A-Fa-f]{6}", accent) else CSS
    depot = valeurs.get("{DEPOT}", "{DEPOT}")
    entreprise = valeurs.get("{ENTREPRISE}", "votre entreprise")
    prompts = sorted(Path(dossier).glob("*.md"))
    readme = (ICI / "README.md").read_text(encoding="utf-8")
    readme = readme.split("## Les prompts")[0]  # le sommaire est refait plus bas
    intro = ("Remplissez d'abord parametres.md et lancez personnaliser.py : les valeurs entre accolades seront remplacées par les vôtres."
             if not valeurs else f"Ces prompts sont déjà personnalisés pour {E(entreprise)}.")
    parties = ['<span class="badge">Toog Expertise</span>',
               f'<h1 class="titre">Créer l\'agent fiche Google de {E(entreprise)} : les prompts</h1>',
               f'<p>Les 14 étapes, dans l\'ordre. Collez chaque prompt dans Claude Code, attendez qu\'il ait fini, puis vérifiez « ce qu\'on voit à la fin » avant de passer au suivant. '
               f'{intro} Code de référence et kit : <a href="{E(depot)}">{E(depot)}</a>.</p>',
               md(readme.split("\n", 2)[2] if readme.startswith("# ") else readme)]
    sommaire = "".join(f"<li>{inline(p.read_text(encoding='utf-8').splitlines()[0].lstrip('# '))}</li>" for p in prompts)
    parties.append(f"<h2>Sommaire</h2><ol>{sommaire}</ol>")
    for p in prompts:
        parties.append(md(p.read_text(encoding="utf-8")))
    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{E(sortie.stem)}</title>'
                      f'<style>{css}</style></head><body>{"".join(parties)}</body></html>', encoding="utf-8")
    return sortie


def main():
    print(construire(ICI / "prompts", SORTIE))


if __name__ == "__main__":
    main()
