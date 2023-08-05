# python-lang
A simple library for building multilingual applications in Python
## Installation
### Using `pip`
`pip install python-lang`
### From the source
- Clone the repo `git clone https://github.com/Programista3/python-lang.git`
- Run `python setup.py install`
## Usage
#### `.py` file
Add pyLang to your project
```python
import python_lang as lang
_ = lang.get
```
Add language files (you can specify the language symbol as the second parameter)
```python
lang.add("C:/project/locales/de.xml")
lang.add("C:/project/locales/pl.xml", "pl")
```
Select language for translation
```python
lang.select('pl')
```
You can turn off the translation using
```python
lang.select()
```
Use `_()` function to translate text
```python
print(_("Hello World"))
```
You can view the list of added languages using
```python
lang.all()
```
#### `XML` file
Use following template:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<language code="language symbol">
  <translation text="first original text">first translated text</translation>
  <translation text="second original text">second translated text</translation>
  ...
</language>
```
## Documentation
### Functions
lang.**add(path, code=None)**<br>
&emsp;&emsp;Adds path and language code to the list of languages.<br>
&emsp;&emsp;Returns True if the language has been added successfully.<br><br>
lang.**all()**<br>
&emsp;&emsp;Returns the list of added languages<br><br>
lang.**get(text)**<br>
&emsp;&emsp;Returns translated text (if not found translation or language is not selected returns original text)<br><br>
lang.**select(lang=None)**<br>
&emsp;&emsp;Selects the language used to translation.<br>
&emsp;&emsp;Returns True if the language has been selected successfully.<br><br>
### Variables
lang.**file**<br>
&emsp;&emsp;Contains the parsed file of the currently selected language<br><br>
lang.**langs**<br>
&emsp;&emsp;Contains the list of added languages with their file paths<br><br>
lang.**selected**<br>
&emsp;&emsp;Contains the code of the currently selected language
