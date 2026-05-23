"""
Portail Applications R&D
Configuration : data/apps.yaml
Screenshots  : assets/screenshots/<id>.png  (optionnel, <1 Mo)
Admin        : st.secrets["admin_password"]
"""

import base64
import pathlib

import streamlit as st
import yaml

# ── Chemins ────────────────────────────────────────────────────────────────────
APP_ROOT = pathlib.Path(__file__).parent
APPS_FILE = APP_ROOT / "data" / "apps.yaml"

# ── Palettes par catégorie (clés = valeurs FR du YAML) ────────────────────────
CAT_COLORS: dict[str, str] = {
    "Modélisation électrochimique": "#004B87",
    "Modélisation électrodéposition": "#005A9E",
    "Modélisation microfluidique": "#0077CC",
    "Normes & RAG": "#B83200",
    "Gestion de projet": "#2A6E2A",
    "Qualité & Vision": "#6E2A6E",
}

STATUS_INFO: dict[str, tuple[str, str]] = {
    "live": ("● Disponible", "#1e9e42"),
    "dev": ("◐ En développement", "#c07800"),
    "hidden": ("◯ Masqué", "#888888"),
}

# ── Textes UI FR / EN ─────────────────────────────────────────────────────────
UI: dict[str, dict[str, str]] = {
    "fr": {
        "title": "Portail Applications R&D",
        "subtitle": "application disponible",
        "subtitles": "applications disponibles",
        "search": "Nom ou description...",
        "categories": "Catégories",
        "no_result": "Aucune application ne correspond aux filtres.",
        "admin_title": "Administration",
        "admin_on": "Mode admin actif.",
        "admin_logout": "Se déconnecter",
        "admin_pwd": "Mot de passe",
        "admin_login": "Connexion",
        "admin_save": "► Enregistrer les statuts",
        "admin_saved": "Statuts enregistrés - la grille se met à jour.",
        "admin_panel": "Panneau admin - statuts des applications",
        "status_live": "● Disponible",
        "status_dev": "◐ En développement",
        "status_hid": "◯ Masqué",
    },
    "en": {
        "title": "R&D Applications Portal",
        "subtitle": "application available",
        "subtitles": "applications available",
        "search": "Name or description...",
        "categories": "Categories",
        "no_result": "No application matches the selected filters.",
        "admin_title": "Administration",
        "admin_on": "Admin mode active.",
        "admin_logout": "Log out",
        "admin_pwd": "Password",
        "admin_login": "Log in",
        "admin_save": "► Save statuses",
        "admin_saved": "Statuses saved - grid is updating.",
        "admin_panel": "Admin panel - application statuses",
        "status_live": "● Available",
        "status_dev": "◐ In development",
        "status_hid": "◯ Hidden",
    },
}


def lang() -> str:
    return st.session_state.get("_lang", "fr")


def u(key: str) -> str:
    return UI[lang()][key]


def t(app: dict, key: str) -> str:
    """Retourne le champ FR ou EN selon la langue active."""
    if lang() == "en":
        return app.get(f"{key}_en") or app.get(key, "")
    return app.get(key, "")


# ── CSS ────────────────────────────────────────────────────────────────────────
CSS = """
<style>
/* Grille responsive */
.portal-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(265px, 1fr));
    gap: 1.4rem;
    padding: 0.25rem 0;
}

/* Carte de base */
.pcard {
    border-radius: 16px;
    overflow: hidden;
    display: block;
    color: inherit;
    text-decoration: none !important;
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.08);
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}
/* Surcharge du CSS global Streamlit qui force text-decoration:underline sur <a> */
.pcard, .pcard:hover, .pcard:visited, .pcard:active,
.pcard *, .pcard *:hover {
    text-decoration: none !important;
    color: inherit;
}
.pcard:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.18);
}
.pcard-dev {
    opacity: 0.50;
    filter: grayscale(65%);
    cursor: not-allowed;
}
.pcard-dev:hover {
    transform: none !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08) !important;
}
.pcard-hidden {
    opacity: 0.28;
    border: 2px dashed #bbbbbb;
    cursor: not-allowed;
}
.pcard-hidden:hover {
    transform: none !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08) !important;
}

/* Vignette couleur ou screenshot */
.pcard-thumb-wrap {
    width: 100%;
    height: 140px;
    overflow: hidden;
    position: relative;
    background: #1a1a2e;
}
.pcard-thumb-wrap img {
    width: 100%;
    height: 140px;
    object-fit: contain;
    display: block;
}
.pcard-thumb-placeholder {
    width: 100%;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.pcard-abbrev {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: white;
    opacity: 0.92;
    text-shadow: 0 1px 4px rgba(0,0,0,0.25);
    font-family: monospace;
}
.pcard-status-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(255,255,255,0.93);
    border-radius: 12px;
    padding: 2px 9px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid rgba(0,0,0,0.10);
}

/* Corps de carte */
.pcard-body    { padding: 14px 16px 16px; }
.pcard-cat-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 9px;
    border-radius: 12px;
    margin-bottom: 8px;
}
.pcard-title   { margin: 0 0 5px; font-size: 15px; font-weight: 700; color: #1a1a2e; }
.pcard-desc    { margin: 0 0 10px; font-size: 12px; color: #555; line-height: 1.55; }

/* Hero banner */
.hero-portal {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2c50 55%, #0f3460 100%);
    border-radius: 20px;
    padding: 44px 32px 38px;
    margin-bottom: 26px;
    text-align: center;
}
.hero-portal h1 {
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 800;
    margin: 0 0 8px;
    letter-spacing: -0.3px;
}
.hero-portal .hero-sub {
    color: rgba(255,255,255,0.70);
    font-size: 1rem;
    margin: 0;
}
.hero-dots {
    color: rgba(255,255,255,0.35);
    margin: 0 6px;
}

/* Barre de filtres */
.filter-bar {
    background: #ffffff;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,0,0,0.07);
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
</style>
"""


# ── Chargement config ──────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_apps() -> list[dict]:
    with open(APPS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f).get("apps", [])


# ── Crossfade CSS (N images, 4 s par frame) ────────────────────────────────────
def _crossfade_html(frames: list, app_id: str, app_name: str) -> str:
    n = len(frames)
    step = 4  # secondes par image
    total = n * step
    x_pct = round((step - 0.8) / total * 100, 1)  # fin de la phase visible
    y_pct = round(step / total * 100, 1)  # début de la phase cachée
    uid = f"cf_{app_id.replace('-', '_').replace('.', '_')}"

    style = (
        f"<style>@keyframes {uid}{{"
        f"0%,{x_pct}%{{opacity:1}}"
        f"{y_pct}%,100%{{opacity:0}}"
        f"}}</style>"
    )
    imgs = ""
    for i, p in enumerate(frames):
        b64 = base64.b64encode(p.read_bytes()).decode()
        delay = i * step
        mime = "image/gif" if p.suffix == ".gif" else "image/png"
        imgs += (
            f'<img src="data:{mime};base64,{b64}" '
            f'style="position:absolute;top:0;left:0;width:100%;height:140px;'
            f"object-fit:contain;display:block;opacity:{1 if i == 0 else 0};"
            f'animation:{uid} {total}s {delay}s infinite;" '
            f'alt="{app_name}">'
        )
    return (
        f'{style}<div class="pcard-thumb-wrap" style="position:relative;">{imgs}</div>'
    )


# ── Rendu vignette ─────────────────────────────────────────────────────────────
def thumb_html(app: dict) -> str:
    cat_color = CAT_COLORS.get(app.get("category", ""), "#4A90D9")
    app_id = str(app["id"])
    shots_dir = APP_ROOT / "assets" / "screenshots"

    # Priorité 1 : crossfade - PNG et GIF mélangés (<id>_*.png / <id>_*.gif), triés par stem
    _all = [
        p
        for ext in ("*.png", "*.gif")
        for p in shots_dir.glob(f"{app_id}_{ext}")
        if p.stat().st_size < 1_000_000
    ]
    # déduplique par stem (même index en png et gif : on garde le gif)
    _by_stem: dict[str, pathlib.Path] = {}
    for p in sorted(_all, key=lambda p: (p.stem, 0 if p.suffix == ".png" else 1)):
        _by_stem[p.stem] = p  # png traité en premier, gif écrase (last-write wins)
    frames = sorted(_by_stem.values(), key=lambda p: p.stem)
    if len(frames) >= 2:
        return _crossfade_html(frames, app_id, app["name"])

    # Priorité 2 : GIF animé
    gif_path = shots_dir / f"{app_id}.gif"
    if gif_path.exists() and gif_path.stat().st_size < 1_000_000:
        b64 = base64.b64encode(gif_path.read_bytes()).decode()
        return (
            f'<div class="pcard-thumb-wrap">'
            f'<img src="data:image/gif;base64,{b64}" '
            f'style="width:100%;height:140px;object-fit:cover;display:block;" '
            f'alt="{app["name"]}"></div>'
        )

    # Priorité 3 : PNG statique
    png_path = shots_dir / f"{app_id}.png"
    if png_path.exists() and png_path.stat().st_size < 1_000_000:
        b64 = base64.b64encode(png_path.read_bytes()).decode()
        return (
            f'<div class="pcard-thumb-wrap">'
            f'<img src="data:image/png;base64,{b64}" '
            f'style="width:100%;height:140px;object-fit:cover;display:block;" '
            f'alt="{app["name"]}"></div>'
        )

    # Priorité 4 : placeholder coloré généré
    abbrev = app.get("abbrev", app_id.upper())
    gradient = f"linear-gradient(145deg, {cat_color}dd, {cat_color}88)"
    return (
        f'<div class="pcard-thumb-wrap">'
        f'<div class="pcard-thumb-placeholder" style="background:{gradient};">'
        f'<span class="pcard-abbrev">{abbrev}</span>'
        f"</div></div>"
    )


# ── Rendu carte ────────────────────────────────────────────────────────────────
def card_html(app: dict, is_admin: bool) -> str:
    status = app.get("status", "live")
    if status == "hidden" and not is_admin:
        return ""

    cat = app.get("category", "")
    cat_disp = t(app, "category")
    cat_color = CAT_COLORS.get(cat, "#4A90D9")
    s_map = {
        "live": u("status_live"),
        "dev": u("status_dev"),
        "hidden": u("status_hid"),
    }
    s_color_map = {"live": "#1e9e42", "dev": "#c07800", "hidden": "#888888"}
    s_label = s_map.get(status, u("status_live"))
    s_color = s_color_map.get(status, "#1e9e42")

    inner = (
        f"{thumb_html(app)}"
        f'<span class="pcard-status-badge" style="color:{s_color};">{s_label}</span>'
        f'<div class="pcard-body">'
        f'<span class="pcard-cat-tag" style="background:{cat_color}1a;color:{cat_color};">{cat_disp}</span>'
        f'<p class="pcard-title">{t(app, "name")}</p>'
        f'<p class="pcard-desc">{t(app, "description")}</p>'
        f"</div>"
    )

    if status == "live":
        return f'<a href="{app["url"]}" target="_blank" rel="noopener" class="pcard">{inner}</a>'
    elif status == "dev":
        tooltip = (
            "In development - not yet available."
            if lang() == "en"
            else "En cours de développement."
        )
        return f'<div class="pcard pcard-dev" title="{tooltip}">{inner}</div>'
    else:
        return f'<div class="pcard pcard-hidden" title="[Admin]">{inner}</div>'


# ── Sidebar admin ──────────────────────────────────────────────────────────────
def admin_sidebar() -> bool:
    with st.sidebar:
        # Toggle FR / EN
        st.markdown("---")
        col_fr, col_en = st.columns(2)
        with col_fr:
            if st.button(
                "FR",
                use_container_width=True,
                type="primary" if lang() == "fr" else "secondary",
            ):
                st.session_state["_lang"] = "fr"
                st.rerun()
        with col_en:
            if st.button(
                "EN",
                use_container_width=True,
                type="primary" if lang() == "en" else "secondary",
            ):
                st.session_state["_lang"] = "en"
                st.rerun()
        st.markdown("---")

        st.markdown(f"### {u('admin_title')}")
        if st.session_state.get("_admin_ok"):
            st.success(u("admin_on"))
            if st.button(u("admin_logout")):
                st.session_state._admin_ok = False
            return bool(st.session_state.get("_admin_ok"))

        pwd = st.text_input(u("admin_pwd"), type="password", key="admin_pwd_input")
        if st.button(u("admin_login"), key="admin_login_btn"):
            try:
                expected = st.secrets["admin_password"]
            except Exception as e:
                st.error(f"Secrets non trouvés : {e}")
                return False
            if pwd == expected:
                st.session_state._admin_ok = True
                st.rerun()
            else:
                st.error(
                    "Mot de passe incorrect." if lang() == "fr" else "Wrong password."
                )
    return False


# ── Sauvegarde YAML ────────────────────────────────────────────────────────────
def save_apps(apps: list[dict]) -> None:
    with open(APPS_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["apps"] = apps
    with open(APPS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f, allow_unicode=True, sort_keys=False, default_flow_style=False
        )
    load_apps.clear()


# ── Panneau admin (bas de page) ────────────────────────────────────────────────
def render_admin_panel(apps: list[dict]) -> None:
    st.divider()
    st.subheader(u("admin_panel"))

    STATUS_OPTIONS = ["live", "dev", "hidden"]
    STATUS_LABELS_ADMIN = {"live": "🟢 live", "dev": "🟡 dev", "hidden": "⚫ hidden"}

    updated = [dict(a) for a in apps]  # copie pour modifications

    for i, app in enumerate(updated):
        col_name, col_cat, col_sel = st.columns([4, 2, 2])
        with col_name:
            st.markdown(f"**{app.get('abbrev', '')}** - {app['name']}")
        with col_cat:
            st.caption(app.get("category", ""))
        with col_sel:
            current = app.get("status", "dev")
            new_status = st.selectbox(
                "Statut",
                options=STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(current),
                format_func=lambda s: STATUS_LABELS_ADMIN[s],
                key=f"status_{app['id']}",
                label_visibility="collapsed",
            )
            updated[i]["status"] = new_status

    st.markdown("")
    if st.button(u("admin_save"), type="primary"):
        save_apps(updated)
        st.success(u("admin_saved"))
        st.rerun()


# ── Page principale ────────────────────────────────────────────────────────────
def main() -> None:
    st.set_page_config(
        page_title="Portail Applications R&D",
        page_icon="★",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(CSS, unsafe_allow_html=True)

    apps = load_apps()
    is_admin = admin_sidebar()

    # Hero banner
    n_live = sum(1 for a in apps if a.get("status") == "live")
    sub_word = u("subtitles") if n_live != 1 else u("subtitle")
    cats_live = sorted(
        {
            t(a, "category")
            for a in apps
            if a.get("status") == "live" and a.get("category")
        }
    )
    tagline = '<span class="hero-dots">·</span>'.join(cats_live) if cats_live else ""
    sep = '<span class="hero-dots">·</span>'
    tagline_html = (sep + tagline) if tagline else ""
    st.markdown(
        f'<div class="hero-portal">'
        f"<h1>★ {u('title')}</h1>"
        f'<p class="hero-sub">{n_live} {sub_word}{tagline_html}</p>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # Filtres - options en FR (clés internes) mais affichage traduit
    all_cats_fr = sorted({a.get("category", "") for a in apps if a.get("category")})
    cat_labels = {
        c: (
            t(
                {
                    "category": c,
                    "category_en": next(
                        (
                            a.get("category_en", "")
                            for a in apps
                            if a.get("category") == c
                        ),
                        "",
                    ),
                },
                "category",
            )
        )
        for c in all_cats_fr
    }

    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col_cat, col_search = st.columns([4, 2])
    with col_cat:
        sel_cats = st.multiselect(
            u("categories"),
            options=all_cats_fr,
            default=all_cats_fr,
            format_func=lambda c: cat_labels.get(c, c),
            label_visibility="collapsed",
            key=f"cats_{lang()}",
        )
    with col_search:
        search = st.text_input(
            "search",
            placeholder=u("search"),
            label_visibility="collapsed",
            key=f"search_{lang()}",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Filtrage (recherche dans les deux langues)
    visible: list[dict] = []
    q = search.strip().lower()
    for app in apps:
        if app.get("status") == "hidden" and not is_admin:
            continue
        if sel_cats and app.get("category") not in sel_cats:
            continue
        if q and not any(
            q in (app.get(f, "") or "").lower()
            for f in ("name", "name_en", "description", "description_en")
        ):
            continue
        visible.append(app)

    if not visible:
        st.info(u("no_result"))
    else:
        grid = '<div class="portal-grid">'
        for app in visible:
            h = card_html(app, is_admin)
            if h:
                grid += h
        grid += "</div>"
        st.markdown(grid, unsafe_allow_html=True)

    if is_admin:
        render_admin_panel(apps)


if __name__ == "__main__":
    main()
