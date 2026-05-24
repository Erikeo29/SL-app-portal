# CP_003 - UX badges, statuts admin et hero

**Date** : 2026-05-24 ~17h
**Projet** : 26_SL_AppPortal
**Statut** : TERMINÉ

---

## Actions réalisées

- Système de statuts admin refondé : sélecteur 2 niveaux (visible/masqué + opérationnel/en dév.) + slider % avancement (0-100, pas 10).
- Champ optionnel `progress` ajouté dans apps.yaml pour les apps dev.
- Apps dev : rendues cliquables (`<a>` au lieu de `<div>`), opacité 0.65, grayscale 30%.
- Badges statut : masqués par défaut (`opacity: 0`), révélés au hover (`opacity: 1`, transition 0.18s). Dot seul pour live, dot + texte pour dev/hidden.
- Badge dev : affiche le % d'avancement si défini ("En développement · 60%").
- Hero : note veille SL ajoutée en ligne avec le subtitle (flex row, `column-gap`, `flex-wrap: nowrap`).
- Segmented control FR/EN : couleur sélectionné `#475569` (même que pill "Tous").
- Espacements hero resserrés : padding 0.5rem haut/bas, marges titre/subtitle forcées avec `!important`.

## Résultats clés

| Élément | Avant | Après |
|---------|-------|-------|
| Admin statuts | selectbox 3 options | segmented_control 2 niveaux + slider % |
| Apps dev | bloquées (div, cursor:not-allowed) | cliquables (a href) |
| Badges | toujours visibles | hover only (live), toujours visibles (dev/hidden) |
| Hero note | absente | 1 ligne à droite du subtitle |
| FR/EN actif | couleur primaire Streamlit | #475569 |

## Fichiers modifiés

- `app.py` - refonte complète UX badges, admin panel, hero, CSS.
- `data/apps.yaml` - reformaté par yaml.dump (contenu identique, ordre préservé).

## Problèmes rencontrés

| # | Problème | Cause | Résolu ? |
|---|----------|-------|----------|
| 1 | Badge live toujours visible sur 1 carte | Fond clair de la capture rendait le badge visible même à opacity 1 | ✓ - opacity 0 par défaut |
| 2 | Note hero sur 4 lignes | `gap: 2.5rem` avec `flex-wrap: wrap` créait row-gap | ✓ - column-gap + nowrap |
| 3 | Segmented control CSS sans effet | Sélecteur `:has(input:checked)` non applicable | ✓ - `button[kind='segmented_controlActive']` |
| 4 | Marges hero sans effet avec !important | `gap` du flex container, pas les marges | ✓ - diagnostic corrigé |

## Décisions prises

- Apps dev cliquables : le badge "En développement · XX%" suffit comme indicateur, pas besoin de bloquer l'accès.
- Note veille SL : texte exact imposé par l'utilisateur, placement ligne subtitle via flex nowrap.
- Couleur #475569 pour segmented control : cohérence visuelle avec les pills de filtres.

## Notes

- Le sélecteur `button[kind='segmented_controlActive']` est spécifique à Streamlit 1.56 et peut changer en version majeure suivante.
- `flex-wrap: nowrap` sur `.rdlab-subtitle-row` peut faire déborder sur très petits écrans - acceptable car l'app est desktop-first.
