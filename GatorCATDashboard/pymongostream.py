# streamlit_app.py
import os
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
# Initialize connection.
mongopass = os.getenv("mongopassword")
#print(mongopass)
client = MongoClient(f"mongodb+srv://admin:{mongopass}@streamlit-test.u4cyq.mongodb.net/test-game?retryWrites=true&w=majority")
db = client.test
db = client.get_database("test-game")
# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def get_data():
    items = db.player.distinct("name")
    items = list(items)  # make hashable for st.cache
    #print(items)
    return items

@st.cache(ttl=600)
def get_person(player_name):
    db = client.get_database("test-game")
    output = db.player.find({"name": player_name})
    output = list(output)
    return output

def get_class(chsn_class):
    results = db.player.find({"name":chsn_class},{"_id":0,"class":1})
    choices = get_assignments(results)
    return choices

def get_assignments(items):
    output = set()
    for entry in items:
        output.add(entry["class"])
    return list(output)

if "class" not in st.session_state:
    st.session_state["class"] = get_data()

st.session_state["name"] = st.selectbox("Select a name", st.session_state["class"])
st.session_state["other"] = st.selectbox("Select a class", get_class(st.session_state["name"]))
if st.session_state["name"] and st.session_state["other"]:
    st.write(get_person(st.session_state["other"]))