import requests

token = "6f298a6f68c27deb7dcd10aacef33abbd6819fdc"

WackWack_Mandaluyong = "https://api.waqi.info/feed/A132778/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
Baltazar_Caloocan = "https://api.waqi.info/feed/A64045/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
Forbestown_Taguig = "https://api.waqi.info/feed/A248974/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
SerendraBamboo_Taguig = "https://api.waqi.info/feed/A50926/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
Calzada_Taguig = "https://api.waqi.info/feed/A204484/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"
Multinational_Paranaque = "https://api.waqi.info/feed/A127897/?token=6f298a6f68c27deb7dcd10aacef33abbd6819fdc"

response = requests.request("GET", WackWack_Mandaluyong)
print(response.json())
response = requests.request("GET", Baltazar_Caloocan)
print(response.json())
response = requests.request("GET", Forbestown_Taguig)
print(response.json())
response = requests.request("GET", SerendraBamboo_Taguig)
print(response.json())
response = requests.request("GET", Calzada_Taguig)
print(response.json())
response = requests.request("GET", Multinational_Paranaque)
print(response.json())