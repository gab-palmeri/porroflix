#!/usr/bin/env python3
"""
Funnel enable/disable for Jellyfin and Jellyseerr
Preserves newlines, indentation, and quotes
Restarts container only if label state changes
Usage: ./funnel.py on|off
"""

import sys
import subprocess
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

COMPOSE_FILE = "docker-compose.yml"
SERVICES = ["jellyfin", "jellyseerr"]
LABEL_TEXT = "tsbridge.service.funnel_enabled=true"

# --- Validate CLI argument ---
if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off"):
    print("Usage: ./funnel.py on|off")
    sys.exit(1)

action = sys.argv[1]

# --- Setup YAML parser ---
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096  # prevents line wrapping
yaml.indent(mapping=2, sequence=2, offset=2)  # preserve label indentation

# --- Load docker-compose.yml ---
with open(COMPOSE_FILE, "r") as f:
    data = yaml.load(f)

containers_to_restart = []

# --- Iterate over services ---
for service in SERVICES:
    svc = data.get("services", {}).get(service)
    if not svc:
        print(f"Service {service} not found, skipping...")
        continue

    labels = svc.get("labels")
    if labels is None:
        labels = []
        svc["labels"] = labels

    # Double-quoted label
    new_label = DoubleQuotedScalarString(LABEL_TEXT)

    if action == "on":
        # Add label only if not present
        if LABEL_TEXT not in [str(l) for l in labels]:
            labels.append(new_label)
            print(f"Funnel enabled for {service}.")
            containers_to_restart.append(service)
        else:
            print(f"Funnel already enabled for {service}.")
    else:
        # Remove label if present
        new_labels = [l for l in labels if str(l) != LABEL_TEXT]
        if len(new_labels) != len(labels):
            svc["labels"] = new_labels
            print(f"Funnel disabled for {service}.")
            containers_to_restart.append(service)
        else:
            print(f"Funnel already disabled for {service}.")

# --- Save changes preserving formatting ---
with open(COMPOSE_FILE, "w") as f:
    yaml.dump(data, f)

# --- Restart only modified containers ---
for service in containers_to_restart:
    print(f"Restarting {service}...")
    subprocess.run(["docker", "compose", "up", "-d", service])
