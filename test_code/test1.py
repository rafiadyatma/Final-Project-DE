import requests

# API Endpoint
api_url = "http://103.150.197.96:5005/api/v1/rekapitulasi_v2/jabar/harian"
api_params = {"level": "kab"}

# Make a GET request to the API
response = requests.get(api_url, params=api_params, headers={"accept": "application/json"})

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    api_data = response.json()

    # Extract relevant information from the response
    status_code = api_data.get("status_code")
    data = api_data.get("data")

    if status_code == 200 and data:
        content = data.get("content")
        if content:
            # Print details for the first 10 entries
            for entry in content[:10]:
                tanggal = entry.get("tanggal")
                kode_prov = entry.get("kode_prov")
                nama_prov = entry.get("nama_prov")
                suspek = entry.get("SUSPECT")
                close_contact = entry.get("CLOSECONTACT")
                probable = entry.get("PROBABLE")
                # Access other data points similarly

                # Print or process the data as needed
                print(f"Date: {tanggal}, Province Code: {kode_prov}, Province Name: {nama_prov}")
                print(f"Suspect: {suspek}, Close Contact: {close_contact}, Probable: {probable}")
                print("---")
        else:
            print("No content in the API response.")
    else:
        print(f"API request failed with status code: {status_code}")
else:
    print(f"API request failed with status code: {response.status_code}")


