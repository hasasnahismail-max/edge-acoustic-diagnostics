import numpy as np


class AudioProcessor:

    def __init__(
        self, sample_rate=22050, n_fft=512, hop_length=256, n_features=20
    ):
        self.sample_rate = sample_rate
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.n_features = n_features

    def extract_features(self, audio_signal):
        """Pure NumPy Spectral Feature Extractor.

        Designed for lightweight Edge computing without external audio dependencies.
        """
        signal = np.asarray(audio_signal, dtype=np.float32)

        # 1. Framing signal for Short-Time Fourier Analysis
        num_frames = max(1, (len(signal) - self.n_fft) // self.hop_length + 1)
        window = np.hanning(self.n_fft)

        spectrogram = []
        for i in range(num_frames):
            start = i * self.hop_length
            frame = signal[start : start + self.n_fft]
            if len(frame) < self.n_fft:
                frame = np.pad(frame, (0, self.n_fft - len(frame)))

            # Compute Fast Fourier Transform (FFT) Magnitude Spectrum
            fft_mag = np.abs(np.fft.rfft(frame * window))
            spectrogram.append(fft_mag)

        spectrogram = np.array(spectrogram)

        # 2. Extract Spectral Energy & Zero-Crossing Rates
        spec_mean = np.mean(spectrogram, axis=0)[: self.n_features - 2]
        energy = np.mean(signal**2)
        zcr = np.mean(np.diff(np.signbit(signal)) != 0)

        # 3. Form compact Edge Feature Vector
        feature_vector = np.concatenate([spec_mean, [energy, zcr]])
        return feature_vector
