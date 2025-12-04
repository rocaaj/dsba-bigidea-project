# xG Shot Map Dashboard

**DSBA 5122: Visual Analytics and Storytelling**

## Project Description

This interactive Streamlit dashboard demonstrates the use of Expected Goals (xG) analytics for soccer player development and tactical analysis. The application provides:

- **Educational Introduction**: A concise overview of the xG metric and its applications for attackers, defenders, and coaches
- **Interactive Shot Maps**: Visual exploration of professional match data with shot locations, xG values, and goal outcomes
- **Team & Match Analysis**: Filter by season and team to analyze shot selection, positioning, and goal-scoring opportunities

The dashboard is designed to help college soccer players understand how data analytics can inform their development, focusing on shot selection, positioning, and tactical awareness.

## How to Run

### Prerequisites

Install the required Python libraries:
```bash
pip install streamlit pandas numpy matplotlib mplsoccer statsmodels
```

### Running the Application

1. Navigate to the project directory:
   ```bash
   cd xG_model_stats_approach
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. The application will open in your default web browser. Use the sidebar filters to:
   - Select a season
   - Select a team
   - Select a specific match
   
   The interactive shot map will display with xG values, goal outcomes, and summary statistics.

## Contact

For questions or issues, contact: aroca@charlotte.edu
