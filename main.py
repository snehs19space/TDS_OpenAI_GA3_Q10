from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(..., description="User query")):
    q_lower = q.lower().strip()

    # Precompute all regex matches
    ticket_match = re.search(r"ticket (\d+)", q_lower)
    meeting_match = re.search(r"schedule meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in ([\w\s]+)", q_lower)
    expense_match = re.search(r"employee (\d+)", q_lower)
    bonus_match = re.search(r"employee (\d+) for (\d{4})", q_lower)
    issue_match = re.search(r"issue (\d+) for the ([\w\s]+) department", q_lower)

    # --- 1️⃣ Ticket Status ---
    if "status" in q_lower and ticket_match:
        ticket_id = int(ticket_match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": ticket_id})
        }

    # --- 2️⃣ Meeting Scheduling ---
    if "schedule" in q_lower and meeting_match:
        date, time, room = meeting_match.groups()
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": room.strip().title()
            })
        }

    # --- 3️⃣ Expense Balance ---
    if "expense" in q_lower and expense_match:
        employee_id = int(expense_match.group(1))
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": employee_id})
        }

    # --- 4️⃣ Performance Bonus ---
    if "bonus" in q_lower and bonus_match:
        employee_id, year = bonus_match.groups()
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(employee_id),
                "current_year": int(year)
            })
        }

    # --- 5️⃣ Office Issue Reporting ---
    if "report" in q_lower and "issue" in q_lower and issue_match:
        issue_code, department = issue_match.groups()
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_code),
                "department": department.strip().title()
            })
        }

    # Default fallback if no match found
    return {"error": "Could not identify function call."}
