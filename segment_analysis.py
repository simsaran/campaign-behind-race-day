"""Segment analysis for The Campaign Behind Race Day.
Fictional portfolio project for a premium Canadian loyalty program event activation.
"""
import pandas as pd

DATA_FILE = "race_day_campaign_data.csv"


def load_data(path: str = DATA_FILE) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["open_rate_delta"] = df["actual_open_rate"] - df["target_open_rate"]
    df["ctr_delta"] = df["actual_ctr"] - df["target_ctr"]
    df["conversion_delta"] = df["actual_conversion"] - df["target_conversion"]
    df["estimated_conversions"] = (df["audience_size"] * df["actual_conversion"]).round(0).astype(int)
    df["estimated_revenue"] = (df["audience_size"] * df["revenue_per_cardholder"]).round(2)
    df["meets_compliance_control"] = df["compliance_pass_rate"] >= 0.98
    return df


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "segment",
        "audience_size",
        "channel",
        "actual_open_rate",
        "actual_ctr",
        "actual_conversion",
        "conversion_delta",
        "estimated_conversions",
        "revenue_per_cardholder",
        "estimated_revenue",
        "compliance_pass_rate",
        "customer_feedback_score",
    ]
    return df[columns].sort_values("estimated_revenue", ascending=False)


if __name__ == "__main__":
    campaign = load_data()
    summary = summarize(campaign)
    print("Race Day Campaign Segment Summary")
    print(summary.to_string(index=False))
    print("\nOverall metrics:")
    print(f"Total audience: {campaign['audience_size'].sum():,}")
    print(f"Estimated conversions: {campaign['estimated_conversions'].sum():,}")
    print(f"Estimated revenue: ${campaign['estimated_revenue'].sum():,.2f}")
    print(f"Average compliance pass rate: {campaign['compliance_pass_rate'].mean():.1%}")
