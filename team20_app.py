"""Streamlit entry point. Run: streamlit run team20_app.py."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().with_name('rada_ui.py')),run_name='__main__')
