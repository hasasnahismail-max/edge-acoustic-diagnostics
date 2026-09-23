import logging
import numpy as np
from anomaly_model import AcousticAnomalyDetector
from audio_processor import AudioProcessor

# Configure logging for edge diagnostic tracking
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_diagnostic_demo():
    """Executes an end-to-end acoustic anomaly detection pipeline simulation."""
    logging.info("=== Starting Edge Acoustic Diagnostic Engine (EADE) ===")

    # 1. Initialize Signal Processor and Anomaly Detector
    processor = AudioProcessor(sample_rate=22050)
    detector = AcousticAnomalyDetector(contamination=0.02)

    # 2. Simulate baseline audio signals (Healthy machinery operations)
    logging.info("Step 1/3: Extracting acoustic fingerprints from baseline signals...")
    normal_samples = [np.random.normal(0, 0.1, size=22050 * 2) for _ in range(30)]
    X_train = np.array([processor.extract_features(s) for s in normal_samples])

    # 3. Fit Isolation Forest model on healthy acoustic baseline
    logging.info("Step 2/3: Training Isolation Forest model on baseline features...")
    detector.fit(X_train)

    # 4. Simulate test audio with a mechanical defect (Transient acoustic impact)
    logging.info("Step 3/3: Evaluating target audio stream for structural defects...")
    abnormal_signal = np.random.normal(0, 0.1, size=22050 * 2)
    abnormal_signal[4000:6000] += 3.0  # High-amplitude mechanical noise spike

    # Extract features and compute anomaly score
    test_features = processor.extract_features(abnormal_signal)
    report = detector.predict(test_features)

    # 5. Output Diagnostic Summary Report
    print("\n===========================================")
    print("         EADE DIAGNOSTIC REPORT            ")
    print("===========================================")
    print(f"System Health Status : {report['status']}")
    print(f"Anomaly Score (%)    : {report['anomaly_score_pct']}%")
    print(f"Anomaly Detected     : {report['is_anomaly']}")
    print("===========================================\n")


if __name__ == "__main__":
    run_diagnostic_demo()
