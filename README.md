# 🎓 Merit Calculator & Career Advisor

A complete, modern Streamlit application designed for NED University BSCS students to accurately calculate merit seat allocation, explore specialization pathways, and make data-driven career choices.

## 🌟 Features

- **📊 Merit Calculator**:
  - Dynamically parse raw merit lists and calculate exact seat allocations.
  - Accounts for specific quotas (100 CS seats, 50 for other specializations).
  - Handles edge-cases, missing data, and ties with a greedy merit algorithm.
  - Interactive "Smart Solo Lookup" to view real-time seat availability at the time of your turn.
  
- **🎯 Career Advisor**:
  - Maps CS specializations to real-world roles (Data Analyst, Software Engineer, Machine Learning Engineer, Cybersecurity Analyst, Game Developer).
  - Provides localized (Karachi) PKR salary expectations, key skills, and a career roadmap.
  
- **📚 Course Helper**:
  - Digitized rendering of the latest undergraduate prospectus.
  - Separate views for Foundation Core Courses vs. Specialization Core Courses.
  - Detailed, structured tables outlining all available Elective options by group (Elective I, II, III, IV, V).

## 🚀 Running the App Locally

Ensure you have Python 3.9+ installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Supl3x/Merit-Calculator.git
   cd Merit-Calculator
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure

```
Merit-Calculator/
├── .streamlit/
│   └── config.toml          # Custom dark glassmorphism theme settings
├── data/
│   ├── GPA.txt              # Raw student data source
│   ├── Course Outline.txt   # Raw course prospectus source
│   ├── allocator.py         # Merit allocation engine logic
│   ├── parser.py            # GPA text parsing logic
│   ├── models.py            # System constants and limits
│   ├── career_data.py       # Hardcoded career mapping data
│   └── course_data.py       # Hardcoded course and elective data
├── pages/
│   ├── 1_merit_calculator.py
│   ├── 2_career_advisor.py
│   └── 3_course_helper.py
├── utils/
│   ├── charts.py            # Plotly interactive chart generation
│   └── styles.py            # Centralized CSS and UI components
├── app.py                   # Main landing page
└── requirements.txt
```

## 🛠️ Built With
- [Streamlit](https://streamlit.io/) - The core frontend framework
- [Pandas](https://pandas.pydata.org/) - Data parsing and processing
- [Plotly](https://plotly.com/) - Interactive charting

## 📝 License
This project is for educational utility.
