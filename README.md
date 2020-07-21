# Autocomplete-Server

To start the server run server.py. It should automatically create the data model and run locally on port 13000. Requests can be made using the following syntax:
  `curl http://localhost:13000/autocomplete?query=What+is+y&max_results=5`.
Alternatively, you can access the web interface for completions by visiting <http://localhost:13000/> from a browser after starting the server or directly running autocomplete.py and inputting prefixes through the console.

Unit tests for model.py and autocomplete.py can be ran using the files testModel.py and testAutocomplete.py in the 'tests' folder.

The code requires the following Python packages:
  - Pandas
  - NLTK
  - Flask
  - Pickle

And it also requires data from NLTK which can be obtained by running `nltk.download()` from a Python console after installing the package.
