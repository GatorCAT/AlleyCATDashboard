# streamlit_app.py
import os
import plotly.express as px
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
# Initialize connection.
username = os.getenv("username")
mongopass = os.getenv("password")
cluster_name = os.getenv("cluster_name")
collection_name = os.getenv("collection_name")
client = MongoClient(f"mongodb+srv://admin:{mongopass}@{cluster_name}.u4cyq.mongodb.net/{collection_name}?retryWrites=true&w=majority")
db = client.test
db = client.get_database(collection_name)
# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def get_class():
    """Query database for all unique classes."""
    items = db.StudentData.distinct("class")
    items = list(items)  # make hashable for st.cache
    return items

# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def get_assignment(chosen_class):
    """Query database for all assignments in a certain class."""
    results = db.StudentData.find({"class":chosen_class},{"_id":0,"assignment":1})
    choices = get_unique_assignments(results)
    return choices

def get_unique_assignments(items):
    """Remove duplicate assignments."""
    output = set()
    for entry in items:
        output.add(entry["assignment"])
    return list(output)

def get_bar_data(df):
    """Manipulate data to visualize in bar graph."""
    df = df.drop(["date"], axis=1)
    length = len(df)
    total = df.sum(axis=0)
    return ((total/length)*100)

def get_line_data(df):
    """Manipulate data to visualize in line graph."""
    dftotal = pd.DataFrame({"total": df.sum(axis=1)})
    dftotal["date"] = df["date"]
    dftotal = dftotal.groupby(dftotal["date"]).mean()
    print(len(df.columns)-1)
    dfaverage = dftotal/(len(df.columns)-1)
    return (dfaverage * 100)

# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def get_from_database(org, assignment):
    """Query data from database."""
    output = db.StudentData.find({"class": org, "assignment": assignment},{"_id": 0, "data": 1})
    output = [document["data"] for document in output]
    df = pd.DataFrame(output)
    return df

def main():
    if "classes" not in st.session_state:
        st.session_state["classes"] = get_class()

    st.session_state["class"] = st.sidebar.selectbox("Select a class", st.session_state["classes"],index=0)
    st.session_state["assignments"] = st.sidebar.selectbox("Select a assignment", get_assignment(st.session_state["class"]),index=0)
    st.session_state["Type"] = st.selectbox("Select a graph", ["Bar", "Line"])
    query = get_from_database(st.session_state["class"],st.session_state["assignments"])
    if st.session_state["Type"] == "Line":
        data = get_line_data(query)
        fig = px.line(data, markers=True)
        fig.update_yaxes(range=[0,100])
    elif st.session_state["Type"] == "Bar":
        data = get_bar_data(query)
        switch = st.checkbox("Switch Orientation")
        if switch:
            st.session_state["Orientation"] = "h"
        else:
            st.session_state["Orientation"] = ""
        fig = px.bar(data, labels={"index": "Checks", "value": "Average Checks Completed"},width=800,height=1000,orientation=st.session_state["Orientation"])
        fig.update_layout(showlegend=False)
        fig.update_traces(width=.5)
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()