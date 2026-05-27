import pandas as pd
import numpy as np

np.random.seed(42)

MODELS = [f"Model {i+1}" for i in range(15)]

# Real-world inspired shoe characteristics (randomized assignment)
shoe_chars = [
    {"Stack Height (mm)": 40, "Heel Drop (mm)": 6,  "Midsole Stiffness": 45, "Stability Index": 10, "Foam Type": "PEBA", "Plated": "Yes", "Rocker Angle (°)": 20, "Weight (g)": 268},
    {"Stack Height (mm)": 46, "Heel Drop (mm)": 10, "Midsole Stiffness": 40, "Stability Index": 15, "Foam Type": "PEBA", "Plated": "Yes", "Rocker Angle (°)": 18, "Weight (g)": 285},
    {"Stack Height (mm)": 61, "Heel Drop (mm)": 4,  "Midsole Stiffness": 65, "Stability Index": 5,  "Foam Type": "PEBA", "Plated": "Yes", "Rocker Angle (°)": 25, "Weight (g)": 312},
    {"Stack Height (mm)": 40, "Heel Drop (mm)": 8,  "Midsole Stiffness": 60, "Stability Index": 8,  "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 15, "Weight (g)": 298},
    {"Stack Height (mm)": 40, "Heel Drop (mm)": 5,  "Midsole Stiffness": 38, "Stability Index": 5,  "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 14, "Weight (g)": 242},
    {"Stack Height (mm)": 29, "Heel Drop (mm)": 10, "Midsole Stiffness": 35, "Stability Index": 4,  "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 10, "Weight (g)": 198},
    {"Stack Height (mm)": 32, "Heel Drop (mm)": 5,  "Midsole Stiffness": 30, "Stability Index": 5,  "Foam Type": "PEBA", "Plated": "Yes", "Rocker Angle (°)": 16, "Weight (g)": 225},
    {"Stack Height (mm)": 31, "Heel Drop (mm)": 10, "Midsole Stiffness": 38, "Stability Index": 7,  "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 12, "Weight (g)": 215},
    {"Stack Height (mm)": 36, "Heel Drop (mm)": 10, "Midsole Stiffness": 40, "Stability Index": 3,  "Foam Type": "PEBA", "Plated": "Yes", "Rocker Angle (°)": 18, "Weight (g)": 255},
    {"Stack Height (mm)": 33, "Heel Drop (mm)": 8,  "Midsole Stiffness": 45, "Stability Index": 15, "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 13, "Weight (g)": 238},
    {"Stack Height (mm)": 36, "Heel Drop (mm)": 9,  "Midsole Stiffness": 42, "Stability Index": 18, "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 15, "Weight (g)": 262},
    {"Stack Height (mm)": 33, "Heel Drop (mm)": 10, "Midsole Stiffness": 37, "Stability Index": 6,  "Foam Type": "PEBA", "Plated": "Yes", "Rocker Angle (°)": 17, "Weight (g)": 232},
    {"Stack Height (mm)": 31, "Heel Drop (mm)": 7,  "Midsole Stiffness": 42, "Stability Index": 16, "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 14, "Weight (g)": 248},
    {"Stack Height (mm)": 29, "Heel Drop (mm)": 6,  "Midsole Stiffness": 33, "Stability Index": 5,  "Foam Type": "EVA",  "Plated": "No",  "Rocker Angle (°)": 11, "Weight (g)": 205},
    {"Stack Height (mm)": 33, "Heel Drop (mm)": 9,  "Midsole Stiffness": 40, "Stability Index": 6,  "Foam Type": "PEBA", "Plated": "Yes", "Rocker Angle (°)": 16, "Weight (g)": 244},
]

# Randomize which physical profile gets assigned to which model number
rng = np.random.default_rng(99)
shuffled_idx = rng.permutation(15)
shoe_chars_shuffled = [shoe_chars[i] for i in shuffled_idx]

char_df = pd.DataFrame(shoe_chars_shuffled, index=MODELS).reset_index().rename(columns={"index": "Model"})

def simulate_participants(n=20):
    rows = []
    for _, char_row in char_df.iterrows():
        model = char_row["Model"]
        sh = char_row["Stack Height (mm)"]
        dr = char_row["Heel Drop (mm)"]
        st = char_row["Midsole Stiffness"] / 10

        for i in range(n):
            vo2 = np.random.choice(["Low", "Moderate", "High"])
            vo2_val = {"Low": 35, "Moderate": 50, "High": 65}[vo2] + np.random.normal(0, 3)
            speed = np.random.choice(["Walking", "Jogging", "Running"])
            speed_mult = {"Walking": 0.7, "Jogging": 1.0, "Running": 1.35}[speed]

            loading_rate    = (80 - sh * 1.2 + dr * 0.8 + np.random.normal(0, 4)) * speed_mult
            braking_impulse = (0.18 - st * 0.008 + dr * 0.003 + np.random.normal(0, 0.01)) * speed_mult
            vertical_osc    = (8 + sh * 0.15 - st * 0.3 + np.random.normal(0, 0.5)) * speed_mult
            contact_time    = (280 - sh * 1.5 - speed_mult * 40 + np.random.normal(0, 10))
            ankle_angle     = (12 + dr * 0.6 + np.random.normal(0, 1.5))
            knee_angle      = (18 + sh * 0.2 - dr * 0.3 + np.random.normal(0, 2))
            pronation       = (6 - st * 0.4 + np.random.normal(0, 1))
            running_power   = (280 + braking_impulse * 200 + vertical_osc * 8 + np.random.normal(0, 10)) * speed_mult
            vertical_ratio  = vertical_osc / (150 * speed_mult) * 100
            day_strain      = (10 + running_power * 0.02 + np.random.normal(0, 1))
            hrv             = (65 - braking_impulse * 80 - day_strain * 0.5 + vo2_val * 0.3 + np.random.normal(0, 5))

            rows.append({
                "Model": model,
                "Stack Height (mm)": sh,
                "Heel Drop (mm)": dr,
                "Midsole Stiffness": char_row["Midsole Stiffness"],
                "Stability Index": char_row["Stability Index"],
                "Foam Type": char_row["Foam Type"],
                "Plated": char_row["Plated"],
                "Rocker Angle (°)": char_row["Rocker Angle (°)"],
                "Weight (g)": char_row["Weight (g)"],
                "VO2 Max Category": vo2,
                "Speed Category": speed,
                "Loading Rate (BW/s)": round(loading_rate, 2),
                "Braking Impulse (N·s/kg)": round(braking_impulse, 3),
                "Vertical Oscillation (cm)": round(vertical_osc, 2),
                "Contact Time (ms)": round(contact_time, 1),
                "Ankle Angle (°)": round(ankle_angle, 1),
                "Knee Angle (°)": round(knee_angle, 1),
                "Pronation Angle (°)": round(pronation, 1),
                "Running Power (W)": round(running_power, 1),
                "Vertical Ratio (%)": round(vertical_ratio, 2),
                "Day Strain": round(day_strain, 2),
                "HRV (ms)": round(hrv, 1),
            })
    return pd.DataFrame(rows)

df = simulate_participants(n=20)

def simulate_waveforms(n=20):
    """
    Simulate time-normalized vGRF waveforms (0-100% stance) for each shoe model.
    Returns a dict: {model_name: array of shape (n, 101)}
    """
    waveforms = {}
    t = np.linspace(0, 1, 101)

    for _, char_row in char_df.iterrows():
        model = char_row["Model"]
        sh = char_row["Stack Height (mm)"]
        dr = char_row["Heel Drop (mm)"]
        st = char_row["Midsole Stiffness"]

        # Shoe properties influence curve shape
        impact_peak  = 1.8 - sh * 0.01 + dr * 0.005   # first peak (BW)
        loading_rate = 0.12 - sh * 0.001               # how quickly first peak rises
        valley       = 0.75 + sh * 0.003               # midstance valley
        active_peak  = 1.6 + st * 0.004 - sh * 0.005  # propulsive peak
        contact_frac = 0.65 - sh * 0.002               # fraction of cycle in stance

        trials = []
        for _ in range(n):
            # Add participant-level noise
            ip  = impact_peak  + np.random.normal(0, 0.05)
            lr  = loading_rate + np.random.normal(0, 0.005)
            v   = valley       + np.random.normal(0, 0.02)
            ap  = active_peak  + np.random.normal(0, 0.05)
            cf  = contact_frac + np.random.normal(0, 0.02)
            cf  = np.clip(cf, 0.45, 0.80)

            curve = np.zeros(101)
            stance_end = int(cf * 100)

            for i in range(stance_end + 1):
                pct = i / stance_end
                # Impact peak: quick rise then fall
                impact   = ip * np.exp(-((pct - lr) ** 2) / (2 * 0.015 ** 2))
                # Midstance valley
                mid      = v  * np.exp(-((pct - 0.50) ** 2) / (2 * 0.12  ** 2))
                # Active/propulsive peak
                active   = ap * np.exp(-((pct - 0.75) ** 2) / (2 * 0.10  ** 2))
                curve[i] = impact + mid + active

            # Smooth and add small noise
            from scipy.ndimage import gaussian_filter1d
            curve = gaussian_filter1d(curve, sigma=2)
            curve += np.random.normal(0, 0.02, 101)
            curve = np.clip(curve, 0, None)
            trials.append(curve)

        waveforms[model] = np.array(trials)

    return waveforms

waveform_data = simulate_waveforms(n=20)

def simulate_ap_waveforms(n=20):
    """
    Simulate time-normalized anterior-posterior GRF waveforms (0-100% stance).
    Negative = braking phase, Positive = propulsive phase.
    Returns a dict: {model_name: array of shape (n, 101)}
    """
    ap_waveforms = {}
    
    for _, char_row in char_df.iterrows():
        model = char_row["Model"]
        sh = char_row["Stack Height (mm)"]
        dr = char_row["Heel Drop (mm)"]
        st = char_row["Midsole Stiffness"]
        plated = char_row["Plated"] == "Yes"
        rocker = char_row["Rocker Angle (°)"]

        # Shoe properties influence A-P curve shape
        braking_peak  = -(0.25 - sh * 0.002 + dr * 0.003)   # negative = braking
        braking_timing = 0.20 + sh * 0.001                   # when braking peaks
        propulsive_peak = 0.22 + st * 0.002 + (0.03 if plated else 0) + rocker * 0.001
        propulsive_timing = 0.78 - rocker * 0.002            # rockers shift propulsion earlier

        trials = []
        for _ in range(n):
            bp  = braking_peak    + np.random.normal(0, 0.015)
            bt  = braking_timing  + np.random.normal(0, 0.02)
            pp  = propulsive_peak + np.random.normal(0, 0.015)
            pt  = propulsive_timing + np.random.normal(0, 0.02)

            curve = np.zeros(101)
            for i in range(101):
                pct = i / 100
                braking    = bp * np.exp(-((pct - bt)  ** 2) / (2 * 0.08 ** 2))
                propulsive = pp * np.exp(-((pct - pt)  ** 2) / (2 * 0.09 ** 2))
                curve[i]   = braking + propulsive

            from scipy.ndimage import gaussian_filter1d
            curve = gaussian_filter1d(curve, sigma=2)
            curve += np.random.normal(0, 0.008, 101)
            trials.append(curve)

        ap_waveforms[model] = np.array(trials)

    return ap_waveforms

ap_waveform_data = simulate_ap_waveforms(n=20)

def simulate_cumulative_impulse(n=20):
    """
    Cumulative vGRF impulse across stance (0-100%).
    At each time point, returns the running sum of vGRF up to that point.
    Units: BW·% stance (normalized)
    Returns a dict: {model_name: array of shape (n, 101)}
    """
    cumulative = {}
    for model, trials in waveform_data.items():
        cum_trials = []
        for trial in trials:
            cum = np.cumsum(trial) / 100
            cum_trials.append(cum)
        cumulative[model] = np.array(cum_trials)
    return cumulative

cumulative_impulse_data = simulate_cumulative_impulse()