import pandas as pd
import streamlit as st

st.set_page_config(page_title="Race Day Campaign Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("race_day_campaign_data.csv")
    df["open_rate_delta"] = df["actual_open_rate"] - df["target_open_rate"]
    df["ctr_delta"] = df["actual_ctr"] - df["target_ctr"]
    df["conversion_delta"] = df["actual_conversion"] - df["target_conversion"]
    df["estimated_conversions"] = (df["audience_size"] * df["actual_conversion"]).round(0).astype(int)
    df["estimated_revenue"] = (df["audience_size"] * df["revenue_per_cardholder"]).round(2)
    return df

df = load_data()

st.title("The Campaign Behind Race Day")
st.caption("Fictional premium Canadian loyalty program event activation dashboard")

left, mid, right, comp = st.columns(4)
left.metric("Total Audience", f"{df['audience_size'].sum():,}")
mid.metric("Estimated Conversions", f"{df['estimated_conversions'].sum():,}")
right.metric("Estimated Revenue", f"${df['estimated_revenue'].sum():,.0f}")
comp.metric("Compliance Pass Rate", f"{df['compliance_pass_rate'].mean():.1%}")

segment_filter = st.multiselect(
    "Select segment(s)",
    options=df["segment"].tolist(),
    default=df["segment"].tolist(),
)
filtered = df[df["segment"].isin(segment_filter)]

st.subheader("KPI Results vs Targets")
view = filtered[[
    "segment", "channel", "actual_open_rate", "target_open_rate", "actual_ctr", "target_ctr",
    "actual_conversion", "target_conversion", "revenue_per_cardholder", "redemption_lift",
    "compliance_pass_rate", "customer_feedback_score"
]].copy()
st.dataframe(
    view.style.format({
        "actual_open_rate": "{:.1%}",
        "target_open_rate": "{:.1%}",
        "actual_ctr": "{:.1%}",
        "target_ctr": "{:.1%}",
        "actual_conversion": "{:.1%}",
        "target_conversion": "{:.1%}",
        "revenue_per_cardholder": "${:.2f}",
        "redemption_lift": "{:.1%}",
        "compliance_pass_rate": "{:.1%}",
        "customer_feedback_score": "{:.1f}",
    }),
    use_container_width=True,
)

chart_data = filtered.set_index("segment")[["actual_open_rate", "actual_ctr", "actual_conversion"]]
st.bar_chart(chart_data)

st.subheader("What this shows")
st.write(
    "The strongest performance came from high-spend travel cardmembers, where premium access messaging drove the highest revenue per cardholder. "
    "Active redeemers performed above target because the offer connected to an existing points habit. Lapsed members had lower absolute conversion, "
    "but still beat target with a lighter reactivation message. Compliance controls passed across all segments, supporting launch confidence."
)

st.subheader("Recommended Next Actions")
st.markdown(
    """
1. Keep the next race-day activation focused on fewer, higher-value cardmember moments instead of broad mass offers.
2. Test a points-plus-experience message for active redeemers, since the segment showed strong redemption lift.
3. Preserve legal, compliance, translation, and digital QA gates in the workback tracker to avoid late-stage rework.
"""
)
