"""A simple support ticket tracking application."""

import json
import logging

TICKETS = {}


# pylint: disable=too-many-arguments,too-many-positional-arguments
def create_ticket(
    title,
    description,
    reporter,
    priority="medium",
    category="general",
    audit_log=None,
):
    """Create a ticket and optionally record its audit event."""
    if not title:
        return None

    if audit_log is None:
        audit_log = []

    ticket_id = str(len(TICKETS) + 1)
    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "reporter": reporter,
        "assignee": None,
    }

    TICKETS[ticket_id] = ticket
    audit_log.append(f"Created ticket {ticket_id} for {reporter}")
    return ticket


def assign_ticket(ticket_id, agent, notify=False):
    """Assign a ticket to an agent if the ticket exists."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return False

    ticket["assignee"] = agent
    if notify:
        logging.info("Ticket %s assigned to %s", ticket_id, agent)
    return True


def update_status(ticket_id, status):
    """Update a ticket's status if the ticket exists."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return None

    ticket["status"] = status
    return ticket


def search_tickets(status=None, priority=None):
    """Return tickets matching the supplied filters."""
    results = []
    for ticket in TICKETS.values():
        if status is not None and ticket["status"] != status:
            continue
        if priority and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def save_tickets(path="tickets.json"):
    """Save tickets to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(TICKETS, file, indent=2)


def load_tickets(path="tickets.json"):
    """Load tickets from a JSON file.

    Parse and validate before updating the shared dictionary.
    """
    with open(path, "r", encoding="utf-8") as file:
        loaded_tickets = json.load(file)

    if not isinstance(loaded_tickets, dict):
        raise ValueError("Ticket data must be a JSON object.")

    TICKETS.clear()
    TICKETS.update(loaded_tickets)


def print_ticket_report():
    """Print a summary of all tickets."""
    print("Support Tickets")
    if not TICKETS:
        print("No tickets yet")
        return

    for ticket_id, ticket in TICKETS.items():
        print(ticket_id, ticket["title"], ticket["status"])


def close_ticket(ticket_id):
    """Close a ticket if it exists."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return False

    ticket["status"] = "closed"
    return True


def is_open(ticket_id):
    """Check whether a ticket is open or in progress."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return False

    return ticket["status"] in ("open", "in_progress")


def main():
    """Run the support ticket tracker demo."""
    logging.basicConfig(level=logging.INFO)
    create_ticket(
        "Cannot sign in",
        "Password reset link fails",
        "alex@example.com",
    )
    create_ticket(
        "Billing question",
        "Charged twice",
        "lee@example.com",
        "high",
    )

    assign_ticket("1", "agent-01")
    update_status("1", "in_progress")
    print_ticket_report()

    logging.info("Tickets created: %s", len(TICKETS))
    print("Ticket 1 open?", is_open("1"))

    ticket_id = input("Ticket id to close (Enter to skip): ").strip()
    if ticket_id:
        if close_ticket(ticket_id):
            print("Ticket closed successfully.")
        else:
            print("Ticket not found.")

    save_tickets()


if __name__ == "__main__":
    main()
