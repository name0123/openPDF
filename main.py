# -*- coding: utf-8 -*-
import pdfquery

filename = 'ProyectoEncuestas//SLDS_Project_Questions_Highlighted.pdf'
pdf = pdfquery.PDFQuery(filename)
pdf.load()
print('loaded ' + filename)

pdf.tree.write("test.xml", pretty_print=True, encoding="utf-8")
