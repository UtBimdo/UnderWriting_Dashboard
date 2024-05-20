# from asyncio.constants import FLOW_CONTROL_HIGH_WATER_SSL_READ
import streamlit as st
import plotly.express as px
import os
import warnings 
warnings.filterwarnings('ignore')
import pandas as pd
# import numpy as np
from datetime import datetime,timedelta
from functools import reduce
# import json_normalize
# import json
# import re
from openpyxl import load_workbook

#PAGE TITLE
st.set_page_config(page_title="U/W Dashboard",page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: U/W Dashboard")
st.markdown('<style>div.block-container{padding-top:lrem;}</style>',unsafe_allow_html=True)

#DATA UPLOADING
f1 = st.file_uploader(":file_folder: Upload a file",type=(["csv","text","xlsx","xls"]))  # CREATED A file uploader
if f1 is not None:
    filename = f1.name
    st.write(filename)
    os.chdir(r"C:\Users\somya\Downloads")
    df = pd.read_excel(filename)
else:
    os.chdir(r"C:\Users\somya\Desktop\sdp")
    df = pd.read_excel("TrackerSheetCopy.xlsx")


# Date input widgets
start_date = st.date_input("Start date", df['Sent to U/W'].min())
end_date = st.date_input("End date", df['Sent to U/W'].max())

if start_date > end_date:
    st.error("Error: End date must be after start date.")
else:
    # Filter the DataFrame
    mask = (df['Sent to U/W'] >= pd.to_datetime(start_date)) & (df['Sent to U/W'] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]


#APPLY FILTERS
st.sidebar.header("Choose your filter: ")

# U/W STATUS FILTER
uw_status = st.sidebar.multiselect("Pick your Status",df["UW Status"].unique())
if not uw_status:
    filtered_df = filtered_df
else:
    filtered_df = filtered_df.loc[filtered_df["UW Status"].isin(uw_status)]

# AGENT NAME FILTER
emp_name = st.sidebar.multiselect("Pick your Employee",df["Agent Name"].unique())
if not emp_name:
    filtered_df = filtered_df
else:
    filtered_df = filtered_df.loc[filtered_df["Agent Name"].isin(emp_name)]

#NBFC STATUS FILTER
nbfc_status = st.sidebar.multiselect("Pick NBFC Status",df["NBFC Status"].unique())
if not nbfc_status:
    filtered_df = filtered_df
else:
    filtered_df = filtered_df.loc[filtered_df["NBFC Status"].isin(nbfc_status)]

# NBFC APPROVED COMPANY FILTER
approval_comp = st.sidebar.multiselect("Pick NBFC Approved Company",df["Approved by NBFC Partner"].unique())
if not approval_comp:
    filtered_df = filtered_df
else:
    filtered_df = filtered_df.loc[filtered_df["Approved by NBFC Partner"].isin(approval_comp)]


# disbursal_start_date = st.date_input("Disbursal Start date", df['Disbursal Date'].min())
# disbursal_end_date = st.date_input("Disbursal End date", df['Disbursal Date'].max())

# if disbursal_start_date > disbursal_end_date:
#     st.error("Error: End date must be after start date.")
# else:
#     # Filter the DataFrame
#     mask = (df['Disbursal Date'] >= pd.to_datetime(disbursal_start_date)) & (df['Disbursal Date'] <= pd.to_datetime(disbursal_end_date))
#     filtered_df = df.loc[mask]

st.dataframe(filtered_df)


col1 , col2 = st.columns((2))

#U/W STATUS GROUP BY
pivot_df = filtered_df.groupby(['UW Status',],as_index=False).agg(count=('UW Status','count'))
with col1:
    with st.expander("U/W Status plots"):
        st.subheader("U/W STATUS PLOTS")
        fig = px.bar(pivot_df,x="UW Status",y="count",text=['{:,.0f}'.format(x) for x in pivot_df["count"]],
                    template="seaborn")
        st.plotly_chart(fig,use_container_width=True,height=200)
    with st.expander("U/W status Data"):
            st.write(pivot_df.style.background_gradient(cmap="Blues"))
            csv = pivot_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data",data=csv,file_name="U/W Status Data.csv",mime="text/csv",
                               help="Click here to download data to excel")
            

agent_pivot = filtered_df.groupby(['Agent Name',],as_index=False).agg(count=('Agent Name','count'))
with col2:
    with st.expander("Employee Plots"):
        st.subheader("EMPLOYEE PLOTS")
        fig = px.bar(agent_pivot,x="Agent Name",y="count",text=['{:,.0f}'.format(x) for x in agent_pivot["count"]],
                     template="seaborn")
        st.plotly_chart(fig,use_container_width=True,height=200)
    with st.expander("Employee Data"):
        st.write(agent_pivot.style.background_gradient(cmap="Blues"))
        csv = agent_pivot.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Agent Data.csv",mime="text/csv",
                           help="Click here to download data to excel")
