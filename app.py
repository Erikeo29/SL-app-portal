"""
Portail Applications R&D
Configuration : data/apps.yaml
Screenshots  : assets/screenshots/<id>.png  (optionnel, <1 Mo)
Admin        : st.secrets["admin_password"]  +  ?admin=1 dans l'URL
"""

import base64
import pathlib

import streamlit as st
import yaml

# ── Chemins ────────────────────────────────────────────────────────────────────
APP_ROOT = pathlib.Path(__file__).parent
APPS_FILE = APP_ROOT / "data" / "apps.yaml"
SHOTS_DIR = APP_ROOT / "assets" / "screenshots"

# ── Codes courts catégorie (FR → code pill) ───────────────────────────────────
CAT_CODE: dict[str, str] = {
    "Modélisation électrochimique": "ec",
    "Modélisation électrodéposition": "ed",
    "Modélisation microfluidique": "mf",
    "Normes & RAG": "rag",
    "Gestion de projet": "pm",
    "Qualité & Vision": "qv",
}

# Couleur CSS par code (pour --c dans les cards)
CAT_COLOR: dict[str, str] = {
    "ec": "#16a34a",
    "ed": "#ca8a04",
    "mf": "#64748b",
    "rag": "#ea580c",
    "pm": "#16a34a",
    "qv": "#dc2626",
}

# Mapping status YAML → data-s HTML
STATUS_S: dict[str, str] = {"live": "ok", "dev": "wip", "hidden": "soon"}

# ── Textes UI FR / EN ─────────────────────────────────────────────────────────
UI: dict[str, dict[str, str]] = {
    "fr": {
        "title_html": "<span class='a'>Applications</span> : modélisation, utilitaires",
        "eyebrow": "outils partagés",
        "subtitle": "Ouvertes et évolutives à ceux qui les trouveront utiles.",
        "sleep_note": "Note : les applications se mettent en veille après ~24h d'inactivité. Cliquer sur \"Yes, get this app back up\" et attendre 10-30 sec de chargement.",
        "search": "Rechercher...",
        "no_result": "Aucune application ne correspond aux filtres.",
        "open": "Ouvrir l'outil →",
        "s_ok": "Disponible",
        "s_wip": "En développement",
        "s_soon": "Masqué",
        "admin_title": "Administration",
        "admin_on": "Mode admin actif.",
        "admin_logout": "Se déconnecter",
        "admin_pwd": "Mot de passe",
        "admin_login": "Connexion",
        "admin_save": "► Enregistrer les statuts",
        "admin_saved": "Statuts enregistrés.",
        "admin_panel": "Panneau admin — statuts des applications",
    },
    "en": {
        "title_html": "<span class='a'>Applications</span>: modelling, utilities",
        "eyebrow": "shared tools",
        "subtitle": "Open and evolving, for those who will find them useful.",
        "sleep_note": "Note: applications go to sleep after ~24h of inactivity. Click \"Yes, get this app back up\" and wait 10-30 sec to reload.",
        "search": "Search...",
        "no_result": "No application matches the selected filters.",
        "open": "Open tool →",
        "s_ok": "Available",
        "s_wip": "In development",
        "s_soon": "Hidden",
        "admin_title": "Administration",
        "admin_on": "Admin mode active.",
        "admin_logout": "Log out",
        "admin_pwd": "Password",
        "admin_login": "Log in",
        "admin_save": "► Save statuses",
        "admin_saved": "Statuses saved.",
        "admin_panel": "Admin panel — application statuses",
    },
}

# ── CSS injectable (préfixe rdlab-) ───────────────────────────────────────────
CSS = """
<style>
.rdlab-hero, .rdlab-filters, .rdlab-grid, .rdlab-card, .rdlab-admin {
  font-family: 'IBM Plex Sans', 'Segoe UI', system-ui, sans-serif;
}

@keyframes rdlab-shimmer {
  0%   { background-position: 0%   50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0%   50%; }
}

/* HERO */
.rdlab-hero {
  position: relative;
  background: linear-gradient(135deg, #2c2c2c 0%, #546e7a 40%, #90a4ae 70%, #2c2c2c 100%);
  background-size: 200% 200%;
  animation: rdlab-shimmer 8s ease infinite;
  border-radius: 16px;
  padding: 0.5rem 3rem 0.5rem;
  margin-bottom: 1.2rem;
  overflow: hidden;
}
.rdlab-hero::after { display: none; }
.rdlab-hero-inner { position: relative; z-index: 1; text-align: center; }
.rdlab-title {
  font-size: 2.55rem; font-weight: 700; color: #fff !important;
  letter-spacing: -0.03em; line-height: 1.05; margin: 0 0 0.3rem 0 !important;
  text-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.rdlab-title .a   { color: #fff; }
.rdlab-title .sep { color: rgba(255,255,255,0.40); font-weight: 300; margin: 0 0.18em; }
.rdlab-subtitle-row {
  display: flex; align-items: center; justify-content: center;
  column-gap: 2.5rem; flex-wrap: nowrap; margin: 0.2rem auto 0 !important;
}
.rdlab-subtitle {
  font-size: 1.05rem; font-weight: 400; font-style: italic; color: rgba(255,255,255,0.82);
  line-height: 1.7; letter-spacing: 0.01em; margin: 0 !important; flex-shrink: 0;
}
.rdlab-sleep-note {
  font-size: 0.73rem; color: rgba(255,255,255,0.52); font-style: italic;
  white-space: nowrap; margin: 0 !important;
  border-left: 1px solid rgba(255,255,255,0.20); padding-left: 1.2rem;
}

/* Réduction espace supérieur Streamlit */
div[data-testid="stMainBlockContainer"],
div.block-container { padding-top: 2rem !important; }


/* FILTRES PILLS */
.rdlab-filters {
  display: flex; align-items: center; gap: 0.7rem; margin-bottom: 1.4rem; flex-wrap: wrap;
}
.rdlab-pills { display: flex; flex-wrap: wrap; gap: 0.4rem; flex: 1; min-width: 0; }
.rdlab-pill {
  display: inline-flex; align-items: center; gap: 0.32rem;
  padding: 0.28rem 0.82rem; border-radius: 999px;
  border: 1.5px solid var(--c, #475569); color: var(--c, #475569);
  background: transparent; text-decoration: none !important;
  font-family: 'IBM Plex Sans', system-ui, sans-serif;
  font-size: 0.77rem; font-weight: 500; cursor: pointer; user-select: none;
  white-space: nowrap; transition: background 0.13s, color 0.13s, opacity 0.13s;
}
.rdlab-pill.active { background: var(--c, #475569); color: #fff; }
.rdlab-pill:hover { opacity: 0.78; }
.rdlab-pill.active:hover { opacity: 0.88; }
.rdlab-pill .pc {
  font-size: 0.61rem; font-weight: 700; min-width: 15px; height: 15px;
  border-radius: 99px; display: inline-flex; align-items: center; justify-content: center;
  background: rgba(0,0,0,0.11);
}
.rdlab-pill.active .pc { background: rgba(255,255,255,0.22); }
.rdlab-pill[data-c=all] { --c: #475569; }
.rdlab-pill[data-c=ec]  { --c: #16a34a; }
.rdlab-pill[data-c=mf]  { --c: #64748b; }
.rdlab-pill[data-c=ed]  { --c: #ca8a04; }
.rdlab-pill[data-c=rag] { --c: #ea580c; }
.rdlab-pill[data-c=pm]  { --c: #1d4ed8; }
.rdlab-pill[data-c=qv]  { --c: #dc2626; }
.rdlab-search {
  height: 34px; background: #fff; border: 1.5px solid #e2e8f0; border-radius: 9px;
  padding: 0 0.9rem 0 2.05rem;
  font-family: 'IBM Plex Sans', system-ui, sans-serif;
  font-size: 0.8rem; color: #0f172a; min-width: 180px; outline: none;
  transition: border-color 0.14s;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='13' height='13' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: 0.58rem center;
}
.rdlab-search:focus { border-color: #2563eb; }
.rdlab-search::placeholder { color: #94a3b8; }

/* GRILLE CARDS */
.rdlab-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.05rem; }

.rdlab-card {
  display: flex; flex-direction: column; background: #fff; border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 2px 10px rgba(0,0,0,0.04);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  text-decoration: none !important; color: inherit; cursor: pointer;
}
.rdlab-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 28px rgba(0,0,0,0.10), 0 2px 6px rgba(0,0,0,0.05);
}
.rdlab-card, .rdlab-card *, .rdlab-card *:hover { text-decoration: none !important; }
.rdlab-card-dev  { opacity: 0.65; filter: grayscale(30%); }
.rdlab-card-hidden { opacity: 0.30; border: 2px dashed #ccc; cursor: not-allowed; }
.rdlab-card-hidden:hover { transform: none !important; }

.rdlab-thumb {
  width: 100%; aspect-ratio: 16 / 9; background: #0d1f3c;
  position: relative; overflow: hidden; flex-shrink: 0;
}
.rdlab-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.rdlab-thumb-placeholder {
  width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
}
.rdlab-abbrev {
  font-size: 1.4rem; font-weight: 800; color: #fff; opacity: 0.9;
  font-family: monospace; letter-spacing: 0.05em;
}

.rdlab-status {
  position: absolute; top: 0.5rem; right: 0.5rem;
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(0,0,0,0.50); backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px); border-radius: 99px; padding: 3px 9px 3px 6px;
  font-size: 0.62rem; font-weight: 600; color: #fff;
  letter-spacing: 0.05em; text-transform: uppercase;
  opacity: 0; transition: opacity 0.18s;
}
.rdlab-card:hover .rdlab-status { opacity: 1; }
.rdlab-card-dev .rdlab-status, .rdlab-card-hidden .rdlab-status { opacity: 1 !important; }
.rdlab-sdot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.rdlab-status[data-s=ok]   .rdlab-sdot { background: #4ade80; }
.rdlab-status[data-s=wip]  .rdlab-sdot { background: #fbbf24; }
.rdlab-status[data-s=soon] .rdlab-sdot { background: #94a3b8; }

.rdlab-card-body {
  padding: 0.85rem 1rem 1rem; display: flex; flex-direction: column; gap: 0.38rem; flex: 1;
}
.rdlab-cat {
  display: inline-flex; align-items: center; padding: 2px 9px; border-radius: 99px;
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.02em; width: fit-content;
}
.rdlab-cat[data-c=ec]  { background: #f0fdf4; color: #166534; }
.rdlab-cat[data-c=mf]  { background: #f1f5f9; color: #475569; }
.rdlab-cat[data-c=ed]  { background: #fef9c3; color: #854d0e; }
.rdlab-cat[data-c=rag] { background: #fff7ed; color: #9a3412; }
.rdlab-cat[data-c=pm]  { background: #eff6ff; color: #1d4ed8; }
.rdlab-cat[data-c=qv]  { background: #dc2626; color: #fff; }

.rdlab-card-title { font-size: 1.07rem !important; font-weight: 600; color: #0f172a !important; line-height: 1.35; margin-top: 0.05rem; }
.rdlab-card-desc { font-size: 0.78rem; color: #64748b; line-height: 1.62; }
.rdlab-open {
  margin-top: auto; padding-top: 0.5rem; font-size: 0.74rem; font-weight: 600;
  color: var(--c, #2563eb); display: flex; align-items: center; gap: 3px;
  opacity: 0; transform: translateX(-5px); transition: opacity 0.16s, transform 0.16s;
}
.rdlab-card:hover .rdlab-open { opacity: 1; transform: translateX(0); }

/* FOOTER (version + admin) */
.rdlab-footer {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 2.5rem; padding-top: 0.5rem;
}
.rdlab-version {
  font-size: 1.0rem; color: #94a3b8; letter-spacing: 0.03em;
}
.rdlab-admin {
  font-size: 0.65rem; color: #94a3b8;
  text-decoration: none !important; letter-spacing: 0.04em; transition: color 0.2s;
}
.rdlab-admin:hover { color: #cbd5e1; }
button[kind='segmented_controlActive']:not(:disabled) {
  background-color: #475569 !important; color: #fff !important;
}
</style>
"""


# ── Helpers ────────────────────────────────────────────────────────────────────
def lang() -> str:
    return st.session_state.get("_lang", "fr")


def u(key: str) -> str:
    return UI[lang()][key]


def t(app: dict, key: str) -> str:
    if lang() == "en":
        return app.get(f"{key}_en") or app.get(key, "")
    return app.get(key, "")


# ── Chargement config ──────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_apps() -> list[dict]:
    with open(APPS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f).get("apps", [])


# ── Vignette (st.image pour statiques, crossfade CSS pour multi-frames) ────────
def _crossfade_html(frames: list[pathlib.Path], app_id: str, app_name: str) -> str:
    n = len(frames)
    hold  = 4.0   # secondes de visibilité pleine par frame
    fade  = 1.4   # durée du fondu enchaîné (simultané entre A et B)
    total = n * hold

    uid_base = f"cf_{app_id.replace('-', '_').replace('.', '_')}"
    imgs   = ""
    styles = ""

    def pct(t: float) -> float:
        return round((t % total) / total * 100, 2)

    for i, p in enumerate(frames):
        uid_i = f"{uid_base}_{i}"
        # Fenêtres temporelles de ce frame dans le cycle
        t_fade_out_start = (i + 1) * hold - fade   # début fondu sortant
        t_fade_out_end   = (i + 1) * hold           # fin fondu sortant
        t_fade_in_start  = i * hold - fade           # début fondu entrant (négatif pour i=0 → wrapping)

        if n == 1:
            kf = f"@keyframes {uid_i}{{0%,100%{{opacity:1}}}}"
        elif i == 0:
            # fade-in wraps autour du début du cycle (de ~100% à 0%)
            # 0%        → opacity:1   (fin du fade-in en provenance du dernier frame)
            # p_fo_s %  → opacity:1   (début fade-out)
            # p_fo_e %  → opacity:0   (fin fade-out)
            # p_fi_s %  → opacity:0   (début fade-in pour le prochain loop)
            # 100%      → opacity:1   (fin fade-in, rejoint 0%)
            p_fo_s = pct(t_fade_out_start)
            p_fo_e = pct(t_fade_out_end)
            p_fi_s = pct(t_fade_in_start)   # = pct(total - fade)
            kf = (
                f"@keyframes {uid_i}{{"
                f"0%,{p_fo_s}%{{opacity:1}}"
                f"{p_fo_e}%,{p_fi_s}%{{opacity:0}}"
                f"100%{{opacity:1}}"
                f"}}"
            )
        elif i == n - 1:
            # fade-out wraps autour de la fin du cycle (de ~90% à 0% du cycle suivant)
            p_fi_s = pct(t_fade_in_start)
            p_fi_e = pct(i * hold)
            p_fo_s = pct(t_fade_out_start)
            kf = (
                f"@keyframes {uid_i}{{"
                f"0%,{p_fi_s}%{{opacity:0}}"
                f"{p_fi_e}%,{p_fo_s}%{{opacity:1}}"
                f"100%{{opacity:0}}"
                f"}}"
            )
        else:
            p_fi_s = pct(t_fade_in_start)
            p_fi_e = pct(i * hold)
            p_fo_s = pct(t_fade_out_start)
            p_fo_e = pct(t_fade_out_end)
            kf = (
                f"@keyframes {uid_i}{{"
                f"0%,{p_fi_s}%{{opacity:0}}"
                f"{p_fi_e}%,{p_fo_s}%{{opacity:1}}"
                f"{p_fo_e}%,100%{{opacity:0}}"
                f"}}"
            )

        b64  = base64.b64encode(p.read_bytes()).decode()
        mime = "image/gif" if p.suffix == ".gif" else "image/png"
        styles += kf
        imgs += (
            f'<img src="data:{mime};base64,{b64}" '
            f'style="position:absolute;top:0;left:0;width:100%;height:100%;'
            f"object-fit:cover;display:block;opacity:{1 if i == 0 else 0};"
            f'animation:{uid_i} {total:.1f}s 0s infinite;" '
            f'alt="{app_name}">'
        )

    style = f"<style>{styles}</style>"
    return f'{style}<div class="rdlab-thumb" style="position:relative;">{imgs}</div>'


def thumb_html(app: dict) -> str:
    app_id = str(app["id"])
    cat_code = CAT_CODE.get(app.get("category", ""), "ec")
    cat_color = CAT_COLOR.get(cat_code, "#2563eb")

    # Frames crossfade (<id>_N.png / <id>_N.gif) — gif prioritaire sur png de même stem
    _all = [
        p
        for ext in ("*.png", "*.gif")
        for p in SHOTS_DIR.glob(f"{app_id}_{ext}")
        if p.stat().st_size < 1_000_000
    ]
    _by_stem: dict[str, pathlib.Path] = {}
    for p in sorted(_all, key=lambda p: (p.stem, 0 if p.suffix == ".png" else 1)):
        _by_stem[p.stem] = p
    frames = sorted(_by_stem.values(), key=lambda p: p.stem)
    if len(frames) >= 2:
        return _crossfade_html(frames, app_id, app["name"])

    # Image unique (GIF ou PNG) — servie via st.image, pas base64
    for candidate in (
        SHOTS_DIR / f"{app_id}.gif",
        SHOTS_DIR / f"{app_id}.png",
        frames[0] if frames else None,
    ):
        if candidate and candidate.exists() and candidate.stat().st_size < 1_000_000:
            b64 = base64.b64encode(candidate.read_bytes()).decode()
            mime = "image/gif" if candidate.suffix == ".gif" else "image/png"
            return (
                f'<div class="rdlab-thumb">'
                f'<img src="data:{mime};base64,{b64}" '
                f'alt="{app["name"]}" style="width:100%;height:100%;object-fit:cover;">'
                f"</div>"
            )

    # Placeholder coloré
    abbrev = app.get("abbrev", app_id.upper())
    gradient = f"linear-gradient(145deg, {cat_color}dd, {cat_color}66)"
    return (
        f'<div class="rdlab-thumb">'
        f'<div class="rdlab-thumb-placeholder" style="background:{gradient};">'
        f'<span class="rdlab-abbrev">{abbrev}</span>'
        f"</div></div>"
    )


# ── Hero ───────────────────────────────────────────────────────────────────────
def render_hero() -> str:
    return f"""
    <div class="rdlab-hero">
      <div class="rdlab-hero-inner">
        <h1 class="rdlab-title">{u("title_html")}</h1>
        <div class="rdlab-subtitle-row">
          <p class="rdlab-subtitle">{u("subtitle")}</p>
          <p class="rdlab-sleep-note">{u("sleep_note")}</p>
        </div>
      </div>
    </div>
    """


# ── Filtres pills — liens <a> purs, pas de JS ─────────────────────────────────
def render_filters(apps: list[dict], active_code: str) -> str:
    current_lang = lang()
    # Lang param inclus dans les URLs pour conserver la langue après navigation pill
    def _pill_url(cats_code: str = "") -> str:
        parts = []
        if current_lang != "fr":
            parts.append(f"lang={current_lang}")
        if cats_code:
            parts.append(f"cats={cats_code}")
        return "?" + "&".join(parts) if parts else "?"

    tous_cls = "rdlab-pill active" if not active_code else "rdlab-pill"
    tous_label = "Tous" if current_lang == "fr" else "All"
    pills_html = f'<a href="{_pill_url()}" class="{tous_cls}" data-c="all" target="_self">{tous_label}</a>'

    for cat_fr, code in CAT_CODE.items():
        count = sum(1 for a in apps if a.get("category") == cat_fr)
        if count == 0:
            continue
        cat_label = t(
            {"category": cat_fr, "category_en": _cat_en(apps, cat_fr)}, "category"
        )
        cls = "rdlab-pill active" if code == active_code else "rdlab-pill"
        pills_html += (
            f'<a href="{_pill_url(code)}" class="{cls}" data-c="{code}" target="_self">'
            f'{cat_label} <span class="pc">{count}</span></a>'
        )

    return f"""
    <div class="rdlab-filters">
      <div class="rdlab-pills">{pills_html}</div>
    </div>
    """


def _cat_en(apps: list[dict], cat_fr: str) -> str:
    return next(
        (a.get("category_en", "") for a in apps if a.get("category") == cat_fr), ""
    )


# ── Card ───────────────────────────────────────────────────────────────────────
def render_card(app: dict, is_admin: bool) -> str:
    status = app.get("status", "live")
    if status == "hidden" and not is_admin:
        return ""

    cat_fr = app.get("category", "")
    cat_code = CAT_CODE.get(cat_fr, "ec")
    cat_color = CAT_COLOR.get(cat_code, "#2563eb")
    cat_label = t(app, "category")
    data_s = STATUS_S.get(status, "ok")
    s_labels = {"ok": u("s_ok"), "wip": u("s_wip"), "soon": u("s_soon")}
    s_label = s_labels.get(data_s, u("s_ok"))
    if data_s == "wip":
        progress = int(app.get("progress", 0))
        if progress:
            s_label = f"{s_label} · {progress}%"
    title = t(app, "name")
    desc = t(app, "description")

    extra_cls = ""
    if status == "dev":
        extra_cls = " rdlab-card-dev"
    elif status == "hidden":
        extra_cls = " rdlab-card-hidden"

    # Badge : dot seul pour live, dot + texte pour dev/hidden
    _text = s_label if data_s != "ok" else ""
    _badge = (
        f'<div class="rdlab-status" data-s="{data_s}">'
        f'<span class="rdlab-sdot"></span>{_text}</div>'
    )

    body = f"""
      {thumb_html(app)}
      {_badge}
      <div class="rdlab-card-body">
        <span class="rdlab-cat" data-c="{cat_code}">{cat_label}</span>
        <h3 class="rdlab-card-title">{title}</h3>
        <p class="rdlab-card-desc">{desc}</p>
        <span class="rdlab-open" style="--c:{cat_color}">{u("open")}</span>
      </div>
    """

    if status == "hidden":
        return f'<div class="rdlab-card{extra_cls}" title="[Admin]">{body}</div>'
    return f'<a href="{app["url"]}" class="rdlab-card{extra_cls}" target="_blank" rel="noopener">{body}</a>'


# ── Sidebar admin ──────────────────────────────────────────────────────────────
def admin_sidebar() -> bool:
    with st.sidebar:
        st.markdown(f"### {u('admin_title')}")
        if st.session_state.get("_admin_ok"):
            st.success(u("admin_on"))
            if st.button(u("admin_logout")):
                st.session_state["_admin_ok"] = False
                st.rerun()
            return True

        pwd = st.text_input(u("admin_pwd"), type="password", key="admin_pwd_input")
        if st.button(u("admin_login"), key="admin_login_btn"):
            try:
                expected = st.secrets["admin_password"]
            except Exception as e:
                st.error(f"Secrets non trouvés : {e}")
                return False
            if pwd == expected:
                st.session_state["_admin_ok"] = True
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


# ── Panneau admin ──────────────────────────────────────────────────────────────
def render_admin_panel(apps: list[dict]) -> None:
    st.divider()
    st.subheader(u("admin_panel"))
    updated = [dict(a) for a in apps]

    for i, app in enumerate(updated):
        col_name, col_vis, col_type, col_pct = st.columns([4, 2, 2, 2])
        current_status = app.get("status", "live")
        is_visible = current_status != "hidden"
        is_dev = current_status == "dev"
        current_progress = int(app.get("progress", 0))

        with col_name:
            st.markdown(f"**{app.get('abbrev', app['id'])}** - {app['name']}")
            st.caption(app.get("category", ""))

        with col_vis:
            vis = st.segmented_control(
                "Affichage",
                options=["Visible", "Masqué"],
                default="Visible" if is_visible else "Masqué",
                key=f"vis_{app['id']}",
                label_visibility="collapsed",
            )

        _vis = vis or ("Visible" if is_visible else "Masqué")

        if _vis == "Visible":
            with col_type:
                app_type = st.segmented_control(
                    "Type",
                    options=["Opérationnel", "En dév."],
                    default="En dév." if is_dev else "Opérationnel",
                    key=f"type_{app['id']}",
                    label_visibility="collapsed",
                )
            _type = app_type or ("En dév." if is_dev else "Opérationnel")

            if _type == "En dév.":
                with col_pct:
                    pct_opts = list(range(0, 101, 10))
                    safe_pct = current_progress if current_progress in pct_opts else 0
                    pct = st.select_slider(
                        "Avancement",
                        options=pct_opts,
                        value=safe_pct,
                        key=f"pct_{app['id']}",
                        format_func=lambda x: f"{x}%",
                        label_visibility="collapsed",
                    )
                updated[i]["status"] = "dev"
                updated[i]["progress"] = pct
            else:
                updated[i]["status"] = "live"
                updated[i].pop("progress", None)
        else:
            updated[i]["status"] = "hidden"

    st.markdown("")
    if st.button(u("admin_save"), type="primary"):
        save_apps(updated)
        st.success(u("admin_saved"))
        st.rerun()


# ── Page principale ────────────────────────────────────────────────────────────
def main() -> None:
    st.set_page_config(
        page_title="SimLab",
        page_icon="★",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Font IBM Plex Sans
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:'
        'wght@300;400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(CSS, unsafe_allow_html=True)

    # Lecture query params
    params = st.query_params

    # Restauration langue depuis URL (survit à la navigation par pills de filtre)
    qp_lang = params.get("lang", "")
    if qp_lang in ("fr", "en") and st.session_state.get("_lang") != qp_lang:
        st.session_state["_lang"] = qp_lang

    show_admin = params.get("admin") == "1"
    if show_admin and not st.session_state.get("_sidebar_shown"):
        st.session_state["_sidebar_shown"] = True

    # Catégorie active (depuis ?cats=<code>, radio-style : une seule à la fois)
    apps = load_apps()
    CODE_TO_FR = {v: k for k, v in CAT_CODE.items()}
    active_code = params.get("cats", "")  # code court (ec, ed…) ou "" = tous
    active_cat_fr = CODE_TO_FR.get(active_code, "")

    # Admin sidebar (conditionnelle)
    is_admin = False
    if (
        show_admin
        or st.session_state.get("_sidebar_shown")
        or st.session_state.get("_admin_ok")
    ):
        is_admin = admin_sidebar()

    # Bascule FR/EN — segmented_control (segments nativement collés)
    _col_lang, _ = st.columns([1, 9])
    with _col_lang:
        _sel = st.segmented_control(
            "lang",
            options=["FR", "EN"],
            default="FR" if lang() == "fr" else "EN",
            label_visibility="collapsed",
            key="lang_seg",
        )
    if _sel and _sel.lower() != lang():
        st.session_state["_lang"] = _sel.lower()
        st.query_params["lang"] = _sel.lower()
        st.rerun()

    # Hero
    st.markdown(render_hero(), unsafe_allow_html=True)

    # Filtres (pills liens — URLs contiennent lang pour persistance)
    st.markdown(render_filters(apps, active_code), unsafe_allow_html=True)

    # Recherche texte — widget Streamlit natif
    search_label = "Filtrer par mot-clé" if lang() == "fr" else "Filter by keyword"
    search_val = st.text_input(
        search_label, placeholder=search_label + "...", label_visibility="collapsed",
        key=f"search_{lang()}"
    )

    # Filtrage
    q = search_val.strip().lower()
    visible: list[dict] = []
    for app in apps:
        if app.get("status") == "hidden" and not is_admin:
            continue
        if active_cat_fr and app.get("category") != active_cat_fr:
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
        grid = '<div class="rdlab-grid">'
        for app in visible:
            h = render_card(app, is_admin)
            if h:
                grid += h
        grid += "</div>"
        st.markdown(grid, unsafe_allow_html=True)

    # Panneau admin
    if is_admin:
        render_admin_panel(apps)

    # Footer : version + lien admin discret
    if not is_admin:
        st.markdown(
            '<div class="rdlab-footer">'
            '<span class="rdlab-version">Version 1.1.0 - April 2026 - Eric QUEAU</span>'
            '<a href="?admin=1" class="rdlab-admin">⚙ admin</a>'
            '</div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
