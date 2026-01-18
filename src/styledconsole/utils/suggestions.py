"""Suggestion utilities for improved error messages.

Provides fuzzy matching and suggestion generation for user-friendly
error messages when invalid names are provided.

Example:
    >>> from styledconsole.utils.suggestions import suggest_similar
    >>> suggest_similar("rounde", ["rounded", "solid", "double"])
    "Did you mean 'rounded'?"
"""

from __future__ import annotations


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein (edit) distance between two strings.

    The edit distance is the minimum number of single-character edits
    (insertions, deletions, substitutions) needed to transform s1 into s2.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Integer edit distance between the strings.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row: list[int] = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost is 0 if characters match, 1 otherwise
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def find_closest_match(
    query: str,
    candidates: list[str] | set[str] | tuple[str, ...],
    *,
    max_distance: int = 3,
    case_sensitive: bool = False,
) -> str | None:
    """Find the closest matching candidate to the query string.

    Uses Levenshtein distance to find the best match within the
    specified maximum distance threshold.

    Args:
        query: The input string to match.
        candidates: Collection of valid candidate strings.
        max_distance: Maximum edit distance to consider a match.
            Defaults to 3.
        case_sensitive: Whether to perform case-sensitive matching.
            Defaults to False.

    Returns:
        The closest matching candidate, or None if no match within threshold.

    Example:
        >>> find_closest_match("rounde", ["rounded", "solid", "double"])
        'rounded'
        >>> find_closest_match("xyz", ["rounded", "solid", "double"])
        None
    """
    if not query or not candidates:
        return None

    query_normalized = query if case_sensitive else query.lower()
    best_match = None
    best_distance = max_distance + 1

    for candidate in candidates:
        candidate_normalized = candidate if case_sensitive else candidate.lower()

        # Check for exact match (case-insensitive)
        if query_normalized == candidate_normalized:
            return candidate

        distance = levenshtein_distance(query_normalized, candidate_normalized)
        if distance < best_distance:
            best_distance = distance
            best_match = candidate

    return best_match if best_distance <= max_distance else None


def find_closest_matches(
    query: str,
    candidates: list[str] | set[str] | tuple[str, ...],
    *,
    max_results: int = 3,
    max_distance: int = 3,
    case_sensitive: bool = False,
) -> list[str]:
    """Find multiple closest matching candidates to the query string.

    Args:
        query: The input string to match.
        candidates: Collection of valid candidate strings.
        max_results: Maximum number of results to return. Defaults to 3.
        max_distance: Maximum edit distance to consider a match. Defaults to 3.
        case_sensitive: Whether to perform case-sensitive matching. Defaults to False.

    Returns:
        List of closest matching candidates, sorted by distance (best first).

    Example:
        >>> find_closest_matches("fire", ["fire", "forest", "ocean", "sunrise"])
        ['fire']
        >>> find_closest_matches("fore", ["fire", "forest", "ocean"])
        ['fire', 'forest']
    """
    if not query or not candidates:
        return []

    query_normalized = query if case_sensitive else query.lower()
    matches: list[tuple[int, str]] = []

    for candidate in candidates:
        candidate_normalized = candidate if case_sensitive else candidate.lower()
        distance = levenshtein_distance(query_normalized, candidate_normalized)
        if distance <= max_distance:
            matches.append((distance, candidate))

    # Sort by distance, then alphabetically
    matches.sort(key=lambda x: (x[0], x[1]))
    return [match[1] for match in matches[:max_results]]


def suggest_similar(
    query: str,
    candidates: list[str] | set[str] | tuple[str, ...],
    *,
    max_distance: int = 3,
) -> str | None:
    """Generate a "Did you mean?" suggestion string.

    Args:
        query: The invalid input string.
        candidates: Collection of valid options.
        max_distance: Maximum edit distance for suggestions. Defaults to 3.

    Returns:
        A suggestion string like "Did you mean 'rounded'?", or None if
        no close match found.

    Example:
        >>> suggest_similar("rounde", ["rounded", "solid", "double"])
        "Did you mean 'rounded'?"
        >>> suggest_similar("xyz", ["rounded", "solid", "double"])
        None
    """
    match = find_closest_match(query, candidates, max_distance=max_distance)
    if match:
        return f"Did you mean '{match}'?"
    return None


def format_error_with_suggestion(
    message: str,
    query: str,
    candidates: list[str] | set[str] | tuple[str, ...],
    *,
    max_distance: int = 3,
    show_available: bool = True,
    max_available: int = 10,
) -> str:
    """Format an error message with optional suggestion and available options.

    Args:
        message: Base error message (e.g., "Unknown border style: 'rounde'").
        query: The invalid input that caused the error.
        candidates: Collection of valid options.
        max_distance: Maximum edit distance for suggestions. Defaults to 3.
        show_available: Whether to list available options. Defaults to True.
        max_available: Maximum number of available options to show. Defaults to 10.

    Returns:
        Formatted error message with suggestion and/or available options.

    Example:
        >>> format_error_with_suggestion(
        ...     "Unknown style: 'rounde'",
        ...     "rounde",
        ...     ["rounded", "solid", "double"]
        ... )
        "Unknown style: 'rounde'. Did you mean 'rounded'? Available: double, rounded, solid"
    """
    parts = [message]

    # Add suggestion if found
    suggestion = suggest_similar(query, candidates, max_distance=max_distance)
    if suggestion:
        parts.append(suggestion)

    # Add available options
    if show_available and candidates:
        sorted_candidates = sorted(candidates)
        if len(sorted_candidates) > max_available:
            display = sorted_candidates[:max_available]
            parts.append(f"Available: {', '.join(display)}, ... ({len(sorted_candidates)} total)")
        else:
            parts.append(f"Available: {', '.join(sorted_candidates)}")

    return " ".join(parts)


def normalize_name(name: str) -> str:
    """Normalize a name for comparison.

    Converts to lowercase and normalizes separators (hyphens, underscores).

    Args:
        name: Input name string.

    Returns:
        Normalized name suitable for comparison.

    Example:
        >>> normalize_name("Light-Blue")
        'lightblue'
        >>> normalize_name("dark_green")
        'darkgreen'
    """
    return name.lower().replace("-", "").replace("_", "")


def find_normalized_match(
    query: str,
    candidates: list[str] | set[str] | tuple[str, ...],
) -> str | None:
    """Find an exact match after normalizing both query and candidates.

    Useful for catching common formatting variations like:
    - Case differences: "RED" vs "red"
    - Separator variations: "light-blue" vs "lightblue"

    Args:
        query: The input string to match.
        candidates: Collection of valid candidate strings.

    Returns:
        The matching candidate in its original form, or None if no match.

    Example:
        >>> find_normalized_match("light-blue", ["lightblue", "red", "green"])
        'lightblue'
        >>> find_normalized_match("FIRE", ["fire", "ocean", "sunset"])
        'fire'
    """
    query_normalized = normalize_name(query)

    for candidate in candidates:
        if normalize_name(candidate) == query_normalized:
            return candidate

    return None
