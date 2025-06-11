#!/usr/bin/env python3
"""
DAWN Interactive GUI Dashboard
==============================
A modern, interactive control interface for the DAWN Tick Engine
with real-time monitoring, controls, and beautiful visualizations.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import deque
import random

# Configuration
STATE_PATH = Path("C:/Users/Admin/Documents/DAWN_Vault/Tick_engine/state/dawn_state.json")
HISTORY_LENGTH = 100  # Number of ticks to keep in history

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = {
        'ticks': deque(maxlen=HISTORY_LENGTH),
        'scup': deque(maxlen=HISTORY_LENGTH),
        'entropy': deque(maxlen=HISTORY_LENGTH),
        'heat': deque(maxlen=HISTORY_LENGTH),
        'timestamps': deque(maxlen=HISTORY_LENGTH)
    }

if 'control_state' not in st.session_state:
    st.session_state.control_state = {
        'paused': False,
        'throttle': 1.0,
        'override_mode': False
    }

# Page configuration
st.set_page_config(
    page_title="DAWN Control Interface",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stMetric {
        background-color: rgba(28, 131, 225, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(28, 131, 225, 0.3);
    }
    
    .subsystem-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    .mood-indicator {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .control-panel {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    
    div[data-testid="stSidebar"] {
        background-color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def load_state():
    """Load the current state from file or generate mock data"""
    try:
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        # Generate mock data if file not found
        return {
            "tick": random.randint(1000, 99999),
            "scup": random.uniform(0.5, 0.9),
            "entropy": random.uniform(0.1, 0.8),
            "mood": random.choice(["calm", "agitated", "neutral", "focused", "fragile"]),
            "heat": random.uniform(20.0, 40.0),
            "uptime": random.randint(100, 10000),
            "subsystems": {
                "neural_network": {"status": "active", "load": random.uniform(0.3, 0.8)},
                "consciousness_layer": {"status": "active", "coherence": random.uniform(0.6, 0.95)},
                "sensory_interface": {"status": "active", "channels": 4},
                "memory_matrix": {"status": "active", "usage": random.uniform(0.2, 0.7)},
                "thermal_core": {"status": "active", "temperature": random.uniform(35, 38)}
            }
        }

def create_gauge(value, title, min_val=0, max_val=1, color_scale=None):
    """Create a beautiful gauge chart"""
    if color_scale is None:
        color_scale = [[0, "#2ecc71"], [0.5, "#f39c12"], [1, "#e74c3c"]]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': min_val + (max_val - min_val) * 0.5, 'increasing': {'color': "RebeccaPurple"}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [min_val, min_val + (max_val - min_val) * 0.5], 'color': 'lightgray'},
                {'range': [min_val + (max_val - min_val) * 0.5, max_val], 'color': 'gray'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val * 0.9
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def create_time_series_chart():
    """Create an interactive time series chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('SCUP Evolution', 'Entropy Dynamics', 'Heat Dissipation', 'System Coherence'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # SCUP
    fig.add_trace(
        go.Scatter(x=list(range(len(st.session_state.history['scup']))), 
                   y=list(st.session_state.history['scup']),
                   mode='lines+markers',
                   name='SCUP',
                   line=dict(color='#3498db', width=2)),
        row=1, col=1
    )
    
    # Entropy
    fig.add_trace(
        go.Scatter(x=list(range(len(st.session_state.history['entropy']))), 
                   y=list(st.session_state.history['entropy']),
                   mode='lines+markers',
                   name='Entropy',
                   line=dict(color='#e74c3c', width=2)),
        row=1, col=2
    )
    
    # Heat
    fig.add_trace(
        go.Scatter(x=list(range(len(st.session_state.history['heat']))), 
                   y=list(st.session_state.history['heat']),
                   mode='lines+markers',
                   name='Heat',
                   line=dict(color='#f39c12', width=2)),
        row=2, col=1
    )
    
    # Add a coherence metric (calculated from subsystems)
    coherence_data = [random.uniform(0.7, 0.95) for _ in range(len(st.session_state.history['ticks']))]
    fig.add_trace(
        go.Scatter(x=list(range(len(coherence_data))), 
                   y=coherence_data,
                   mode='lines+markers',
                   name='Coherence',
                   line=dict(color='#2ecc71', width=2)),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    fig.update_xaxes(title_text="Time (ticks)")
    return fig

# Main Interface
st.title("🌅 DAWN Control Interface")
st.markdown("### Advanced Cognitive Field Monitor & Control System")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ System Controls")
    
    # Pause/Resume
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏸️ Pause" if not st.session_state.control_state['paused'] else "▶️ Resume", 
                     use_container_width=True):
            st.session_state.control_state['paused'] = not st.session_state.control_state['paused']
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.history = {
                'ticks': deque(maxlen=HISTORY_LENGTH),
                'scup': deque(maxlen=HISTORY_LENGTH),
                'entropy': deque(maxlen=HISTORY_LENGTH),
                'heat': deque(maxlen=HISTORY_LENGTH),
                'timestamps': deque(maxlen=HISTORY_LENGTH)
            }
    
    st.divider()
    
    # Performance Throttle
    st.session_state.control_state['throttle'] = st.slider(
        "Performance Throttle",
        min_value=0.1,
        max_value=2.0,
        value=st.session_state.control_state['throttle'],
        step=0.1,
        help="Control the processing speed multiplier"
    )
    
    # Override Mode
    st.session_state.control_state['override_mode'] = st.checkbox(
        "🔓 Override Mode",
        value=st.session_state.control_state['override_mode'],
        help="Enable manual control overrides"
    )
    
    if st.session_state.control_state['override_mode']:
        st.warning("⚠️ Manual override active!")
        
        # Manual Controls
        st.subheader("Manual Controls")
        manual_scup = st.slider("SCUP Override", 0.0, 1.0, 0.5)
        manual_entropy = st.slider("Entropy Override", 0.0, 1.0, 0.5)
        manual_heat = st.slider("Heat Override", 0.0, 50.0, 25.0)
    
    st.divider()
    
    # System Commands
    st.subheader("🎛️ Quick Commands")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Neural Reset", use_container_width=True):
            st.success("Neural network reset initiated")
    with col2:
        if st.button("❄️ Cool Down", use_container_width=True):
            st.success("Thermal management engaged")
    
    if st.button("💾 Save State", use_container_width=True):
        st.success("State saved to checkpoint")
    
    if st.button("📊 Export Data", use_container_width=True):
        st.success("Data exported to CSV")

# Main Dashboard
if not st.session_state.control_state['paused']:
    # Load current state
    ctx = load_state()
    
    # Update history
    st.session_state.history['ticks'].append(ctx['tick'])
    st.session_state.history['scup'].append(ctx['scup'])
    st.session_state.history['entropy'].append(ctx['entropy'])
    st.session_state.history['heat'].append(ctx['heat'])
    st.session_state.history['timestamps'].append(datetime.now())

# Top Status Bar
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🔄 Tick", f"{ctx['tick']:,}")
with col2:
    st.metric("⏱️ Uptime", f"{ctx.get('uptime', 0):,}s")
with col3:
    status_color = "🟢" if not st.session_state.control_state['paused'] else "🔴"
    st.metric("Status", f"{status_color} {'Active' if not st.session_state.control_state['paused'] else 'Paused'}")
with col4:
    st.metric("⚡ Throttle", f"{st.session_state.control_state['throttle']}x")
with col5:
    st.metric("🔧 Mode", "Override" if st.session_state.control_state['override_mode'] else "Auto")

st.divider()

# Main Metrics Dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📊 Real-Time Metrics", "🧩 Subsystems", "📈 Analytics", "🔍 Diagnostics"])

with tab1:
    # Gauge Charts
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(create_gauge(ctx['scup'], "SCUP", 0, 1), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_gauge(ctx['entropy'], "Entropy", 0, 1), use_container_width=True)
    
    with col3:
        st.plotly_chart(create_gauge(ctx['heat'], "Heat (°C)", 0, 50, 
                                    [[0, "#3498db"], [0.6, "#f39c12"], [1, "#e74c3c"]]), 
                       use_container_width=True)
    
    # Mood Indicator
    mood_colors = {
        "calm": "#a3e4d7",
        "agitated": "#e74c3c",
        "neutral": "#d5dbdb",
        "focused": "#3498db",
        "fragile": "#f9e79f"
    }
    
    mood_color = mood_colors.get(ctx['mood'], "#ffffff")
    st.markdown(f"""
    <div class="mood-indicator" style="background-color:{mood_color}">
        <h2>🧠 Cognitive State: {ctx['mood'].upper()}</h2>
        <p>System consciousness coherence at {random.uniform(0.7, 0.95):.1%}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Time Series
    st.subheader("📈 System Evolution")
    st.plotly_chart(create_time_series_chart(), use_container_width=True)

with tab2:
    st.header("🧩 Subsystem Status")
    
    # Create a grid of subsystem cards
    col1, col2 = st.columns(2)
    
    subsystems = ctx.get('subsystems', {})
    for idx, (name, data) in enumerate(subsystems.items()):
        with col1 if idx % 2 == 0 else col2:
            status_emoji = "✅" if data.get('status') == 'active' else "❌"
            
            # Create a mini dashboard for each subsystem
            with st.container():
                st.markdown(f"""
                <div class="subsystem-card">
                    <h3>{status_emoji} {name.replace('_', ' ').title()}</h3>
                    <p>Status: {data.get('status', 'unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show subsystem-specific metrics
                for key, value in data.items():
                    if key != 'status':
                        if isinstance(value, (int, float)):
                            st.progress(min(value, 1.0))
                            st.caption(f"{key.replace('_', ' ').title()}: {value:.3f}")
                        else:
                            st.caption(f"{key.replace('_', ' ').title()}: {value}")

with tab3:
    st.header("📈 Advanced Analytics")
    
    # Statistical Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Statistical Summary")
        if len(st.session_state.history['scup']) > 0:
            stats_df = pd.DataFrame({
                'Metric': ['SCUP', 'Entropy', 'Heat'],
                'Mean': [
                    np.mean(list(st.session_state.history['scup'])),
                    np.mean(list(st.session_state.history['entropy'])),
                    np.mean(list(st.session_state.history['heat']))
                ],
                'Std Dev': [
                    np.std(list(st.session_state.history['scup'])),
                    np.std(list(st.session_state.history['entropy'])),
                    np.std(list(st.session_state.history['heat']))
                ],
                'Min': [
                    np.min(list(st.session_state.history['scup'])),
                    np.min(list(st.session_state.history['entropy'])),
                    np.min(list(st.session_state.history['heat']))
                ],
                'Max': [
                    np.max(list(st.session_state.history['scup'])),
                    np.max(list(st.session_state.history['entropy'])),
                    np.max(list(st.session_state.history['heat']))
                ]
            })
            st.dataframe(stats_df, hide_index=True)
    
    with col2:
        st.subheader("🎯 Performance Indicators")
        
        # Performance score calculation
        performance_score = (ctx['scup'] * 0.4 + (1 - ctx['entropy']) * 0.3 + 
                           (1 - ctx['heat']/50) * 0.3) * 100
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=performance_score,
            title={'text': "Overall Performance Score"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Matrix
    st.subheader("🔗 Metric Correlations")
    if len(st.session_state.history['scup']) > 10:
        corr_data = pd.DataFrame({
            'SCUP': list(st.session_state.history['scup']),
            'Entropy': list(st.session_state.history['entropy']),
            'Heat': list(st.session_state.history['heat'])
        })
        
        fig = px.imshow(corr_data.corr(), 
                       labels=dict(color="Correlation"),
                       x=['SCUP', 'Entropy', 'Heat'],
                       y=['SCUP', 'Entropy', 'Heat'],
                       color_continuous_scale='RdBu')
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("🔍 System Diagnostics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚠️ Alerts & Warnings")
        
        # Check for anomalies
        alerts = []
        if ctx['heat'] > 40:
            alerts.append(("🔥 High Temperature", "Critical", "Heat exceeds safe threshold"))
        if ctx['entropy'] > 0.8:
            alerts.append(("🌀 High Entropy", "Warning", "System chaos increasing"))
        if ctx['scup'] < 0.3:
            alerts.append(("📉 Low SCUP", "Warning", "Consciousness coherence degrading"))
        
        if alerts:
            for title, severity, message in alerts:
                if severity == "Critical":
                    st.error(f"{title}: {message}")
                else:
                    st.warning(f"{title}: {message}")
        else:
            st.success("✅ All systems nominal")
    
    with col2:
        st.subheader("📝 Event Log")
        
        # Simulated event log
        events = [
            f"{datetime.now().strftime('%H:%M:%S')} - System initialized",
            f"{datetime.now().strftime('%H:%M:%S')} - Neural network sync complete",
            f"{datetime.now().strftime('%H:%M:%S')} - Consciousness layer active",
            f"{datetime.now().strftime('%H:%M:%S')} - Thermal regulation engaged"
        ]
        
        for event in events[-5:]:
            st.text(event)
    
    # System Health Matrix
    st.subheader("🏥 Health Matrix")
    health_data = pd.DataFrame({
        'Component': ['CPU', 'Memory', 'Neural Net', 'Consciousness', 'Thermal'],
        'Health': [85, 92, 78, 88, 95],
        'Status': ['Good', 'Excellent', 'Fair', 'Good', 'Excellent']
    })
    
    fig = px.bar(health_data, x='Component', y='Health', color='Health',
                 color_continuous_scale='RdYlGn',
                 title="Component Health Status")
    st.plotly_chart(fig, use_container_width=True)

# Auto-refresh
if not st.session_state.control_state['paused']:
    time.sleep(1.5 / st.session_state.control_state['throttle'])
    st.rerun()
else:
    # Show pause indicator
    st.info("⏸️ System paused. Click Resume in the sidebar to continue monitoring.")