"""Streamlit dashboard entry point and page router."""

from __future__ import annotations

import streamlit as st

from components.theme import inject_css
from utils.data_loader import EMS_LABEL_TO_TIER, ensure_session_defaults


st.set_page_config(
    page_title="Hybrid UAV Propulsion Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

ensure_session_defaults()

with st.sidebar:
    st.markdown("## Propulsion Dashboard")
    st.session_state["theme_mode"] = st.radio(
        "Theme",
        ["Dark", "Light"],
        index=["Dark", "Light"].index(st.session_state.get("theme_mode", "Dark")),
        horizontal=True,
    )

inject_css()


def sidebar_configuration() -> None:
    """Shared hardware and EMS input panel."""

    cfg = st.session_state["selected_config"]
    with st.sidebar:
        st.markdown("### Hardware Configuration")
        cfg["turbine_rating_kw"] = st.number_input(
            "Turbine rating (kW)",
            min_value=30.0,
            max_value=120.0,
            value=float(cfg["turbine_rating_kw"]),
            step=1.0,
        )
        cfg["generator_rating_kw"] = st.number_input(
            "Generator rating (kW)",
            min_value=30.0,
            max_value=130.0,
            value=float(cfg["generator_rating_kw"]),
            step=1.0,
        )
        cfg["battery_capacity_kwh"] = st.number_input(
            "Battery capacity (kWh)",
            min_value=1.0,
            max_value=120.0,
            value=float(cfg["battery_capacity_kwh"]),
            step=1.0,
        )
        cfg["battery_peak_power_kw"] = st.number_input(
            "Battery peak power (kW)",
            min_value=10.0,
            max_value=180.0,
            value=float(cfg["battery_peak_power_kw"]),
            step=1.0,
        )
        cfg["fuel_mass_kg"] = st.number_input(
            "Fuel mass (kg)",
            min_value=1.0,
            max_value=250.0,
            value=float(cfg["fuel_mass_kg"]),
            step=1.0,
        )

        st.markdown("### Energy Management")
        ems_labels = list(EMS_LABEL_TO_TIER)
        cfg["ems_label"] = st.selectbox(
            "EMS tier",
            ems_labels,
            index=ems_labels.index(cfg.get("ems_label", "Rule-Based")),
        )
        cfg["generator_setpoint_kw"] = st.slider(
            "Generator setpoint (kW)",
            min_value=0.0,
            max_value=120.0,
            value=float(cfg.get("generator_setpoint_kw", 58.0)),
            step=1.0,
        )
        soc_low, soc_high = st.slider(
            "Target SoC band",
            min_value=0.20,
            max_value=1.00,
            value=(float(cfg.get("target_soc_low", 0.35)), float(cfg.get("target_soc_high", 0.90))),
            step=0.01,
        )
        cfg["target_soc_low"] = soc_low
        cfg["target_soc_high"] = soc_high
        cfg["max_charge_c_rate"] = st.slider(
            "Max charge C-rate",
            min_value=0.1,
            max_value=3.0,
            value=float(cfg.get("max_charge_c_rate", 1.0)),
            step=0.1,
        )
        cfg["ecms_equivalence_factor"] = st.slider(
            "ECMS equivalence factor (kg/kWh)",
            min_value=0.0,
            max_value=1.0,
            value=float(cfg.get("ecms_equivalence_factor", 0.22)),
            step=0.01,
        )
        st.session_state["selected_config"] = cfg


sidebar_configuration()

pages = [
    st.Page("pages/mission_overview.py", title="1. Mission Overview"),
    st.Page("pages/mission_timeline.py", title="2. Mission Timeline"),
    st.Page("pages/energy_management.py", title="3. Energy Management"),
    st.Page("pages/optimization_pareto.py", title="4. Optimization Explorer"),
    st.Page("pages/sensitivity_analysis.py", title="5. Sensitivity Analysis"),
    st.Page("pages/analytics_dashboard.py", title="6. Analytics Dashboard"),
    st.Page("pages/design_summary_export.py", title="7. Design Report"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
