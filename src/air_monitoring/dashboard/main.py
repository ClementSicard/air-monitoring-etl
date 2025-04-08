"""Streamlit code for air quality monitoring dashboard."""

import pandas as pd
import streamlit as st

from air_monitoring.db.connection import DBConnection


st.set_page_config(
    page_title="Air Quality Monitoring Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)


def dashboard() -> None:
    """Main function to run the air quality dashboard."""
    st.title("Température et humidité")

    measurements = DBConnection().get_measurements()
    measurements_df = pd.DataFrame([m.model_dump() for m in measurements])

    st.dataframe(
        measurements_df,
        use_container_width=True,
        hide_index=True,
    )

    # Create two panels side to side for humidity and temperature
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Humidity")
        st.line_chart(measurements_df, x="timestamp", y="humidity")
    with col2:
        st.subheader("Temperature")
        st.line_chart(measurements_df, x="timestamp", y="temperature")


if __name__ == "__main__":
    dashboard()
