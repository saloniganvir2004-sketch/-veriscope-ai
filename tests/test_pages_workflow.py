"""
Integration tests for Streamlit UI pages, workflows, team members, and input options.
"""

from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

BASE_DIR = Path(__file__).resolve().parent.parent


def test_about_page_team_members_and_enrolments():
    """Verifies all five team members and their exact enrolment numbers on About page."""
    at = AppTest.from_file(str(BASE_DIR / "pages/6_About.py"), default_timeout=20)
    at.run()
    assert not at.exception

    markdown_all = " ".join([m.value for m in at.markdown])

    # Member 1: Ayushman Kumar
    assert "Ayushman Kumar" in markdown_all
    assert "A010175625019" in markdown_all
    assert "Dataset and NLP Preprocessing" in markdown_all

    # Member 2: Astha Thapa
    assert "Astha Thapa" in markdown_all
    assert "A010175625014" in markdown_all
    assert "Machine-Learning Models and Tuning" in markdown_all

    # Member 3: Saloni Ganvir
    assert "Saloni Ganvir" in markdown_all
    assert "A010175625017" in markdown_all
    assert "Explainable AI and Interpretation" in markdown_all

    # Member 4: Sarvesh
    assert "Sarvesh" in markdown_all
    assert "A010175625016" in markdown_all
    assert "Web Application and OCR Integration" in markdown_all

    # Member 5: Sri Rinith
    assert "Sri Rinith" in markdown_all
    assert "A010175625018" in markdown_all
    assert "Evaluation, Testing and Integration" in markdown_all


def test_landing_page_structure():
    """Verifies that the landing page (app.py) has the required 5-part structure."""
    at = AppTest.from_file(str(BASE_DIR / "app.py"), default_timeout=20)
    at.run()
    assert not at.exception

    markdown_all = " ".join([m.value for m in at.markdown])

    # 1. Hero
    assert "VeriScope AI" in markdown_all
    assert "Intelligence Beyond the Headline" in markdown_all

    # 2. How it works
    assert "How It Works" in markdown_all
    assert "Story Submission" in markdown_all
    assert "OCR & Preprocessing" in markdown_all
    assert "Model Classification" in markdown_all
    assert "Explainable AI" in markdown_all

    # 3. Core capabilities
    assert "Core Capabilities" in markdown_all
    assert "Dual-Method News Classification" in markdown_all
    assert "Dual Explainable AI Lab" in markdown_all

    # 4. Visual proof of workflow
    assert "Visual Proof of the Workflow" in markdown_all

    # 5. Call to action
    assert "Ready to inspect a news story?" in markdown_all


def test_news_analyzer_empty_input_validation():
    """Verifies that clicking analyze with empty input displays error messages."""
    at = AppTest.from_file(str(BASE_DIR / "pages/2_News_Analyzer.py"), default_timeout=20)
    at.run()
    assert not at.exception

    # Click analyze with empty fields
    at.button(key="btn_manual_analyze").click().run(timeout=20)
    assert not at.exception

    # Error message should be rendered
    assert len(at.error) > 0
    error_texts = [e.value for e in at.error]
    assert any("Please enter both a News Headline and News Context" in err for err in error_texts)


def test_analysis_history_retention_notice():
    """Verifies that the 3-month retention notice is displayed on the history page."""
    at = AppTest.from_file(str(BASE_DIR / "pages/5_Analysis_History.py"), default_timeout=20)
    at.run()
    assert not at.exception

    markdown_all = " ".join([m.value for m in at.markdown])
    assert "Retention Policy" in markdown_all
    assert "3 calendar months" in markdown_all
