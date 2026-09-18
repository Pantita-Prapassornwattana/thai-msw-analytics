"""
theme.py
=========================================================
Shared design system for "Thai MSW Analytics".
=========================================================
"""

import streamlit as st

COLORS = {
    "primary": "#0ea5e9",
    "success": "#10b981",
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "info": "#3b82f6",
    "purple": "#8b5cf6",
}

FONT_IMPORT_URL = "https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800&display=swap"

def inject_global_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('{FONT_IMPORT_URL}');

        html, body, p, h1, h2, h3, h4, h5, h6, label, li, a, .stMarkdown {{
            font-family: 'Prompt', 'Segoe UI', sans-serif;
        }}

        .material-symbols-rounded, .material-icons, i, svg, [class*="icon"], button span {{
            font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        }}

        .stButton > button, .stDownloadButton > button {{
            border-radius: 10px !important;
            font-weight: 600 !important;
            border: 1px solid var(--secondary-background-color) !important;
            transition: all 0.15s ease-in-out;
        }}
        .stDownloadButton > button {{
            background: linear-gradient(135deg, {COLORS['primary']}, #0284c7) !important;
            color: white !important;
            border: none !important;
        }}
        .stDownloadButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(14,165,233,0.35);
        }}

        button[data-baseweb="tab"] {{ font-weight: 600; font-size: 15px; font-family: 'Prompt', sans-serif; }}
        div[data-baseweb="tab-highlight"] {{ background-color: {COLORS['primary']} !important; }}
        
        details {{
            border-radius: 12px !important;
            border: 1px solid var(--secondary-background-color) !important;
            background-color: var(--background-color);
        }}
        
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important;
            border: 1px solid var(--secondary-background-color) !important;
            background: var(--background-color);
        }}

        footer {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )

def page_header(icon: str, title: str, subtitle: str = "") -> None:
    subtitle_html = f'<div style="color:var(--text-color); opacity:0.7; font-size:16px; margin-top:6px;">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div style="padding:4px 0 6px 0;">
            <div style="font-size:36px; font-weight:800; display:flex; align-items:center; gap:12px;
                        background:-webkit-linear-gradient(45deg, {COLORS['primary']}, {COLORS['purple']});
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                <span style="-webkit-text-fill-color:initial;">{icon}</span><span>{title}</span>
            </div>
            {subtitle_html}
        </div>
        <div style='height:6px'></div>
        """,
        unsafe_allow_html=True,
    )

def section_title(icon: str, text: str) -> None:
    st.markdown(
        f"""
        <div style="font-size:21px; font-weight:700; color:var(--text-color);
                    border-left:5px solid {COLORS['primary']}; padding:2px 0 2px 12px;
                    margin: 8px 0 14px 0;">
            {icon} {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

def kpi_card(icon: str, label: str, value: str, sub: str = "", color: str = None) -> None:
    color = color or COLORS["primary"]
    sub_html = f'<div style="font-size:13px; font-weight:600; color:{color}; margin-top:auto; padding-top:8px;">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div style="background:var(--background-color); border-radius:14px; padding:18px 20px;
                    border:1px solid var(--secondary-background-color); border-left:5px solid {color};
                    box-shadow:0 2px 8px rgba(0,0,0,0.05); display:flex; flex-direction:column;
                    height:100%; min-height:140px;">
            <div style="font-size:13px; font-weight:600; color:var(--text-color); opacity:0.8; font-family:'Prompt', sans-serif;">
                {icon}&nbsp; {label}
            </div>
            <div style="font-size:26px; font-weight:800; color:var(--text-color); margin-top:8px; line-height:1.2;">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

def info_card(icon: str, title: str, text: str, color: str = None) -> None:
    color = color or COLORS["primary"]
    st.markdown(
        f"""
        <div style="background:var(--secondary-background-color);
                    border:1px solid var(--secondary-background-color); border-left:5px solid {color};
                    border-radius:14px; padding:16px 20px; margin: 6px 0 14px 0;
                    display:flex; flex-direction:column; height:100%; min-height:120px;">
            <div style="font-weight:700; color:var(--text-color); font-size:15px; font-family:'Prompt', sans-serif;">{icon} {title}</div>
            <div style="color:var(--text-color); opacity:0.8; font-size:14px; margin-top:6px; line-height:1.6; font-family:'Prompt', sans-serif;">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def empty_state(message: str = "ไม่พบข้อมูลในระบบ", detail: str = "ปรับเงื่อนไขตัวกรองแล้วลองใหม่อีกครั้ง") -> None:
    st.markdown(
        f"""
        <div style="text-align:center; padding:70px 20px; background:var(--background-color); border-radius:16px;
                    border:1px dashed var(--text-color); opacity:0.8;">
            <div style="font-size:52px;">🗂️</div>
            <div style="font-size:19px; font-weight:700; color:var(--text-color); margin-top:10px; font-family:'Prompt', sans-serif;">{message}</div>
            <div style="color:var(--text-color); margin-top:6px; font-size:14px; font-family:'Prompt', sans-serif;">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

def footer(module_name: str = "") -> None:
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align:center; color:var(--text-color); opacity:0.5; font-size:13px; padding:6px 0 18px 0; font-family:'Prompt', sans-serif;">
            🇹🇭 <b>Thai MSW Analytics</b>{" · " + module_name if module_name else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

PLOTLY_LAYOUT_DEFAULTS = dict(
    font=dict(family="Prompt, sans-serif", size=13),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=60, b=20, l=10, r=10),
    hoverlabel=dict(font_family="Prompt, sans-serif"),
)

def style_fig(fig, **overrides):
    layout = {**PLOTLY_LAYOUT_DEFAULTS, **overrides}
    fig.update_layout(**layout)
    return fig