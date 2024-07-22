import streamlit as st
import pyomo.environ as pyo
import maximizeInterest as MI
import re

st.header("Maximize my Portfolio")
st.write("Motivated by the problem proposed in Facebook page \"เนิร์ดไฟแนนซ์\", it is solved by formulating to Linear Programming problem. The Python library Pyomo is the main tool of this project. This is created by Phaphontee Yamchote (my profile page: [link](https://yamchote-ppt.github.io/profile/))")
inputDict = {
        'LH':([0.0025, 0.0175,0.0555,0.015,0.0025,0],[100000, 900000, 1000000, 3000000, 100000000]),
        'KPP':([0.02,0.04,0.02,0.0155,0.005],[5000,10000,50000,1500000]),
        'Dime':([0.03,0.015,0.005],[10000,1000000]),
        'CIMBChill': ([0.005,0.018,0.0288,0.002],[10000,50000,100000]),
        'Kept':([0.0175],[]),
        'TTB':([0.022,0.016,0.012],[100000,1000000]),
        'Alpha':([0.02,0.007],[500000]),
        'CIMBSpeed':([0.008,0.0188],[100000]),
    }
# st.code(str(inputDict),line_numbers=True)

principle = st.number_input("How much is your principle?", value=10000, placeholder="Type a number...")

m = MI.optimize(principle,inputDict,False)

if principle==0:
    st.write(f"""Principle = `{principle}`

Maximum interest = `{pyo.value(m.interest)}`""")
else:
    st.write(f"""Principle = `{principle}`

Maximum interest = `{pyo.value(m.interest)}`

Average interest rate = `{pyo.value(m.interest)/principle *100:.2f}%`""")

asset_value = {}
interest = {}
for rate, bankName in zip(MI.getInterestRate(inputDict),MI.getDeltaName(inputDict)):
    key = re.match(r'(.+)(\d+)',bankName).group(1)
    asset_value[key] = asset_value.get(key,0) + pyo.value(m.delta[bankName])
    interest[key] = interest.get(key,0) + pyo.value(rate*m.delta[bankName])
# print(asset_value)
# print(interest)
code = f"""{'.':15s} {'amount':^12s} {'interest':^12s}
"""
for key in asset_value:
    code += f"""{key:>10s}:\t{asset_value[key]:^12.0f} {interest[key]:^12.0f}
"""
st.code(code)
# report += '=============================='