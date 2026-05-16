#!/usr/bin/env python3
"""
products/ フォルダ内の .glb / .gltf ファイルを走査して
products.json を再生成するヘルパー。

使い方:
    python3 build_manifest.py
    python3 build_manifest.py --brand "あなたのブランド名"
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand", default=None,
                        help="manifest.brand の値を上書き")
    parser.add_argument("--label", default=None,
                        help="manifest.label の値を上書き")
    parser.add_argument("--products-dir", default="products",
                        help="商品ファイルを置いたフォルダ名（既定: products）")
    parser.add_argument("--out", default="products.json",
                        help="出力先（既定: products.json）")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    products_dir = base / args.products_dir
    out_path = base / args.out

    if not products_dir.exists():
        print(f"商品フォルダが見つかりません: {products_dir}", file=sys.stderr)
        print(f"  作成してから .glb / .gltf を入れてください。", file=sys.stderr)
        sys.exit(1)

    # 既存の manifest を読んで brand / label を引き継ぐ
    existing = {}
    if out_path.exists():
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except json.JSONDecodeError:
            existing = {}

    items = []
    for ext in ("*.glb", "*.gltf"):
        for f in sorted(products_dir.rglob(ext)):
            rel = f.relative_to(base).as_posix()
            items.append({"name": f.stem, "url": rel})

    # ファイル名でソート（日本語にも対応）
    items.sort(key=lambda x: x["name"])

    manifest = {
        "brand": args.brand or existing.get("brand", "商品サイズ感プレビュー"),
        "label": args.label or existing.get("label", "Virtual Studio"),
        "products": items,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"{len(items)} 件の商品を {out_path.name} に書き出しました。")
    for item in items:
        print(f"  - {item['name']}  ({item['url']})")


if __name__ == "__main__":
    main()
