"""
theme.py
=========================================================
Shared design system for "Thai MSW Analytics" (Green / Eco theme)

หลักการออกแบบ
- สีหลักเป็นเขียว (Emerald) ส่วนสีที่สื่อความหมาย (แดง/น้ำเงิน/ม่วง) คงเดิม
- ไม่พึ่งพา CSS variable ของ Streamlit (--text-color ฯลฯ) เพื่อให้ทำงานได้ทุกเวอร์ชัน
  ใช้ color: inherit และสีโปร่งใส (rgba) แทน จึงสวยทั้งโหมด Light และ Dark
- Responsive: มือถือ / แท็บเล็ต / เดสก์ท็อป
=========================================================
"""

from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#059669",   # เขียวหลักของธีม (Emerald 600)
    "success": "#10b981",   # เขียวสว่าง: นำกลับมาใช้ประโยชน์
    "danger": "#ef4444",    # แดง: กำจัดไม่ถูกต้อง / เตือน
    "warning": "#f59e0b",   # เหลือง: ระวัง
    "info": "#3b82f6",      # น้ำเงิน: กำจัดถูกต้อง
    "purple": "#8b5cf6",    # ม่วง: ขยะที่เกิดขึ้น
}

GREEN = {
    "deep": "#064e3b",
    "forest": "#047857",
    "primary": "#059669",
    "leaf": "#10b981",
    "soft": "#6ee7b7",
    "mint": "#d1fae5",
    "teal": "#0d9488",
}

# สีสำหรับแยกกลุ่ม (Categorical) ที่ไม่ได้สื่อความหมายเรื่องดี/ไม่ดี
CLUSTER_COLORS = ["#059669", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899", "#14b8a6"]

# สเกลสีเขียวสำหรับ Treemap (ค่าน้อย = เขียวอ่อน, ค่ามาก = เขียวเข้ม)
GREEN_SCALE = ["#d1fae5", "#6ee7b7", "#10b981", "#047857", "#064e3b"]

FONT_IMPORT_URL = "https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800&display=swap"

# สีเส้นขอบ/พื้นหลังแบบโปร่งใส ใช้ได้ทั้ง Light และ Dark
_BORDER = "rgba(127,127,127,0.25)"
_SURFACE = "rgba(127,127,127,0.06)"

_ROOT = Path(__file__).resolve().parent


def page_path(name: str) -> str:
    """คืน path ของไฟล์หน้า (สำหรับ st.Page / st.page_link)
    รองรับทั้งกรณีไฟล์อยู่ในโฟลเดอร์ pages/ และกรณีอยู่โฟลเดอร์เดียวกับ app.py"""
    for rel in (f"pages/{name}.py", f"{name}.py"):
        if (_ROOT / rel).exists():
            return rel
    return f"pages/{name}.py"


# ---------------------------------------------------------------------------
# Global CSS
# ---------------------------------------------------------------------------
def inject_global_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('{FONT_IMPORT_URL}');

        html, body, p, h1, h2, h3, h4, h5, h6, label, li, a, .stMarkdown {{
            font-family: 'Prompt', 'Segoe UI', sans-serif;
        }}
        .stApp {{ font-family: 'Prompt', 'Segoe UI', sans-serif; }}

        .material-symbols-rounded, .material-icons, i, svg, [class*="icon"], button span {{
            font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        }}

        .block-container, [data-testid="stMainBlockContainer"] {{ padding-bottom: 3rem; }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{ border-right: 1px solid {_BORDER}; }}
        section[data-testid="stSidebar"] h2 {{ font-size: 1.3rem; font-weight: 700; }}
        section[data-testid="stSidebar"] h3 {{ font-size: 1.02rem; font-weight: 600; }}

        /* ---------- Buttons ---------- */
        .stButton > button, .stDownloadButton > button {{
            border-radius: 10px !important;
            font-weight: 600 !important;
            border: 1px solid {_BORDER} !important;
            transition: all 0.15s ease-in-out;
            min-height: 2.6rem;
        }}
        .stButton > button:hover {{
            border-color: {COLORS['primary']} !important;
            color: {COLORS['primary']} !important;
        }}
        .stDownloadButton > button {{
            background: linear-gradient(135deg, {GREEN['leaf']}, {GREEN['forest']}) !important;
            color: white !important;
            border: none !important;
        }}
        .stDownloadButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(5,150,105,0.35);
            color: white !important;
        }}

        /* ---------- Tabs ---------- */
        button[data-baseweb="tab"] {{ font-weight: 600; font-size: 15px; font-family: 'Prompt', sans-serif; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ color: {COLORS['primary']}; }}
        div[data-baseweb="tab-highlight"] {{ background-color: {COLORS['primary']} !important; }}

        /* ---------- Containers / alerts / tables ---------- */
        details {{
            border-radius: 12px !important;
            border: 1px solid {_BORDER} !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important;
            border: 1px solid {_BORDER} !important;
        }}
        div[data-testid="stAlert"] {{ border-radius: 12px; }}
        div[data-testid="stDataFrame"] {{ border-radius: 12px; overflow: hidden; }}

        footer {{ visibility: hidden; }}

        /* ---------- Page header ---------- */
        .msw-header {{ padding: 4px 0 10px 0; }}
        .msw-header-title {{
            font-size: clamp(24px, 4.2vw, 36px); font-weight: 800; line-height: 1.25;
            display: flex; align-items: center; gap: 12px;
        }}
        .msw-header-glyph {{ flex: none; }}
        .msw-header-text {{
            background: -webkit-linear-gradient(45deg, {GREEN['primary']}, {GREEN['teal']});
            -webkit-background-clip: text; background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .msw-header-sub {{
            color: inherit; opacity: 0.72; font-size: clamp(13px, 1.9vw, 16px);
            margin-top: 6px; line-height: 1.6;
        }}

        /* ---------- Section title ---------- */
        .msw-section {{
            font-size: clamp(17px, 2.4vw, 21px); font-weight: 700; color: inherit;
            border-left: 5px solid {COLORS['primary']}; padding: 2px 0 2px 12px;
            margin: 8px 0 14px 0; line-height: 1.4;
        }}

        /* ---------- KPI card ---------- */
        .msw-kpi {{
            background: {_SURFACE};
            background: color-mix(in srgb, var(--accent) 7%, transparent);
            border: 1px solid {_BORDER}; border-left: 5px solid var(--accent);
            border-radius: 14px; padding: 16px 18px;
            display: flex; flex-direction: column;
            min-height: 128px; box-sizing: border-box; margin-bottom: 8px;
        }}
        .msw-kpi-label {{ font-size: 13px; font-weight: 600; color: inherit; opacity: 0.8; line-height: 1.4; }}
        .msw-kpi-value {{
            font-size: clamp(20px, 2.2vw, 27px); font-weight: 800; color: inherit;
            margin-top: 8px; line-height: 1.25; overflow-wrap: anywhere;
        }}
        .msw-kpi-sub {{
            display: inline-block; align-self: flex-start;
            font-size: 12.5px; font-weight: 600; color: var(--accent);
            margin-top: auto; padding: 3px 10px; border-radius: 999px;
            background: {_SURFACE};
            background: color-mix(in srgb, var(--accent) 12%, transparent);
        }}

        /* ---------- Info card ---------- */
        .msw-info {{
            background: {_SURFACE}; border: 1px solid {_BORDER}; border-left: 5px solid var(--accent);
            border-radius: 14px; padding: 16px 20px; margin: 6px 0 14px 0;
        }}
        .msw-info-title {{ font-weight: 700; color: inherit; font-size: 15px; }}
        .msw-info-text {{ color: inherit; opacity: 0.8; font-size: 14px; margin-top: 6px; line-height: 1.7; }}

        /* ---------- Empty state ---------- */
        .msw-empty {{
            text-align: center; padding: 56px 20px; border-radius: 16px;
            border: 1px dashed {_BORDER}; background: {_SURFACE};
        }}
        .msw-empty-emoji {{ font-size: 48px; }}
        .msw-empty-title {{ font-size: 19px; font-weight: 700; margin-top: 10px; color: inherit; }}
        .msw-empty-detail {{ color: inherit; opacity: 0.7; margin-top: 6px; font-size: 14px; }}

        /* ---------- Footer ---------- */
        .msw-footer {{ text-align: center; color: inherit; opacity: 0.5; font-size: 13px; padding: 6px 0 18px 0; }}

        /* ---------- Home ---------- */
        .msw-hero {{ text-align: center; padding: 8px 0 4px 0; }}
        .msw-hero-title {{
            font-size: clamp(30px, 6vw, 46px); font-weight: 800; line-height: 1.2;
        }}
        .msw-hero-text {{
            background: -webkit-linear-gradient(45deg, {GREEN['primary']}, {GREEN['teal']});
            -webkit-background-clip: text; background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .msw-hero-sub {{
            font-size: clamp(15px, 2.4vw, 20px); color: inherit; opacity: 0.8;
            margin: 6px 0 22px 0; font-weight: 500;
        }}
        .msw-nav-card {{
            background: {_SURFACE};
            background: color-mix(in srgb, var(--accent) 6%, transparent);
            border: 1px solid {_BORDER}; border-top: 4px solid var(--accent);
            border-radius: 16px; padding: 20px 20px 16px 20px;
            min-height: 150px; box-sizing: border-box; margin-bottom: 6px;
        }}
        .msw-nav-glyph {{ font-size: 30px; line-height: 1; }}
        .msw-nav-title {{ font-size: 18px; font-weight: 700; color: inherit; margin-top: 10px; }}
        .msw-nav-desc {{ font-size: 14px; color: inherit; opacity: 0.78; line-height: 1.65; margin-top: 6px; }}
        a[data-testid="stPageLink-NavLink"] {{ border-radius: 10px; font-weight: 600; }}

        /* ---------- Responsive ---------- */
        /* แท็บเล็ต: แถวที่มี 4 คอลัมน์ขึ้นไปให้แบ่งเป็น 2 คอลัมน์ต่อแถว */
        @media (min-width: 641px) and (max-width: 992px) {{
            div[data-testid="stHorizontalBlock"]:has(> div:nth-child(4)) {{ flex-wrap: wrap; }}
            div[data-testid="stHorizontalBlock"]:has(> div:nth-child(4)) > div {{
                flex: 1 1 calc(50% - 1rem); min-width: calc(50% - 1rem);
            }}
        }}
        /* มือถือ */
        @media (max-width: 640px) {{
            .msw-kpi {{ min-height: 0; padding: 14px 16px; }}
            .msw-kpi-value {{ font-size: 22px; }}
            .msw-nav-card {{ min-height: 0; }}
            .msw-empty {{ padding: 36px 16px; }}
            button[data-baseweb="tab"] {{ font-size: 14px; padding-left: 10px; padding-right: 10px; }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            .stButton > button, .stDownloadButton > button {{ transition: none; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Components
# หมายเหตุ: ใน HTML ที่ส่งเข้า st.markdown ห้ามมีบรรทัดว่าง มิฉะนั้น Markdown จะตัด block
# ---------------------------------------------------------------------------
def page_header(icon: str, title: str, subtitle: str = "") -> None:
    subtitle_html = f'<div class="msw-header-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="msw-header">
        <div class="msw-header-title"><span class="msw-header-glyph">{icon}</span><span class="msw-header-text">{title}</span></div>{subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(icon: str, text: str) -> None:
    st.markdown(f'<div class="msw-section">{icon} {text}</div>', unsafe_allow_html=True)


def kpi_card(icon: str, label: str, value: str, sub: str = "", color: str = None) -> None:
    color = color or COLORS["primary"]
    sub_html = f'<div class="msw-kpi-sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="msw-kpi" style="--accent:{color};">
        <div class="msw-kpi-label">{icon}&nbsp; {label}</div>
        <div class="msw-kpi-value">{value}</div>{sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(icon: str, title: str, text: str, color: str = None) -> None:
    color = color or COLORS["primary"]
    st.markdown(
        f"""
        <div class="msw-info" style="--accent:{color};">
        <div class="msw-info-title">{icon} {title}</div>
        <div class="msw-info-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str = "") -> None:
    """หัวเรื่องขนาดใหญ่กลางหน้า สำหรับหน้าแรก"""
    subtitle_html = f'<div class="msw-hero-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="msw-hero">
        <div class="msw-hero-title"><span class="msw-hero-text">{title}</span></div>{subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def nav_card(icon: str, title: str, desc: str, color: str = None) -> None:
    """การ์ดเมนูสำหรับหน้าแรก"""
    color = color or COLORS["primary"]
    st.markdown(
        f"""
        <div class="msw-nav-card" style="--accent:{color};">
        <div class="msw-nav-glyph">{icon}</div>
        <div class="msw-nav-title">{title}</div>
        <div class="msw-nav-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message: str = "ไม่พบข้อมูลในระบบ", detail: str = "ปรับเงื่อนไขตัวกรองแล้วลองใหม่อีกครั้ง") -> None:
    st.markdown(
        f"""
        <div class="msw-empty">
        <div class="msw-empty-emoji">🗂️</div>
        <div class="msw-empty-title">{message}</div>
        <div class="msw-empty-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


def footer(module_name: str = "") -> None:
    st.markdown("---")
    suffix = f" · {module_name}" if module_name else ""
    st.markdown(
        f'<div class="msw-footer">🇹🇭 <b>Thai MSW Analytics</b>{suffix}</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Plotly
# ---------------------------------------------------------------------------
PLOTLY_LAYOUT_DEFAULTS = dict(
    font=dict(family="Prompt, sans-serif", size=13),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=60, b=20, l=10, r=10),
    hoverlabel=dict(font_family="Prompt, sans-serif"),
    colorway=[COLORS["primary"], COLORS["info"], COLORS["purple"], COLORS["warning"], COLORS["danger"]],
)


def style_fig(fig, **overrides):
    layout = {**PLOTLY_LAYOUT_DEFAULTS, **overrides}
    fig.update_layout(**layout)
    return fig