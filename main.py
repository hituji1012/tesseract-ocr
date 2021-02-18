from tesseract_ocr import render_doc_text

if __name__ == '__main__':
    # OCR検知
    data_list = render_doc_text('sample.png')
    print(','.join(data_list))
