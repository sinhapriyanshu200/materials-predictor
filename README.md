# Materials PredictAI

An AI-powered web application that predicts the three most stable materials and provides interactive 3D visualizations of their crystal structures and key material properties. Built with Streamlit, it seamlessly integrates Gemini, OpenAI models, and the Materials Project API, making it a powerful tool for materials science research, discovery, and education. 

Developed & maintained at IIT (BHU), Varanasi, specifically for material scientists.

## Features

### Core Features

- **AI-Powered Predictions:**
   - Predict crystal structures and material properties using advanced AI models.
- **Materials Project Integration:**
   - Seamlessly query the Materials Project database for real-world materials data and properties.
- **Interactive 3D Visualization:**
   - Visualize crystal structures and materials in 3D using py3Dmol for enhanced understanding and presentation.
- **Modern Web Interface:**
   - Intuitive, user-friendly interface built with Streamlit for easy access and rapid prototyping.
- **Extensible & Customizable:**
   - Designed for research, education, and further development in materials science and AI.

### Evaluation Models

**Deployed Models:**
   - Google Gemini (`gemini-1.5-flash-latest`)
   - OpenAI GPT (`gpt-4o`)

**Evaluation Approach:**
   - Both models are used to generate and evaluate material formulas.
   - Results are compared for accuracy, reliability, and scientific relevance.

## Getting Started


### Prerequisites

- Python 3.11
- API keys for Gemini, OpenAI, and Materials Project (see below)

### Installation


#### Option 1: Using Anaconda Navigator (Recommended GUI Method)

1. **Install Anaconda** (if not already installed):
   - Download and install Anaconda from the [official website](https://www.anaconda.com/products/distribution).

2. **Clone the repository:**
   ```bash
   git clone https://github.com/sinhapriyanshu200/materials-predictor.git
   cd materials-predictor
   ```

3. **Open Anaconda Navigator.**

4. Go to the **Environments** tab and click **Import**.

5. Browse to select the `matenv.yaml` file.

6. Name the environment (e.g., `matenv`) and click **Import**. Anaconda Navigator will create the environment with all required dependencies.

7. Once the environment is created, select it and click **Open Terminal** (or use the play button > Open Terminal) to activate it.

8. Continue to the next steps to add your API keys and run the app.

#### Option 2: Using Python venv and requirements.txt (Alternative CLI Method)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sinhapriyanshu200/materials-predictor.git
   cd materials-predictor
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API keys to a `.env` file:**
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
