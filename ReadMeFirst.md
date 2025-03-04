Python 3.13.1 is quite new and might not be fully compatible with all libraries, especially pdfminer.six and spacy. I recommend downgrading to Python 3.10 or 3.11 for better compatibility.


> python3 -m venv virt1 # Ignore


> brew install python@3.11
> python3.11 -m venv virt1  # Replace "python3.11" with your installed version
> source virt1/bin/activate
> deactivate

> python3 --version # check current version
> pip install -r requirements.txt


> 1.Open Command Palette (Cmd + Shift + P).
> 2.Search for "Python: Select Interpreter" and click it. /Users/ThanhNguyen/PythonWS/NLP/OCR_Process/virt1/bin/python
> 3.Look for an interpreter inside your project,
> 4.Select it.


> python -m spacy download en_core_web_sm # install missing model



> brew uninstall --ignore-dependencies tcl-tk
> brew install tcl-tk
> brew uninstall --ignore-dependencies python@3.11
> brew install python@3.11


> pip3.11 install <package>
> brew install python-tk@3.11


> data/output/sample_json_to_view.json
> data/output/esg_cleaned_data_v2.json


--no-cache-dir