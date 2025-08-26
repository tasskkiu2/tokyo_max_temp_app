import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

plt.rcParams['font.family'] = 'Noto Sans CJK JP'

st.set_page_config(page_title="東京都心最高気温モニター", layout="centered")
st.title("東京都心・最高気温モニター（実測 & 予測）")

thr = st.slider("閾値（℃）", 25, 35, 30, step=1)

# ---- CSV固定読み込み ----
actual_path = pathlib.Path(__file__).parent / "data" / "max_data.csv"
actual_path_2 = pathlib.Path(__file__).parent / "data" / "output.csv"
df_max = pd.read_csv(actual_path,skiprows=3)
df_max = df_max.iloc[:,[0,1]]
df_max = df_max.drop(index=0).reset_index(drop=True)
df_max = df_max.drop(index=0).reset_index(drop=True)

df_max["年月日"] = pd.to_datetime(df_max["年月日"])
df_max["year"] = df_max["年月日"].dt.year
actual = (df_max["最高気温(℃)"] >= thr).groupby(df_max["year"]).sum().reset_index()
actual.columns = ["year", "days"]



forecast = pd.read_csv(actual_path_2)
forecast["ds"] = pd.to_datetime(forecast["ds"])
forecast["year"] = forecast["ds"].dt.year
pred = (forecast[forecast["year"] >= 2025]["yhat"] >= thr).groupby(forecast["year"]).sum().reset_index()
pred.columns = ["year", "days"]

# ---- 結合 ----
annual = pd.concat([actual, pred], ignore_index=True)
annual["kind"] = ["実測" if y <= 2024 else "予測" for y in annual["year"]]

# ---- プロット ----
plt.figure(figsize=(8,4))
colors = annual["kind"].map({"実測":"steelblue","予測":"tomato"})
plt.bar(annual["year"].astype(str), annual["days"], color=colors)

plt.xticks(rotation=45)
plt.xlabel("年")
plt.ylabel("日数")
plt.title(f"年ごとの {thr}℃ 以上の日数（青:実測 & 赤:予測）")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

st.pyplot(plt, use_container_width=False)