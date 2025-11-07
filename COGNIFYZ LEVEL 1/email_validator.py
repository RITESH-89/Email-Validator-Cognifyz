#!/usr/bin/env python3
"""
email_validator.py

A robust email validator suitable for application-level checks.
Not a full RFC 5322 parser (that's extremely complex), but enforces
practical, commonly-required rules:
 - Exactly one '@'
 - Local-part length <= 64, domain length <= 255, overall <= 254
 - Local-part allows unquoted local tokens with allowed characters,
   dots not at ends and not consecutive
 - Domain is one or more labels separated by '.', each 1-63 chars,
   label must start/end with letter or digit, may contain hyphens
 - TLD must be alphabetic and 2..63 chars
"""

import re
import sys


# Allowed characters in unquoted local-part (per common usage)
_LOCAL_ALLOWED = set("abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     "0123456789"
                     "!#$%&'*+/=?^_`{|}~.-")  # dot handled separately

_label_re = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")
_tld_re = re.compile(r"^[A-Za-z]{2,63}$")


def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate an email address.

    Returns:
      (True, "OK") if valid,
      (False, "reason") if invalid.

    Notes: This is a practical validator, not a full RFC 5322 implementation.
    """
    if not isinstance(email, str):
        return False, "Email must be a string."

    email = email.strip()
    if not email:
        return False, "Email is empty after stripping whitespace."

    # Overall length check
    if len(email) > 254:
        return False, "Email is too long (more than 254 characters)."

    # Must contain exactly one '@'
    if email.count('@') != 1:
        return False, "Email must contain exactly one '@' character."

    local, domain = email.rsplit('@', 1)

    # Local part basic checks
    if not local:
        return False, "Local part (before '@') is empty."
    if len(local) > 64:
        return False, "Local part is too long (more than 64 characters)."

    # Local part: dot rules (no leading/trailing dot, no consecutive dots)
    if local.startswith('.') or local.endswith('.'):
        return False, "Local part must not start or end with a dot."
    if '..' in local:
        return False, "Local part must not contain consecutive dots."

    # Validate characters of local (this excludes quoted strings like "John..Doe")
    for ch in local:
        if ch not in _LOCAL_ALLOWED:
            return False, f"Invalid character in local part: {repr(ch)}"

    # Domain basic checks
    if not domain:
        return False, "Domain part (after '@') is empty."
    # Domain total length (each label max 63, total typically <=255)
    if len(domain) > 255:
        return False, "Domain part is too long (more than 255 characters)."

    # Domain must not have consecutive dots, and no leading/trailing dot
    if domain.startswith('.') or domain.endswith('.'):
        return False, "Domain must not start or end with a dot."
    if '..' in domain:
        return False, "Domain must not contain consecutive dots."

    labels = domain.split('.')
    if len(labels) < 2:
        return False, "Domain should contain at least one dot (e.g., example.com)."

    # Validate each label
    for label in labels:
        if not label:
            return False, "Empty domain label (consecutive dots or leading/trailing dot)."
        if len(label) > 63:
            return False, f"Domain label '{label}' is too long (more than 63 chars)."
        if not _label_re.match(label):
            return False, f"Invalid domain label: '{label}'. Labels must start and end with letter or digit; internal chars may include hyphens."

    # Validate TLD (last label)
    tld = labels[-1]
    if not _tld_re.match(tld):
        return False, f"Top-level domain '{tld}' must be alphabetic and 2-63 characters long."

    # All checks passed
    return True, "OK"


def main():
    # Simple command line interface
    if len(sys.argv) == 1:
        print("Usage: python email_validator.py <email1> [<email2> ...]")
        print("Or import validate_email(email) in your code.")
        sys.exit(0)

    for em in sys.argv[1:]:
        valid, reason = validate_email(em)
        if valid:
            print(f"[VALID]   {em}")
        else:
            print(f"[INVALID] {em}  -> {reason}")


if __name__ == "__main__":
    main()
