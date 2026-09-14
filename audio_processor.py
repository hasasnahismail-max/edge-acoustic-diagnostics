# import numpy as np
import librosa

class AcousticFeatureExtractor:
    """
    Real-time Acoustic Feature Extractor for Mechanical Diagnostics.
    Converts raw sound signals into normalized Log-Mel Spectrograms.
    """
    def __init__(self, sample_rate: int = 22050, n_mels: int = 64, n_fft: int = 1024, hop_length: int = 512):
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length

    def load_audio_buffer(self, file_path: str) -> np.ndarray:
        """Loads audio file and converts it to a single mono channel."""
        y, _ = librosa.load(file_path, sr=self.sample_rate, mono=True)
        return y

    def extract_mel_spectrogram(self, audio_buffer: np.ndarray) -> np.ndarray:
        """Transforms raw audio buffer into a normalized Mel Spectrogram tensor."""
        mel_spec = librosa.feature.melspectrogram(
            y=audio_buffer,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )
        # Convert power spectrogram to decibel scale
        mel_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Min-Max Normalization (0 to 1 scale) for Edge Deep Learning models
        normalized_spec = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-6)
        return normalized_spec

if __name__ == "__main__":
    extractor = AcousticFeatureExtractor()
    print("[EADE] Acoustic Feature Extractor initialized successfully.")
