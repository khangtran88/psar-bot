"""Bot Telegram báo Parabolic SAR đảo chiều (crypto, dữ liệu OKX, miễn phí)."""
import json
import os
import requests

# ======================= CHỈNH Ở ĐÂY =======================
# Danh sách cặp tiền (định dạng OKX: COIN-USDT)
PAIRS = ["BTC-USDT", "ETH-USDT", "SOL-USDT"]

# Khung thời gian: "1H" và "4H"
# Thông số SAR cho từng khung: (bắt đầu, bước tăng, tối đa)
# Mặc định chuẩn TradingView là (0.02, 0.02, 0.2)
SAR_SETTINGS = {
    "1H": (0.02, 0.02, 0.2),
    "4H": (0.02, 0.02, 0.2),
}
# ===========================================================

STATE_FILE = "state.json"


def get_candles(pair, bar):
    """Lấy tối đa 300 nến ĐÃ ĐÓNG, cũ -> mới. Mỗi nến: (ts, high, low, close)."""
    url = "https://www.okx.com/api/v5/market/candles"
    r = requests.get(url, params={"instId": pair, "bar": bar, "limit": 300}, timeout=20)
    r.raise_for_status()
    rows = r.json()["data"]  # mới -> cũ
    out = []
    for row in reversed(rows):
        if row[8] != "1":  # bỏ nến đang chạy
            continue
        out.append((int(row[0]), float(row[2]), float(row[3]), float(row[4])))
    return out


def psar(highs, lows, start, inc, maxaf):
    """Trả về (danh sách xu hướng True=tăng, danh sách giá trị SAR)."""
    n = len(highs)
    up = highs[1] >=
