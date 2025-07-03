import cv2
import numpy as np
from pyzbar.pyzbar import decode


def get_barcode_data(image: np.ndarray) -> str | None:
    """
    Identifies barcode data in a single image represented by a NumPy array. Will return the first barcode found, so should not be used on an image with multiple barcodes.

    ### Args:
    `image`: a single frame from video capture.

    ### Returns:
    The barcode string if one has been identified, `None` otherwise.
    """
    # Convert to greyscale to improve detection
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcode = decode(grey_image)

    for obj in barcode:
        barcode_data = obj.data.decode("utf-8")
        return barcode_data

    return None


def scan_barcode() -> str | None:
    """
    Opens the device camera in position 0 for video capture. Will capture video until either `q` is pressed or an ISBN13 is identified.

    ### Returns:
    The ISBN13 tied to the barcode in the image if found, `None` otherwise.
    """
    # VideoCapture may take a different value for input device but there is currently no way to list all avaialble input devices
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera. Exiting...")
        cap.release()
        cv2.destroyAllWindows()
        return None

    print("Press 'q' to quit the barcode scanning process.")
    while True:
        ret, image = cap.read()

        if not ret:
            print("Can't receive frames (is the camera working?). Exiting...")
            break

        barcode_data = get_barcode_data(image)
        cv2.imshow("Image", image)

        if barcode_data is not None and len(barcode_data) == 13:
            cap.release()
            cv2.destroyAllWindows()
            return barcode_data

        command = cv2.waitKey(10)
        if command == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


if __name__ == "__main__":
    print(scan_barcode())
