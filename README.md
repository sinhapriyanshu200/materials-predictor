# Materials Predictor

An AI-powered web application for predicting and visualizing crystal structures and material properties. Built with Streamlit, integrates Gemini and OpenAI models, Materials Project API, and interactive 3D visualization. Ideal for materials science research, discovery, and education.

## Features

- Predict crystal structures and material properties using AI (Gemini & OpenAI APIs)
- Query Materials Project database
- Interactive 3D visualization with py3Dmol
- User-friendly Streamlit interface
- Extensible for research and educational use

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for Gemini, OpenAI, and Materials Project (see below)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sinhapriyanshu200/materials-predictor.git
   cd materials-predictor
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
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
