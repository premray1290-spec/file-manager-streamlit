import html
from datetime import datetime
from pathlib import Path

import streamlit as st

# All files live inside this folder (safe sandbox).
WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

st.set_page_config(page_title="File Manager", page_icon="📁", layout="wide")

ICONS = {".txt": "📄", ".py": "🐍", ".md": "📝", ".json": "🧾",
         ".csv": "📊", ".html": "🌐", ".js": "⚡"}

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;700&family=Inter:wght@400;500;600&display=swap');

html, body, .stApp, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background:
        radial-gradient(900px 400px at 85% -5%, rgba(99,102,241,.22), transparent 60%),
        radial-gradient(700px 400px at -5% 10%, rgba(2,132,199,.18), transparent 60%),
        #0B1020;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1050px; }

/* ---------- hero ---------- */
.hero {
    background: linear-gradient(120deg, #0284C7 0%, #4F46E5 55%, #7C3AED 100%);
    border-radius: 22px; padding: 2rem 2.3rem; margin-bottom: 1.5rem;
    box-shadow: 0 24px 60px -24px rgba(99,102,241,.8);
}
.hero h1 { font-family: 'Outfit', sans-serif; font-size: 2.5rem; color: #fff; margin: 0; letter-spacing: -0.02em; }
.hero p { color: rgba(255,255,255,.92); margin: .4rem 0 0; font-size: 1.05rem; }

/* ---------- headings ---------- */
h2, h3 { font-family: 'Outfit', sans-serif !important; color: #FFFFFF !important; }
label p, [data-testid="stWidgetLabel"] p { color: #C9D3F0 !important; font-weight: 500; }

/* ---------- stat cards ---------- */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.6rem; }
.stat { background: #141B34; border: 1px solid #232C4F; border-radius: 16px; padding: 1.1rem 1.3rem; }
.stat .ic { font-size: 1.4rem; }
.stat .v { font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 700; color: #fff; line-height: 1.2; }
.stat .l { color: #9AA6C8; font-size: .9rem; }

/* ---------- file cards ---------- */
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 1rem; margin-top: .8rem; }
.fcard { background: #141B34; border: 1px solid #232C4F; border-radius: 16px; padding: 1.1rem 1.2rem; transition: all .2s; }
.fcard:hover { border-color: #38BDF8; transform: translateY(-3px); box-shadow: 0 14px 30px -16px rgba(56,189,248,.6); }
.fic { font-size: 1.9rem; }
.fname { font-weight: 600; color: #fff; word-break: break-all; margin-top: .35rem; }
.fmeta { color: #9AA6C8; font-size: .82rem; margin-top: .25rem; }

.chips { display: flex; gap: .6rem; flex-wrap: wrap; margin: .2rem 0 1rem; }
.chip { background: #1B2445; border: 1px solid #2B3763; color: #DDE5FF; border-radius: 999px; padding: .3rem .85rem; font-size: .85rem; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0E1430, #0B1020); border-right: 1px solid #1E2748; }
.brand { font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 700; color: #fff; }
.brand-sub { color: #8FA1B3; font-size: .85rem; margin-bottom: 1.4rem; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: .35rem; }
[data-testid="stSidebar"] [role="radiogroup"] label { border-radius: 12px; padding: .65rem .9rem; width: 100%; transition: background .15s; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: #18214A; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background: linear-gradient(90deg, #0284C7, #4F46E5); }
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label p { color: #fff !important; font-weight: 500; }

/* ---------- inputs & buttons ---------- */
input, textarea { border-radius: 10px !important; }
.stButton > button, [data-testid="stFormSubmitButton"] > button, .stDownloadButton > button {
    background: linear-gradient(90deg, #0284C7, #4F46E5); color: #fff; border: none;
    border-radius: 10px; padding: .6rem 1.5rem; font-weight: 600; transition: all .2s;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover, .stDownloadButton > button:hover {
    color: #fff; filter: brightness(1.15); transform: translateY(-1px);
}
.stButton > button:disabled { opacity: .45; }
.st-key-delete_btn button { background: linear-gradient(90deg, #DC2626, #F43F5E); }
[data-testid="stCode"] { border: 1px solid #232C4F; border-radius: 14px; }

@media (max-width: 700px) { .stats { grid-template-columns: 1fr; } .hero h1 { font-size: 1.9rem; } }
</style>
""",
    unsafe_allow_html=True,
)


# ---------- helpers ----------
def safe_path(name: str):
    clean = Path(name.strip()).name
    return WORKSPACE / clean if clean else None


def list_files():
    return sorted(p for p in WORKSPACE.iterdir() if p.is_file())


def fmt_size(n: float) -> str:
    for unit in ("B", "KB", "MB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def fmt_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")


def flash(kind: str, message: str):
    st.session_state["flash"] = (kind, message)
    st.rerun()


def pick_file(label: str):
    files = list_files()
    if not files:
        st.info("The workspace is empty. Create a file first.")
        return None
    return safe_path(st.selectbox(label, [f.name for f in files]))


def stat(icon, value, label):
    return f'<div class="stat"><div class="ic">{icon}</div><div class="v">{value}</div><div class="l">{label}</div></div>'


def file_card(f: Path):
    s = f.stat()
    icon = ICONS.get(f.suffix.lower(), "📄")
    return (f'<div class="fcard"><div class="fic">{icon}</div>'
            f'<div class="fname">{html.escape(f.name)}</div>'
            f'<div class="fmeta">{fmt_size(s.st_size)} · {fmt_time(s.st_mtime)}</div></div>')


# ---------- pages ----------
def page_files():
    files = list_files()
    total = sum(f.stat().st_size for f in files)
    latest = max((f.stat().st_mtime for f in files), default=None)

    st.markdown(
        '<div class="stats">'
        + stat("📁", len(files), "Total files")
        + stat("💾", fmt_size(total), "Total size")
        + stat("🕒", fmt_time(latest) if latest else "None yet", "Last change")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.subheader("Your files")
    query = st.text_input("Search", placeholder="🔍 Search by file name...", label_visibility="collapsed")
    shown = [f for f in files if query.lower() in f.name.lower()]

    if not files:
        st.info("No files yet. Open 'Create file' in the sidebar to add one.")
    elif not shown:
        st.warning("No files match your search.")
    else:
        st.markdown('<div class="grid">' + "".join(file_card(f) for f in shown) + "</div>",
                    unsafe_allow_html=True)


def page_create():
    st.subheader("Create a file")
    with st.form("create", clear_on_submit=True):
        name = st.text_input("File name", placeholder="notes.txt")
        data = st.text_area("Content", height=220)
        submitted = st.form_submit_button("Create file")
    if submitted:
        path = safe_path(name)
        if path is None:
            st.error("Enter a file name.")
        elif path.exists():
            st.error(f"{path.name} already exists. Pick another name or use Update file.")
        else:
            path.write_text(data, encoding="utf-8")
            flash("success", f"Created {path.name}.")


def page_read():
    st.subheader("Read a file")
    path = pick_file("Choose a file")
    if path is None:
        return
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        st.error("This is not a plain text file, so it can't be shown.")
        return
    s = path.stat()
    st.markdown(
        f'<div class="chips"><span class="chip">📏 {fmt_size(s.st_size)}</span>'
        f'<span class="chip">🧾 {len(content.splitlines())} lines</span>'
        f'<span class="chip">🕒 {fmt_time(s.st_mtime)}</span></div>',
        unsafe_allow_html=True,
    )
    st.code(content or "(empty file)", language=None)
    st.download_button("⬇ Download", content, file_name=path.name)


def page_update():
    st.subheader("Update a file")
    path = pick_file("Choose a file")
    if path is None:
        return
    mode = st.radio("What do you want to do?", ["Rename", "Append", "Overwrite"], horizontal=True)

    with st.form(f"update_{mode}_{path.name}"):
        if mode == "Rename":
            new_name = st.text_input("New name", value=path.name)
        elif mode == "Append":
            text = st.text_area("Text to add at the end of the file", height=160)
        else:
            text = st.text_area("New content", value=path.read_text(encoding="utf-8"), height=220)
        submitted = st.form_submit_button(f"{mode} file")

    if not submitted:
        return
    if mode == "Rename":
        target = safe_path(new_name)
        if target is None:
            st.error("Enter a new name.")
        elif target.exists():
            st.error(f"{target.name} already exists.")
        else:
            path.rename(target)
            flash("success", f"Renamed {path.name} to {target.name}.")
    elif mode == "Append":
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n" + text)
        flash("success", f"Added text to {path.name}.")
    else:
        path.write_text(text, encoding="utf-8")
        flash("success", f"Overwrote {path.name}.")


def page_delete():
    st.subheader("Delete a file")
    path = pick_file("Choose a file")
    if path is None:
        return
    st.warning(f"{path.name} can't be recovered after deletion.")
    confirm = st.checkbox("Yes, permanently delete this file")
    if st.button("Delete file", key="delete_btn", disabled=not confirm):
        path.unlink()
        flash("success", f"Deleted {path.name}.")


# ---------- layout ----------
PAGES = {
    "🗂️  My files": page_files,
    "➕  Create file": page_create,
    "📖  Read file": page_read,
    "✏️  Update file": page_update,
    "🗑️  Delete file": page_delete,
}

with st.sidebar:
    st.markdown('<div class="brand">📁 File Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Python + Streamlit project</div>', unsafe_allow_html=True)
    choice = st.radio("Go to", list(PAGES), label_visibility="collapsed")

st.markdown(
    '<div class="hero"><h1>File Manager</h1>'
    "<p>Create, read, update and delete text files, all in one place.</p></div>",
    unsafe_allow_html=True,
)

if "flash" in st.session_state:
    kind, message = st.session_state.pop("flash")
    if kind == "success":
        st.toast(message, icon="✅")
    else:
        getattr(st, kind)(message)

PAGES[choice]()