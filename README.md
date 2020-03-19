# R<sup>2</sup> Data Labs OCR (optical character recognition)

r2dl_ocr is a python package for the digitisation of scanned documents. It is explicitly designed for complex 
documents such as engineering drawings, contracts and other documents with mixtures of tables, images, and sparse text.

r2dl_ocr harnesses optical character recognition (OCR) to recognise and 'read' text embedded in images and reconstruct 
the text in a digital format.

r2dl_ocr uses both 3rd party OCR libraries such as Tesseract, and OCR technology developed by R<sup>2</sup> Data Labs in 
house and trained explicitly on the type of documents expected in an engineering setting. 

---

## Table of Contents

See the sections below for a quick start guide. See the [Documentation](#documentation) section for detailed 
explanation of the methods contained in the library.

- [Usage](#usage)
- [Installing Package](#installing-package)
- [Installing Tesseract](#installing-tesseract)
- [Examples](#examples)
- [Contributing](#contributing)
- [FAQ](#faq)
- [Support](#support)

---
## Usage

Note that in order to run OCR on an image, you will need to install **both** the r2dl_ocr python package and the relevant
OCR model. See instructions for both below.

The directory in the below usage example should be replaced by the location of a directory with all the pdf/tiff files
needing to be converted to text.

```shell
r2dl_ocr -i dir_with_images
```

## Installing Package

Download the python wheel file for r2dl_ocr, `export.pkl` file and `map.json` file. Then install the wheel file as below.

```shell
$ pip install ${HOME}/Downloads/r2dl_ocr-0.2.0-py2.py3-none-any.whl
```
<ul>
<li>If the wheel file name of your version is different, use that name instead in the command above.</li>
<li>Check that all dependencies are installed with no errors. You may need to attempt reinstallation of a package
manually if it is not successful first time.</li>
</ul>

Make sure files `export.pkl` and `map.json` exist in the directory ~/.r2dl_ocr
```shell
$ mkdir -p ${HOME}/.r2dl_ocr
$ cp ${HOME}/Downloads/export.pkl ${HOME}/.r2dl_ocr/export.pkl
$ cp ${HOME}/Downloads/map.json ${HOME}/.r2dl_ocr/map.json
```

## Installing Tesseract
[Link to Tesseract Documentation](https://tesseract-ocr.github.io/tessdoc/Home.html).

Please see the Tesseract documentation to install tesseract and the appropriate training data for the required language.

Below are the basic steps for all main operating systems

### **Linux**
```shell
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

### **MacOS**
```shell
brew install tesseract
```
The tesseract directory can then be found using brew info tesseract, e.g. /usr/local/Cellar/tesseract/3.05.02/share/tessdata/.

### **Windows**
From Tesseract:

``
Installer for Windows for Tesseract 3.05, Tesseract 4 and development version 5.00 Alpha are available from Tesseract at UB Mannheim. These include the training tools. Both 32-bit and 64-bit installers are available.
``

``
To access tesseract-OCR from any location you may have to add the directory where the tesseract-OCR binaries are located to the Path variables, probably C:\Program Files\Tesseract-OCR.
``

Download installers from the [UB Mannheim git repo](https://github.com/UB-Mannheim/tesseract/wiki)

### Problems installing Tesseract?
Please refer to the [Tesseract Documentation](https://tesseract-ocr.github.io/tessdoc/Home.html).

## Examples
Go to [Examples Page](docs/Examples.md) for more detailed usage.

NOTE: For each OCR tool in this package to run, the appropriate model will need to be installed.

```python
from r2dl_ocr import Bulk, BulkOcr

input_dir = './r2dl_ocr/tests/files/test_input_dir'
bulk = Bulk(input_dir)
bulk.apply_function_to_each_file(BulkOcr.do_ocr_save_output)
print('done')
```

---

## Contributing

### Install r2dl_ocr from source code
Alternatively, you can install r2dl_ocr from source code by the following method

#### Clone

Clone this repo to your local machine using:
```shell
$ git clone CDS-ADC-TFS@vs-ssh.visualstudio.com:v3/CDS-ADC-TFS/Innovation%20Hub%20-%20Hunts/r2dl-ocr
```
You will need appropriate access to the Azure DevOps location.

#### Setup

Navigate to the newly created directory
```shell
$ cd r2dl-ocr
```

Now run setup from the makefile to automatically install r2dl_ocr
```shell
$ make setup
```
---

## FAQ

- **Question 1?**
    - Answer 1

---

## Support

Reach out to anybody in the London R<sup>2</sup> Data Labs Team for support. Below are some useful contacts in the team:

Muhannad Alomari

[James.Arney@Rolls-Royce.com](mailto:James.Arney@Rolls-Royce.com)

Linus Casassa

Jill Mambetova

