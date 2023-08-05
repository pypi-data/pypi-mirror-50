import PyPDF2


def extract_text(pdf_file_name):
    '''Extract text contents from a PDF file'''

    with  open(pdf_file_name, 'rb') as infile:
        pdfFileObj = infile.read()

    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    full_text = ''

    for page_number in range(0, pdfReader.numPages):
        new_page_text = pdfReader.getPage(page_number).extractText()
        full_text = full_text +  '\n' + new_page_text
    return full_text
