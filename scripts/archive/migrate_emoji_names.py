#!/usr/bin/env python3
"""Migration script: Rename emoji constants to canonical names.

This script updates EMOJI.* and icons.* usages from short names
to canonical names from the emoji package.

Usage:
    python scripts/migrate_emoji_names.py --dry-run  # Preview changes
    python scripts/migrate_emoji_names.py            # Apply changes
"""

import argparse
import re
from pathlib import Path

# Mapping of old names to new canonical names (from emoji package)
RENAMES = {
    "ALARM": "ALARM_CLOCK",
    "ARROW_UP_RIGHT": "UP_RIGHT_ARROW",
    "ART": "ARTIST_PALETTE",
    "BLOSSOM": "CHERRY_BLOSSOM",
    "BOOK": "OPEN_BOOK",
    "CAR": "AUTOMOBILE",
    "CHART_BAR": "BAR_CHART",
    "CHECK": "CHECK_MARK_BUTTON",
    "CLOCK": "ONE_OCLOCK",  # Simplified from ONE_O'CLOCK
    "COMPUTER": "LAPTOP",
    "CONFETTI": "CONFETTI_BALL",
    "CROSS": "CROSS_MARK",
    "DIAMOND": "GEM_STONE",
    "DOCUMENT": "PAGE_WITH_CURL",
    "DOLLAR": "DOLLAR_BANKNOTE",
    "EARTH_GLOBE_EUROPE_AFRICA": "GLOBE_SHOWING_EUROPE_AFRICA",
    "EMAIL": "E_MAIL",
    "EVERGREEN": "EVERGREEN_TREE",
    "FILE": "PAGE_FACING_UP",
    "FLOPPY": "FLOPPY_DISK",
    "FOLDER": "FILE_FOLDER",
    "GEM": "GEM_STONE",
    "GIFT": "WRAPPED_GIFT",
    "GLOBE": "GLOBE_WITH_MERIDIANS",
    "GLOBE_MERIDIANS": "GLOBE_WITH_MERIDIANS",
    "HEART": "RED_HEART",
    "HOURGLASS": "HOURGLASS_DONE",
    "INFO": "INFORMATION",
    "LEAF": "LEAF_FLUTTERING_IN_WIND",
    "LEAVES": "LEAF_FLUTTERING_IN_WIND",
    "LIGHTBULB": "LIGHT_BULB",
    "LIGHTNING": "HIGH_VOLTAGE",
    "LOCK": "LOCKED",
    "MAGNIFYING_GLASS": "MAGNIFYING_GLASS_TILTED_LEFT",
    "MEMORY": "FLOPPY_DISK",
    "MICROPROCESSOR": "DESKTOP_COMPUTER",
    "OCEAN": "WATER_WAVE",
    "OPEN_FOLDER": "OPEN_FILE_FOLDER",
    "ORANGE_FRUIT": "TANGERINE",
    "PAGE": "PAGE_FACING_UP",
    "PALETTE": "ARTIST_PALETTE",
    "PARTY": "PARTY_POPPER",
    "PEOPLE": "BUSTS_IN_SILHOUETTE",
    "PHONE": "MOBILE_PHONE",
    "QUESTION": "RED_QUESTION_MARK",
    "REFRESH": "COUNTERCLOCKWISE_ARROWS_BUTTON",
    "ROLLED_NEWSPAPER": "ROLLED_UP_NEWSPAPER",
    "SIREN": "POLICE_CAR_LIGHT",
    "TARGET": "BULLSEYE",
    "TRAIN": "LOCOMOTIVE",
    "TREE": "EVERGREEN_TREE",
    "TRIANGLE_RULER": "TRIANGULAR_RULER",
    "WATER": "DROPLET",
    "WAVE": "WAVING_HAND",
}


def migrate_file(file_path: Path, dry_run: bool = True) -> tuple[int, list[str]]:
    """Migrate emoji names in a single file.

    Returns:
        Tuple of (changes_count, list of change descriptions)
    """
    content = file_path.read_text()
    original = content
    changes = []

    for old_name, new_name in RENAMES.items():
        # Pattern 1: Match EMOJI.OLD_NAME or icons.OLD_NAME or E.OLD_NAME
        pattern1 = rf"\b(EMOJI|icons|E)\.{old_name}\b"
        matches = list(re.finditer(pattern1, content))
        if matches:
            for match in matches:
                prefix = match.group(1)
                changes.append(f"  {prefix}.{old_name} -> {prefix}.{new_name}")
            content = re.sub(pattern1, rf"\1.{new_name}", content)

        # Pattern 2: Match dictionary keys like "CHECK": or 'CHECK':
        pattern2 = rf'(["\']){old_name}\1(\s*:)'
        matches2 = list(re.finditer(pattern2, content))
        if matches2:
            for _match in matches2:
                changes.append(f'  "{old_name}": -> "{new_name}":')
            content = re.sub(pattern2, rf"\1{new_name}\1\2", content)

    if content != original:
        if not dry_run:
            file_path.write_text(content)
        return len(changes), changes

    return 0, []


def main():
    parser = argparse.ArgumentParser(description="Migrate emoji names to canonical form")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Root path to search for files",
    )
    args = parser.parse_args()

    # Find all Python files
    root = args.path
    patterns = ["examples/**/*.py", "src/**/*.py", "tests/**/*.py"]

    all_files = []
    for pattern in patterns:
        all_files.extend(root.glob(pattern))

    total_changes = 0
    files_changed = 0

    print(f"{'DRY RUN: ' if args.dry_run else ''}Migrating emoji names...")
    print(f"Scanning {len(all_files)} files...")
    print()

    for file_path in sorted(all_files):
        count, changes = migrate_file(file_path, dry_run=args.dry_run)
        if count > 0:
            files_changed += 1
            total_changes += count
            print(f"{file_path} ({count} changes)")
            for change in changes[:5]:
                print(change)
            if len(changes) > 5:
                print(f"  ... and {len(changes) - 5} more")
            print()

    print("=" * 60)
    print(f"Total: {total_changes} changes in {files_changed} files")
    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
