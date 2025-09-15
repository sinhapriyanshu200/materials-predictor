# =============================
# 📚 Imports
# =============================
import os  
import re 
import streamlit as st  # Streamlit UI framework
import streamlit.components.v1 as components  
from dotenv import load_dotenv  # Load environment variables from .env
from openai import OpenAI  # OpenAI API client
import google.generativeai as genai  # Google Gemini API client
from mp_api.client import MPRester  # Materials Project API client
import py3Dmol  # 3D molecular visualization
import base64  # For encoding downloads
from typing import Union  
import ast  # Safe evaluation of Python literals
import json  # JSON parsing
import html  # HTML escaping

# =============================
# Download Link Utility
# =============================
def make_data_download_link(content: Union[bytes, str], filename: str, mime: str = "text/plain", label: str = "Download") -> str:
    """Return an HTML anchor tag (data URI) for downloading `content` without triggering a Streamlit rerun."""
    if isinstance(content, str):
        b = content.encode('utf-8')
    else:
        b = content
    b64 = base64.b64encode(b).decode()
    href = f"data:{mime};base64,{b64}"
    # simple styled link that looks like a button
    return f'<a href="{href}" download="{filename}" style="text-decoration:none; background:#00c3ff; color:#001218; padding:8px 12px; border-radius:6px; font-weight:600;">{label}</a>'

# =============================
# API setup
# =============================
load_dotenv()  # Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI key
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")  # Gemini key
MATERIALS_PROJECT_API_KEY = os.getenv("MATERIALS_PROJECT_API_KEY")  # Materials Project key

# Safety check for API keys
if not OPENAI_API_KEY or not GEMINI_API_KEY or not MATERIALS_PROJECT_API_KEY:
    st.error("❌ One or more API keys are missing from `.env`.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)  # OpenAI client
genai.configure(api_key=GEMINI_API_KEY)  # Gemini client config
gemini_model = genai.GenerativeModel("gemini-1.5-flash-latest")  # Gemini model
mpr = MPRester(MATERIALS_PROJECT_API_KEY)  # Materials Project client

# =============================
# LLM Generation Functions
# =============================

# Generate material formulas using OpenAI gpt-4o
# -----------------------------------------------
def generate_openai_formulas(user_prompt):
    """Generate material formulas using OpenAI GPT."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a materials scientist. Reply ONLY with a Python list of valid chemical formulas."},
                {"role": "user", "content": f"Suggest chemical formulas for: {user_prompt}"}
            ]
        )
        return extract_formulas(response.choices[0].message.content, source="OpenAI")
    except Exception as e:
        st.error(f"OpenAI error: {e}")
        return []

# Evaluate deduplicated materials for compliance using OpenAI
# ------------------------------------------------------------
def evaluate_openai_materials(material_list, user_prompt):
    """Filter formulas for compliance using OpenAI GPT."""
    try:
        prompt = (
            f"Given the following list of chemical formulas: {material_list}\n"
            f"Check each formula and return a Python list of only those that fully comply with this design goal: '{user_prompt}'.\n"
            f"Reply ONLY with the filtered list."
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a materials scientist. Reply ONLY with a Python list of valid chemical formulas."},
                {"role": "user", "content": prompt}
            ]
        )
        return extract_formulas(response.choices[0].message.content, source="OpenAI Eval")
    except Exception as e:
        st.error(f"OpenAI evaluation error: {e}")
        return []

# Generate material formulas using Gemini 1.5 flash latest
# ---------------------------------------------------------
def generate_gemini_formulas(user_prompt):
    """Generate material formulas using Google Gemini."""
    try:
        prompt = (
            f"Suggest a Python list of 10 chemical formulas (e.g., ['TiO2', 'ZnO', ...]) for the following design goal:\n"
            f"'{user_prompt}'\n"
            f"Reply ONLY with the list."
        )
        response = gemini_model.generate_content(prompt)
        return extract_formulas(response.text, source="Gemini")
    except Exception as e:
        st.error(f"Gemini error: {e}")
        return []

# Evaluate deduplicated materials for compliance using Gemini
# ------------------------------------------------------------
def evaluate_gemini_materials(material_list, user_prompt):
    """Filter formulas for compliance using Gemini."""
    try:
        prompt = (
            f"Given the following list of chemical formulas: {material_list}\n"
            f"Check each formula and return a Python list of only those that fully comply with this design goal: '{user_prompt}'.\n"
            f"Reply ONLY with the filtered list."
        )
        response = gemini_model.generate_content(prompt)
        return extract_formulas(response.text, source="Gemini Eval")
    except Exception as e:
        st.error(f"Gemini evaluation error: {e}")
        return []

# =============================
# Cleanup & Validation
# =============================
def extract_formulas(text, source="LLM"):
    """Parse and validate formulas from LLM output."""
    try:
        if not text:
            return []

        # strip common code fences
        text_clean = re.sub(r"```(?:python|text)?\n|```", "", text)

        # Try to locate a Python/JSON list in the LLM output and parse safely
        match = re.search(r"\[.*?\]", text_clean, re.DOTALL)
        if match:
            candidate = match.group()
            formulas = None
            # Prefer safe literal eval
            try:
                formulas = ast.literal_eval(candidate)
            except Exception:
                # try JSON parse as a fallback
                try:
                    formulas = json.loads(candidate)
                except Exception:
                    formulas = None

            if isinstance(formulas, list):
                valid = []
                for item in formulas:
                    if not isinstance(item, str):
                        continue
                    s = item.strip()
                    # looser token validation (keeps common formula characters)
                    if re.match(r"^[A-Za-z0-9()]+$", s):
                        valid.append(s)
                # preserve order, dedupe
                seen = set()
                out = []
                for v in valid:
                    if v not in seen:
                        seen.add(v)
                        out.append(v)
                return out

        # If strict parsing fails, return empty list (avoid guessing from noisy text)
        return []
    except Exception:
        st.warning(f"⚠️ {source} output parsing failed:\n{text}")
        return []

# =============================
# Materials Project Search
# =============================
@st.cache_resource
def query_mp_for_formula(formula):
    """Query Materials Project for a given formula."""
    try:
        entries = mpr.materials.summary.search(
            formula=formula,
            is_stable=True,
            fields=["material_id", "formula_pretty", "formation_energy_per_atom", "band_gap", "density", "structure"]
        )
        if not entries:
            return None
        return sorted(entries, key=lambda x: getattr(x, "formation_energy_per_atom", 9999))[0]
    except Exception as e:
        # don't spam the UI repeatedly for cached failures; return None
        st.error(f"🚫 MP query failed for {formula}: {e}")
        return None

# =============================
# Structure Viewer
# =============================
def show_structure(structure, supercell=(2, 2, 2)):
    """Render 3D structure viewer for a material."""
    try:
        conventional = structure.get_conventional_standard_structure()
    except:
        conventional = structure
    big = conventional * supercell
    cif = big.to(fmt="cif")

    viewer = py3Dmol.view(width=500, height=500)
    viewer.addModel(cif, "cif")

    # Ball-and-stick for all atoms
    #------------------------------
    viewer.setStyle({}, {
        "stick": {"radius": 0.15, "colorscheme": "Jmol"},
        "sphere": {"scale": 0.3, "colorscheme": "Jmol"}
    })

    viewer.zoomTo()
    return viewer

def structure_to_cif_and_poscar(structure, supercell=(2, 2, 2)):
    """Return CIF and POSCAR strings for a structure (applies supercell)."""
    try:
        try:
            conventional = structure.get_conventional_standard_structure()
        except Exception:
            conventional = structure
        big = conventional * supercell
        cif = big.to(fmt="cif")
        # poscar/vasp
        try:
            poscar = big.to(fmt="poscar")
        except Exception:
            poscar = None
        return cif, poscar
    except Exception:
        return None, None

# =============================
# Best Material Search
# =============================
def find_best_material(formulas):
    """Find top 3 materials from formulas using MP data."""
    candidates = []
    for formula in formulas:
        st.write(f"🔍 Searching MP for `{formula}` ...")
        result = query_mp_for_formula(formula)
        if result:
            ef = getattr(result, "formation_energy_per_atom", 0.0)
            bg = getattr(result, "band_gap", 0.0)
            pretty = getattr(result, "formula_pretty", formula)
            st.success(f"✅ Found: {pretty} | E_f: {ef:.3f} eV/atom | Band Gap: {bg:.3f} eV")
            candidates.append(result)
        else:
            st.warning("🚫 No result found")
    if not candidates:
        return []
    # Sort by formation energy and return top 3
    return sorted(candidates, key=lambda x: getattr(x, "formation_energy_per_atom", 9999))[:3]

# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="Material Predictor", layout="wide")  # Page config
st.title("🔬 Materials Predictor")  # Main title
st.markdown("Enter **Requirements to be present in material** and let AI suggest candidates from the Materials Project database.")  # Instructions

user_query = st.text_input(
    "Enter your materials design goal:",
    placeholder="e.g., transparent conductor, battery cathode"
)

if st.button("Find Best Material"):
    # Button click handler
    if not user_query.strip():
        st.warning("⚠️ Please enter a valid materials design goal.")
    else:
        with st.spinner("Generating suggestions..."):
            openai_formulas = generate_openai_formulas(user_query)
            gemini_formulas = generate_gemini_formulas(user_query)

        st.subheader("🤖 Suggested Formulas")  # LLM suggestions headline
        col1, col2 = st.columns(2)
        col1.write("**LLM A Suggestions:**")
        col1.write(openai_formulas)
        col2.write("**LLM B Suggestions:**")
        col2.write(gemini_formulas)

        # Combine suggestions but deduplicate while preserving order (do not show this intermediate list to the user)
        combined_raw = openai_formulas + gemini_formulas
        seen = set()
        combined = []
        for f in combined_raw:
            if f not in seen:
                seen.add(f)
                combined.append(f)

        # LLM-based evaluation step
        with st.spinner("Evaluating materials for compliance..."):
            openai_eval = evaluate_openai_materials(combined, user_query)
            gemini_eval = evaluate_gemini_materials(combined, user_query)
            # Intersection: only keep materials approved by both
            final_materials = [f for f in combined if f in openai_eval and f in gemini_eval]

        st.subheader("✅ Selecting only High complying Materials: ")  # Filtered materials headline
        if final_materials:
            st.write(final_materials)
        else:
            st.warning("No materials passed both evaluations.")

        with st.spinner("Finding best candidates..."):
            best_list = find_best_material(final_materials)

        if best_list:
            st.subheader("🎯 Top 3 Candidates Found")  # Top candidates headline
            table_data = [
                {
                    "#": idx + 1,
                    "Formula": getattr(best, "formula_pretty", "N/A"),
                    "MP ID": getattr(best, "material_id", "N/A"),
                    "Formation Energy (eV/atom)": f"{getattr(best, 'formation_energy_per_atom', 0.0):.3f}",
                    "Band Gap (eV)": f"{getattr(best, 'band_gap', 0.0):.3f}",
                    "Density (g/cm³)": f"{getattr(best, 'density', 0.0):.3f}",
                }
                for idx, best in enumerate(best_list)
            ]

            st.table(table_data)  # Show results table

            # CSV download (manual build)
            import csv
            from io import StringIO

            csv_buf = StringIO()
            if table_data:
                w = csv.DictWriter(csv_buf, fieldnames=list(table_data[0].keys()))
                w.writeheader()
                w.writerows(table_data)
            csv_bytes = csv_buf.getvalue().encode("utf-8")
            st.markdown(make_data_download_link(csv_bytes, "top3_materials.csv", mime="text/csv", label="Download table CSV"), unsafe_allow_html=True)

            # Fixed viewer iframe height (no slider)
            VIEWER_IFRAME_HEIGHT = 500

            st.subheader("🔍 Structure Viewers")  # Structure viewers headline
            cols = st.columns(min(3, len(best_list)))
            for idx, best in enumerate(best_list):
                col = cols[idx] if idx < len(cols) else st.container()
                with col:
                    # escape values before interpolating into HTML
                    safe_formula = html.escape(str(getattr(best, "formula_pretty", "N/A")))
                    safe_mid = html.escape(str(getattr(best, "material_id", "N/A")))
                    ef_val = getattr(best, "formation_energy_per_atom", 0.0)
                    bg_val = getattr(best, "band_gap", 0.0)
                    st.markdown(
                        f"""
                        <div style='background:#181c24; border-radius:12px; padding:10px; margin-bottom:8px; border:1px solid #23272f; text-align:center;'>
                          <div style='font-weight:700; color:#00c3ff; font-size:16px;'>🧬 {safe_formula}</div>
                          <div style='font-size:12px; color:#b0b8c1;'>MP ID: {safe_mid} | E_f: {ef_val:.3f} eV/atom | Band Gap: {bg_val:.3f} eV</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    try:
                        viewer_key = f"viewer_html_{getattr(best, 'material_id', 'N/A')}"
                        # If a stale wrapper with the old internal slider remains in session_state,
                        # regenerate the raw viewer HTML to remove it. Detect by known marker strings.
                        existing = st.session_state.get(viewer_key)
                        if existing and ("height_slider_" in existing or "viewer_container_" in existing or "height_value_" in existing):
                            viewer = show_structure(getattr(best, "structure", None))
                            raw_html = viewer._make_html()
                            st.session_state[viewer_key] = raw_html
                        elif not existing:
                            viewer = show_structure(getattr(best, "structure", None))
                            raw_html = viewer._make_html()
                            st.session_state[viewer_key] = raw_html

                        viewer_html = st.session_state.get(viewer_key)
                        if viewer_html:
                            components.html(viewer_html, height=VIEWER_IFRAME_HEIGHT)
                        else:
                            st.error(f"No viewer HTML for {safe_formula}")
                    except Exception as e:
                        st.error(f"Error rendering structure for {safe_formula}: {e}")

                    # Downloads
                    cif_str, poscar_str = structure_to_cif_and_poscar(getattr(best, "structure", None))
                    dlc1, dlc2 = st.columns([1, 1])

                    def sanitize_filename(name: str) -> str:
                        # keep alnum, dash, underscore and dot
                        return re.sub(r"[^A-Za-z0-9._-]", "_", name)

                    if cif_str:
                        with dlc1:
                            fname = sanitize_filename(f"{getattr(best, 'formula_pretty', 'N/A')}.cif")
                            label = f"CIF ({html.escape(str(getattr(best, 'formula_pretty', 'N/A')))})"
                            st.markdown(make_data_download_link(cif_str, fname, mime="chemical/x-cif", label=label), unsafe_allow_html=True)
                    if poscar_str:
                        with dlc2:
                            fname = sanitize_filename(f"{getattr(best, 'formula_pretty', 'N/A')}_POSCAR.vasp")
                            label = f"POSCAR ({html.escape(str(getattr(best, 'formula_pretty', 'N/A')))})"
                            st.markdown(make_data_download_link(poscar_str, fname, mime="text/plain", label=label), unsafe_allow_html=True)
        else:
            st.error("No suitable material found.")

# If nothing entered yet, show instructions
if not user_query:
    st.info("👆 Enter a goal above and click **Find Best Material** to get started.")  # Initial instructions
