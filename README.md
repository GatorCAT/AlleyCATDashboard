# GatorCATDashboard
A python based tool for visualizing Gator Gradle data collected from [GatorCATUpload](https://github.com/GatorCAT/GatorCATUpload)

## Requirements:
* [Pandas](https://pandas.pydata.org/)
* [Plotly](https://plotly.com/python/)
* [Poetry](https://python-poetry.org/)
* [Pymongo](https://pymongo.readthedocs.io/en/stable/)
* [python_dotenv](https://pypi.org/project/python-dotenv/)
* [Python](https://www.python.org/)
* [Streamlit](https://docs.streamlit.io/)

## Usage:

### Entering Environment Variables:
After pulling the repository, you must set the environment variables within the `.env` file.  Or you can set the environment variables on your local machine.  This is done to ensure that no sensitive information about the database you are working with is vulnerable. The environment variables needed are:

| Variable | Description |
|----------|---------|
| username | Username for interacting with MongoDB |
| password | Password for interacting with MongoDB |
| cluster_name | Name of the MongoDB cluster to interact with |
| collection_name | Name of the MongoDB collection to interact with |

### Using Python:
After the above packages are installed run this command in the root directory: `streamlit run AlleyCATDashboard/pymongostream.py`
### Using Poetry:
Using poetry is much like the command for just running with python.  After performing `poetry install` in the root directory, simply run `poetry run streamlit run AlleyCATDashboard/pymongostream.py`.

Either of these commands will open up the streamlit dashboard, with internet connection, and will visualize the data given through the database accessed with the environment variables.

