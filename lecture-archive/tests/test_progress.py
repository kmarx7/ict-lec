from src.download.progress import DownloadProgress


def test_progress_percentage_and_eta_payload():
    progress = DownloadProgress(
        filename="recording.mp4",
        downloaded_bytes=50,
        total_bytes=200,
        speed_bytes_per_second=10,
        eta_seconds=15,
        strategy="zoom_direct",
    )
    assert progress.percentage == 25


def test_progress_without_total_is_indeterminate():
    progress = DownloadProgress("recording.mp4", 50, None, 10, None, "zoom_direct")
    assert progress.percentage is None
