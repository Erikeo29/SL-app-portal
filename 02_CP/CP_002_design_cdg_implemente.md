# CP_002 - design CDG implemente, portail deploye

**Date** : 2026-05-24
**Projet** : 26_SL_AppPortal
**Statut** : EN COURS (optimisations visuelles a faire en VSCode)

---

## Actions realisees

- Init projet : CLAUDE.md (gitignore), ruff + hook PostToolUse, pyproject.toml, 8 tests pytest.
- Git init + repo GitHub public `Erikeo29/SL-app-portal` cree et pousse.
- Deploiement Streamlit Cloud sur `https://app-library.streamlit.app/`.
- Integration design CDG hifi (handoff dans `cdc/design_handoff_portail_outils/`) :
  - Hero gradient `#08111f` + motif grille + eyebrow + toggle FR/EN.
  - Pills filtres par categorie (codes ec/ed/mf/rag/pm/qv).
  - Grille cards responsive `auto-fill minmax(300px, 1fr)`, ratio 16/9, hover lift.
  - Lien admin discret `?admin=1`.
- Corrections visuelles post-retours utilisateur :
  - Titre : "Applications : modelisation, utilitaires".
  - Sous-titre : "Ouvertes et evolutives a ceux qui les trouveront utiles."
  - Badges : electrodéposition jaune clair, gestion projet bleu clair.
  - Description complete (suppression line-clamp:3).
  - Filtres : `<a href target=_self>` (sans JS) + bouton Tous + radio-select.
  - Recherche : widget Streamlit natif.
  - Toggle FR/EN : `target=_self`, position top-left.

## Resultats cles

| Element | Etat |
|---------|------|
| Tests pytest | 8/8 passes |
| Lint ruff | 0 erreur |
| Streamlit Cloud | 200 OK |
| Git | clean (3 commits) |

## Problemes rencontres

| # | Probleme | Cause | Resolu ? |
|---|----------|-------|----------|
| 1 | JS onclick bloque dans st.markdown | CSP Streamlit | Oui - remplaces par `<a href>` |
| 2 | Titre h1 invisible (gris sur noir) | Streamlit surcharge la couleur | Oui - `!important` |
| 3 | FR/EN ouvre nouvel onglet | Liens sans `target=_self` | Oui |
| 4 | Repo non visible sur Streamlit Cloud | Repo prive | Oui - passe public |

## Fichiers modifies

- `app.py` - refonte complete (CSS rdlab-, hero, filtres, cards, admin)
- `CLAUDE.md` - URL prod, architecture CSS, filtres, pieges Streamlit
- `pyproject.toml` - config ruff (nouveau)
- `tests/test_apps.py` - 8 tests validation YAML (nouveau)
- `cdc/` - handoff design CDG (nouveau)
- `.claude/settings.json` - hook ruff PostToolUse (non gite - global gitignore)

## Plan d'action

1. [ ] Optimisations visuelles fines en VSCode + CC (zoom, espacements, responsive mobile).
2. [ ] Valider FR/EN sur Streamlit Cloud (comportement different localhost possible).
3. [ ] Tester admin panel sur Streamlit Cloud (secrets.toml configure ?).
4. [ ] Ajouter `cdc/` au .gitignore si le handoff ne doit pas etre public.

## Notes

- `onclick` JS dans `st.markdown(unsafe_allow_html=True)` : bloque par CSP, confirme sur localhost et cloud. Toujours utiliser `<a href target=_self>`.
- Streamlit Cloud a ajoute un `.devcontainer/` (commit `4d30358`) lors du deploiement initial.
- Hook ruff (.claude/settings.json) fonctionnel mais non active dans la session courante (watcher ne surveille pas les dossiers crees apres demarrage). Actif a la prochaine session.
