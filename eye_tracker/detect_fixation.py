import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

TRACKING_FILE = "gaze_data_log.csv"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200

DISTANCE_THRESHOLD = 100
TIME_THRESHOLD = 1000

def plot_eye_trajectory(df, screen_w=SCREEN_WIDTH, screen_h=SCREEN_HEIGHT):
    plt.figure(figsize=(12, 7))
    plt.xlim(0, screen_w)
    plt.ylim(0, screen_h)

    plt.plot(df['x'] * screen_w, df['y'] * screen_h, color='blue', alpha=0.5, label='Trajectoire Oculaire')
    plt.gca().invert_yaxis()
    plt.title("Trajectoire Oculaire")
    plt.xlabel("Pixels X")
    plt.ylabel("Pixels Y")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def detect_fixation(df, screen_w=SCREEN_WIDTH, screen_h=SCREEN_HEIGHT, dist_threshold=100, time_threshold=1000000):
    """
    Analyse les données et retourne uniquement les fixations valides.
    """
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

def plot_fixations(fix_df, screen_w=SCREEN_WIDTH, screen_h=SCREEN_HEIGHT):
    plt.figure(figsize=(12, 7))
    plt.xlim(0, screen_w)
    plt.ylim(0, screen_h)

    if not fix_df.empty:
        plt.scatter(fix_df['x'], fix_df['y'], s=50, c='red', edgecolors='black', label='Fixations (>1000ms)')
        plt.plot(fix_df['x'], fix_df['y'], color='blue', alpha=0.2, linestyle='--')
    else:
        print("Aucune fixation de plus de 1000ms n'a été détectée.")

    plt.gca().invert_yaxis()
    plt.title("Localisation des Fixations Oculaires (Taille fixe)")
    plt.xlabel("Pixels X")
    plt.ylabel("Pixels Y")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv(TRACKING_FILE)
    plot_eye_trajectory(df)
    fixations_df = detect_fixation(df)
    plot_fixations(fixations_df)
