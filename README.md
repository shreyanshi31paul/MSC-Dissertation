# MSC-Dissertation

This project develops a data-driven water management system using real-time smart meter data to monitor consumption, detect anomalies, and identify potential leaks. It integrates anomaly detection with visual analytics and a Streamlit dashboard to provide facility teams with actionable insights for improved water conservation and operational efficiency.

## Features

- **Data Preprocessing**  
  - Load and clean water consumption data from Excel files.  
  - Handle missing values and ensure proper `DateTime` indexing.  

- **Exploratory Data Analysis (EDA)**  
  - Visualize total water consumption over time to identify **trends and seasonality**.  
  - Plot daily consumption for individual buildings (`Bronte`, `Dome_Tudor`, `Fry`, `Fussey`, `Grey`, `Library`).  
  - Generate **average daily usage patterns** to detect deviations from normal behavior.  

- **Anomaly Detection**  
  - Apply the **Isolation Forest algorithm** to identify unusual daily consumption (tested on *Dome_Tudor* building).  
  - Highlight days with abnormal spikes/drops in water usage (possible leaks, unusual operations).  

- **Leak & Off-Hour Usage Detection**  
  - Analyze consumption during **nighttime hours (00:00–04:00)**.  
  - Flag buildings with continuous off-hour usage as **suspected leaks**.  

- **Automated Reporting**  
  - Generate **weekly and monthly reports** summarizing:  
    - Total consumption  
    - Individual building consumption  
    - Detected anomalies & suspected leaks  
  - Export reports and leak data to **CSV files** for easy access.  

- **Streamlit Dashboard**  
  - Interactive dashboard for facility teams to:  
    - Visualize consumption trends & anomalies  
    - Monitor average daily patterns  
    - Track leak flags in real time  
    - Get actionable insights for proactive decision-making  
