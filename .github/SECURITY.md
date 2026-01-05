# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.9.x   | :white_check_mark: |
| < 0.9   | :x:                |

## Security Scope

StyledConsole is a terminal output formatting library. It:

- Does **not** handle sensitive data (passwords, tokens, PII)
- Does **not** make network requests
- Does **not** execute arbitrary code
- Does **not** read/write files (except optional HTML/image export to user-specified paths)

The attack surface is minimal, but we take all reports seriously.

### Dependencies

Security issues in our dependencies (Rich, Pillow, etc.) should be reported directly to those upstream projects. We trust our dependencies and will update when they release security fixes.

## Reporting a Vulnerability

If you discover a security vulnerability in StyledConsole itself, please open a GitHub issue with **[SECURITY]** in the title.

Example: `[SECURITY] Potential issue with XYZ`

Please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Disclosure Policy

- We follow coordinated disclosure
- Credit will be given to reporters (unless anonymity is requested)

## Out of Scope

The following are **not** considered security vulnerabilities:

- ANSI escape sequence injection (this is the library's purpose)
- Terminal-specific rendering differences
- Performance issues
- Bugs that don't have security implications
