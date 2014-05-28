import requests

user = ""
password = ""

host = "http://g89rtpsrv.med.tu-dresden.de"
port = "8080"
instance = "OpenClinica"
baseUrl = host + ":" + port + "/" + instance

session = requests.Session()
loginCredentials = { "j_username": user, "j_password" : password }
r = session.post(baseUrl + "/j_spring_security_check", loginCredentials)

# xml, html
format = "json"

r = session.get(baseUrl + "/rest/clinicaldata/json/view/S_DEFAULTS1/SS_XXY/*/*?includeDNs=y&includeAudits=y")

print r.text

