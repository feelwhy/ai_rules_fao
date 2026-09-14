#!/usr/bin/env python3
"""Assert the port group assignment (rule 36, "Group order").

The owner's group/order file is authoritative. This asserts three things at every branch
creation and at every group start:

  1. every module in the repo is assigned exactly once in the group file;
  2. the ledger's per-group module lists equal the group file's;
  3. the ledger's order equals the group file's order, except that the pilot group is
     pulled to the front (owner's explicit override for the first experiment).

Note on YAML: group keys MUST be quoted in the ledger. YAML 1.1 reads underscores as digit
separators, so a bare `20_2:` becomes the integer 202 and every lookup by name misses.

Usage:
  python3 migration/check_group_assignment.py \
      --repo /home/feelwhy/Odoo/tools \
      [--groups migration/20-tools-groups.md] \
      [--ledger migration/20-tools-port.state.yaml]

Exit code 1 on any mismatch.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))


def parse_groups(path: str) -> dict[str, list[str]]:
    """`## <group>` headings, then `- <display name> / <technical name>` lines."""
    groups: dict[str, list[str]] = {}
    current = None
    for line in open(path, encoding="utf-8"):
        head = re.match(r"^##\s+(\S+)\s*$", line)
        if head:
            current = head.group(1)
            groups[current] = []
            continue
        mod = re.match(r"^-\s+.*?\s*/\s*([a-z0-9_]+)\s*$", line)
        if mod and current:
            groups[current].append(mod.group(1))
    return groups


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--groups", default=os.path.join(HERE, "20-tools-groups.md"))
    ap.add_argument("--ledger", default=os.path.join(HERE, "20-tools-port.state.yaml"))
    args = ap.parse_args()

    groups = parse_groups(args.groups)
    assigned = [m for mods in groups.values() for m in mods]
    repo = sorted(d for d in os.listdir(args.repo)
                  if os.path.isfile(os.path.join(args.repo, d, "__manifest__.py")))

    ledger = yaml.safe_load(open(args.ledger, encoding="utf-8"))
    # str() guards against an unquoted key silently arriving as an int.
    led_mods = {str(k): v["modules"] for k, v in ledger["groups"].items()}
    led_order = [str(k) for k, v in sorted(ledger["groups"].items(), key=lambda kv: kv[1]["order"])]
    pilots = [str(k) for k, v in ledger["groups"].items() if v.get("pilot")]

    problems: list[str] = []

    dupes = sorted({m for m in assigned if assigned.count(m) > 1})
    if dupes:
        problems.append(f"assigned more than once: {', '.join(dupes)}")
    unassigned = sorted(set(repo) - set(assigned))
    if unassigned:
        problems.append(f"in the repo but in no group: {', '.join(unassigned)}")
    phantom = sorted(set(assigned) - set(repo))
    if phantom:
        problems.append(f"assigned but not an addon of the repo: {', '.join(phantom)}")

    for name in sorted(set(groups) | set(led_mods)):
        want, have = sorted(groups.get(name) or []), sorted(led_mods.get(name) or [])
        if want != have:
            problems.append(f"{name}: group file {want} != ledger {have}")

    if len(pilots) > 1:
        problems.append(f"more than one pilot group: {', '.join(pilots)}")
    expected_order = list(groups)
    for pilot in pilots:
        if pilot in expected_order:
            expected_order.remove(pilot)
            expected_order.insert(0, pilot)
    if led_order != expected_order:
        problems.append(f"order: expected {expected_order} (group file, pilot first), "
                        f"ledger has {led_order}")

    print(f"groups {len(groups)}  assigned {len(assigned)}  repo addons {len(repo)}")
    print(f"pilot  {', '.join(pilots) or '(none)'}")
    print(f"order  {' '.join(led_order)}")
    if problems:
        print("\nFAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nPASS: every addon assigned exactly once; ledger matches the group file; "
          "order matches with the pilot first")
    return 0


if __name__ == "__main__":
    sys.exit(main())
