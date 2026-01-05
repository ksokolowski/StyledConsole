# Security Policy

## Scope

StyledConsole is a terminal output formatting library. It has a minimal security surface:

- **No network operations** - The library does not make network requests
- **No authentication** - No user credentials or secrets are handled
- **No external data parsing** - Output only; does not parse untrusted input
- **Local file operations** - Export features write to user-specified local paths

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.9.x   | :white_check_mark: |
| < 0.9   | :x:                |

## Reporting a Vulnerability

If you discover a security issue, please report it by:

1. **Email:** krzysiek.sokolowski@gmail.com
1. **Subject:** `[SECURITY] StyledConsole - <brief description>`

Please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

**Response timeline:**

- Acknowledgment within 48 hours
- Assessment within 7 days
- Fix timeline depends on severity

## Known Considerations

### Dependencies

StyledConsole depends on:

- `rich` - Terminal rendering
- `Pillow` - Image export (optional)
- `pyfiglet` - ASCII art banners
- `wcwidth` - Character width calculation
- `emoji` - Emoji support

We recommend keeping dependencies updated. Use `pip list --outdated` or enable Dependabot.

### Export Features

The `export_html()`, `export_text()`, and `export_image()` methods write to paths specified by the caller. The library does not sanitize paths - callers are responsible for validating output locations.

### Rich Markup

If you pass untrusted strings to StyledConsole methods, be aware that Rich markup (e.g., `[bold]`, `[link]`) will be interpreted. Use `markup=False` or escape untrusted content if needed.

## Security Updates

Security fixes are released as patch versions (e.g., 0.9.9.2) and announced in the changelog.
