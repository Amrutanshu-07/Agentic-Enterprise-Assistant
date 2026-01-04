from langchain_core.tools import Tool

import json

def schedule_meeting(input: str):
    return json.dumps({
        "action": "schedule_meeting",
        "department": "HR",
        "details": input
    })

def raise_it_ticket(input: str):
    return json.dumps({
        "action": "raise_it_ticket",
        "issue": input
    })

TOOLS = [
    Tool(
        name="ScheduleMeeting",
        func=schedule_meeting,
        description="Schedule a meeting with HR or another department"
    ),
    Tool(
        name="RaiseITTicket",
        func=raise_it_ticket,
        description="Raise an IT support ticket"
    )
]
