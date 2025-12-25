from tobii_research import EyeTracker, find_all_eyetrackers

def main():
    eye_trackers = find_all_eyetrackers()
    if not eye_trackers:
        print("No eye trackers found.")
        return
    eye_tracker = eye_trackers[0]
    print(f"Connected to Eye Tracker Model: {eye_tracker.model}, Serial Number: {eye_tracker.serial_number}")


if __name__ == "__main__":
    main()
