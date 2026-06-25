## Empty State Handling
- Implemented Django template `{% empty %}` fallback inside the main items loop.
- Displayed "No lost/found items available" message with a dashed card layout for empty listings.

---

## Architectural Decisions

## Website Footer Implementation
- Created a semantic `<footer>` element layout featuring College of Engineering Chengannur name and 2026 copyright text.
- Styled with a uniform dark theme for consistent UI appearance.
## Email notifications

Item claim notifications are sent through Django's SMTP email backend. SMTP credentials are read from environment variables in `lost_and_found/settings.py`, and claim email composition lives in `items/notifications.py` so the claim view only coordinates the workflow.
