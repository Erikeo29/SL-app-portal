# Handoff design — Portail Outils Streamlit

## Vue d'ensemble

Refonte visuelle d'une application Streamlit servant de portail de liens vers des outils R&D personnels (modélisation électrochimique, microfluidique, RAG normes, gestion de projet, vision artificielle). Le ton est professionnel mais personnel — ce n'est pas un portail corporate.

## À propos des fichiers

`Maquette Portail Outils.html` est une **référence design en HTML** — un prototype haute-fidélité montrant l'apparence et le comportement attendus. **Il ne faut pas copier ce fichier dans l'app Streamlit.** La tâche est de **reproduire ce design dans l'environnement Streamlit existant** en utilisant `st.markdown(unsafe_allow_html=True)` pour injecter le CSS et le HTML.

## Fidelité

**Haute fidélité (hifi)** — couleurs exactes, typographie, espacements et interactions définis. Reproduire pixel pour pixel.

---

## Structure de la page

### Hiérarchie des blocs

```
st.set_page_config(...)          ← sidebar collapsed par défaut
st.markdown(load_css(), ...)     ← CSS global (bloc <style>)
st.markdown(render_hero(), ...)  ← Bloc 1 : hero
st.markdown(render_filters(), ...)← Bloc 2 : pills filtres
# boucle cards :
for app in filtered_apps:
    st.markdown(render_card(app), ...)
st.markdown(render_admin_link(), ...)  ← lien admin discret
```

---

## 1. Configuration Streamlit

```python
st.set_page_config(
    page_title="SimLab",          # ou titre choisi
    layout="wide",
    initial_sidebar_state="collapsed"   # ← sidebar TOUJOURS fermée par défaut
)
```

### Accès admin (sidebar)

La sidebar contient le mot de passe. Pour les visiteurs elle est invisible. Pour l'admin :

```python
# En bas de page, lien discret → ?admin=1
if st.query_params.get("admin") == "1":
    st.session_state["show_sidebar"] = True

if st.session_state.get("show_sidebar"):
    with st.sidebar:
        # ... mot de passe, administration
```

---

## 2. Font

Ajouter en tout début d'app :

```python
st.markdown(
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
    unsafe_allow_html=True
)
```

---

## 3. CSS global injectable

Copier le bloc entier dans une variable et l'injecter une seule fois :

```python
def load_css():
    return """
    <style>
    /* Copier ici tout le contenu du bloc
       "CSS INJECTABLE" de la maquette HTML
       (de la ligne "/* ── Typographie globale */"
       jusqu'à "/* FIN CSS INJECTABLE */")
    */
    </style>
    """

st.markdown(load_css(), unsafe_allow_html=True)
```

Le CSS utilise le préfixe `rdlab-` pour éviter les conflits avec les classes internes de Streamlit.

---

## 4. Bloc Hero

### Apparence
- Fond : `#08111f` avec deux radial-gradients (bleu nord-est, violet sud-ouest)
- Motif grille : `linear-gradient` 40×40px, opacité ~2.5%
- Border-radius : `16px`
- Padding : `2.6rem 3rem 2.9rem`
- Marge basse : `1.2rem`

### Toggle FR/EN (haut droite du hero)
- Position : `absolute`, `top: 1.1rem`, `right: 1.2rem`
- Conteneur : fond `rgba(255,255,255,0.07)`, border-radius `8px`, padding `3px`
- Bouton actif : fond `rgba(255,255,255,0.13)`, texte blanc
- Bouton inactif : texte `rgba(255,255,255,0.35)`
- **En Streamlit** : gérer via `st.session_state["lang"]` + `st.rerun()`

### Titre
- Taille : `2.55rem`, weight `700`, couleur `#fff`
- Fragment accentué `.a` : couleur `#93c5fd` (bleu ciel)
- Séparateur bilingue `.sep` : couleur `rgba(255,255,255,0.22)`, weight `300`

### Eyebrow (sur-titre)
- Texte : `"outils partagés"`
- Style : `0.65rem`, weight `600`, letter-spacing `0.15em`, uppercase, couleur `rgba(255,255,255,0.28)`

### Sous-titre
- Taille : `0.93rem`, weight `400`, couleur `rgba(255,255,255,0.46)`
- Max-width : `450px`, centré, line-height `1.7`

### HTML template

```python
def render_hero(lang="fr", title_html="<span class='a'>Sim</span>Lab", subtitle="Des simulations et analyses à portée de clic — explorez librement."):
    return f"""
    <div class="rdlab-hero">
      <div class="rdlab-lang">
        <button class="rdlab-lang-btn {'on' if lang=='fr' else ''}" onclick="...">FR</button>
        <button class="rdlab-lang-btn {'on' if lang=='en' else ''}" onclick="...">EN</button>
      </div>
      <div class="rdlab-hero-inner">
        <span class="rdlab-eyebrow">outils partagés</span>
        <h1 class="rdlab-title">{title_html}</h1>
        <p class="rdlab-subtitle">{subtitle}</p>
      </div>
    </div>
    """
```

---

## 5. Filtres Pills

### Principe
HTML/CSS pur — les pills sont des `<label>` wrappant un `<input type="checkbox">`. Le CSS checkbox-hack (`input:checked + .pl`) gère l'état actif/inactif sans JS.

**En production Streamlit** : utiliser `st.components.html()` pour capturer les clics et les renvoyer via `postMessage` vers `session_state`, OU utiliser des paramètres URL `?cats=ec,mf` lus par `st.query_params`.

### Couleurs des catégories (variable CSS `--c`)

| Code | Catégorie | Couleur `--c` |
|------|-----------|---------------|
| `ec` | Modélisation électrochimique | `#16a34a` (vert) |
| `mf` | Modélisation microfluidique | `#64748b` (gris) |
| `ed` | Modélisation électrodéposition | `#d97706` (jaune) |
| `rag` | Normes & RAG | `#ea580c` (orange) |
| `pm` | Gestion de projet | `#16a34a` (vert) |
| `qv` | Qualité & Vision | `#dc2626` (rouge) |

### Pill inactive (état défaut)
- Fond : transparent
- Bordure : `1.5px solid var(--c)`
- Texte : `var(--c)`

### Pill active (cochée)
- Fond : `var(--c)`
- Texte : `#fff`

### Badge compteur `.pc`
- Taille : `0.61rem`, weight `700`
- Fond inactif : `rgba(0,0,0,0.11)`
- Fond actif : `rgba(255,255,255,0.22)`

### Champ de recherche
- Hauteur : `34px`, border-radius : `9px`
- Bordure : `1.5px solid #e2e8f0`
- Focus : `border-color: #2563eb`
- Icône loupe : SVG inline en `background-image` (data URI — voir maquette)

---

## 6. Cartes

### Layout grille
- `display: grid`, `grid-template-columns: repeat(3, 1fr)`, `gap: 1.05rem`

### Carte individuelle
- Fond : `#fff`, border-radius : `14px`
- Ombre repos : `0 1px 3px rgba(0,0,0,0.06), 0 2px 10px rgba(0,0,0,0.04)`
- Ombre hover : `0 8px 28px rgba(0,0,0,0.10), 0 2px 6px rgba(0,0,0,0.05)`
- Hover : `transform: translateY(-4px)`, transition `0.18s ease`

### Thumbnail
- Ratio : `16 / 9` (aspect-ratio CSS)
- Fond par défaut : `#0d1f3c`
- Image : `object-fit: cover`

### Badge statut (overlay thumbnail, coin haut-droit)
- Fond : `rgba(0,0,0,0.50)` + `backdrop-filter: blur(6px)`
- Border-radius : `99px`, padding : `3px 9px 3px 6px`
- Point couleur : `6px` — vert `#4ade80` (ok), jaune `#fbbf24` (wip), gris `#94a3b8` (soon)
- Texte : `0.62rem`, weight `600`, uppercase

### Badge catégorie (dans le corps)

| Code | Fond | Texte |
|------|------|-------|
| `ec` | `#f0fdf4` | `#166534` |
| `mf` | `#f1f5f9` | `#475569` |
| `ed` | solide `#d97706` | `#fff` |
| `rag` | `#fff7ed` | `#9a3412` |
| `pm` | `#f0fdf4` | `#166534` |
| `qv` | solide `#dc2626` | `#fff` |

- Taille : `0.65rem`, weight `600`, border-radius `99px`, padding `2px 9px`

### Titre carte
- `0.875rem`, weight `600`, couleur `#0f172a`, line-height `1.35`

### Description
- `0.78rem`, couleur `#64748b`, line-height `1.62`
- **Limiter à 3 lignes** : `-webkit-line-clamp: 3`

### "Ouvrir l'outil →"
- Visible **seulement au hover** : `opacity: 0` → `opacity: 1` + `translateX(-5px)` → `translateX(0)`
- Couleur : couleur de la catégorie (`var(--c)`)
- Taille : `0.74rem`, weight `600`

### HTML template carte

```python
def render_card(app):
    return f"""
    <a href="{app['url']}" class="rdlab-card" target="_blank">
      <div class="rdlab-thumb">
        <img src="{app['thumbnail']}" alt="{app['title']}">
        <div class="rdlab-status" data-s="{app['status']}">
          <span class="rdlab-sdot"></span>{app['status_label']}
        </div>
      </div>
      <div class="rdlab-card-body">
        <span class="rdlab-cat" data-c="{app['cat_code']}">{app['cat_label']}</span>
        <h3 class="rdlab-card-title">{app['title']}</h3>
        <p class="rdlab-card-desc">{app['description']}</p>
        <span class="rdlab-open" style="--c:{app['cat_color']}">Ouvrir l'outil →</span>
      </div>
    </a>
    """
```

`app['status']` = `"ok"` | `"wip"` | `"soon"`

---

## 7. Lien admin discret

```python
def render_admin_link():
    return '<a href="?admin=1" class="rdlab-admin">⚙ admin</a>'
```

Style : `0.65rem`, couleur `#dce3ef` au repos → `#94a3b8` au hover. Aligné à droite.

---

## Design tokens résumé

| Token | Valeur |
|-------|--------|
| Fond page | `#f0f2f6` (Streamlit défaut) |
| Fond hero | `#08111f` |
| Accent titre | `#93c5fd` |
| Fond carte | `#ffffff` |
| Texte principal | `#0f172a` |
| Texte secondaire | `#64748b` |
| Texte muted | `#94a3b8` |
| Border repos | `#e2e8f0` |
| Font | IBM Plex Sans 300/400/500/600/700 |
| Border-radius carte | `14px` |
| Border-radius hero | `16px` |
| Border-radius pill | `999px` |

---

## Fichiers inclus

| Fichier | Description |
|---------|-------------|
| `Maquette Portail Outils.html` | Prototype haute-fidélité interactif — référence visuelle principale |
| `README.md` | Ce document |

**Ouvrir la maquette dans un navigateur** pour voir le rendu final et interagir avec les options de titre (panel bas-droite).
