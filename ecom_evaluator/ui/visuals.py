"""Plotly charts and platform visuals for the results dashboard."""

from __future__ import annotations

import plotly.graph_objects as go

from ecom_evaluator.models import MarketingPlan, PlatformRecommendation, ScoredDimension

PLATFORM_VISUALS: dict[str, dict[str, str]] = {
    "TikTok": {"emoji": "🎵", "color": "#010101", "slug": "tiktok"},
    "Instagram": {"emoji": "📸", "color": "#E4405F", "slug": "instagram"},
    "Facebook": {"emoji": "👥", "color": "#1877F2", "slug": "facebook"},
    "YouTube": {"emoji": "▶️", "color": "#FF0000", "slug": "youtube"},
    "Google Ads": {"emoji": "🔍", "color": "#4285F4", "slug": "googleads"},
    "Amazon Ads": {"emoji": "📦", "color": "#FF9900", "slug": "amazon"},
    "Pinterest": {"emoji": "📌", "color": "#BD081C", "slug": "pinterest"},
    "Email/SMS": {"emoji": "✉️", "color": "#6366F1", "slug": "maildotru"},
    "Other": {"emoji": "🌐", "color": "#64748B", "slug": "googlechrome"},
}

CHANNEL_VISUALS: dict[str, dict[str, str]] = {
    "Amazon": {"emoji": "📦", "color": "#FF9900", "slug": "amazon"},
    "AliExpress": {"emoji": "🛒", "color": "#E43225", "slug": "aliexpress"},
    "Independent stores": {"emoji": "🏪", "color": "#6366F1", "slug": "shopify"},
}

ROI_COLORS = {"Low": "#94a3b8", "Medium": "#f59e0b", "High": "#10b981"}


def platform_icon_url(platform: str) -> str:
    meta = PLATFORM_VISUALS.get(platform, PLATFORM_VISUALS["Other"])
    slug = meta["slug"]
    color = meta["color"].lstrip("#")
    return f"https://cdn.simpleicons.org/{slug}/{color}"


def platform_color(platform: str) -> str:
    return PLATFORM_VISUALS.get(platform, PLATFORM_VISUALS["Other"])["color"]


def platform_emoji(platform: str) -> str:
    return PLATFORM_VISUALS.get(platform, PLATFORM_VISUALS["Other"])["emoji"]


def make_dimension_radar_chart(
    dimensions: list[tuple[str, ScoredDimension]],
    *,
    height: int = 340,
) -> go.Figure:
    labels = [label for label, _ in dimensions]
    values = [dim.score for _, dim in dimensions]
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            fillcolor="rgba(59, 130, 246, 0.18)",
            line={"color": "#2563EB", "width": 2},
            marker={"size": 7, "color": "#1E40AF"},
            name="Score",
        )
    )
    fig.update_layout(
        polar={
            "radialaxis": {
                "visible": True,
                "range": [0, 100],
                "tickvals": [0, 25, 50, 75, 100],
                "gridcolor": "#E2E8F0",
            },
            "angularaxis": {"gridcolor": "#E2E8F0", "linecolor": "#CBD5E1"},
            "bgcolor": "rgba(248, 250, 252, 0.6)",
        },
        height=height,
        margin=dict(l=40, r=40, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font={"family": "Inter, Segoe UI, sans-serif", "color": "#334155", "size": 11},
    )
    return fig


def make_platform_fit_chart(platforms: list[PlatformRecommendation], *, height: int = 320) -> go.Figure:
    ordered = sorted(platforms, key=lambda p: p.fit_score, reverse=True)
    names = [p.platform for p in ordered]
    scores = [p.fit_score for p in ordered]
    colors = [platform_color(name) for name in names]
    roi_labels = [p.roi_potential for p in ordered]

    fig = go.Figure(
        go.Bar(
            x=scores,
            y=names,
            orientation="h",
            marker={"color": colors, "line": {"color": "#ffffff", "width": 1}},
            text=[f"{s}/100 · ROI {r}" for s, r in zip(scores, roi_labels, strict=True)],
            textposition="outside",
            hovertemplate="%{y}<br>Fit: %{x}/100<extra></extra>",
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=80, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"range": [0, 110], "title": "Platform fit score", "gridcolor": "#E2E8F0"},
        yaxis={"autorange": "reversed"},
        font={"family": "Inter, Segoe UI, sans-serif", "color": "#334155"},
    )
    return fig


def make_organic_paid_chart(plan: MarketingPlan, *, height: int = 260) -> go.Figure:
    organic_score = sum(
        p.fit_score for p in plan.platform_recommendations if p.organic_vs_paid != "Paid-first"
    )
    paid_score = sum(
        p.fit_score for p in plan.platform_recommendations if p.organic_vs_paid != "Organic-first"
    )
    total = max(organic_score + paid_score, 1)
    organic_pct = round(organic_score / total * 100)
    paid_pct = 100 - organic_pct

    fig = go.Figure(
        go.Pie(
            labels=["Organic content", "Paid ads"],
            values=[organic_pct, paid_pct],
            hole=0.55,
            marker={"colors": ["#10B981", "#3B82F6"]},
            textinfo="label+percent",
            textfont={"size": 12, "color": "#0F172A"},
            hovertemplate="%{label}: %{percent}<extra></extra>",
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        annotations=[
            {
                "text": "Mix",
                "x": 0.5,
                "y": 0.5,
                "font": {"size": 14, "color": "#64748B"},
                "showarrow": False,
            }
        ],
    )
    return fig


def make_demand_gauge(level: str, *, height: int = 180) -> go.Figure:
    level_map = {"Low": 30, "Medium": 60, "High": 85, "Unknown": 45}
    value = level_map.get(level, 45)
    color = ROI_COLORS.get(level if level in ROI_COLORS else "Medium", "#64748B")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"prefix": level, "font": {"size": 18, "color": "#0f172a"}},
            title={"text": "Demand signal", "font": {"size": 13, "color": "#64748B"}},
            gauge={
                "axis": {"range": [0, 100], "visible": False},
                "bar": {"color": color, "thickness": 0.35},
                "bgcolor": "#f8fafc",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "#ecfdf5"},
                    {"range": [40, 70], "color": "#fffbeb"},
                    {"range": [70, 100], "color": "#fef2f2"},
                ],
            },
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def make_competition_gauge(signal: str, *, height: int = 180) -> go.Figure:
    signal_map = {"Few": 25, "Moderate": 55, "Many": 85, "Unknown": 45}
    value = signal_map.get(signal, 45)
    color = {"Few": "#10b981", "Moderate": "#f59e0b", "Many": "#ef4444", "Unknown": "#94a3b8"}.get(
        signal, "#94a3b8"
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"prefix": signal, "font": {"size": 16, "color": "#0f172a"}},
            title={"text": "Competition density", "font": {"size": 13, "color": "#64748B"}},
            gauge={
                "axis": {"range": [0, 100], "visible": False},
                "bar": {"color": color, "thickness": 0.35},
                "bgcolor": "#f8fafc",
                "borderwidth": 0,
            },
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
