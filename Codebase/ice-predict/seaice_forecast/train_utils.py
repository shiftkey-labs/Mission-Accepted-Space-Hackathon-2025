import torch
import torch.nn.functional as F
from tqdm import tqdm

def dice_loss(pred, target, eps=1e-6):
    inter = (pred * target).sum()
    union = pred.sum() + target.sum()
    dice = (2 * inter + eps) / (union + eps)
    return 1 - dice

def combined_loss(out, y):
    bce = F.binary_cross_entropy(out, y)
    dice = dice_loss(out, y)
    return bce + dice

def train_epoch(model, loader, opt, device):
    model.train()
    total_loss = 0.0

    pbar = tqdm(loader, desc="🧊 Training", leave=False, dynamic_ncols=True)

    for X, y in pbar:
        X, y = X.to(device), y.to(device)
        X = X.transpose(1, 2)  # (B, 3, seq, H, W)
        out = model(X)

        loss = combined_loss(out, y)

        opt.zero_grad()
        loss.backward()
        opt.step()

        total_loss += loss.item()
        pbar.set_postfix(loss=f"{loss.item():.4f}")

    return total_loss / len(loader)

def validate_epoch(model, loader, device):
    model.eval()
    total_loss = 0.0

    pbar = tqdm(loader, desc="🧪 Validating", leave=False, dynamic_ncols=True)

    with torch.no_grad():
        for X, y in pbar:
            X, y = X.to(device), y.to(device)
            X = X.transpose(1, 2)
            out = model(X)

            loss = combined_loss(out, y)
            total_loss += loss.item()
            pbar.set_postfix(loss=f"{loss.item():.4f}")

    return total_loss / len(loader)
