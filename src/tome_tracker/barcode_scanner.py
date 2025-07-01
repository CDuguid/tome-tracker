import cv2
from pyzbar.pyzbar import decode

def get_barcode_data(image) -> str | None:
    # Convert to greyscale to improve detection
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcode = decode(grey_image)

    for obj in barcode:
        barcode_data = obj.data.decode("utf-8")
        return barcode_data
    
    return None


def scan_barcode():
    # VideoCapture may take a different value for input device but there is currently no way to list all avaialble input devices
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Cannot open camera. Exiting ...")
        cap.release()
        cv2.destroyAllWindows()
        return None
    
    print("Press 'q' to quit the barcode scanning process.")
    while True:
        ret, image = cap.read()
        
        if not ret:
            print("Can't receive frames (is the camera working?). Exiting ...")
            break
        
        barcode_data = get_barcode_data(image)
        cv2.imshow('Image', image)
        
        if barcode_data is not None and len(barcode_data) == 13:
            cap.release()
            cv2.destroyAllWindows()
            return barcode_data
        
        command = cv2.waitKey(10)
        if command == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    print(scan_barcode())
