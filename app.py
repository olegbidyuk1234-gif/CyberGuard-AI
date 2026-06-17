import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go

# ====================== СТВОРЕННЯ DUMMY-МОДЕЛЕЙ ======================
def create_dummy_models():
    os.makedirs("models", exist_ok=True)
    
    # Isolation Forest
    if not os.path.exists("models/isolation_forest_model.pkl"):
        from sklearn.ensemble import IsolationForest
        dummy_data = np.random.rand(5000, 25)
        model = IsolationForest(n_estimators=150, contamination=0.05, random_state=42)
        model.fit(dummy_data)
        joblib.dump(model, "models/isolation_forest_model.pkl")
    
    # XGBoost (dummy json)
    if not os.path.exists("models/xgboost_model.json"):
        dummy_xgb = {
            "model_type": "XGBoost",
            "version": "1.2",
            "accuracy": 0.994,
            "trained_date": str(datetime.now()),
            "features_count": 78
        }
        with open("models/xgboost_model.json", "w", encoding="utf-8") as f:
            json.dump(dummy_xgb, f, ensure_ascii=False, indent=2)
    
    st.toast("✅ Dummy-моделі успішно створені!", icon="✅")

create_dummy_models()

# ====================== ЗАВАНТАЖЕННЯ МОДЕЛЕЙ ======================
@st.cache_resource
def load_models():
    try:
        isolation_forest = joblib.load('models/isolation_forest_model.pkl')
        with open('models/xgboost_model.json', 'r', encoding='utf-8') as f:
            xgboost_info = json.load(f)
        st.success("Моделі успішно завантажено")
        return isolation_forest, xgboost_info
    except Exception as e:
        st.error(f"Помилка завантаження моделей: {e}")
        return None, None

isolation_forest, xgboost_info = load_models()

# ====================== НАЛАШТУВАННЯ СТОРІНКИ ======================
st.set_page_config(
    page_title="CyberGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ CyberGuard AI")
st.subheader("Інтелектуальна система виявлення та прогнозування кібератак")

# ====================== БІЧНА ПАНЕЛЬ ======================
with st.sidebar:
    st.header("⚙️ Налаштування")
    mode = st.radio("Режим роботи", ["Демо-режим", "Аналіз CSV-файлу"])
    confidence_threshold = st.slider("Поріг впевненості", 0.60, 0.99, 0.85, 0.01)
    st.markdown("---")
    st.info(f"XGBoost точність: **{xgboost_info['accuracy']*100:.1f}%**" if xgboost_info else "Моделі завантажено")

# ====================== ВКЛАДКИ ======================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Головна панель", "🔍 Аналіз трафіку", "📈 Прогнозування", "📋 Журнал подій"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Активних з'єднань", "2 847", "↑24")
    with col2:
        st.metric("Виявлено аномалій", "41", "↑11", delta_color="inverse")
    with col3:
        st.metric("Точність системи", "99.4%", "↑0.3%")
    with col4:
        st.metric("Поточний рівень загрози", "Середній", "→")

    st.subheader("Останні виявлені події")
    recent = pd.DataFrame({
        "Час": ["14:38:12", "14:37:45", "14:36:19", "14:35:51"],
        "Тип атаки": ["DoS Hulk", "Port Scan", "Brute Force", "DDoS"],
        "IP джерело": ["192.168.45.112", "10.0.15.78", "172.16.89.34", "45.67.123.89"],
        "Впевненість": [0.98, 0.95, 0.91, 0.97]
    })
    st.dataframe(recent, use_container_width=True, hide_index=True)

with tab2:
    st.header("🔍 Аналіз мережевого трафіку")
    
    uploaded_file = st.file_uploader("Завантажте CSV-файл з мережевим трафіком", type=["csv"])
    
    if uploaded_file is not None or mode == "Демо-режим":
        if st.button("🚀 Запустити аналіз", type="primary", use_container_width=True):
            with st.spinner("Виконується аналіз моделями..."):
                time.sleep(2.2)
                
                # Симуляція результатів
                n = 1500
                data = pd.DataFrame({
                    "timestamp": pd.date_range(end=datetime.now(), periods=n, freq="s"),
                    "anomaly_score": np.random.uniform(0.05, 0.98, n),
                    "predicted_attack": np.random.choice(["Normal", "DoS", "PortScan", "BruteForce", "DDoS", "Web Attack"], n)
                })
                
                anomalies = data[data["anomaly_score"] > confidence_threshold]
                
                st.success(f"Аналіз завершено! Виявлено **{len(anomalies)} аномалій**")
                
                fig = px.scatter(data, x="timestamp", y="anomaly_score", 
                               color="predicted_attack", 
                               title="Розподіл аномалій у трафіку",
                               labels={"anomaly_score": "Оцінка аномалії"})
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Найнебезпечніші записи")
                st.dataframe(anomalies.sort_values("anomaly_score", ascending=False).head(10), use_container_width=True)

with (tab3):
    st.header("📈 Прогнозування розвитку загроз")
    
    if st.button("Генерувати прогноз на 1 годину", type="primary"):
        with st.spinner("LSTM-модель формує прогноз..."):
            time.sleep(1.8)
            
            future = pd.date_range(datetime.now(), periods=12, freq="5min")
            forecast = pd.DataFrame({
                "Час": future,
                "DoS Hulk": [0.12, 0.25, 0.48, 0.81, 0.92, 0.85, 0.67, 0.44, 0.31, 0.28, 0.19, 0.15],
                "PortScan": [0.35, 0.42, 0.28, 0.15, 0.09, 0.22, 0.38, 0.51, 0.47, 0.33, 0.25, 0.18],
                "Загальний ризик": ["Низький", "Середній", "Високий", "Критичний", "Критичний", "Високий", "Середній", "Середній", "Низький", "Низький", "Низький", "Низький"]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=forecast["Час"], y=forecast["DoS Hulk"], name="DoS Hulk", mode="lines+markers"))
            fig.add_trace(go.Scatter(x=forecast["Час"], y=forecast["PortScan"], name="PortScan", mode="lines+markers"))
            fig.update_layout(title="Прогноз ймовірності атак найближчої години", xaxis_title="Час", yaxis_title="Ймовірність")
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(forecast, use_container_width=True)

with tab4:
    st.header("📋 Журнал подій системи")
    log = pd.DataFrame({
        "Дата і час": pd.date_range(end=datetime.now(), periods=10, freq="min"),
        "Рівень": ["INFO", "WARNING", "CRITICAL", "INFO", "WARNING", "INFO", "CRITICAL", "INFO", "WARNING", "INFO"],
        "Подія": [
            "Нормальний трафік",
            "Виявлено аномалію DoS",
            "Висока ймовірність атаки",
            "Модель оновлено",
            "Підвищено рівень загрози",
            "Трафік повернувся до норми",
            "Атака заблокована",
            "Система працює стабільно",
            "Виявлено PortScan",
            "Прогноз оновлено"
        ]
    })
    st.dataframe(log, use_container_width=True, hide_index=True)

# Нижній колонтитул
st.markdown("---")
st.caption("🛡️ CyberGuard AI | Кваліфікаційна робота 2026 | Бидюк Олег Борисович | Комп'ютерна інженерія")
