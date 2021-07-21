# Funimals
This is an API which serves fun animal facts.
## Core Requirements
To use this, you'll need:
* ****Python 3.8**** or higher
* ****pip**** package manager
## Installation
```bash
git clone https://github.com/k-cichorski/Funimals
```
Go to project directory and create a virtual environment:
```bash
cd Funimals
python -m venv venv
```
then activate it: \
****Unix/macOS****
```bash
source venv/bin/activate
```
****Windows****
```bash
.\venv\Scripts\activate
```
and install all required packages:
```bash
pip install -r requirements.txt
```
## Configuration
Remove ****.example**** from ****.env.example**** filename, and fill out the fields.
```bash
GOOGLE_APPLICATION_CREDENTIALS=String
```
This variable should be a path to Google API's ****authorization_key.json**** (required only for translations).
## Usage
Go to project directory, activate the virtual environment and start the app: \
****Unix/macOS****
```bash
source venv/bin/activate
python app.py
```
****Windows****
```bash
.\venv\Scripts\activate
python app.py
```
or use the ****launch.bat**** file by double-clicking it, or through cmd:
```bash
call launch.bat
```
and make a GET request to the ****link**** printed to the console (e.g ****http://localhost:5000/****). You might have to scroll up a little bit :)
## Request Arguments
****amount**** (****required****) \
specifies how many facts will be returned. Has to be in range of 1-500 (1000 if ****useAltFactSrc**** is ****True****).

****animal**** \
specifies which animal the facts will be about. Currently, the only acceptable value is 'cat'. Defaults to 'cat'.

****sendTo**** \
specifies an email address to which first 10 facts will be sent as a CSV file.

****translateTo**** \
specifies a language which the facts will be translated to. Has to be an ISO-639-1 Code, e.g. 'es'.

****useAltFactSrc**** \
if ****True****, an alternate fact source will be used. If ****False**** and main fact source fails to respond, a redirect will be called with this argument set to ****True****.