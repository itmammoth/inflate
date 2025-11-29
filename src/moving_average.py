"""N週移動平均値を出力する"""

from __future__ import annotations

import argparse

import pandas as pd
import yfinance as yf


def format_or_na(value: float | pd.Series) -> str:
    """数値を小数点以下2桁に整形し、NaNなら「データ不足」を返す。"""
    if pd.isna(value):
        return "データ不足"
    return f"{value:.2f}"


def parse_args() -> argparse.Namespace:
    """コマンドライン引数からティッカーと期間を取得する。"""
    parser = argparse.ArgumentParser(description="13週移動平均を取得")
    parser.add_argument(
        "--ticker",
        required=True,
        help="取得対象のティッカーシンボル (例: 7203.T)",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        required=True,
        help="移動平均の週数",
    )
    return parser.parse_args()


def main() -> None:
    """ティッカーの週足履歴を取得し、移動平均を表示する。"""
    args = parse_args()
    ticker_code = args.ticker
    period_weeks = args.weeks

    if period_weeks < 1:
        raise ValueError("weeks は 1 以上を指定してください")

    ticker = yf.Ticker(ticker_code)
    df = ticker.history(
        period=f"{period_weeks - 1}wk", interval="1wk", auto_adjust=False
    )
    if df.empty:
        raise RuntimeError("データが取得できませんでした")

    print(f"今週の【{ticker_code}:{ticker.info['shortName']}】")
    print(df.tail(1))
    print("終値")
    print(df.tail(1)["Close"].iloc[0])

    print(f"{period_weeks}週移動平均値")
    ma = df["Close"].rolling(window=period_weeks).mean().iloc[-1]
    print(format_or_na(ma))


if __name__ == "__main__":
    main()
