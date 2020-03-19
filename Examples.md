## Index

- [Extracting Text with Tesseract](#extracting-text-with-char_lib_30)
- [Extracting Text with char_lib_30](#extracting-text-with-char_lib_30)
- [Separating into Contours Before Extracting](#separating-into-contours-before-extracting)
- [Batch Processing Files](#batch-processing-files)
- [Searching for Text Embedded in Images](Searching for Text Embedded in Images)
- [See Also](#See Also)

## Extracting Text With Tesseract
Example
```python
import cv2
import os
from r2dl_ocr.ocr import OcrTesseract
path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "files")), 'test_image.png')
img = cv2.imread(path)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tocr = OcrTesseract(gray_image)
text = tocr.get_text()
print(text)
```

## Extracting Text With char_lib_30
Example
```python
import cv2
import os
from r2dl_ocr.ocr import OcrCNN
path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "files")), 'cnn_test_image.png')
img = cv2.imread(path)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cnn_ocr = OcrCNN(gray_image)
text = cnn_ocr.get_text()
print(text)
```
>HARDNESS TESTING IS NOT AN\nACCEPTANCE REQUIREMENT

## Separating into Contours Before Extracting
For dealing with images containing tables, drawings and other not text features that can confuse the OCR techniques, it
can be useful to split the image into groups of text before attempting to read it. In the case of tables the below 
method will split the text into cells first, and in the case of continuous text, the page will be split into paragraphs.

The method COcr calculates this segregation and the applies one of the standard OCR techniques (OcrCNN or OcrTesseract)
on each element. See the [COcr](../../reference/r2dl_ocr/c_ocr/) class for more details.
```python
import cv2
import os
from r2dl_ocr.c_ocr import COcr
path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "files")), 'test_image.png')
test_image = cv2.imread(path)
c_ = COcr(test_image)
text = c_.get_text_cnn()
print(len(c_.contours))
print(text)
```
>1
>
>Testing Tesseract OCR

## Batch Processing Files
The [Bulk](../../reference/r2dl_ocr/bulk_ocr/) class can be used to apply a function such as OCR, or 
indeed a complete process of converting, processing, and saving files, to a large group of input files at the same time.

The [Bulk Ocr](../../reference/r2dl_ocr/bulk_ocr/) class demonstrates this nicely, converting PDF documents to TIFF
images, extracting the text, and saving the results in a directory tree. 

A simplified version of this can be seen below. The method `apply_function_to_each_file` requires an input file
directory and a function to apply to each file in that directory. See the [Bulk](../../reference/r2dl_ocr/bulk_ocr/)
documentation for more details.

```python
from r2dl_ocr import Bulk, COcr
import os
import cv2
import re


def main():
    input_dir = os.path.realpath('./r2dl_ocr/tests/files/test_input_dir')
    bulk = Bulk(input_dir)
    bulk.apply_function_to_each_file(do_ocr_save_output)
    print('done')


def do_ocr_save_output(file_database): # file_database is the file tree object created by the bulk method before applying this function. It containds the paths to the input drectory, output directory and the auto-generated output subdirectories (for each file and each page of each file)
    for i, img_path in enumerate(os.listdir(file_database.input_by_pages_dir)): # maybe pass this from file_database instead of reading again. Would preserve order
        img_path = os.path.join(file_database.input_by_pages_dir, img_path)
        output_page_dir = os.path.join(file_database.output_by_pages_dir, str(file_database.input_file_name) + '_page_'
                                       + str(i + 1))

        contours_path = os.path.join(output_page_dir, '0_contours')
        text_tesseract_path = os.path.join(output_page_dir, '1_text_tesseract')

        os.makedirs(contours_path, exist_ok=True)
        os.makedirs(text_tesseract_path, exist_ok=True)

        img = cv2.imread(img_path)
        c_ = COcr(img)

        c_.get_text_tesseract()

        all_text_tess = ''
        spec_codes_tess = []
        for c in c_.get_contours():

            bounding_box_str = str(c.bounding_box[0]) + '_' + str(c.bounding_box[1]) + '_' + str(c.bounding_box[2]) + \
                               '_' + str(c.bounding_box[3])

            # save contour
            cv2.imwrite(os.path.join(contours_path, bounding_box_str + '.tiff'), c.img)

            # save tesseract text
            with open(os.path.join(text_tesseract_path, bounding_box_str + '.txt'), 'w') as f:
                f.write(c.text_tesseract)


            all_text_tess += c.text_tesseract + '\n'

        with open(os.path.join(output_page_dir, 'all_text_tess.txt'), 'w') as f:
            f.write(all_text_tess)


if __name__ == '__main__':
    main()
```

## See Also
- [More Docs](moredocs.md)
- [Functional Diagram](R2DL_OCR_Functional_Diagram.html)