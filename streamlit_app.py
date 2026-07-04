import streamlit as st
import json
from snowflake.snowpark.context import get_active_session

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Value Realization Catalog",
    page_icon="❄️",
    layout="wide",
)

# ── Snowflake-branded CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Base */
  [data-testid="stAppViewContainer"] { background: #07111F; }
  [data-testid="stHeader"] { background: transparent; }
  section[data-testid="stSidebar"] {
    background: #0A1628;
    border-right: 1px solid rgba(41,181,232,0.12);
  }
  /* App header */
  .vrc-header {
    display: flex; align-items: center; gap: 14px;
    padding: 8px 0 24px;
    border-bottom: 1px solid rgba(41,181,232,0.18);
    margin-bottom: 8px;
  }
  .vrc-title { font-size: 22px; font-weight: 700; color: #FFFFFF; margin: 0; }
  .vrc-subtitle { font-size: 13px; color: rgba(255,255,255,0.5); margin: 2px 0 0; }
  /* Stat chips */
  .stat-row { display: flex; gap: 16px; margin: 16px 0 24px; }
  .stat-chip {
    background: rgba(41,181,232,0.08);
    border: 1px solid rgba(41,181,232,0.2);
    border-radius: 20px; padding: 5px 16px;
    font-size: 12px; font-weight: 600;
    color: #29B5E8; letter-spacing: .04em;
  }
  /* Cards */
  .vr-card {
    background: linear-gradient(160deg, #0D1F3A 0%, #0A1628 100%);
    border: 1px solid rgba(41,181,232,0.18);
    border-radius: 12px;
    padding: 20px;
    height: 100%;
    transition: border-color 0.2s;
    cursor: pointer;
    margin-bottom: 16px;
  }
  .vr-card:hover { border-color: rgba(41,181,232,0.5); }
  .card-persona {
    display: inline-block;
    background: rgba(41,181,232,0.12);
    border: 1px solid rgba(41,181,232,0.25);
    border-radius: 20px; padding: 3px 10px;
    font-size: 10px; font-weight: 700;
    letter-spacing: .08em; text-transform: uppercase;
    color: #29B5E8; margin-bottom: 10px;
  }
  .card-title {
    font-size: 16px; font-weight: 700;
    color: #FFFFFF; margin: 0 0 6px;
    line-height: 1.3;
  }
  .card-tagline {
    font-size: 12px; color: rgba(255,255,255,0.6);
    line-height: 1.5; margin-bottom: 12px;
  }
  .chip-row { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 14px; }
  .chip-sm {
    background: rgba(41,181,232,0.08);
    border: 1px solid rgba(41,181,232,0.2);
    border-radius: 4px; padding: 2px 8px;
    font-size: 10px; font-weight: 600;
    color: rgba(41,181,232,0.9);
  }
  .card-footer {
    font-size: 11px; color: rgba(255,255,255,0.3);
    border-top: 1px solid rgba(41,181,232,0.08);
    padding-top: 10px; margin-top: 4px;
  }
  /* Dialog overrides */
  [data-testid="stDialog"] > div {
    background: #0A1628 !important;
    border: 1px solid rgba(41,181,232,0.25) !important;
    border-radius: 14px !important;
    max-width: 900px !important;
  }
  [data-testid="stDialog"] h2 { color: #FFFFFF !important; }
  .detail-section-label {
    font-size: 10px; font-weight: 700; letter-spacing: .12em;
    text-transform: uppercase; color: #29B5E8;
    margin-bottom: 10px;
  }
  .bullet-item {
    display: flex; gap: 10px; align-items: flex-start;
    font-size: 13px; color: rgba(255,255,255,0.8);
    line-height: 1.5; margin-bottom: 8px;
  }
  .bullet-arrow { color: #29B5E8; flex-shrink: 0; font-size: 10px; margin-top: 3px; }
  .outcome-badge {
    background: rgba(41,181,232,0.08);
    border: 1px solid rgba(41,181,232,0.2);
    border-radius: 8px; padding: 8px 12px;
    font-size: 12px; font-weight: 600;
    color: #FFFFFF; margin-bottom: 6px;
  }
  .step-row { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 10px; }
  .step-num {
    width: 22px; height: 22px; border-radius: 50%;
    background: #29B5E8; color: #07111F;
    font-size: 11px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .step-text { font-size: 13px; color: rgba(255,255,255,0.8); line-height: 1.5; }
  /* Sidebar labels */
  .sb-label {
    font-size: 10px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: #29B5E8;
    margin-bottom: 8px; display: block;
  }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_resource
def get_session():
    return get_active_session()


@st.cache_data(ttl=120)
def load_catalog():
    session = get_session()
    rows = session.sql("""
        SELECT
            REPO, PROJECT_NAME, PERSONA, TAGLINE, SUMMARY,
            CHALLENGE_HEADING, CAPABILITY_HEADING, OUTCOME_HEADING,
            CHIPS, BULLETS, OUTCOMES, NEXT_STEPS,
            URL, SLIDE_HTML,
            TO_CHAR(LAST_UPDATED_AT, 'Mon DD, YYYY') AS UPDATED
        FROM AFE.TEST.VALUE_REALIZATION_CATALOG
        ORDER BY LAST_UPDATED_AT DESC
    """).collect()

    catalog = []
    for r in rows:
        def parse_arr(val):
            if val is None:
                return []
            if isinstance(val, (list, tuple)):
                return list(val)
            try:
                return json.loads(str(val))
            except Exception:
                return [str(val)]

        catalog.append({
            "repo":               r["REPO"],
            "project_name":       r["PROJECT_NAME"] or r["REPO"],
            "persona":            r["PERSONA"] or "",
            "tagline":            r["TAGLINE"] or "",
            "summary":            r["SUMMARY"] or "",
            "challenge_heading":  r["CHALLENGE_HEADING"] or "",
            "capability_heading": r["CAPABILITY_HEADING"] or "",
            "outcome_heading":    r["OUTCOME_HEADING"] or "",
            "chips":              parse_arr(r["CHIPS"]),
            "bullets":            parse_arr(r["BULLETS"]),
            "outcomes":           parse_arr(r["OUTCOMES"]),
            "next_steps":         parse_arr(r["NEXT_STEPS"]),
            "url":                r["URL"] or "",
            "slide_html":         r["SLIDE_HTML"] or "",
            "updated":            r["UPDATED"] or "",
        })
    return catalog


# ── App header ────────────────────────────────────────────────────────────────

st.markdown("""
<div class="vrc-header">
  <svg width="36" height="36" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M28 4L34.5 15.5L28 27L21.5 15.5L28 4Z" fill="#29B5E8"/>
    <path d="M28 29L34.5 40.5L28 52L21.5 40.5L28 29Z" fill="#29B5E8"/>
    <path d="M4 28L15.5 21.5L27 28L15.5 34.5L4 28Z" fill="#29B5E8"/>
    <path d="M29 28L40.5 21.5L52 28L40.5 34.5L29 28Z" fill="#29B5E8"/>
    <path d="M9.5 9.5L20 17.5L20 28L11.5 22.5L9.5 9.5Z" fill="#11567F"/>
    <path d="M46.5 9.5L45 22.5L36.5 28L36.5 17.5L46.5 9.5Z" fill="#11567F"/>
    <path d="M9.5 46.5L11.5 33.5L20 28L20 38.5L9.5 46.5Z" fill="#11567F"/>
    <path d="M46.5 46.5L36.5 38.5L36.5 28L45 33.5L46.5 46.5Z" fill="#11567F"/>
  </svg>
  <div>
    <div class="vrc-title">Value Realization Catalog</div>
    <div class="vrc-subtitle">Snowflake solution slides — browse, filter, and preview</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading catalog..."):
    catalog = load_catalog()

personas = sorted(set(r["persona"] for r in catalog if r["persona"]))
all_chips = sorted(set(c for r in catalog for c in r["chips"]))

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="sb-label">Search</span>', unsafe_allow_html=True)
    search = st.text_input("search", placeholder="Search projects...", label_visibility="collapsed")

    st.markdown('<span class="sb-label" style="margin-top:16px;display:block">Persona</span>', unsafe_allow_html=True)
    persona_filter = st.multiselect("persona", personas, label_visibility="collapsed")

    st.divider()
    if st.button("Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = catalog
if search:
    q = search.lower()
    filtered = [
        r for r in filtered
        if q in r["project_name"].lower()
        or q in r["tagline"].lower()
        or q in r["summary"].lower()
        or any(q in c.lower() for c in r["chips"])
        or q in r["repo"].lower()
    ]
if persona_filter:
    filtered = [r for r in filtered if r["persona"] in persona_filter]

# ── Stats row ─────────────────────────────────────────────────────────────────
total = len(catalog)
showing = len(filtered)
persona_counts = {}
for r in catalog:
    persona_counts[r["persona"]] = persona_counts.get(r["persona"], 0) + 1

stats_html = f'<div class="stat-row"><span class="stat-chip">{showing} of {total} solutions</span>'
for p, cnt in sorted(persona_counts.items(), key=lambda x: -x[1])[:4]:
    stats_html += f'<span class="stat-chip">{p}: {cnt}</span>'
stats_html += "</div>"
st.markdown(stats_html, unsafe_allow_html=True)

# ── Detail dialog ────────────────────────────────────────────────────────────
@st.dialog("Solution Details", width="large")
def show_detail(entry):
    st.markdown(f"""
    <span class="card-persona">{entry['persona']}</span>
    <h2 style="color:#FFFFFF;margin:10px 0 4px;font-size:22px;font-weight:700">{entry['project_name']}</h2>
    <p style="color:rgba(255,255,255,0.55);font-size:13px;margin-bottom:14px">{entry['tagline']}</p>
    <p style="color:rgba(255,255,255,0.8);font-size:13px;line-height:1.6;margin-bottom:14px">{entry['summary']}</p>
    <div class="chip-row">{''.join(f'<span class="chip-sm">{c}</span>' for c in entry['chips'])}</div>
    """, unsafe_allow_html=True)

    st.divider()

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown('<div class="detail-section-label">Business Challenge</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:10px">{entry["challenge_heading"]}</div>', unsafe_allow_html=True)
        st.markdown("".join(
            f'<div class="bullet-item"><span class="bullet-arrow">▸</span><span>{b}</span></div>'
            for b in entry["bullets"]
        ), unsafe_allow_html=True)

    with d2:
        st.markdown('<div class="detail-section-label">Business Outcomes</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:13px;font-weight:600;color:#FFFFFF;margin-bottom:10px">{entry["outcome_heading"]}</div>', unsafe_allow_html=True)
        for o in entry["outcomes"]:
            st.markdown(f'<div class="outcome-badge">{o}</div>', unsafe_allow_html=True)

    with d3:
        st.markdown('<div class="detail-section-label">Next Steps</div>', unsafe_allow_html=True)
        for i, s in enumerate(entry["next_steps"]):
            st.markdown(
                f'<div class="step-row"><div class="step-num">{i+1}</div><div class="step-text">{s}</div></div>',
                unsafe_allow_html=True,
            )

    if entry["slide_html"]:
        with st.expander("Full slide preview"):
            st.components.v1.html(entry["slide_html"], height=740, scrolling=False)

    if entry["url"]:
        st.markdown(
            f'<a href="{entry["url"]}" target="_blank" style="color:#29B5E8;font-size:12px;text-decoration:none">→ View on GitHub</a>',
            unsafe_allow_html=True,
        )


# ── Card grid ─────────────────────────────────────────────────────────────────
if not filtered:
    st.info("No solutions match your filters.")
else:
    COLS = 3
    rows_of_cards = [filtered[i : i + COLS] for i in range(0, len(filtered), COLS)]

    for row in rows_of_cards:
        cols = st.columns(COLS)
        for col, entry in zip(cols, row):
            with col:
                chips_html = "".join(
                    f'<span class="chip-sm">{c}</span>' for c in entry["chips"][:5]
                )
                more = len(entry["chips"]) - 5
                if more > 0:
                    chips_html += f'<span class="chip-sm">+{more}</span>'

                st.markdown(f"""
                <div class="vr-card">
                  <span class="card-persona">{entry['persona']}</span>
                  <div class="card-title">{entry['project_name']}</div>
                  <div class="card-tagline">{entry['tagline']}</div>
                  <div class="chip-row">{chips_html}</div>
                  <div class="card-footer">Updated {entry['updated']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    "View details",
                    key=f"btn_{entry['repo']}",
                    use_container_width=True,
                ):
                    show_detail(entry)
