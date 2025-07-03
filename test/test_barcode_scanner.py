from unittest.mock import patch

import cv2
import pytest

from src.tome_tracker.barcode_scanner import get_barcode_data, scan_barcode


@pytest.fixture
def barcode_image():
    return cv2.imread("test/data/wings.png")


class TestGetBarcodeData:
    def test_returns_barcode_from_image(self, barcode_image):
        expected = "9780385400183"
        assert get_barcode_data(barcode_image) == expected

    def test_returns_none_given_no_barcode(self):
        image = cv2.imread("test/data/guardsguards.jpg")
        expected = None
        assert get_barcode_data(image) == expected


class TestScanBarcode:
    @patch("src.tome_tracker.barcode_scanner.get_barcode_data")
    @patch("src.tome_tracker.barcode_scanner.cv2")
    def test_returns_barcode_from_still_image(
        self, mock_cv2, mock_get_barcode_data, barcode_image
    ):
        mock_cv2.VideoCapture().isOpened.return_value = True
        mock_cv2.VideoCapture().read.return_value = (True, barcode_image)
        mock_get_barcode_data.return_value = "9780385400183"
        expected = "9780385400183"
        assert scan_barcode() == expected

    @patch("src.tome_tracker.barcode_scanner.cv2")
    def test_returns_none_if_camera_does_not_open(self, mock_cv2, capsys):
        mock_cv2.VideoCapture().isOpened.return_value = False
        assert scan_barcode() is None
        captured = capsys.readouterr()
        assert "Cannot open camera. Exiting..." in captured.out

    @patch("src.tome_tracker.barcode_scanner.cv2")
    def test_returns_none_if_no_frames_are_received(self, mock_cv2, capsys):
        mock_cv2.VideoCapture().isOpened.return_value = True
        mock_cv2.VideoCapture().read.return_value = (False, None)
        assert scan_barcode() is None
        captured = capsys.readouterr()
        assert "Press 'q' to quit the barcode scanning process." in captured.out
        assert (
            "Can't receive frames (is the camera working?). Exiting..." in captured.out
        )

    @patch("src.tome_tracker.barcode_scanner.get_barcode_data")
    @patch("src.tome_tracker.barcode_scanner.cv2")
    def test_releases_camera_and_destroys_windows(
        self, mock_cv2, mock_get_barcode_data, barcode_image
    ):
        mock_cv2.VideoCapture().isOpened.return_value = True
        mock_cv2.VideoCapture().read.return_value = (True, barcode_image)
        mock_get_barcode_data.return_value = "9780385400183"
        scan_barcode()
        mock_cv2.VideoCapture().release.assert_called_once()
        mock_cv2.destroyAllWindows.assert_called_once()
