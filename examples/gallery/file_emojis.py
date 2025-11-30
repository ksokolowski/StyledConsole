#!/usr/bin/env python3
"""
Demo: File and Document Emojis

Showcases the new file-related emoji constants for file managers,
documentation systems, and file organization interfaces.
"""

from styledconsole import Console
from styledconsole.emojis import EMOJI

console = Console()

# File System Overview
console.banner("FILE & DOCUMENT EMOJIS")

console.frame(
    f"""
{EMOJI.FOLDER} project/
  {EMOJI.OPEN_FOLDER} src/
    {EMOJI.FILE} main.py
    {EMOJI.FILE} utils.py
  {EMOJI.OPEN_FOLDER} docs/
    {EMOJI.DOCUMENT} README.md
    {EMOJI.SCROLL} LICENSE
  {EMOJI.PACKAGE} dist/
    {EMOJI.FLOPPY} app-v1.0.zip
""",
    title=f"{EMOJI.FILE_CABINET} File System",
    border="rounded",
    width=60,
)

console.newline()

# Documentation Library
console.frame(
    f"""
{EMOJI.BOOKS} Documentation Library:
  {EMOJI.GREEN_BOOK} Python Guide
  {EMOJI.BLUE_BOOK} JavaScript Handbook
  {EMOJI.ORANGE_BOOK} Go Tutorial
  {EMOJI.CLOSED_BOOK} Rust Reference

{EMOJI.NOTEBOOK} Current: Learning FastAPI
{EMOJI.LEDGER} Notes: 47 entries
{EMOJI.BOOKMARK} Bookmarks: 12 pages
""",
    title=f"{EMOJI.BOOK} Reading List",
    border="solid",
    width=60,
)

console.newline()

# File Operations
console.frame(
    f"""
{EMOJI.PUSHPIN} Pinned Files (5)
{EMOJI.PAPERCLIP} Attachments (3)
{EMOJI.LABEL} Tagged: "important", "review"
{EMOJI.CARD_INDEX} Indexed: 2,847 files
{EMOJI.CARD_FILE_BOX} Archived: 1,203 items
{EMOJI.WASTEBASKET} Trash: 42 items (empty soon)
""",
    title=f"{EMOJI.CLIPBOARD} File Manager",
    border="double",
    width=60,
)

console.newline()

# News & Media
console.frame(
    f"""
{EMOJI.NEWSPAPER} Daily Tech News
  {EMOJI.ROLLED_NEWSPAPER} Breaking: Python 3.14 Released!
  {EMOJI.ROLLED_NEWSPAPER} Featured: Best VS Code Extensions
  {EMOJI.ROLLED_NEWSPAPER} Tutorial: Docker Compose Guide

{EMOJI.MEMO} Latest Articles: 15 new today
""",
    title=f"{EMOJI.GLOBE} News Feed",
    border="thick",
    width=60,
)

console.newline()

# All File Emojis Reference
console.frame(
    """
📁 FOLDER          📂 OPEN_FOLDER      🗄 FILE_CABINET
🗃 CARD_FILE_BOX   🗑 WASTEBASKET

📄 FILE/PAGE       📃 DOCUMENT         📜 SCROLL
📝 MEMO            📋 CLIPBOARD

📌 PUSHPIN         📎 PAPERCLIP        🔖 BOOKMARK
🏷 LABEL           📇 CARD_INDEX

📖 BOOK            📚 BOOKS            📓 NOTEBOOK
📒 LEDGER          📕 CLOSED_BOOK

📗 GREEN_BOOK      📘 BLUE_BOOK        📙 ORANGE_BOOK

📰 NEWSPAPER       🗞 ROLLED_NEWSPAPER
""",
    title=f"{EMOJI.PACKAGE} Complete File Emoji Set",
    border="rounded",
    border_color="cyan",
    width=70,
)

console.rule()
console.text(
    "✨ All file emojis are single-codepoint (VS16 safe) and work perfectly with gradients!"
)
