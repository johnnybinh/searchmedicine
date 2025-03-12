import streamlit as st
import requests
import pandas as pd

# variable
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i",
}

url = "https://dichvucong.dav.gov.vn/api/services/app/soDangKy/GetAllPublicServerPaging"


# firefoxDriver


# web ui
st.title("Medicine Search Agent")
with st.form("input_from"):
    input = st.text_area(
        label="Enter names(Comma Seperated)",
        placeholder="Trazimera\nBavencio\nEnterobella  ",
    )
    submitted = st.form_submit_button("Search")


res = []
not_found = []
input_split = input.split("\n")

if submitted:
    for name in input_split:
        payload = {
            "filterText": name.strip(),
            "SoDangKyThuoc": {},
            "KichHoat": True,
            "skipCount": 0,
            "maxResultCount": 10,
            "sorting": None,
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if data["result"]["totalCount"] == 0:
                not_found.append(name)
            for item in data["result"]["items"]:
                res.append(item)

res = pd.DataFrame(res)
res = res.loc[:, "tenThuoc":"phanLoaiThuocEnum"]
st.dataframe(res)

st.write("Not Found")
st.write(not_found)
