from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import df, char_df, waveform_data, ap_waveform_data

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

MODELS = [f"Model {i+1}" for i in range(15)]
df["Model"] = df["Model"].replace({f"Model {chr(65+i)}": f"Model {i+1}" for i in range(15)})

BIOMECH_VARS = [
    "Loading Rate (BW/s)",
    "Braking Impulse (N·s/kg)",
    "Vertical Oscillation (cm)",
    "Contact Time (ms)",
    "Ankle Angle (°)",
    "Knee Angle (°)",
    "Pronation Angle (°)"
]

BG_COLOR = "#0d0d0d"
CARD_COLOR = "#1a1a1a"
ACCENT = "#00f5a0"
TEXT = "#ffffff"
SUBTEXT = "#aaaaaa"
GRID_COLOR = "#2a2a2a"

MODEL_COLORS = px.colors.qualitative.Light24[:15]

def card(children, style={}):
    base = {
        "backgroundColor": CARD_COLOR,
        "borderRadius": "12px",
        "padding": "20px",
        "marginBottom": "16px",
    }
    return html.Div(children, style={**base, **style})

app.layout = html.Div(style={"backgroundColor": BG_COLOR, "minHeight": "100vh", "fontFamily": "Inter, sans-serif", "color": TEXT}, children=[

    # Header
    html.Div(style={"padding": "24px 32px 8px", "borderBottom": f"1px solid {GRID_COLOR}"}, children=[
        html.H1("Footwear Biomechanics & Recovery Dashboard",
                style={"color": ACCENT, "fontSize": "24px", "fontWeight": "700", "margin": "0"}),
        html.P("De-identified shoe model analysis | Biomechanics × Wearable Integration",
               style={"color": SUBTEXT, "fontSize": "13px", "margin": "4px 0 0"}),
    ]),

    # Body
    html.Div(style={"display": "flex", "gap": "16px", "padding": "16px 32px"}, children=[

        # Sidebar
        html.Div(style={"width": "220px", "flexShrink": "0"}, children=[
            card([
                html.Label("Shoe Models", style={"color": ACCENT, "fontSize": "12px", "fontWeight": "600", "letterSpacing": "1px"}),
                dcc.Dropdown(
                    id="model-select",
                    options=[{"label": m, "value": m} for m in MODELS],
                    value=MODELS,
                    multi=True,
                    style={"backgroundColor": CARD_COLOR, "color": "#000000", "fontSize": "12px"},
                ),
            ]),
            card([
                html.Label("VO₂ Max", style={"color": ACCENT, "fontSize": "12px", "fontWeight": "600", "letterSpacing": "1px"}),
                dcc.Checklist(
                    id="vo2-filter",
                    options=[{"label": f"  {v}", "value": v} for v in ["Low", "Moderate", "High"]],
                    value=["Low", "Moderate", "High"],
                    labelStyle={"color": TEXT, "display": "block", "fontSize": "13px", "lineHeight": "2"},
                ),
            ]),
            card([
                html.Label("Speed", style={"color": ACCENT, "fontSize": "12px", "fontWeight": "600", "letterSpacing": "1px"}),
                dcc.Checklist(
                    id="speed-filter",
                    options=[{"label": f"  {s}", "value": s} for s in ["Walking", "Jogging", "Running"]],
                    value=["Walking", "Jogging", "Running"],
                    labelStyle={"color": TEXT, "display": "block", "fontSize": "13px", "lineHeight": "2"},
                ),
            ]),
        ]),

        # Main content
        html.Div(style={"flex": "1"}, children=[

            dcc.Tabs(id="tabs", value="tab-mechanics", style={"borderBottom": f"1px solid {GRID_COLOR}"}, children=[
                dcc.Tab(label="Shoe Mechanics", value="tab-mechanics",
                        style={"backgroundColor": BG_COLOR, "color": SUBTEXT, "border": "none", "padding": "10px 20px"},
                        selected_style={"backgroundColor": BG_COLOR, "color": ACCENT, "borderBottom": f"2px solid {ACCENT}", "border": "none", "padding": "10px 20px"}),
                dcc.Tab(label="Energy Cost", value="tab-energy",
                        style={"backgroundColor": BG_COLOR, "color": SUBTEXT, "border": "none", "padding": "10px 20px"},
                        selected_style={"backgroundColor": BG_COLOR, "color": ACCENT, "borderBottom": f"2px solid {ACCENT}", "border": "none", "padding": "10px 20px"}),
                dcc.Tab(label="Recovery Impact", value="tab-recovery",
                        style={"backgroundColor": BG_COLOR, "color": SUBTEXT, "border": "none", "padding": "10px 20px"},
                        selected_style={"backgroundColor": BG_COLOR, "color": ACCENT, "borderBottom": f"2px solid {ACCENT}", "border": "none", "padding": "10px 20px"}),
                dcc.Tab(label="Footwear Characteristics", value="tab-footwear",
                        style={"backgroundColor": BG_COLOR, "color": SUBTEXT, "border": "none", "padding": "10px 20px"},
                        selected_style={"backgroundColor": BG_COLOR, "color": ACCENT, "borderBottom": f"2px solid {ACCENT}", "border": "none", "padding": "10px 20px"}),
                dcc.Tab(label="Methodology", value="tab-methodology",
                        style={"backgroundColor": BG_COLOR, "color": SUBTEXT, "border": "none", "padding": "10px 20px"},
                        selected_style={"backgroundColor": BG_COLOR, "color": ACCENT, "borderBottom": f"2px solid {ACCENT}", "border": "none", "padding": "10px 20px"}),
                dcc.Tab(label="About", value="tab-about",
                        style={"backgroundColor": BG_COLOR, "color": SUBTEXT, "border": "none", "padding": "10px 20px"},
                        selected_style={"backgroundColor": BG_COLOR, "color": ACCENT, "borderBottom": f"2px solid {ACCENT}", "border": "none", "padding": "10px 20px"}),
            ]),

            html.Div(id="tab-content", style={"paddingTop": "16px"}),
        ]),
    ]),
])

def filter_df(models, vo2, speed):
    return df[
        df["Model"].isin(models) &
        df["VO2 Max Category"].isin(vo2) &
        df["Speed Category"].isin(speed)
    ]

def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor=CARD_COLOR,
        paper_bgcolor=CARD_COLOR,
        font_color=TEXT,
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
        legend=dict(bgcolor=CARD_COLOR, font=dict(color=TEXT, size=11)),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig

def eq_table(rows):
    return html.Table([
        html.Thead(html.Tr([
            html.Th("Outcome", style={"color": ACCENT, "padding": "8px 14px", "fontSize": "12px",
                                      "fontWeight": "700", "borderBottom": f"2px solid {ACCENT}",
                                      "width": "18%"}),
            html.Th("Equation", style={"color": ACCENT, "padding": "8px 14px", "fontSize": "12px",
                                       "fontWeight": "700", "borderBottom": f"2px solid {ACCENT}",
                                       "width": "52%"}),
            html.Th("Interpretation", style={"color": ACCENT, "padding": "8px 14px", "fontSize": "12px",
                                              "fontWeight": "700", "borderBottom": f"2px solid {ACCENT}",
                                              "width": "30%"}),
        ])),
        html.Tbody([
            html.Tr([
                html.Td(name, style={"color": ACCENT, "padding": "8px 14px", "fontSize": "12px",
                                     "fontWeight": "600", "borderBottom": f"1px solid {GRID_COLOR}",
                                     "verticalAlign": "top"}),
                html.Td(eq, style={"color": TEXT, "padding": "8px 14px", "fontSize": "12px",
                                   "fontFamily": "monospace", "borderBottom": f"1px solid {GRID_COLOR}",
                                   "lineHeight": "1.6", "verticalAlign": "top"}),
                html.Td(interp, style={"color": SUBTEXT, "padding": "8px 14px", "fontSize": "12px",
                                       "borderBottom": f"1px solid {GRID_COLOR}",
                                       "lineHeight": "1.6", "verticalAlign": "top"}),
            ]) for name, eq, interp in rows
        ])
    ], style={"width": "100%", "borderCollapse": "collapse", "marginBottom": "8px"})

def plot_note(text):
    return html.P(text, style={
        "color": SUBTEXT, "fontSize": "12px", "lineHeight": "1.6",
        "marginTop": "8px", "fontStyle": "italic",
        "borderLeft": f"2px solid {GRID_COLOR}", "paddingLeft": "10px"
    })

def key_findings_card(findings):
    return card([
        html.H3("Key Findings", style={"color": ACCENT, "fontSize": "14px",
                                        "fontWeight": "700", "marginBottom": "12px",
                                        "letterSpacing": "0.5px"}),
        html.Ul([
            html.Li(f, style={"color": TEXT, "fontSize": "13px",
                               "lineHeight": "1.8", "marginBottom": "4px"})
            for f in findings
        ], style={"paddingLeft": "20px", "margin": "0"}),
    ])

@callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    Input("model-select", "value"),
    Input("vo2-filter", "value"),
    Input("speed-filter", "value"),
)
def render_tab(tab, models, vo2, speed):
    filtered = filter_df(models or MODELS, vo2 or ["Low","Moderate","High"], speed or ["Walking","Jogging","Running"])
    avg = filtered.groupby("Model")[BIOMECH_VARS].mean().reset_index()

    # Sort models numerically
    avg["_sort"] = avg["Model"].str.extract(r"(\d+)").astype(int)
    avg = avg.sort_values("_sort").drop(columns="_sort")

    if tab == "tab-mechanics":

        # Heatmap — models × variables
        import numpy as np
        heatmap_data = avg.set_index("Model")[BIOMECH_VARS]
        # Z-score normalize each column so variables are comparable
        normalized = (heatmap_data - heatmap_data.mean()) / (heatmap_data.std() + 1e-9)

        heatmap_fig = go.Figure(go.Heatmap(
            z=normalized.values,
            x=BIOMECH_VARS,
            y=normalized.index.tolist(),
            colorscale=[[0, "#003f5c"], [0.5, "#1a1a1a"], [1, "#00f5a0"]],
            zmid=0,
            text=heatmap_data.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
            hovertemplate="<b>%{y}</b><br>%{x}<br>Value: %{text}<extra></extra>",
            showscale=True,
            colorbar=dict(
                tickfont=dict(color=TEXT),
                title=dict(text="Z-score", font=dict(color=SUBTEXT, size=11)),
            )
        ))
        heatmap_fig.update_layout(
            plot_bgcolor=CARD_COLOR,
            paper_bgcolor=CARD_COLOR,
            font_color=TEXT,
            height=500,
            margin=dict(l=80, r=40, t=40, b=120),
            xaxis=dict(tickangle=-30, tickfont=dict(color=TEXT, size=11), gridcolor=GRID_COLOR),
            yaxis=dict(tickfont=dict(color=TEXT, size=11), gridcolor=GRID_COLOR),
            title=dict(text="Biomechanical Profile Heatmap (Z-scored)", font=dict(color=TEXT, size=14)),
        )

        return html.Div([
            card([
                dcc.Graph(figure=heatmap_fig, config={"displayModeBar": False}),
                plot_note(
                    "Each row is a shoe model; each column is a biomechanical variable. "
                    "Colors reflect z-scored values — green indicates above the cross-model mean, dark blue below — allowing comparison across variables with different units."
                ),
            ]),
        ])

    elif tab == "tab-energy":
        import numpy as np
        selected_models = models or MODELS
        t = np.linspace(0, 100, 101)

        # ── A-P GRF Waveforms ───────────────────────────────────────────────
        ap_fig = go.Figure()
        for i, model in enumerate(selected_models):
            if model not in ap_waveform_data:
                continue
            trials = ap_waveform_data[model]
            mean   = trials.mean(axis=0)
            sd     = trials.std(axis=0)
            color  = MODEL_COLORS[MODELS.index(model) % 15]

            ap_fig.add_trace(go.Scatter(
                x=np.concatenate([t, t[::-1]]),
                y=np.concatenate([mean + sd, (mean - sd)[::-1]]),
                fill="toself",
                fillcolor=color.replace("rgb", "rgba").replace(")", ", 0.08)") if "rgb" in color else color,
                line=dict(width=0), showlegend=False, hoverinfo="skip",
            ))
            ap_fig.add_trace(go.Scatter(
                x=t, y=mean, mode="lines", name=model,
                line=dict(color=color, width=2),
                hovertemplate=f"<b>{model}</b><br>%{{x:.0f}}% stance<br>%{{y:.3f}} BW<extra></extra>",
            ))

        # Zero line
        ap_fig.add_hline(y=0, line_dash="dash", line_color=SUBTEXT, opacity=0.5)

        # Shade braking region
        ap_fig.add_vrect(x0=0, x1=50, fillcolor="#ff4444", opacity=0.04,
                         layer="below", line_width=0,
                         annotation_text="Braking", annotation_position="top left",
                         annotation_font=dict(color="#ff4444", size=11))
        ap_fig.add_vrect(x0=50, x1=100, fillcolor="#00f5a0", opacity=0.04,
                         layer="below", line_width=0,
                         annotation_text="Propulsion", annotation_position="top right",
                         annotation_font=dict(color=ACCENT, size=11))

        ap_fig.update_layout(
            plot_bgcolor=CARD_COLOR, paper_bgcolor=CARD_COLOR, font_color=TEXT,
            height=400,
            title=dict(text="Anterior-Posterior GRF Waveforms (± 1 SD)", font=dict(color=TEXT, size=14)),
            xaxis=dict(title=dict(text="% Stance", font=dict(color=SUBTEXT)),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT)),
            yaxis=dict(title=dict(text="A-P GRF (BW)", font=dict(color=SUBTEXT)),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT)),
            legend=dict(bgcolor=CARD_COLOR, font=dict(color=TEXT, size=10),
                        orientation="v", x=1.01, y=1),
            margin=dict(l=50, r=120, t=50, b=50),
        )

        # ── Impulse summary derived from waveforms ───────────────────────────
        impulse_rows = []
        for model in selected_models:
            if model not in ap_waveform_data:
                continue
            mean_ap = ap_waveform_data[model].mean(axis=0)
            braking_impulse    = abs(mean_ap[mean_ap < 0].sum()) / 100
            propulsive_impulse = mean_ap[mean_ap > 0].sum() / 100
            ratio = propulsive_impulse / (braking_impulse + 1e-9)
            impulse_rows.append({
                "Model": model,
                "Braking Impulse (BW·s)": round(braking_impulse, 4),
                "Propulsive Impulse (BW·s)": round(propulsive_impulse, 4),
                "Propulsion:Braking Ratio": round(ratio, 3),
            })
        impulse_df = pd.DataFrame(impulse_rows).sort_values(
            "Propulsion:Braking Ratio", ascending=False).reset_index(drop=True)

        # Grouped bar: braking vs propulsive impulse
        impulse_fig = go.Figure()
        impulse_fig.add_trace(go.Bar(
            x=impulse_df["Model"], y=impulse_df["Braking Impulse (BW·s)"],
            name="Braking Impulse", marker_color="#ff4444",
        ))
        impulse_fig.add_trace(go.Bar(
            x=impulse_df["Model"], y=impulse_df["Propulsive Impulse (BW·s)"],
            name="Propulsive Impulse", marker_color=ACCENT,
        ))
        impulse_fig.update_layout(
            plot_bgcolor=CARD_COLOR, paper_bgcolor=CARD_COLOR, font_color=TEXT,
            barmode="group", height=320,
            title=dict(text="Braking vs. Propulsive Impulse by Model (derived from A-P waveform)",
                       font=dict(color=TEXT, size=13)),
            xaxis=dict(tickangle=-45, tickfont=dict(color=TEXT, size=9),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
            yaxis=dict(title=dict(text="Impulse (BW·s)", font=dict(color=SUBTEXT)),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT)),
            legend=dict(bgcolor=CARD_COLOR, font=dict(color=TEXT, size=11)),
            margin=dict(l=50, r=20, t=40, b=80),
        )

        # Ratio bar
        ratio_fig = px.bar(
            impulse_df, x="Model", y="Propulsion:Braking Ratio",
            color="Model", color_discrete_sequence=MODEL_COLORS,
            title="Propulsion:Braking Ratio by Model"
        )
        ratio_fig = apply_dark_theme(ratio_fig)
        ratio_fig.update_layout(height=320, showlegend=False, title_font_size=13)
        ratio_fig.update_xaxes(tickangle=-45, tickfont=dict(size=9))
        ratio_fig.add_hline(y=1.0, line_dash="dash", line_color=SUBTEXT, opacity=0.5,
                            annotation_text="Braking = Propulsion",
                            annotation_font=dict(color=SUBTEXT, size=10),
                            annotation_position="bottom right")

        # Impulse summary table
        table_header = [html.Tr([
            html.Th(c, style={"color": ACCENT, "padding": "8px 12px",
                               "borderBottom": f"2px solid {ACCENT}", "fontSize": "12px",
                               "fontWeight": "700"})
            for c in ["Rank", "Model", "Braking Impulse (BW·s)",
                      "Propulsive Impulse (BW·s)", "Propulsion:Braking Ratio"]
        ])]
        table_rows_html = [html.Tr([
            html.Td(str(i+1), style={"color": SUBTEXT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(row["Model"], style={"color": TEXT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(f"{row['Braking Impulse (BW·s)']:.4f}",
                    style={"color": "#ff4444", "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(f"{row['Propulsive Impulse (BW·s)']:.4f}",
                    style={"color": ACCENT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(f"{row['Propulsion:Braking Ratio']:.3f}",
                    style={"color": ACCENT if row['Propulsion:Braking Ratio'] >= 1.0 else "#ff4444",
                           "padding": "6px 12px", "fontSize": "12px", "fontWeight": "600"}),
        ]) for i, (_, row) in enumerate(impulse_df.iterrows())]

        # Key findings
        top_ratio = impulse_df.iloc[0]
        bottom_ratio = impulse_df.iloc[-1]
        plated_set = set(char_df[char_df["Plated"] == "Yes"]["Model"].tolist())
        plated_models = [m for m in selected_models if m in plated_set]
        energy_findings = [
            f"Most economical model: {top_ratio['Model']} (Propulsion:Braking Ratio = {top_ratio['Propulsion:Braking Ratio']:.2f})",
            f"Least economical model: {bottom_ratio['Model']} (Propulsion:Braking Ratio = {bottom_ratio['Propulsion:Braking Ratio']:.2f})",
            f"{len(plated_models)} of {len(selected_models)} selected models are plated — plated models tend to cluster toward higher propulsion:braking ratios.",
            "Models with higher midsole stiffness and rocker geometry show shallower braking phases in the A-P waveform.",
        ]

        return html.Div([
            key_findings_card(energy_findings),
            card([
                html.P(
                    "Energy cost is visualized through both waveform shape and derived impulse metrics. "
                    "The A-P GRF waveform shows the full braking-to-propulsion profile across stance — "
                    "models that minimize the braking phase (red region) and maximize propulsion (green region) "
                    "are the most economical. The Propulsion:Braking Ratio summarizes this as a single number: "
                    "values above 1.0 indicate net propulsive efficiency.",
                    style={"color": SUBTEXT, "fontSize": "12px", "lineHeight": "1.6",
                           "fontStyle": "italic", "borderLeft": f"2px solid {ACCENT}",
                           "paddingLeft": "10px"}
                ),
            ]),
            card([
                dcc.Graph(figure=ap_fig, config={"displayModeBar": False}),
                plot_note(
                    "The curve crosses zero at ~50% stance, separating braking (negative, red shaded) from propulsion (positive, green shaded). "
                    "Models with a shallow braking dip and a tall propulsive peak impose less energy cost per stride."
                ),
            ]),
            card([
                html.Div([
                    html.Div([
                        dcc.Graph(figure=impulse_fig, config={"displayModeBar": False}),
                        plot_note(
                            "Impulse is the area under the A-P GRF curve — capturing both the magnitude and duration of braking and propulsive forces. "
                            "A smaller red bar relative to the green bar indicates the shoe facilitates more efficient horizontal force production."
                        ),
                    ], style={"width": "55%"}),
                    html.Div([
                        dcc.Graph(figure=ratio_fig, config={"displayModeBar": False}),
                        plot_note(
                            "The Propulsion:Braking Ratio divides propulsive impulse by braking impulse. "
                            "Values above the dashed line (ratio > 1.0) indicate the shoe returns more energy forward than it wastes on deceleration."
                        ),
                    ], style={"width": "45%"}),
                ], style={"display": "flex", "gap": "16px"}),
            ]),
            card([
                html.H3("Impulse Summary", style={"color": ACCENT, "fontSize": "14px",
                                                   "marginBottom": "8px"}),
                html.P(
                    "Braking and propulsive impulse are calculated as the area under the negative and positive "
                    "phases of the A-P GRF waveform respectively, normalized to body weight × time (BW·s). "
                    "A higher Propulsion:Braking Ratio indicates the shoe facilitates more forward energy "
                    "return relative to deceleration cost. Models are ranked by this ratio.",
                    style={"color": SUBTEXT, "fontSize": "11px", "lineHeight": "1.6",
                           "marginBottom": "12px", "fontStyle": "italic",
                           "borderLeft": f"2px solid {ACCENT}", "paddingLeft": "10px"}
                ),
                html.Table(table_header + table_rows_html,
                           style={"width": "100%", "borderCollapse": "collapse"}),
            ]),
        ])

    elif tab == "tab-recovery":
        import numpy as np
        selected_models = models or MODELS
        t = np.linspace(0, 100, 101)

        recovery_vars = ["Braking Impulse (N·s/kg)", "Pronation Angle (°)", "Running Power (W)", "Day Strain", "HRV (ms)"]
        avg_recovery = filtered.groupby("Model")[recovery_vars].mean().reset_index()
        avg_recovery["_sort"] = avg_recovery["Model"].str.extract(r"(\d+)").astype(int)
        avg_recovery = avg_recovery.sort_values("_sort").drop(columns="_sort")

        # ── vGRF Impact Phase Zoom (0-30% stance) ───────────────────────────
        impact_fig = go.Figure()
        for i, model in enumerate(selected_models):
            if model not in waveform_data:
                continue
            trials = waveform_data[model]
            mean   = trials.mean(axis=0)
            sd     = trials.std(axis=0)
            color  = MODEL_COLORS[MODELS.index(model) % 15]

            t_impact = t[:31]
            mean_impact = mean[:31]
            sd_impact   = sd[:31]

            impact_fig.add_trace(go.Scatter(
                x=np.concatenate([t_impact, t_impact[::-1]]),
                y=np.concatenate([mean_impact + sd_impact, (mean_impact - sd_impact)[::-1]]),
                fill="toself",
                fillcolor=color.replace("rgb", "rgba").replace(")", ", 0.08)") if "rgb" in color else color,
                line=dict(width=0), showlegend=False, hoverinfo="skip",
            ))
            impact_fig.add_trace(go.Scatter(
                x=t_impact, y=mean_impact, mode="lines", name=model,
                line=dict(color=color, width=2),
                hovertemplate=f"<b>{model}</b><br>%{{x:.0f}}% stance<br>%{{y:.2f}} BW<extra></extra>",
            ))

            # Annotate loading rate as slope between 5-15% stance
            slope_x = [5, 15]
            slope_y = [mean[5], mean[15]]
            loading_rate = (slope_y[1] - slope_y[0]) / 10
            impact_fig.add_trace(go.Scatter(
                x=slope_x, y=slope_y, mode="lines",
                line=dict(color=color, width=1, dash="dot"),
                showlegend=False, hoverinfo="skip",
            ))

        impact_fig.add_vrect(x0=0, x1=15, fillcolor="#ff4444", opacity=0.04,
                             layer="below", line_width=0,
                             annotation_text="Rapid Loading", annotation_position="top left",
                             annotation_font=dict(color="#ff4444", size=10))
        impact_fig.add_vrect(x0=15, x1=30, fillcolor="#ffffff", opacity=0.02,
                             layer="below", line_width=0,
                             annotation_text="Load Acceptance", annotation_position="top left",
                             annotation_font=dict(color=SUBTEXT, size=10))

        impact_fig.update_layout(
            plot_bgcolor=CARD_COLOR, paper_bgcolor=CARD_COLOR, font_color=TEXT,
            height=380,
            title=dict(text="vGRF Impact Phase (0–30% Stance) — Loading Rate Comparison",
                       font=dict(color=TEXT, size=14)),
            xaxis=dict(title=dict(text="% Stance", font=dict(color=SUBTEXT)),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT)),
            yaxis=dict(title=dict(text="vGRF (BW)", font=dict(color=SUBTEXT)),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT)),
            legend=dict(bgcolor=CARD_COLOR, font=dict(color=TEXT, size=10),
                        orientation="v", x=1.01, y=1),
            margin=dict(l=50, r=120, t=50, b=50),
        )

        # ── Scatter plots using waveform-derived impulse ─────────────────────
        # Derive braking impulse from ap waveforms for selected models
        impulse_map = {}
        for model in selected_models:
            if model in ap_waveform_data:
                mean_ap = ap_waveform_data[model].mean(axis=0)
                impulse_map[model] = abs(mean_ap[mean_ap < 0].sum()) / 100

        avg_recovery["Waveform Braking Impulse"] = avg_recovery["Model"].map(impulse_map)

        # Recovery ranking table
        avg_recovery["Recovery Score"] = (
            (avg_recovery["HRV (ms)"] / avg_recovery["HRV (ms)"].max()) * 0.5 +
            (1 - avg_recovery["Day Strain"] / avg_recovery["Day Strain"].max()) * 0.3 +
            (1 - avg_recovery["Waveform Braking Impulse"] / avg_recovery["Waveform Braking Impulse"].max()) * 0.2
        ) * 100
        ranking = avg_recovery[["Model", "HRV (ms)", "Day Strain",
                                 "Waveform Braking Impulse", "Recovery Score"]].sort_values(
            "Recovery Score", ascending=False).reset_index(drop=True)

        table_header = [html.Tr([
            html.Th(c, style={"color": ACCENT, "padding": "8px 12px",
                               "borderBottom": f"2px solid {ACCENT}", "fontSize": "12px",
                               "fontWeight": "700"})
            for c in ["Rank", "Model", "HRV (ms)", "Day Strain",
                      "Braking Impulse (BW·s)", "Recovery Score"]
        ])]
        table_rows = [html.Tr([
            html.Td(str(i+1), style={"color": SUBTEXT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(row["Model"], style={"color": TEXT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(f"{row['HRV (ms)']:.1f}", style={"color": TEXT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(f"{row['Day Strain']:.2f}", style={"color": TEXT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(f"{row['Waveform Braking Impulse']:.4f}", style={"color": TEXT, "padding": "6px 12px", "fontSize": "12px"}),
            html.Td(f"{row['Recovery Score']:.1f}", style={"color": ACCENT, "padding": "6px 12px",
                                                            "fontSize": "12px", "fontWeight": "600"}),
        ]) for i, (_, row) in enumerate(ranking.iterrows())]

        # Key findings
        best_recovery = ranking.iloc[0]
        worst_recovery = ranking.iloc[-1]
        high_hrv = ranking.nlargest(3, "HRV (ms)")["Model"].tolist()
        recovery_findings = [
            f"Best recovery model: {best_recovery['Model']} (Recovery Score = {best_recovery['Recovery Score']:.1f})",
            f"Worst recovery model: {worst_recovery['Model']} (Recovery Score = {worst_recovery['Recovery Score']:.1f})",
            f"Highest HRV models: {', '.join(high_hrv)} — indicating lower autonomic stress post-run.",
            "Models with lower waveform-derived braking impulse consistently show higher HRV and lower Day Strain.",
        ]

        return html.Div([
            key_findings_card(recovery_findings),
            card([
                html.P(
                    "Recovery impact is assessed through the mechanical load profile during stance and its "
                    "downstream effect on wearable-derived recovery metrics. "
                    "The impact phase waveform shows how abruptly each model loads the body — "
                    "steeper slopes indicate greater physiological stress. "
                    "The Recovery Rankings table summarizes the full mechanical-to-physiological chain as a single composite score.",
                    style={"color": SUBTEXT, "fontSize": "12px", "lineHeight": "1.6",
                           "fontStyle": "italic", "borderLeft": f"2px solid {ACCENT}",
                           "paddingLeft": "10px"}
                ),
            ]),
            card([
                dcc.Graph(figure=impact_fig, config={"displayModeBar": False}),
                plot_note(
                    "This zoomed view isolates the first 30% of stance where impact loading occurs. "
                    "The slope of each curve during the rapid loading phase (0–15%) reflects instantaneous loading rate — steeper slopes indicate more abrupt force application and greater injury and recovery stress."
                ),
            ]),
            card([
                html.H3("Recovery Rankings", style={"color": ACCENT, "fontSize": "14px",
                                                     "marginBottom": "8px"}),
                html.P(
                    "Recovery Score is a weighted composite: HRV (50%) + inverse Day Strain (30%) + "
                    "inverse Waveform-Derived Braking Impulse (20%). All components normalized 0–1. "
                    "Scores range from 0–100; higher scores indicate better post-run recovery. "
                    "Braking impulse is derived directly from the A-P GRF waveform for methodological consistency.",
                    style={"color": SUBTEXT, "fontSize": "11px", "lineHeight": "1.6",
                           "marginBottom": "12px", "fontStyle": "italic",
                           "borderLeft": f"2px solid {ACCENT}", "paddingLeft": "10px"}
                ),
                html.Table(table_header + table_rows,
                           style={"width": "100%", "borderCollapse": "collapse"}),
            ]),
            card([
                html.H3("Statistical Parametric Mapping (SPM)", style={
                    "color": ACCENT, "fontSize": "14px", "marginBottom": "8px"
                }),
                html.P([
                    "SPM tests for statistically significant differences in vGRF waveforms across selected models. ",
                    html.Span("Select between 2 and 4 models in the sidebar to see SPM results — ",
                              style={"color": ACCENT, "fontWeight": "600"}),
                    "selecting 1 model or all 15 will not produce meaningful inference. "
                    "2 models runs a t-test; 3–4 models runs a one-way ANOVA. "
                    "Shaded regions indicate where waveform differences exceed the α=0.05 threshold.",
                ], style={"color": SUBTEXT, "fontSize": "12px", "lineHeight": "1.6",
                          "marginBottom": "16px", "borderLeft": f"2px solid {ACCENT}",
                          "paddingLeft": "10px", "fontStyle": "italic"}),
                html.Div(id="spm-content"),
            ]),
        ])

    elif tab == "tab-footwear":

        # Filter to selected models only
        display = char_df[char_df["Model"].isin(models or MODELS)].copy()
        display["_sort"] = display["Model"].str.extract(r"(\d+)").astype(int)
        display = display.sort_values("_sort").drop(columns="_sort")

        CHAR_COLS = [
            "Model", "Stack Height (mm)", "Heel Drop (mm)", "Midsole Stiffness",
            "Stability Index", "Foam Type", "Plated", "Rocker Angle (°)", "Weight (g)"
        ]

        col_labels = {
            "Model": "Shoe Model",
            "Stack Height (mm)": "Stack Height (mm)",
            "Heel Drop (mm)": "Drop (mm)",
            "Midsole Stiffness": "Midsole Stiffness",
            "Stability Index": "Stability Index",
            "Foam Type": "Foam Type",
            "Plated": "Plated",
            "Rocker Angle (°)": "Rocker Angle (°)",
            "Weight (g)": "Weight (g)",
        }

        def cell_color(col, val):
            """Return accent color for notable values."""
            if col == "Plated":
                return ACCENT if val == "Yes" else TEXT
            if col == "Foam Type":
                return ACCENT if val == "PEBA" else TEXT
            return TEXT

        header = html.Tr([
            html.Th(col_labels[c], style={
                "color": ACCENT, "padding": "10px 14px",
                "borderBottom": f"2px solid {ACCENT}",
                "fontSize": "12px", "fontWeight": "700",
                "letterSpacing": "0.5px", "textAlign": "center",
                "whiteSpace": "nowrap",
            }) for c in CHAR_COLS
        ])

        rows_html = []
        for i, row in display.iterrows():
            bg = "#1f1f1f" if i % 2 == 0 else CARD_COLOR
            cells = []
            for c in CHAR_COLS:
                val = row[c]
                color = cell_color(c, val)
                cells.append(html.Td(str(val), style={
                    "color": color, "padding": "8px 14px",
                    "fontSize": "13px", "textAlign": "center",
                    "borderBottom": f"1px solid {GRID_COLOR}",
                }))
            rows_html.append(html.Tr(cells, style={"backgroundColor": bg}))

        description = html.P(
            "The table below lists the physical and structural properties for each de-identified shoe model. "
            "These characteristics are the inputs that drive the biomechanical simulation model.",
            style={"color": SUBTEXT, "fontSize": "13px", "marginBottom": "16px", "lineHeight": "1.6"}
        )

        legend = html.Div([
            html.Span("● PEBA foam  ", style={"color": ACCENT, "fontSize": "12px"}),
            html.Span("● Plated models highlighted in green  ", style={"color": ACCENT, "fontSize": "12px"}),
            html.Span("● All others in white", style={"color": TEXT, "fontSize": "12px"}),
        ], style={"marginBottom": "16px"})

        table = html.Table(
            [html.Thead(header), html.Tbody(rows_html)],
            style={"width": "100%", "borderCollapse": "collapse"}
        )

        return card([description, legend, table])

    elif tab == "tab-methodology":
        return html.Div([
            card([
                html.H2("Methodology", style={"color": ACCENT, "fontSize": "20px",
                                               "fontWeight": "700", "marginBottom": "16px"}),
                html.P(
                    "All biomechanical and physiological outcomes in this dashboard are derived from shoe physical "
                    "properties using the equations below. Each equation incorporates a normally distributed noise "
                    "term (ε) to simulate real-world biological variability across participants. "
                    "Speed multipliers are dimensionless scaling factors applied relative to jogging as the reference condition (1.00). "
                    "Walking outputs are scaled to 70% of the jogging reference; running outputs to 135%. "
                    "These multipliers reflect the relative increase in mechanical demand across speed conditions rather than absolute velocity values.",
                    style={"color": SUBTEXT, "fontSize": "13px", "lineHeight": "1.7",
                           "fontStyle": "italic"}
                ),
            ]),
            card([
                html.H3("Biomechanical Outcomes", style={"color": TEXT, "fontSize": "14px",
                                                          "fontWeight": "700", "marginBottom": "12px",
                                                          "borderBottom": f"1px solid {GRID_COLOR}",
                                                          "paddingBottom": "6px"}),
                eq_table([
                    ("Loading Rate", "(80 − Stack Height × 1.2 + Heel Drop × 0.8 + ε) × Speed Multiplier",
                     "Higher stack reduces abrupt loading; greater heel drop increases it."),
                    ("Braking Impulse", "(0.18 − Stiffness × 0.008 + Heel Drop × 0.003 + ε) × Speed Multiplier",
                     "Stiffer midsoles reduce braking; higher heel drop increases deceleration force."),
                    ("Vertical Oscillation", "(8 + Stack Height × 0.15 − Stiffness × 0.3 + ε) × Speed Multiplier",
                     "More cushion increases bounce; stiffer plates reduce it."),
                    ("Contact Time", "280 − Stack Height × 1.5 − Speed Multiplier × 40 + ε",
                     "Thicker stacks and faster speeds reduce ground contact duration."),
                    ("Ankle Angle", "12 + Heel Drop × 0.6 + ε",
                     "Higher heel drop reduces dorsiflexion demand at the ankle."),
                    ("Knee Angle", "18 + Stack Height × 0.2 − Heel Drop × 0.3 + ε",
                     "More stack increases knee flexion; higher drop slightly reduces it."),
                    ("Pronation Angle", "6 − Stiffness × 0.4 + ε",
                     "Stiffer midsoles reduce rearfoot eversion."),
                ]),
            ]),
            card([
                html.H3("Energy Cost Outcomes", style={"color": TEXT, "fontSize": "14px",
                                                        "fontWeight": "700", "marginBottom": "12px",
                                                        "borderBottom": f"1px solid {GRID_COLOR}",
                                                        "paddingBottom": "6px"}),
                eq_table([
                    ("Running Power", "(280 + Braking Impulse × 200 + Vertical Oscillation × 8 + ε) × Speed Multiplier",
                     "Power demand rises with both braking cost and vertical bounce."),
                    ("Vertical Ratio", "Vertical Oscillation / (150 × Speed Multiplier) × 100",
                     "Normalizes oscillation by stride length to allow speed-independent economy comparison."),
                    ("Braking Impulse (A-P)", "Area under negative A-P GRF curve / 100",
                     "Derived from waveform integration — captures duration and magnitude of deceleration force."),
                    ("Propulsive Impulse (A-P)", "Area under positive A-P GRF curve / 100",
                     "Derived from waveform integration — captures forward energy return per stride."),
                    ("Propulsion:Braking Ratio", "Propulsive Impulse / Braking Impulse",
                     "Values above 1.0 indicate net propulsive efficiency. Primary economy ranking metric."),
                ]),
            ]),
            card([
                html.H3("Wearable Outcomes", style={"color": TEXT, "fontSize": "14px",
                                                     "fontWeight": "700", "marginBottom": "12px",
                                                     "borderBottom": f"1px solid {GRID_COLOR}",
                                                     "paddingBottom": "6px"}),
                eq_table([
                    ("Day Strain", "10 + Running Power × 0.02 + ε",
                     "Cardiovascular load scales with mechanical power demand."),
                    ("HRV", "65 − Braking Impulse × 80 − Day Strain × 0.5 + VO₂ Max × 0.3 + ε",
                     "Recovery quality decreases with mechanical stress and strain; higher fitness buffers this effect."),
                ]),
            ]),
            card([
                html.H3("Recovery Score", style={"color": TEXT, "fontSize": "14px",
                                                  "fontWeight": "700", "marginBottom": "12px",
                                                  "borderBottom": f"1px solid {GRID_COLOR}",
                                                  "paddingBottom": "6px"}),
                eq_table([
                    ("Recovery Score", "((HRV / HRV_max) × 0.5 + (1 − Strain / Strain_max) × 0.3 + (1 − Braking / Braking_max) × 0.2) × 100",
                     "All components normalized 0–1 across models before weighting. Scores range 0–100; higher is better."),
                ]),
                html.P(
                    "Note: A-P GRF waveforms for braking and propulsive impulse are simulated using shoe physical properties "
                    "(stack height, heel drop, midsole stiffness, plate presence, rocker angle) as inputs, with participant-level "
                    "noise added to each trial. SPM inference uses the spm1d Python library.",
                    style={"color": SUBTEXT, "fontSize": "12px", "lineHeight": "1.6",
                           "marginTop": "16px", "fontStyle": "italic",
                           "borderLeft": f"2px solid {ACCENT}", "paddingLeft": "10px"}
                ),
            ]),
        ])

    elif tab == "tab-about":

        def section(title, content):
            return html.Div([
                html.H3(title, style={"color": ACCENT, "fontSize": "15px", "fontWeight": "700",
                                      "marginBottom": "10px", "letterSpacing": "0.5px"}),
                html.P(content, style={"color": TEXT, "fontSize": "13px", "lineHeight": "1.8", "marginBottom": "0"}),
            ], style={"marginBottom": "24px"})

        def var_row(name, definition):
            return html.Tr([
                html.Td(name, style={"color": ACCENT, "padding": "8px 14px", "fontSize": "13px",
                                     "fontWeight": "600", "borderBottom": f"1px solid {GRID_COLOR}",
                                     "whiteSpace": "nowrap", "verticalAlign": "top"}),
                html.Td(definition, style={"color": TEXT, "padding": "8px 14px", "fontSize": "13px",
                                           "borderBottom": f"1px solid {GRID_COLOR}", "lineHeight": "1.6"}),
            ])

        var_table = html.Table([
            html.Thead(html.Tr([
                html.Th("Variable", style={"color": ACCENT, "padding": "10px 14px",
                                           "borderBottom": f"2px solid {ACCENT}", "fontSize": "12px",
                                           "fontWeight": "700", "letterSpacing": "0.5px"}),
                html.Th("Definition", style={"color": ACCENT, "padding": "10px 14px",
                                              "borderBottom": f"2px solid {ACCENT}", "fontSize": "12px",
                                              "fontWeight": "700", "letterSpacing": "0.5px"}),
            ])),
            html.Tbody([
                var_row("Loading Rate (BW/s)", "How quickly impact force builds at foot strike, relative to body weight. Higher values mean more abrupt loading."),
                var_row("Braking Impulse (N·s/kg)", "The horizontal force that slows the body down on each step, normalized to body mass. Lower is more efficient."),
                var_row("Vertical Oscillation (cm)", "How much the body bounces up and down per stride. Less bounce means more energy directed forward."),
                var_row("Vertical Ratio (%)", "Vertical oscillation relative to stride length. The cleanest single measure of running efficiency."),
                var_row("Contact Time (ms)", "How long the foot stays on the ground each step. Shorter contact is generally associated with better economy."),
                var_row("Ankle Angle (°)", "Peak ankle bend during stance. Affected by heel drop — higher drop tends to reduce ankle flexion demand."),
                var_row("Knee Angle (°)", "Peak knee bend at midstance. Influenced by stack height and how the shoe distributes shock up the leg."),
                var_row("Pronation Angle (°)", "How much the foot rolls inward during stance. Relevant to stability design and long-term injury risk."),
                var_row("Running Power (W)", "Estimated energy output per stride combining propulsion, bounce, and contact time. Lower power at the same speed means a more economical shoe."),
                var_row("Day Strain", "A wearable-derived score (0–21) reflecting how hard the cardiovascular system worked during the session."),
                var_row("HRV (ms)", "Heart rate variability after the run — a measure of how well the body is recovering. Higher is better."),
                var_row("Recovery Score", "A composite ranking weighted by HRV (50%), Day Strain (30%), and Braking Impulse (20%). Higher score = better recovery profile."),
            ])
        ], style={"width": "100%", "borderCollapse": "collapse"})

        return html.Div([
            card([
                html.H2("About This Dashboard", style={"color": ACCENT, "fontSize": "20px",
                                                        "fontWeight": "700", "marginBottom": "16px"}),
                html.P(
                    "For footwear companies: a quantitative framework for comparing shoe models on biomechanical efficiency and recovery impact simultaneously — "
                    "moving beyond single-variable lab testing toward a systems-level evaluation of how shoe design propagates through the body.",
                    style={"color": TEXT, "fontSize": "14px", "lineHeight": "1.8", "marginBottom": "12px"}
                ),
                html.P(
                    "For wearable companies: a demonstration that equipment variables like footwear explain meaningful variance in HRV and strain signals — "
                    "variance that cannot be attributed to sleep or training load alone, and that represents an untapped contextual input for improving sensor interpretation.",
                    style={"color": TEXT, "fontSize": "14px", "lineHeight": "1.8", "marginBottom": "12px"}
                ),
                html.P([
                    "Built on biomechanically-informed simulation across 15 de-identified shoe models, this tool traces the full chain: ",
                    html.Span("shoe properties → ground reaction forces → energy cost → autonomic recovery.",
                              style={"color": ACCENT, "fontWeight": "600"}),
                ], style={"color": TEXT, "fontSize": "14px", "lineHeight": "1.8"}),
            ]),
            card([
                section("Footwear Characteristics",
                    "Describes the physical properties of each de-identified shoe model — stack height, heel drop, "
                    "foam type, plate presence, midsole stiffness, rocker angle, and weight. "
                    "These properties are the inputs that drive differences across all other tabs."),
                section("Shoe Mechanics",
                    "Shows how each model performs across seven biomechanical variables measured during walking, jogging, and running gait. "
                    "The heatmap gives a quick cross-model comparison, with z-scored colors allowing comparison across variables with different units."),
                section("Energy Cost",
                    "Explores how biomechanical variables translate into running power demand. "
                    "Models that minimize braking and vertical bounce require less energy to maintain the same speed."),
                section("Recovery Impact",
                    "Connects running mechanics to post-run recovery outcomes from wearable data. "
                    "Models that create less mechanical stress tend to produce higher HRV and lower cardiovascular strain. "
                    "The Recovery Rankings table summarizes this as a single composite score per model."),
                section("Methodology",
                    "Documents the simulation equations used to derive all biomechanical, energy cost, and wearable outcomes from shoe physical properties. "
                    "Intended for technical reviewers who want to understand how each variable was calculated."),
            ]),
            card([
                html.H3("Variable Definitions", style={"color": ACCENT, "fontSize": "15px",
                                                        "fontWeight": "700", "marginBottom": "16px",
                                                        "letterSpacing": "0.5px"}),
                var_table,
            ]),
        ])

@callback(
    Output("spm-content", "children"),
    Input("model-select", "value"),
)
def render_spm(models):
    import numpy as np
    import spm1d

    selected_models = models or MODELS
    t = np.linspace(0, 100, 101)

    if len(selected_models) < 2 or len(selected_models) > 4:
        return html.P(
            f"{'Select at least 2 models' if len(selected_models) < 2 else 'Select 4 or fewer models'} to run SPM analysis.",
            style={"color": SUBTEXT, "fontSize": "13px", "fontStyle": "italic"}
        )

    arrays = []
    valid_models = []
    for model in selected_models:
        if model in waveform_data:
            arrays.append(waveform_data[model])
            valid_models.append(model)

    try:
        if len(arrays) == 2:
            t_stat = spm1d.stats.ttest2(arrays[0], arrays[1])
            ti     = t_stat.inference(alpha=0.05, two_tailed=True)
            spm_label = f"SPM t-test: {valid_models[0]} vs {valid_models[1]}"
            stat_trace = t_stat.z
            threshold  = ti.zstar
            sig_clusters = ti.clusters
        else:
            f_stat = spm1d.stats.anova1(*arrays)
            fi     = f_stat.inference(alpha=0.05)
            spm_label = f"SPM one-way ANOVA ({len(valid_models)} models)"
            stat_trace = f_stat.z
            threshold  = fi.zstar
            sig_clusters = fi.clusters

        spm_fig = go.Figure()

        if sig_clusters:
            for cluster in sig_clusters:
                spm_fig.add_vrect(
                    x0=cluster.endpoints[0], x1=cluster.endpoints[1],
                    fillcolor=ACCENT, opacity=0.15, line_width=0,
                    annotation_text="p<0.05", annotation_position="top left",
                    annotation_font=dict(color=ACCENT, size=10),
                )

        spm_fig.add_hline(y=threshold, line_dash="dash", line_color=ACCENT, opacity=0.6,
                          annotation_text="α=0.05 threshold",
                          annotation_font=dict(color=ACCENT, size=10),
                          annotation_position="bottom right")
        if len(arrays) == 2:
            spm_fig.add_hline(y=-threshold, line_dash="dash", line_color=ACCENT, opacity=0.6)

        spm_fig.add_trace(go.Scatter(
            x=t, y=stat_trace, mode="lines",
            line=dict(color="#ffffff", width=2),
            name="SPM statistic",
            hovertemplate="%{x:.0f}% stance<br>statistic: %{y:.2f}<extra></extra>",
        ))

        spm_fig.update_layout(
            plot_bgcolor=CARD_COLOR, paper_bgcolor=CARD_COLOR, font_color=TEXT,
            height=280,
            title=dict(text=spm_label, font=dict(color=TEXT, size=13)),
            xaxis=dict(title=dict(text="% Stance", font=dict(color=SUBTEXT)),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT)),
            yaxis=dict(title=dict(text="SPM statistic", font=dict(color=SUBTEXT)),
                       gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT)),
            legend=dict(bgcolor=CARD_COLOR, font=dict(color=TEXT, size=10)),
            margin=dict(l=50, r=30, t=40, b=50),
            showlegend=False,
        )

        if sig_clusters:
            regions = ", ".join([f"{c.endpoints[0]:.0f}–{c.endpoints[1]:.0f}%" for c in sig_clusters])
            sig_note = f"Significant differences detected at: {regions} of the stance phase (p < 0.05)."
        else:
            sig_note = "No significant differences detected across the stance phase (p > 0.05)."

        return html.Div([
            dcc.Graph(figure=spm_fig, config={"displayModeBar": False}),
            html.P(sig_note, style={"color": SUBTEXT, "fontSize": "12px",
                                    "marginTop": "8px", "fontStyle": "italic"}),
        ])

    except Exception as e:
        return html.P(f"SPM could not be computed: {str(e)}",
                      style={"color": SUBTEXT, "fontSize": "12px"})

if __name__ == "__main__":
    app.run(debug=True)