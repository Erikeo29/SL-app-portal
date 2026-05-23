# CP_001 - Création du portail AppPortal

**Date** : 2026-05-23 20:30
**Projet** : 26_SL_AppPortal
**Statut** : TERMINÉ (local) - déploiement Streamlit Cloud à faire

---

## Actions réalisées

- Création complète de `26_SL_AppPortal/` : `app.py`, `data/apps.yaml`, `.streamlit/config.toml`, `requirements.txt`, `.gitignore`.
- Configuration des 11 apps SL déployées avec URLs réelles (récupérées depuis les READMEs GitHub).
- Génération de vignettes Pillow stylisées (`scripts/generate_previews.py`) par catégorie : voltamogramme, vecteurs flux, barres RAG, Gantt, grille vision.
- Support crossfade CSS (N frames PNG/GIF mélangés, `<id>_1.png/_2.png...`, cycle 4 s par frame).
- Support GIF animé (`<id>.gif`) et PNG statique (`<id>.png`) avec priorité crossfade > GIF > PNG > placeholder.
- Compression automatique des GIFs lourds (ffmpeg : fps=8, scale=480, 48-64 couleurs).
- Mode admin : `st.text_input` + `st.button`, mot de passe via `st.secrets["admin_password"]`, panneau de toggle des statuts live/dev/hidden avec sauvegarde YAML.
- Toggle FR/EN complet : textes UI, noms, descriptions, catégories. Recherche bilingue simultanée.
- Fix CSS underline : `text-decoration: none !important` sur `.pcard *` pour surcharger le CSS global Streamlit.
- `object-fit: contain` pour afficher les screenshots en entier (pas de crop).

## Résultats clés

| Métrique | Valeur | Verdict |
|----------|--------|---------|
| Apps configurées | 11 (10 live, 1 hidden) | ✓ |
| Taille max fichier image | 976 Ko (03_2.gif) | ✓ < 1 Mo |
| Frames crossfade app 03 | 3 (03_1.gif, 03_2.gif, 03_4.gif) | ✓ |
| Frames crossfade app 04a | 3 (04a_1.gif, 04a_2.gif, 04a_3.png) | ✓ |
| Langues | FR / EN | ✓ |
| App locale | http://localhost:8510 | ✓ HTTP 200 |

## Problèmes rencontrés

| # | Problème | Cause | Résolu ? |
|---|----------|-------|----------|
| 1 | Mot de passe admin rejeté | Inversion S/X dans la saisie (HC_LSX vs HC_LXS) | ✓ (diagnostic hex) |
| 2 | Crossfade inactif | `ext.lstrip('*')` supprimait le `*` du glob pattern | ✓ |
| 3 | Hot-reload background peu fiable | Streamlit watch en mode `&` | ✓ (restart explicite) |
| 4 | Screenshots coupés | `object-fit: cover` crop au centre | ✓ → `contain` |
| 5 | `st.form` + `st.rerun()` boucle | Form modifié en `st.button` + `st.text_input` | ✓ |
| 6 | `st.secrets.get()` silencieux | Remplacé par `st.secrets["key"]` (bracket) | ✓ |

## Fichiers modifiés

- `26_SL_AppPortal/app.py` - app principale complète
- `26_SL_AppPortal/data/apps.yaml` - 11 apps FR+EN, catégories réelles
- `26_SL_AppPortal/scripts/generate_previews.py` - générateur vignettes Pillow
- `26_SL_AppPortal/.streamlit/secrets.toml` - mot de passe admin (non commité)
- `26_SL_AppPortal/.streamlit/config.toml` - thème bleu
- `26_SL_AppPortal/.gitignore` - exclut secrets.toml
- `26_SL_AppPortal/assets/screenshots/` - vignettes générées + frames utilisateur

## Plan d'action (prochaines étapes)

1. [ ] Créer le repo GitHub `SL-app-portal` et pousser le code.
2. [ ] Déployer sur Streamlit Cloud, configurer `admin_password` dans les Secrets.
3. [ ] Remplacer les vignettes Pillow par de vrais screenshots pour les apps sans frames utilisateur (20a, 20b, 21, 22, 23, 24).
4. [ ] Ajouter `04b_*.png/gif` (aucune frame utilisateur actuellement).
5. [ ] Vérifier les URLs déployées (apps Streamlit Cloud potentiellement en veille).

## Décisions prises

- `object-fit: contain` plutôt que `cover` pour les screenshots (montrer l'app entière).
- Crossfade CSS pur (pas JS - interdit dans `st.markdown`).
- Convention nommage `<id>_N.ext` pour crossfade (glob `<id>_*.png` + `<id>_*.gif`, GIF gagne sur PNG même index).
- Admin sauvegarde dans YAML local (pas de DB) - sur Streamlit Cloud, les changements admin survivent à la session mais pas au redéploiement.
- FR/EN via `st.session_state["_lang"]` + `st.rerun()` légitime (changement de mode UI).

## Notes

- Streamlit natif `/usr/bin/python3` v1.56.0 (pas conda base qui n'a pas streamlit).
- Lancer depuis `26_SL_AppPortal/` : `cd 26_SL_AppPortal && /usr/bin/python3 ~/.local/bin/streamlit run app.py --server.port 8510`.
- Le `.gitignore` exclut `.streamlit/secrets.toml` - ne pas committer le mot de passe.
