import PyPDF2
import collections

def textFromPdf(f):
    read_pdf = PyPDF2.PdfFileReader(f)
    number_of_pages = read_pdf.getNumPages()
    c = collections.Counter(range(number_of_pages))
    text=""
    for i in c:
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        text=text+" "+page_content
    return text

