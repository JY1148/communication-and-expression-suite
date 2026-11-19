#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python build_corpus.py
python learning_content.py
python expand_all_training.py
python split_long_note.py
python unify_training.py
python editorial_pass.py
python add_pronunciation.py
python precision_route.py
python append_extra_training.py
python add_pronunciation.py
python align_learning_answers.py
python audit_answer_alignment.py
python migrate_native_entries.py
python build_learning_highlights.py
python polish_instant.py
python organize_precision.py
python organize_advanced.py
python trim_and_order.py
python reorder_precision.py
python validate_native_entries.py
node --check dist/app.js
