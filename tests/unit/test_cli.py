"""Tests for the StyledConsole CLI."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Run the CLI with given arguments."""
    return subprocess.run(
        [sys.executable, "-m", "styledconsole", *args],
        capture_output=True,
        text=True,
    )


class TestCLIHelp:
    """Test CLI help and basic functionality."""

    def test_help(self):
        """Test --help shows usage."""
        result = run_cli("--help")
        assert result.returncode == 0
        assert "StyledConsole CLI" in result.stdout
        assert "demo" in result.stdout
        assert "render" in result.stdout
        assert "palette" in result.stdout
        assert "effects" in result.stdout
        assert "icons" in result.stdout
        assert "schema" in result.stdout

    def test_no_args_shows_help(self):
        """Test running without args shows help."""
        result = run_cli()
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower() or "styledconsole" in result.stdout.lower()


class TestDemoCommand:
    """Test the demo command."""

    def test_demo_runs(self):
        """Test demo command runs successfully."""
        result = run_cli("demo")
        assert result.returncode == 0
        assert "StyledConsole" in result.stdout
        assert "Frames" in result.stdout or "frames" in result.stdout.lower()


class TestPaletteCommand:
    """Test the palette command."""

    def test_palette_list(self):
        """Test palette --list shows palettes."""
        result = run_cli("palette", "--list")
        assert result.returncode == 0
        assert "Available Palettes" in result.stdout
        assert "ocean_depths" in result.stdout

    def test_palette_no_args_lists(self):
        """Test palette with no args lists all."""
        result = run_cli("palette")
        assert result.returncode == 0
        assert "Available Palettes" in result.stdout

    def test_palette_preview(self):
        """Test palette preview shows palette."""
        result = run_cli("palette", "ocean_depths")
        assert result.returncode == 0
        assert "ocean_depths" in result.stdout
        assert "Colors" in result.stdout

    def test_palette_unknown(self):
        """Test unknown palette shows error."""
        result = run_cli("palette", "nonexistent_palette_xyz")
        assert result.returncode == 1
        assert "Error" in result.stderr or "error" in result.stderr.lower()


class TestEffectsCommand:
    """Test the effects command."""

    def test_effects_list(self):
        """Test effects --list shows effects."""
        result = run_cli("effects", "--list")
        assert result.returncode == 0
        assert "Effect Presets" in result.stdout
        assert "fire" in result.stdout
        assert "ocean" in result.stdout

    def test_effects_no_args_lists(self):
        """Test effects with no args lists all."""
        result = run_cli("effects")
        assert result.returncode == 0
        assert "Effect Presets" in result.stdout

    def test_effects_preview(self):
        """Test effects preview shows effect."""
        result = run_cli("effects", "fire")
        assert result.returncode == 0
        assert "fire" in result.stdout


class TestIconsCommand:
    """Test the icons command."""

    def test_icons_no_args(self):
        """Test icons with no args shows sample."""
        result = run_cli("icons")
        assert result.returncode == 0
        assert "Available Icons" in result.stdout
        assert "ROCKET" in result.stdout

    def test_icons_search(self):
        """Test icons search finds matches."""
        result = run_cli("icons", "rocket")
        assert result.returncode == 0
        assert "ROCKET" in result.stdout

    def test_icons_search_no_match(self):
        """Test icons search with no matches."""
        result = run_cli("icons", "xyznonexistent")
        assert result.returncode == 0
        assert "No icons found" in result.stdout


class TestRenderCommand:
    """Test the render command."""

    def test_render_json(self):
        """Test rendering a JSON config."""
        config = {
            "type": "frame",
            "title": "Test",
            "content": "Hello!",
            "border": "rounded",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            f.flush()

            result = run_cli("render", f.name)
            assert result.returncode == 0
            assert "Test" in result.stdout
            assert "Hello" in result.stdout

            Path(f.name).unlink()

    def test_render_yaml(self):
        """Test rendering a YAML config."""
        pytest.importorskip("yaml")

        yaml_content = """
type: frame
title: YAML Test
content: Hello from YAML!
border: rounded
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            result = run_cli("render", f.name)
            assert result.returncode == 0
            assert "YAML Test" in result.stdout
            assert "Hello from YAML" in result.stdout

            Path(f.name).unlink()

    def test_render_file_not_found(self):
        """Test rendering nonexistent file."""
        result = run_cli("render", "/nonexistent/path/config.yaml")
        assert result.returncode == 1
        assert "not found" in result.stderr.lower()

    def test_render_unsupported_type(self):
        """Test rendering unsupported file type."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello")
            f.flush()

            result = run_cli("render", f.name)
            assert result.returncode == 1
            assert "Unsupported" in result.stderr

            Path(f.name).unlink()


class TestSchemaCommand:
    """Test the schema command."""

    def test_schema_shows_info(self):
        """Test schema command shows usage info."""
        result = run_cli("schema")
        assert result.returncode == 0
        assert "JSON Schema" in result.stdout
        assert "schema.json" in result.stdout.replace("\n", "")  # Handle line wrapping

    def test_schema_path(self):
        """Test schema --path prints path only."""
        result = run_cli("schema", "--path")
        assert result.returncode == 0
        assert "styledconsole.schema.json" in result.stdout
        # Should be path only, no extra text
        assert "IDE" not in result.stdout

    def test_schema_json(self):
        """Test schema --json prints JSON."""
        result = run_cli("schema", "--json")
        assert result.returncode == 0
        # Should be valid JSON
        schema = json.loads(result.stdout)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["title"] == "StyledConsole Configuration"
        assert "$defs" in schema
