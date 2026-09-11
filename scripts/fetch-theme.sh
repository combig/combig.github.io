#!/usr/bin/env bash
# 重新拉取 / 升级 PaperMod 主题（主题已 vendored 进仓库，一般不用跑这个）
# 用法：bash scripts/fetch-theme.sh [版本号，默认 v8.0]
set -euo pipefail

VERSION="${1:-v8.0}"
TMP="$(mktemp -d)"

echo ">> 下载 PaperMod ${VERSION} ..."
curl -sL "https://codeload.github.com/adityatelange/hugo-PaperMod/tar.gz/refs/tags/${VERSION}" \
  | tar -xz -C "${TMP}" --strip-components=1

rm -rf themes/PaperMod
mkdir -p themes/PaperMod
cp -R "${TMP}/." themes/PaperMod/
rm -rf "${TMP}"

echo ">> 完成，主题在 themes/PaperMod"
