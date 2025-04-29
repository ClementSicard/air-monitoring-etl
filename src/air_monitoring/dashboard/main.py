"""Streamlit code for air quality monitoring dashboard."""

from pathlib import Path

import click
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

from air_monitoring.db.connection import DBConnection


st.set_page_config(
    page_title="Air Quality Monitoring Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)


@click.command()
@click.option(
    "--env-file",
    help="Path to the .env file with database connection parameters.",
)
def dashboard(env_file: Path) -> None:
    """Main function to run the air quality dashboard."""
    load_dotenv(dotenv_path=env_file)
    st.title("Température et humidité")

    measurements = DBConnection(env_file_path=env_file).get_measurements()
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
        st.line_chart(
            measurements_df,
            x="timestamp",
            y="humidity",
            color="reference",
            x_label="Date",
            y_label="Humidity (%)",
        )
    with col2:
        st.subheader("Temperature")
        st.line_chart(
            measurements_df,
            x="timestamp",
            y="temperature",
            color="reference",
            x_label="Date",
            y_label="Temperature (°C)",
        )


if __name__ == "__main__":
    dashboard()
