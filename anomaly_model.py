import torch
import torch.nn as nn

class AcousticAutoencoder(nn.Module):
    """
    Deep Autoencoder Neural Network for Unsupervised Acoustic Anomaly Detection.
    Learns normal mechanical sound patterns and calculates reconstruction error (Anomaly Score).
    """
    def __init__(self, input_dim: int = 64):
        super(AcousticAutoencoder, self).__init__()
        
        # Encoder Architecture
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU()
        )
        
        # Decoder Architecture
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed

    def compute_anomaly_score(self, original: torch.Tensor, reconstructed: torch.Tensor) -> float:
        """Calculates Mean Squared Error (MSE) between original and reconstructed sound features."""
        criterion = nn.MSELoss()
        loss = criterion(reconstructed, original)
        return loss.item()

if __name__ == "__main__":
    model = AcousticAutoencoder()
    print("[EADE] Acoustic Autoencoder Model initialized successfully.")
