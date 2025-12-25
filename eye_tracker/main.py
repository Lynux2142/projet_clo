from tobii_research import EyeTracker, find_all_eyetrackers, EYETRACKER_GAZE_DATA

TRACKING_FILE = "gaze_data_log.csv"

def gaze_data_callback(gaze_data):
    left_gaze_point = gaze_data['left_gaze_point_on_display_area']
    right_gaze_point = gaze_data['right_gaze_point_on_display_area']
    timestamp = gaze_data['system_time_stamp']
    mean_y = (left_gaze_point[1] + right_gaze_point[1]) / 2.0
    mean_x = (left_gaze_point[0] + right_gaze_point[0]) / 2.0
    with open(TRACKING_FILE, "a") as file:
        file.write(f"{mean_x},{mean_y},{timestamp}\n")

def main():
    eye_trackers: tuple[EyeTracker] = find_all_eyetrackers()
    if not eye_trackers:
        print("No eye trackers found.")
        return
    eye_tracker: EyeTracker = eye_trackers[0]
    print(f"Connected to Eye Tracker Model: {eye_tracker.model}, Serial Number: {eye_tracker.serial_number}")
    with open(TRACKING_FILE, "w") as file:
        file.write("x,y,timestamp\n")
    eye_tracker.subscribe_to(EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    print("Subscribed to gaze data. Press Enter to stop...")
    input()
    eye_tracker.unsubscribe_from(EYETRACKER_GAZE_DATA, gaze_data_callback)


if __name__ == "__main__":
    main()
