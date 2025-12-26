import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd
import numpy as np

TRACKING_FILE = "gaze_data_log.csv"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200

DISTANCE_THRESHOLD = 20
TIME_THRESHOLD = 1000000

def plot_eye_trajectory(ax, df, screen_w=SCREEN_WIDTH, screen_h=SCREEN_HEIGHT):
    ax.plot(df['x'] * screen_w, df['y'] * screen_h, color='blue', alpha=0.5, label='Trajectoire Oculaire')

def detect_fixation(df, screen_w=SCREEN_WIDTH, screen_h=SCREEN_HEIGHT, dist_threshold=DISTANCE_THRESHOLD, time_threshold=TIME_THRESHOLD):
    df['x_px'] = df['x'] * screen_w
    df['y_px'] = df['y'] * screen_h

    fixations = []
    current_points = []

    for i in range(len(df)):
        p = df.iloc[i]

        if not current_points:
            current_points.append(p)
            continue

        start_p = current_points[0]
        dist = np.sqrt((p['x_px'] - start_p['x_px'])**2 + (p['y_px'] - start_p['y_px'])**2)

        if dist <= dist_threshold:
            current_points.append(p)
        else:
            duration = current_points[-1]['timestamp'] - current_points[0]['timestamp']

            if duration >= time_threshold:
                fixations.append({
                    'x': np.mean([pt['x_px'] for pt in current_points]),
                    'y': np.mean([pt['y_px'] for pt in current_points])
                })

            current_points = [p]

    return pd.DataFrame(fixations)

def plot_fixations(ax, fix_df, screen_w=SCREEN_WIDTH, screen_h=SCREEN_HEIGHT, dist_threshold=DISTANCE_THRESHOLD):
    if not fix_df.empty:
        for i, row in fix_df.iterrows():
            circle = Circle(
                (row['x'], row['y']),
                radius=dist_threshold,
                color='red',
                alpha=0.3,
                label='Zone de fixation' if i == 0 else ""
            )
            ax.add_patch(circle)
        ax.plot(fix_df['x'], fix_df['y'], color='blue', alpha=0.2, linestyle='--')
    else:
        print("Aucune fixation détectée.")

if __name__ == "__main__":
    df = pd.read_csv(TRACKING_FILE)
    fixations_df = detect_fixation(df)

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.set_xlim(0, SCREEN_WIDTH)
    ax.set_ylim(0, SCREEN_HEIGHT)
    ax.invert_yaxis()

    plot_eye_trajectory(ax, df)
    plot_fixations(ax, fixations_df)

    plt.title("Détection de Fixations Oculaires")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()
