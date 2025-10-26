import torch
import torch.nn as nn

class SeaIce3DCNN(nn.Module):
    def __init__(self, in_seq: int):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv3d(3, 16, kernel_size=(3,3,3), padding=1),
            nn.BatchNorm3d(16),
            nn.ReLU(),
            nn.Conv3d(16, 32, kernel_size=(3,3,3), padding=1),
            nn.BatchNorm3d(32),
            nn.ReLU(),
            nn.Dropout3d(0.2),
        )
        self.decoder = nn.Sequential(
            nn.Conv3d(32, 16, kernel_size=(3,3,3), padding=1),
            nn.BatchNorm3d(16),
            nn.ReLU(),
            nn.Conv3d(16, 1, kernel_size=(in_seq,3,3), padding=(0,1,1)),
            nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        y = self.decoder(z)
        return y.squeeze(2)  # (B, 1, H, W)
