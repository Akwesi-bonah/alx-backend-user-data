#!/usr/bin/env python3
""" Main 100
"""
import re
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()
t = a.require_auth("/api/v1/status/", ["/api/v1/us*"])
s = re.search("/api/v1/us*", "/api/v1/status/")
print(s)
print(t)

