
# PhonePe Data Visualization & Exploration Dashboard

This project is an interactive dashboard built with Streamlit to visualize and explore PhonePe Pulse Data.
It connects to a MySQL database, retrieves PhonePe transaction datasets (Aggregated, Map, and Top categories), and provides interactive visualizations using Plotly and Seaborn.


## Features

- Home Page

  - Overview of PhonePe and its features.

  - Download link for the PhonePe app.

- Data Exploration

  - Aggregated Analysis: Explore transactions & insurance by   state, year, and quarter.

  - Map Analysis: View district-level data for transactions, insurance, and users.

  - Top Analysis: Analyze top transactions, users, and insurance by state/quarter.

- Top Charts

  - Compare Top 10 & Bottom 10 States/Districts by:

    - Transaction Amount & Count

    - Registered Users

    - App Opens

- Interactive Visualizations

  - Choropleth maps of India (state-wise trends).

  - Bar, Pie, and Line charts for transaction breakdowns.
## Tech Stack

- Frontend: Streamlit, Streamlit Option Menu

- Database: MySQL

- Visualization: Plotly, Matplotlib, Seaborn

- Data Handling: Pandas, JSON, Requests

- Others: Pillow (for images)
## Tools

- streamlit
- streamlit-option-menu
- mysql-connector-python
- pandas
- plotly
- matplotlib
- seaborn
- requests
- pillow