#!/bin/zsh
set -euo pipefail

project_dir="${0:A:h:h}"
cd "$project_dir"

uv sync --extra packaging
uv run pyinstaller --noconfirm --clean LectureArchive.spec

echo "Built: $project_dir/dist/Lecture Archive.app"
