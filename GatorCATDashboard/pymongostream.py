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
#print(mongopass)
client = MongoClient(f"mongodb+srv://admin:{mongopass}@{cluster_name}.u4cyq.mongodb.net/{collection_name}?retryWrites=true&w=majority")
db = client.test
db = client.get_database(collection_name)
# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def get_class():
    items = db.StudentData.distinct("class")
    items = list(items)  # make hashable for st.cache
    return items

@st.cache(ttl=600)
def get_assignments(class_name):
    output = db.StudentData.find({"class": class_name})
    output = list(output)
    return output

def get_assignment(chosen_class):
    results = db.StudentData.find({"class":chosen_class},{"_id":0,"assignment":1})
    choices = get_unique_assignments(results)
    return choices

def get_unique_assignments(items):
    output = set()
    for entry in items:
        output.add(entry["assignment"])
    return list(output)

def get_bar_data(org, assignment):
    
    output = db.StudentData.find({"class": org, "assignment": assignment},{"_id": 0, "checks": 1})
    output = [document["checks"] for document in output]
    df = pd.DataFrame(output)
    total = df.sum(axis=0)
    return (total/len(output))

def main():
    if "classes" not in st.session_state:
        st.session_state["classes"] = get_class()

    st.session_state["class"] = st.sidebar.selectbox("Select a class", st.session_state["classes"],index=0)
    st.session_state["assignments"] = st.sidebar.selectbox("Select a assignment", get_assignment(st.session_state["class"]),index=0)
    st.session_state["Type"] = st.selectbox("Select a graph", ["Bar", "Line"])
    data = get_bar_data(st.session_state["class"], st.session_state["assignments"])
    if st.session_state["Type"] == "Line":
        st.line_chart(data)
    elif st.session_state["Type"] == "Bar":
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