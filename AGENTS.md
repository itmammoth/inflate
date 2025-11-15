# Repository Guidelines

## Project Structure & Module Organization
このリポジトリ は Python スクリプト主体で、業務ロジックは常に `src/` に置きます。`src/hello.py` は yfinance から日次ヒストリーを取得するベースライン、`src/01.py` は 13 週移動平均の計算例として扱い、ファイル追加時も同階層にシンプルなモジュール単位でまとめてください。依存ライブラリは `requirements.txt`、開発手順の要点は `README.md` に同期し、将来のユニットテストは `tests/` ディレクトリを新設してモジュールごとにサブパッケージ化するとレビューがしやすいです。生成される CSV やグラフ画像などの成果物は `outputs/` フォルダ (未作成の場合は手動追加) に隔離し、リポジトリ直下をクリーンに保つ運用にしてください。

## Build, Test, and Development Commands
- `uv venv` : プロジェクトローカルの仮想環境を生成します。
- `uv pip install -r requirements.txt` : yfinance など依存を一括導入します。
- `source venv/bin/activate` : 以降のスクリプト実行をローカル環境にピン留めします。
- `python src/hello.py` : API 通信と I/O の疎通確認を行う想定サンプルです。
- `python src/01.py` : 週次ローリング計算のリグレッションテストとして素早く走らせます。
- `pytest -q` : `tests/` 配下が整備され次第、このコマンドで高速検証してください。

## Coding Style & Naming Conventions
PEP 8 ベースで 4 スペースインデント、関数・変数は snake_case、定数は UPPER_SNAKE_CASE を徹底します。関数先頭に 1 文の docstring を置き、外部 API への問い合わせ条件 (ticker, period) は必ず引数化してハードコードを避けます。型ヒントは必須ではありませんが、pandas Series/DataFrame を返す関数には戻り値を注釈するとレビューが滑らかです。フォーマッタは未固定なので、PR 前に `python -m compileall src` で構文崩れを検知しつつ、`ruff` や `black` をローカルで使う場合は差分に反映してください。

## Testing Guidelines
テストは pytest 想定です。`tests/test_<module>.py` という命名で、yfinance 呼び出しは `pytest-mock` などでモックし、時系列計算の境界条件 (休日欠損、短期データ) を網羅してください。`pytest -q --maxfail=1` を CI 用の最小コマンドにし、13 週移動平均の窓計算ロジックは 80% 以上のブランチカバレッジを維持します。遅延のあるケースは `pytest --ff` で失敗テストを優先実行すると再現報告が楽です。

## Commit & Pull Request Guidelines
`git log` では短い命令形英語 (例: "Add weekly average helper") が使われているため、同じ形式で要点を 50 文字以内にまとめてください。Topic ブランチは `feature/<issue-id>-<slug>` 形式を推奨し、差分が小さいうちに Draft PR を開いてレビューを待ちます。PR には実行ログやスクリーンショットの代わりに `pytest` 結果、取得したティッカー例、関連 Issue を箇条書きで添付し、ネットワーク依存を含む変更は再現手順を明記すること。

## Security & Configuration Tips
yfinance は外部リクエストを送るため、API リミットやプロキシ設定を `.env` で切り替え、秘匿情報は絶対にリポジトリへコミットしないでください。`.env.example` を準備し、`.gitignore` で本番設定を除外しておくとオンボーディングが早まります。大量銘柄を処理する場合は 429 対策として `time.sleep` などのスロットリングを追加し、例外を丸め込まずに `raise` して上位ハンドラで通知する方針です。
