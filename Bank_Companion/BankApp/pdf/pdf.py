from PyPDF2 import PdfFileReader

def textFromPdf(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
        text=""
        page = pdf.getPage(0)
        print(page.extractText())

    return text

print(textFromPdf("pdf.pdf"))
