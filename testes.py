import requests

headers={
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzYyNTQ4NDc3fQ.R46K1ohgNk-R1I1Xx46JO_J8zKT5v99NDDcdMIvCzMU"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)

print(requisicao.status_code)
print(requisicao.text)