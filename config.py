# config.py

# Authentication tokens
LEETCODE_SESSION_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTEyNTUxMjMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4MGMyODJjNjczMzJjMjQyMjA4MDVjOTM4NTA0NWZlYWZlOWNhMzY2YTkxZGViOTllN2NhNTZhNjBhZWFmZTRhIiwic2Vzc2lvbl91dWlkIjoiMDIyZmY4NDUiLCJpZCI6MTEyNTUxMjMsImVtYWlsIjoiaXB1bmVldC5naXJkaGFyQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiaW1wdW5lZXRnMTIzIiwidXNlcl9zbHVnIjoiaW1wdW5lZXRnMTIzIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2F2YXRhcnMvYXZhdGFyXzE2OTgzNzkzMzQucG5nIiwicmVmcmVzaGVkX2F0IjoxNzM3NDE3ODgzLCJpcCI6Ijk3LjEyNi43NC4xMjUiLCJpZGVudGl0eSI6IjA4NDViMzA5YzdiOWI5NTdhZmQ5ZWNmNzc1YTRjMjFmIiwiZGV2aWNlX3dpdGhfaXAiOlsiNzJmZDk0NWFkNDk4YmE0YWVlYTczNWEwZTdhNGU2ZGQiLCI5Ny4xMjYuNzQuMTI1Il19.141OFH-PeNWDz1Uf_B65LorR9hA3MwqKw3o6hp1OACY"
CSRF_TOKEN = "lmFibhDEUR4SjEfvVRm7va7gKlG7X8VMahQWkJ454IUtzUVv0v9aOmNX0LxdoDxh"

# Database configuration
DATABASE_URL = "sqlite:///leetcode.db"

# API endpoints
LEETCODE_API_ENDPOINT = "https://leetcode.com/graphql"
LEETCODE_API_BROWSER_ENDPOINT = "https://leetcode.com/api/problems/all/"

# HTTP Headers
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION_TOKEN}; csrftoken={CSRF_TOKEN}",
    "x-csrftoken": CSRF_TOKEN
}