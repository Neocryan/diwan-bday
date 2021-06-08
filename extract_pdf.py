import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter

## Read config file
with open('/mnt/c/Users/neoc/Desktop/Untitled.csv', 'r') as r:
    a = r.readlines()

a = [x for x in a if 'pdf' in x]

# sort
a_n = [x for x in a if int(x.split('.pdf')[0]) <= 0]
a_p = [x for x in a if int(x.split('.pdf')[0]) > 0]

a = sorted(a_n, key=lambda x: -int(x.split('.pdf')[0])) + sorted(a_p, key=lambda x: int(x.split('.pdf')[0]))

pdf_writer = PdfFileWriter()
for i in a:
    name = i.split(',')[0]
    page = int(i.strip().split(',')[-1])
    pdf = PdfFileReader(f'/mnt/e/book/{name}')
    pdf_writer.addPage(pdf.getPage(page - 1))

with open('/mnt/e/book.pdf', 'wb') as out:
    pdf_writer.write(out)
