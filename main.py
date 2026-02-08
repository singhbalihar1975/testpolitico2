import streamlit as st
import streamlit.components.v1 as components
import math

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Compás Político", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main .block-container { max-width: 800px; padding-top: 2rem; text-align: center; }
    
    .main-title { font-size: 55px; font-weight: 950; color: #1E3A8A; margin-bottom: 20px; text-align: center; }
    .welcome-box { background-color: #EFF6FF; border: 2px solid #3B82F6; border-radius: 15px; padding: 25px; margin-bottom: 30px; color: #1E40AF; text-align: center; }

    .q-counter { font-size: 18px; color: #64748B; font-weight: 700; margin-bottom: 10px; display: block; text-align: center; }
    
    .question-container { margin: 40px auto; min-height: 120px; display: flex; align-items: center; justify-content: center; }
    .question-text { font-size: 30px !important; font-weight: 800; color: #0F172A; line-height: 1.2; text-align: center; }

    /* Botones de Colores */
    div.stButton > button { width: 100% !important; height: 55px !important; border-radius: 12px !important; font-size: 18px !important; font-weight: 700; margin-bottom: 8px !important; border: none !important; }
    
    .stButton:nth-of-type(1) button { background-color: #059669 !important; color: white !important; } /* Totalmente acuerdo */
    .stButton:nth-of-type(2) button { background-color: #A7F3D0 !important; color: #065F46 !important; } /* Acuerdo */
    .stButton:nth-of-type(3) button { background-color: #E2E8F0 !important; color: #475569 !important; } /* Neutral */
    .stButton:nth-of-type(4) button { background-color: #FECACA !important; color: #991B1B !important; } /* Desacuerdo */
    .stButton:nth-of-type(5) button { background-color: #DC2626 !important; color: white !important; } /* Totalmente desacuerdo */
    
    .back-btn button { background-color: transparent !important; color: #64748B !important; border: 1px solid #CBD5E1 !important; height: 45px !important; margin-top: 25px !important; width: 100% !important; }

    .result-bubble { background-color: white; border-radius: 25px; padding: 40px; border: 5px solid #3B82F6; margin-bottom: 30px; text-align: center; }
    .ideology-title { font-size: 42px !important; font-weight: 900; color: #1D4ED8; text-transform: uppercase; text-align: center; margin-bottom: 10px; display: block; }
    .ideology-desc { font-size: 19px; color: #334155; line-height: 1.5; text-align: center; }
    .match-text { font-size: 24px; font-weight: 800; color: #1E40AF; margin-top: 20px; background: #DBEAFE; padding: 15px; border-radius: 15px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÍDERES (45)
LEADERS = [
    {"n": "Stalin", "x": -9, "y": 9, "c": "#C53030"}, {"n": "Hitler", "x": 8, "y": 9.5, "c": "#2D3748"},
    {"n": "Mao", "x": -9.5, "y": 8.5, "c": "#E53E3E"}, {"n": "Gandhi", "x": -6.5, "y": -7.5, "c": "#48BB78"},
    {"n": "Thatcher", "x": 7.5, "y": 6.5, "c": "#3182CE"}, {"n": "Milei", "x": 9.2, "y": -8.8, "c": "#D69E2E"},
    {"n": "Castro", "x": -8.5, "y": 7, "c": "#2F855A"}, {"n": "Friedman", "x": 8.5, "y": -6, "c": "#ECC94B"},
    {"n": "Sanders", "x": -5.5, "y": -2, "c": "#4299E1"}, {"n": "Pinochet", "x": 8.8, "y": 8, "c": "#1A202C"},
    {"n": "Chomsky", "x": -8.5, "y": -8.5, "c": "#
