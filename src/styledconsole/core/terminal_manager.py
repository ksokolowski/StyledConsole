"""Terminal capability management and detection.

This module provides terminal detection, color system determination,
and debug logging for terminal-related functionality.
"""

import logging
import os
import sys
from typing import Literal

from styledconsole.utils.terminal import TerminalProfile, detect_terminal_capabilities

# Type alias for Rich-compatible color systems
ColorSystemType = Literal["auto", "standard", "256", "truecolor", "windows"]


class TerminalManager:
    """Manages terminal capability detection and configuration.

    This class encapsulates all terminal-related functionality including:
    - Terminal capability detection (ANSI support, color depth, emoji safety)
    - Color system determination (truecolor, 256, standard, auto)
    - Debug logging setup and terminal information logging

    Attributes:
        profile: Detected terminal capabilities (None if detection disabled)

    Example:
        >>> manager = TerminalManager(detect=True, debug=True)
        >>> if manager.profile and manager.profile.ansi_support:
        ...     print("ANSI colors supported!")
        >>> color_system = manager.get_color_system()
        >>> print(f"Using color system: {color_system}")
    """

    def __init__(self, detect: bool = True, debug: bool = False):
        """Initialize terminal manager with optional detection and debugging.

        Args:
            detect: Whether to detect terminal capabilities automatically.
                If False, profile will be None and color_system defaults to "auto".
            debug: Enable debug logging for terminal detection and configuration.

        Example:
            >>> # Full detection with debug logging
            >>> manager = TerminalManager(detect=True, debug=True)

            >>> # No detection (for testing or non-terminal environments)
            >>> manager = TerminalManager(detect=False)
        """
        self._debug = debug
        self._logger = self._setup_logging() if debug else None
        self._virtual_mode = False

        # Detect terminal capabilities if requested
        self.profile: TerminalProfile | None = None
        if detect:
            self.profile = detect_terminal_capabilities()
            if self._debug and self.profile:
                self._log_capabilities()

    def _setup_logging(self) -> logging.Logger:
        """Set up debug logger for TerminalManager.

        Returns:
            Configured logger instance that writes to stderr.

        Note:
            Logger is only created if debug=True in __init__.
            Uses format: [module.class] LEVEL: message
        """
        logger = logging.getLogger("styledconsole.terminal")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        return logger

    def _log_capabilities(self) -> None:
        """Log detected terminal capabilities for debugging.

        Only called when debug=True and profile is available.
        Logs: ANSI support, color depth, emoji safety, terminal dimensions.
        """
        if self._debug and self._logger and self.profile:
            self._logger.debug(
                f"Terminal detected: ANSI={self.profile.ansi_support}, "
                f"colors={self.profile.color_depth}, "
                f"emoji={self.profile.emoji_safe}, "
                f"size={self.profile.width}x{self.profile.height}"
            )

    def get_color_system(self) -> ColorSystemType:
        """Determine appropriate color system based on terminal capabilities.

        Checks in order:
        1. Environment variable SC_FORCE_COLOR_SYSTEM (if set)
        2. Detected terminal color depth (if profile available)
        3. Fallback to "auto" for Rich's auto-detection

        Returns:
            Color system string: "truecolor", "256", "standard", or "auto"

        Example:
            >>> manager = TerminalManager(detect=True)
            >>> color_system = manager.get_color_system()
            >>> # Returns "truecolor" on modern terminals
            >>> # Returns "256" on older terminals
            >>> # Returns "auto" if detection disabled
        """
        # Check for environment variable override
        env_override = os.environ.get("SC_FORCE_COLOR_SYSTEM")
        if env_override in {"standard", "256", "truecolor", "auto"}:
            if self._debug and self._logger:
                self._logger.debug(f"Color system overridden by env: {env_override}")
            # Cast is safe due to the check above
            return env_override  # type: ignore[return-value]

        # Use detected terminal profile if available
        if self.profile:
            if self.profile.color_depth >= 16777216:  # 24-bit truecolor
                return "truecolor"
            elif self.profile.color_depth >= 256:
                return "256"
            elif self.profile.color_depth >= 8:
                return "standard"

        # Fallback to auto-detection
        return "auto"

    def should_force_terminal(self) -> bool:
        """Determine if Rich should force terminal mode.

        Returns:
            True if terminal detection is enabled and ANSI is supported,
            False otherwise (lets Rich decide).

        Example:
            >>> manager = TerminalManager(detect=True)
            >>> if manager.should_force_terminal():
            ...     # Rich will treat output as terminal
            ...     pass
        """
        # Virtual mode always forces terminal (for image/HTML export)
        if self._virtual_mode:
            return True
        return bool(self.profile and self.profile.ansi_support)

    def set_virtual_mode(self, enabled: bool = True) -> None:
        """Enable virtual terminal mode for exports.

        When enabled, the TerminalManager behaves as if it's a perfect
        terminal (TrueColor, Emoji support, modern width handling) regardless
        of the actual environment. This ensures consistent layout for image
        and HTML exports.

        Args:
            enabled: Whether to enable virtual mode. Defaults to True.

        Example:
            >>> manager = TerminalManager(detect=True)
            >>> manager.set_virtual_mode(True)
            >>> # Now behaves as perfect terminal for exports
        """
        self._virtual_mode = enabled
        if enabled:
            # Override with a "perfect" virtual terminal profile
            self.profile = TerminalProfile(
                ansi_support=True,
                color_depth=16777216,  # TrueColor (24-bit)
                emoji_safe=True,
                width=80,
                height=24,
                term="xterm-256color",
                colorterm="truecolor",
                terminal_name="virtual",
                modern_emoji=True,
            )
            if self._debug and self._logger:
                self._logger.debug("Virtual terminal mode enabled (perfect profile)")


__all__ = ["TerminalManager"]
