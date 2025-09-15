# Materials Predictor

An AI-powered web application for predicting and visualizing crystal structures and material properties. Built with Streamlit, integrates Gemini and OpenAI models, Materials Project API, and interactive 3D visualization. Ideal for materials science research, discovery, and education.

## Features

### Core Features

- **AI-Powered Predictions:**
   - Predict crystal structures and material properties using advanced AI models (Gemini & OpenAI APIs).
- **Materials Project Integration:**
   - Seamlessly query the Materials Project database for real-world materials data and properties.
- **Interactive 3D Visualization:**
   - Visualize crystal structures and materials in 3D using py3Dmol for enhanced understanding and presentation.
- **Modern Web Interface:**
   - Intuitive, user-friendly interface built with Streamlit for easy access and rapid prototyping.
- **Extensible & Customizable:**
   - Designed for research, education, and further development in materials science and AI.

### Evaluation Models

- **Supported Models:**
   - Gemini (Google Generative AI)
   - OpenAI GPT models
- **Model Selection:**
   - Easily switch between evaluation models for comparison and benchmarking.
- **Performance Metrics:**
   - Evaluate predictions using accuracy, reliability, and scientific relevance.

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for Gemini, OpenAI, and Materials Project (see below)

### Installation
> **Note:** For Option A, please install [Anaconda](https://www.anaconda.com/products/distribution) before running the Conda commands.

1. Clone the repository:
   ```bash
   git clone https://github.com/sinhapriyanshu200/materials-predictor.git
   cd materials-predictor
   ```

2. (Option A) Create and activate a Conda environment using `matenv.yaml`:
   ```bash
   conda env create -f matenv.yaml
   conda activate matenv
   ```

   (Option B) Create and activate a virtual environment using venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies (if using venv):
   ```bash
   pip install -r requirements.txt
   ```

4. Add your API keys to a `.env` file (do not commit this file):
   ```
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   MATERIALS_PROJECT_API_KEY=your_materials_project_key
   ```

### Running the App

```bash
streamlit run Application.py
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Third-Party APIs

This project uses Gemini, OpenAI, and Materials Project APIs. Usage of these APIs is subject to their respective terms of service. You must obtain your own API keys and comply with:

- [OpenAI Terms of Service](https://openai.com/policies/terms-of-use)
- [Google Generative AI Terms of Service](https://ai.google.dev/terms)
- [Materials Project Terms of Use](https://materialsproject.org/about/terms)

## .gitignore

A `.gitignore` file is included to prevent sensitive and unnecessary files from being tracked. Make sure your `.env` and other secrets are not committed.

## Citation

If you use this project for research, please cite appropriately.

## Contact

For questions, feedback, or collaboration inquiries, please contact:

priyanshusinha.mst24@itbhu.ac.in

---

**Developed at:**

School of Materials Science and Technology  
Indian Institute of Technology (IIT BHU), Varanasi  
Uttar Pradesh, India-221005

