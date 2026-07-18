#!/usr/bin/env python3
from hackathon import list_tree, session_status
import json

print(json.dumps(session_status(), indent=2, default=str)[:800])
print("entries", len(list_tree(".", max_entries=20)))