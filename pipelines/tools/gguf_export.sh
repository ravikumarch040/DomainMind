#!/usr/bin/env bash
# GGUF export — LLD §5.3 (requires llama.cpp locally)
set -euo pipefail

MERGED_MODEL="${1:-./merged_model}"
OUTFILE="${2:-domainmind-7b-f16.gguf}"

if [[ ! -f "convert_hf_to_gguf.py" ]]; then
  echo "Download convert_hf_to_gguf.py from llama.cpp first."
  echo "Usage: $0 <merged_model_path> <output.gguf>"
  exit 1
fi

python convert_hf_to_gguf.py "$MERGED_MODEL" --outfile "$OUTFILE" --outtype f16
echo "Quantize with: ./llama-quantize $OUTFILE domainmind-7b-Q4_K_M.gguf Q4_K_M"
