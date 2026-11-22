set shell := ["bash", "-euo", "pipefail", "-c"]

# List available recipes
default:
    @just --list

# Run full local validation (Python checks + strict agy CLI plugin validation if installed)
check: validate-py validate-agy

# Run zero-dependency Python customization validator (same check run in GitHub Actions)
validate-py:
    python3 scripts/validate_customizations.py

# Run strict Antigravity CLI validation on every plugin under plugins/
validate-agy:
    @if command -v agy >/dev/null 2>&1; then \
        for dir in plugins/*/; do \
            echo "Validating ${dir} with agy..."; \
            agy plugin validate --strict "${dir}"; \
        done; \
    else \
        echo "Skipping agy CLI check ('agy' not found on PATH)."; \
    fi

# List all plugins and bundled skills in this repository
list:
    @for dir in plugins/*/; do \
        echo "Plugin: $(basename "${dir}")"; \
        if [ -d "${dir}skills" ]; then \
            for skill in "${dir}skills"/*/; do \
                [ -d "${skill}" ] && echo "  - skill: $(basename "${skill}")"; \
            done; \
        fi; \
    done
