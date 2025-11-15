"""13週移動平均 (終値+配当) をざっくり確認するスクリプト。"""

from __future__ import annotations

import pandas as pd
import yfinance as yf

TICKER_CODE = "9503.T"
PERIOD_WEEKS = 13


def format_or_na(value: float | pd.Series) -> str:
    if pd.isna(value):
        return "データ不足"
    return f"{value:.2f}"


def main() -> None:
    ticker = yf.Ticker(TICKER_CODE)
    df = ticker.history(
        period=f"{PERIOD_WEEKS - 1}wk", interval="1wk", auto_adjust=False
    )
    if df.empty:
        raise RuntimeError("データが取得できませんでした")

    print(f"今週の【{TICKER_CODE}:{ticker.info['shortName']}】")
    print(df.tail(1))

    print(f"{PERIOD_WEEKS}週移動平均値")
    ma = df["Close"].rolling(window=PERIOD_WEEKS).mean().iloc[-1]
    print(format_or_na(ma))


if __name__ == "__main__":
    main()
