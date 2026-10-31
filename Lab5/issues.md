# Static Code Analysis Issue Log

**Project:** Support Ticket Tracker
**File analyzed:** `support_ticket_tracker.py`
**Lab:** Lab 5 – Static Code Analysis

Line numbers refer to the original file (commit `96c9704`) and match `bandit_before.txt`, `flake8_before.txt` and `pylint_before.txt`.

## Issues Identified and Fixes

| # | Issue | Type / Tool (severity) | Line(s) | Description | Fix Approach |
|---:|---|---|---|---|---|
| 1 | Use of `eval()` | Security – Bandit B307 (Medium), Pylint W0123 | 92 | `eval()` executes arbitrary Python; it ran whenever `RUN_UNSAFE_DEMO=1` was set in the environment. | Removed the `eval` demo block and the now-unused `os` import. |
| 2 | Bare `except: pass` | Reliability – Bandit B110 (Low), Pylint W0702, Flake8 E722 | 24–26 | Swallows every exception, including `KeyboardInterrupt`, and hides real errors in `assign_ticket`. | Replaced try/except with an explicit `if ticket_id in TICKETS` check. |
| 3 | Mutable default argument | Bug – Pylint W0102 | 10 | `audit_log=[]` is created once and shared across all calls, so audit entries leak between callers. | Default changed to `None`; a new list is created inside the function. |
| 4 | Missing ticket-id handling (`KeyError`) | Bug – manual testing | 30–31, 67, 71 | `update_status`, `closeTicket` and `is_open` crash on an unknown id (e.g. entering `999` at the prompt). | Used `TICKETS.get()` with a not-found result; `close_ticket` now returns True/False and `main` prints "Ticket not found." or "Ticket closed successfully." |
| 5 | Unused argument `notify` | Code quality – Pylint W0613 | 20 | `notify` was accepted but never used. | Now logs the assignment when `notify=True`. |
| 6 | Unused imports | Code quality – Pylint W0611, Flake8 F401 | 4, 5 | `sys` and `random` imported but never used. | Removed. |
| 7 | Unused variable `count` | Code quality – Pylint W0612, Flake8 F841 | 84 | Assigned but never used. | Removed. |
| 8 | Comparison to `None` with `!=` | Style – Pylint C0121, Flake8 E711 | 37 | Should use identity comparison. | Changed to `is not None`. |
| 9 | Line too long / trailing whitespace | Style – Flake8 E501, W291; Pylint C0301, C0303 | 10, 14, 63, 71, 79, 80, 84 | Lines over 79 characters (up to 176) and trailing whitespace. | Wrapped long lines and removed trailing whitespace. |
| 10 | File handling without `with` or encoding | Reliability – Pylint R1732, W1514 | 46–48, 53–55 | Files opened without a context manager (leak on error) and without an explicit encoding. | Used `with open(..., encoding="utf-8")`. |
| 11 | `global TICKETS` reassignment | Maintainability – Pylint W0603 | 52 | Rebinding the module-level dict inside `load_tickets` is hard to reason about. | Parse and validate first, then `TICKETS.clear()` and `TICKETS.update()`. |
| 12 | Non-snake_case function name | Style – Pylint C0103 | 66 | `closeTicket` violates PEP 8 naming. | Renamed to `close_ticket` and updated the call in `main`. |
| 13 | Simplifiable `if`/`else` return | Refactor – Pylint R1705, R1703 | 71–74 | Redundant `if ... return True else: return False`. | Return the boolean expression directly, using `in ("open", "in_progress")`. |
| 14 | Old-style / eager string formatting | Style – Pylint C0209, W1203 | 16, 85 | `%` formatting and an f-string inside `logging.info`. | f-string for the audit message; lazy `%s` arguments for logging. |
| 15 | `not len(...)` and missing docstrings | Style – Pylint C1802, C0114, C0116 | 1, 10–92 (all functions), 60 | Missing module and function docstrings; `len()` used as a truth test. | Added docstrings; used `if not TICKETS`. |
| 16 | Too many arguments | Design – Pylint R0913, R0917 | 10 | `create_ticket` takes 6 positional arguments. | Not refactored; suppressed with a `pylint: disable` comment because the signature is part of the public API. |

## Static Analysis Results

| Tool | Before | After |
|---|---|---|
| Bandit | 2 issues (1 Medium, 1 Low) | 0 issues |
| Flake8 | 12 violations | 0 violations |
| Pylint | 5.00/10 | 10.00/10 |

## Functional Testing

| Test case | Input | Observed result | Status |
|---|---|---|---|
| Skip closure | Enter (empty) | Program saves tickets and exits normally | Passed |
| Close existing ticket | `1` | `Ticket closed successfully.` | Passed |
| Close nonexistent ticket | `999` | `Ticket not found.` (no crash) | Passed |
