# California Maternal Health Disparities Dashboard
### Advancing Black Maternal Health Equity & Wellness Through Geospatial Analytics & Qualitative NLP

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Community Partner](https://img.shields.io/badge/Partner-Jewel%20of%20Justice-4B2E58?style=flat)](https://jewelofjustice.org/)
[![Institution](https://img.shields.io/badge/Institution-UChicago%20Data%20Science%20Institute-800000?style=flat)](https://datascience.uchicago.edu/)

---

## Challenge Statement(s) Addressed 🎯

* **How might we bridge the persistent clinical and structural blind spots** in conventional CDC and statewide maternal health surveillance that fail to capture the lived experiences and environmental stressors faced by Black mothers?
* **How might we connect macro-level 10-year longitudinal health trends** (delayed prenatal care, soaring gestational hypertension, and low birth weight) with localized, county-level geospatial and socioeconomic indicators across California?
* **How might we leverage Natural Language Processing (NLP)** to analyze grassroots community feedback and elevate the qualitative voices of Black mothers to the same evidentiary weight as clinical epidemiology?
* **How might we equip community-based organizations like Jewel of Justice** with a unified, interactive, and frictionless data platform to inform targeted interventions, community workshops, and maternal health advocacy?

---

## Project Description

Across the United States, Black mothers consistently experience the highest rates of health complications during pregnancy and childbirth. Our **10-year longitudinal time-series analysis (2014–2024) of national CDC Natality data** uncovers a deep structural barrier burden among adult Black mothers: **roughly 1 in 3 Black mothers (~34%) experience delayed or absent 1st-trimester prenatal care**, occurring alongside a 2-year increase in average maternal age. 

Crucially, our findings reveal a stark clinical paradox: even when early prenatal care entry temporarily peaked at ~70% in 2021, **rates of gestational hypertension doubled from 6.1% in 2014 to 12.2% in 2024**, which directly compounded downstream infant risks as **low birth weight outcomes reached a national peak of 14.6%**. Throughout this decade, Black mothers continuously lagged behind White and Asian counterparts by over 12% in early care entry while confronting disproportionately higher clinical risk overall.

These persistent disparities reinforce what communities have voiced for generations: **the current healthcare architecture continues to fail Black mothers.** The disconnect between access metrics and health outcomes proves that standard CDC and state-level datasets miss the unmeasured structural, social, and environmental factors that shape maternal wellbeing.

To bridge these clinical blind spots, we built a **multi-dimensional analytical framework and interactive Streamlit dashboard** that unites:
1. **National Longitudinal CDC Natality Analytics (2014–2024):** Uncovering systemic time-series disparities in prenatal care timing, maternal hypertension, and birth outcomes.
2. **Statewide California Geospatial Mapping:** Integrating county-level social determinants of health (preterm birth rates, low birth weight, race-specific poverty, diabetes prevalence, cardiovascular disease, and longitudinal violent crime trends from 2016–2024) smoothed with empirical Bayes/regional shrinkage priors for statistical reliability in smaller counties.
3. **Qualitative NLP Topic Modeling on Community Survey Data:** Capturing real attendee voices from 18 community wellness sessions hosted by our community partner, **Jewel of Justice (JOJ)**.

By pairing geospatial epidemiology with authentic community voices, our platform illuminates the lived realities behind the numbers, enabling targeted, community-driven interventions.

---

## Research & Community Impact 💜

* **Elevating Lived Experience as Clinical Evidence:** Conventional public health approaches treat clinical metrics in isolation. Our platform bridges quantitative epidemiology with qualitative community narratives, proving that maternal outcomes cannot be separated from chronic environmental stress, provider bias, and systemic neglect.
* **Empowering Community Partner Jewel of Justice:** Jewel of Justice leads grassroots workshops focused on self-care and wellness. The dashboard directly translates complex state and federal data into actionable community intelligence, helping JOJ target specific regions (such as the Central Valley / Fresno County) and adapt their workshop curriculum.
* **Targeted Regional Advocacy:** By benchmarking county data against statewide averages and highlighting localized risk clusters, community advocates and health workers can pinpoint where maternal healthcare resources, doula networks, and prenatal clinics are most desperately needed.
* **Frictionless Public & Research Access:** Built with an intuitive, interactive UI and instant CSV export capabilities, the dashboard provides researchers, policy analysts, community doulas, and the public with open access to multi-source health metrics without requiring complex coding environments.

---

## Key Epidemiological & Longitudinal Findings 📈

### 1. National CDC Natality Trends (2014–2024)
| Metric | 2014 | 2024 / Peak | Impact & Disparity |
| :--- | :---: | :---: | :--- |
| **Delayed/Absent 1st-Trimester Care** | ~34% | ~34% | **1 in 3 Black mothers** lack timely early prenatal care; **>12% lag** behind White and Asian mothers. |
| **1st-Trimester Care Entry Rate** | ~66% | ~70% (2021 peak) | Temporary access gains failed to reverse underlying clinical complications. |
| **Gestational Hypertension Rate** | **6.1%** | **12.2%** | **Rates doubled (100% relative increase)** over the 10-year study window. |
| **Low Birth Weight (<2,500g) Rate** | — | **14.6% (National Peak)** | Directly compounded by maternal hypertension and chronic weathering stress. |
| **Average Maternal Age** | Baseline | **+2.0 Years** | Gradual increase in maternal age interacting with cumulative health barriers. |

### 2. California County-Level Spatial Analysis & Regional Smoothing
* **Geospatial Disparities:** Across California's 58 counties, preterm birth and low birth weight outcomes cluster heavily in inland agricultural and socioeconomically vulnerable regions (e.g., Fresno County and the Central Valley).
* **Statistical Rigor via Regional Shrinkage:** Smaller counties suffer from small-sample statistical noise and cell suppression in public datasets. We implemented **regional shrinkage smoothing (Empirical Bayes pooling)** across regional peer groups to stabilize county rates while preserving genuine local variation.
* **Fresno County Deep Dive:** Highlighted within the dashboard interface, Fresno County serves as a primary case study where high rates of poverty, cardiovascular risk, and adverse birth outcomes align with urgent community needs.

---

## Community Partnership & Qualitative NLP Pipeline 🗣️

```
   18 Community Sessions                     Data Pipeline                      Machine Learning & Evaluation
+---------------------------+       +-------------------------------+       +------------------------------------+
|  Jewel of Justice (JOJ)   |       | • Digital Transcription       |       | Model Benchmarking:                |
|  "Advancing Black Maternal| ----> | • Missing Entry Removal       | ----> |   - Latent Dirichlet Alloc. (LDA)  |
|  Self-Care & Wellness"    |       | • Preprocessing & Tokenization|       |   - BERTopic                       |
|  (18 Sessions / 2 Years)  |       | • Stopword & Lemmatization    |       |   - NMF                            |
+---------------------------+       +-------------------------------+       +-----------------+------------------+
                                                                                              |
                                                                                  Selected Model: LDA
                                                                              (Highest Coherence Score +
                                                                           Human Interpretability Alignment)
                                                                                              |
                                                                                              v
                                                                            +------------------------------------+
                                                                            | Qualitative Themes Extracted:      |
                                                                            | 1. Systemic & Clinical Barriers    |
                                                                            | 2. Holistic Self-Care & Mental Well|
                                                                            | 3. Community & Doula Support       |
                                                                            | 4. Workshop & Ecosystem Improvement|
                                                                            +------------------------------------+
```

### Stakeholder Overview: Jewel of Justice
Our community stakeholder, **Jewel of Justice**, hosted **18 sessions over the past two years** centered on *"Advancing Black Maternal Self-Care and Wellness."* These sessions engaged a diverse cross-section of the maternal health ecosystem:
* Prenatal mothers & Postpartum mothers
* Preconception individuals
* Family support members & caregivers
* Community agency representatives & maternal health practitioners

### Survey Data Collection & Preprocessing
After each session, detailed surveys were administered to capture participants' lived experiences, workshop takeaways, institutional encounters, and desires for systemic change. Responses were digitally transcribed, standardized, and rigorously preprocessed (imputing/removing missing values, text normalization, and noise filtering) to preserve authentic community sentiment for computational modeling.

### NLP Model Selection: LDA vs. BERTopic vs. NMF
To extract the latent topics embedded within the community responses, we tested and benchmarked three distinct unsupervised NLP architectures:
1. **LDA (Latent Dirichlet Allocation)**
2. **BERTopic (Transformer-based clustering)**
3. **NMF (Non-negative Matrix Factorization)**

**Why LDA was chosen:**
* **Coherence Score Superiority:** Evaluated across multiple topic counts ($k$), LDA demonstrated the highest topic coherence score, indicating consistent, semantically tightly-knit word clusters.
* **Human-in-the-Loop Interpretability:** Outputs were reviewed alongside human qualitative analysis. LDA clustered responses with the clearest, most actionable thematic relationships directly relevant to community health intervention.

### Derived Thematic Clusters
* **Navigating Clinical Gatekeeping & Bias:** Lived experiences of not being heard by healthcare providers, dismissal of pain, and structural hurdles in securing first-trimester appointments.
* **Prioritizing Mental Wellness & Self-Care:** The imperative for dedicated spaces where Black mothers can decompress, practice holistic self-care, and process chronic stress.
* **Ecosystem Advocacy & Peer Support:** The vital role of doulas, community health workers, and family networks in advocating during labor and postpartum recovery.
* **Expanding Community Interventions:** Specific suggestions to expand workshop reach, offer childcare, provide continuous follow-ups, and translate grassroots insights into legislative policy.

---

## Interactive Dashboard Features 🖥️

* **Interactive Choropleth Map (Streamlit + Apache ECharts):** High-performance vector rendering of California's 58 counties with custom smooth color scaling (`#94839C` to `#2E183F`), zoom/pan capabilities, and JavaScript-powered dynamic tooltips.
* **Multi-Variable Exploration:**
  * Preterm Birth Rate (smoothed)
  * Low Birth Weight Rate (%)
  * Overall & Demographic Poverty Rates (ACS 5-Year Estimates)
  * Diabetes Prevalence (%)
  * Cardiovascular Disease Rate (per 10,000)
  * Longitudinal Violent Crime Rate (per 100,000)
* **Longitudinal Crime Time Slider:** Explore annual violent crime rates across California counties from **2016 to 2024**.
* **County-Level Deep Dive & Benchmark Cards:** Automatically computes metrics for **Fresno County** alongside California statewide context (Statewide Average, Highest County, Lowest County, and Statewide Ranking).
* **Ranked County Data Table & One-Click CSV Export:** Fully sortable tabular breakdown with direct CSV download for offline analysis and reporting.
* **Stakeholder-Driven UI:** Customized styling and color palette designed in close weekly feedback loops with Jewel of Justice leadership to align with organizational branding and presentation needs.

---

## Tech Overview 💻

| Layer | Technologies / Tools | Description |
| :--- | :--- | :--- |
| **Frontend & UI** | `Streamlit`, `Streamlit-ECharts`, `Apache ECharts`, `HTML/CSS` | Responsive web interface with interactive choropleth mapping, custom JavaScript tooltips, and custom theme styling. |
| **Data Processing & Analytics** | `Python 3`, `Pandas`, `NumPy`, `Requests` | Data ingestion, FIPS geographic standardization, and real-time metric transformation. |
| **Statistical Modeling** | Empirical Bayes / Regional Shrinkage Smoothing | Small-sample rate stabilization pooling county metrics across California health regions. |
| **Natural Language Processing** | `LDA` (Scikit-Learn / Gensim), `BERTopic`, `NMF` | Unsupervised topic modeling on transcribed qualitative workshop surveys evaluated via Coherence Scores. |
| **Geospatial Boundaries** | Plotly GeoJSON (`geojson-counties-fips.json`) | GeoJSON boundary data filtered specifically for California (`FIPS: 06xxx`). |
| **Primary Data Sources** | CDC WONDER Natality (2014–2024)<br>U.S. Census ACS 5-Year Estimates (2024)<br>CalEnviroScreen 5.0<br>CA Department of Justice Violent Crime Statistics (2016–2024)<br>Jewel of Justice Community Survey Transcripts | Multi-source health, environmental, socioeconomic, and community-generated datasets. |

---

## Project Structure 📁

```text
joj_ca_maternal_health_dashboard/
├── .streamlit/
│   └── config.toml                 # Custom UI theme (primaryColor: #2E183F, background: #d7cce1)
├── app.py                          # Main Streamlit dashboard application & ECharts rendering
├── data_loader.py                  # Data loading, FIPS formatting, and variable configuration dictionary
├── dashboard_master.csv            # County-level master dataset (preterm, poverty, diabetes, CVD, LBW)
├── ca_violent_crime_final.csv      # Longitudinal county violent crime rates with regional shrinkage (2016-2024)
├── preterm_severity_county_final.csv # Granular preterm birth rates by severity (extremely, very, moderate/late)
├── ca_fips_spine.csv               # Master California FIPS crosswalk & county name reference
├── jojLogo.png                     # Community partner logo (Jewel of Justice)
├── requirements.txt                # Python package dependencies
└── README.md                       # Comprehensive research & project documentation
```

---

## Getting Started ⚙️

### Prerequisites
* Python 3.9 or higher
* `pip` and virtual environment manager (`venv`)

### Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lillyalice/joj_ca_maternal_health_dashboard.git
   cd joj_ca_maternal_health_dashboard
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit dashboard:**
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501` to explore the dashboard.

---

## Future Directions & Next Steps 🚀

* **Expanding Community Survey Sample Size:** Partnering with additional maternal health non-profits, birthing justice coalitions, and hospital task forces across California to scale workshop survey collection.
* **Social Listening & Sentiment Analysis:** Developing an automated NLP pipeline to monitor public maternal health discourse and patient sentiment on social platforms (e.g., Twitter/X and community forums) for real-time tracking of community concerns.
* **Predictive Risk Modeling:** Integrating supervised machine learning models to forecast county-level risk trajectories based on changing socioeconomic and environmental indices.
* **Multi-State Scaling:** Expanding the geographic pipeline beyond California to other states exhibiting severe racial disparities in maternal mortality and morbidity.

---

## Conclusion & Core Thesis 🌟

> *"We are using authentic community voices and geospatial epidemiology to uplift the lived experience of Black mothers to the exact same evidentiary weight as clinical data."*

The maternal health crisis cannot be solved by clinical charts alone. By combining rigorous 10-year CDC longitudinal analysis, county-level geospatial modeling, and transparent topic modeling on real community voices, this project turns data into a catalyst for advocacy, systemic accountability, and birthing justice.

---

## Research Program & Acknowledgments 🏛️

* **Program:** Data Science for Social Impact (DSSI) Summer Program
* **Academic & Research Institution:** [University of Chicago Data Science Institute (DSI)](https://datascience.uchicago.edu/)
* **Community Partner:** [Jewel of Justice (JOJ)](https://jewelofjustice.org/) — special thanks to organizational leadership for their continuous guidance, workshop survey access, and weekly collaborative design reviews.

### Research & Project Checklist 🏁
- [x] 10-Year National CDC Natality Longitudinal Trend Analysis (2014–2024)
- [x] Multi-source California county health, crime, and demographic data harmonization
- [x] Empirical Bayes / Regional Shrinkage smoothing for small-county rate stability
- [x] NLP pipeline & model evaluation (LDA vs. BERTopic vs. NMF with Coherence Scoring)
- [x] Interactive Streamlit + Apache ECharts dashboard with Fresno County spotlight
- [x] Weekly stakeholder feedback loops with Jewel of Justice leadership
- [x] Comprehensive documentation and open-source release

### Link to Demo Presentation 📽
* 📽 **Research Presentation Deck:** *[Link to Presentation / Canva Deck]*
* 📹 **Video Demo Walkthrough:** *[Link to Recorded Walkthrough]*

---

## Contributors ✨
* **Lilly Weaver** ([The University of Texas at San Antonio](https://www.linkedin.com/in/lilly-weaver-198839241/))
* **Mali Glemaud-Thesee** ([Morehouse College](https://www.linkedin.com/in/maligt/))
* **Edward Sie** ([Howard University](https://www.linkedin.com/in/edward-kofi-sie/))
* **Peace Amichoh** ([Prairie View A&M University](https://www.linkedin.com/in/peace-fri-amichoh/))
* **Christyana Walker** ([Spelman College](https://www.linkedin.com/in/christyanawalker/))
