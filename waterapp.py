# Streamlit Dashboard for Water Management
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Loading Data
@st.cache_data
def load_data():
    file_path = "Water - 30min_01-04-2023_01-04-2025.xls"
    columns = ["Date", "Time", "Bronte", "Dome_Tudor", "Fry", "Fussey", "Grey", "Library",
               "Seacole", "Southwood", "WM15", "WM2", "WM4", "WM5_1", "WM5", "WM6", "WM7"]
    
    df = pd.read_csv("Water.csv", skiprows=16, header=None, encoding="latin1")

    df.columns = columns

    # DateTime handling
    df["DateTime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce")
    df.drop(columns=["Date","Time"], inplace=True)
    df.dropna(inplace=True)
    df = df.set_index("DateTime").sort_index()

    # Clean numeric
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.interpolate(method="time")

    # Adding total
    df["Total"] = df.sum(axis=1)
    return df

df = load_data()

# Sidebar Controls
st.sidebar.title("Dashboard Controls")
building = st.sidebar.selectbox("Select Building", df.columns)
view = st.sidebar.radio("View", ["30-min Data","Daily","Weekly","Monthly"])
show_anoms = st.sidebar.checkbox("Show Anomalies", value=True)

# Resample Data
if view == "30-min Data":
    data = df
elif view == "Daily":
    data = df.resample("D").sum()
elif view == "Weekly":
    data = df.resample("W").sum()
elif view == "Monthly":
    data = df.resample("M").sum()

# Anomaly Detection
if show_anoms and building in data.columns:
    series = data[building].values.reshape(-1,1)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(series)
    iso = IsolationForest(contamination=0.02, random_state=42)
    preds = iso.fit_predict(scaled)
    data["Anomaly"] = preds
else:
    data["Anomaly"] = 1

# Main Dashboard
st.title(" Data-Driven Water Management System")
st.write(f"### Viewing: {building} ({view})")
fig, ax = plt.subplots(figsize=(14,5))
ax.plot(data.index, data[building], label=building, color="blue")
if show_anoms:
    ax.scatter(data.index[data["Anomaly"]==-1],
               data[building][data["Anomaly"]==-1],
               color="red", label="Anomaly")
ax.set_title(f"{building} Consumption ({view})")
ax.set_xlabel("Date")
ax.set_ylabel("m³")
ax.legend()
st.pyplot(fig)


# Leak Detection (Midnight–4am)
night = df.between_time("00:00","04:00")
night_flags = (night[building] > 0.05).astype(int)

# Longest run per day
def longest_run(x):
    run = best = 0
    for v in x:
        run = run+1 if v else 0
        best = max(best, run)
    return best
night_runs = night_flags.groupby(pd.Grouper(freq="D")).agg(longest_run)
suspected_leaks = night_runs[night_runs >= 4]
st.write("### Suspected Leak Days")
st.dataframe(suspected_leaks)

# Summary Statistics

st.write("### Summary Statistics")
st.dataframe(data[[building]].describe())
