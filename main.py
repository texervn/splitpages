#/bin/python3#####
##By Hanh Nguyen##
import string, math, copy
from PyPDF2 import PdfFileReader, PdfFileWriter

def split_pages(inf, outf):
	r_file = open(inf, 'rb')
	w_file = open(outf, 'wb')
	#List of exclude pages#
	#starting page = 0#
	
	input_file = PdfFileReader(r_file)
	pdf_pages = PdfFileWriter()

	for i in range(input_file.getNumPages()):
		p = input_file.getPage(i)
		#calculate the dimensions of the page#
		x1, x2 = p.mediaBox.lowerLeft
		x3, x4 = p.mediaBox.upperRight
		x1, x2 = math.floor(x1), math.floor(x2)
		x3, x4 = math.floor(x3), math.floor(x4)
		b = math.floor(x4/2)
		while True:
			
			#duplicate the current page#
			t = copy.copy(p)
			t.mediaBox = copy.copy(p.mediaBox)			
			
			t.mediaBox.upperRight = (x3, x4)
			t.mediaBox.lowerLeft = (x1, b)

			#cropping the top page#
			t.artBox = t.mediaBox
			t.bleedBox = t.mediaBox
			t.cropBox = t.mediaBox

			#adding the top page#
			pdf_pages.addPage(t)
			
			#duplicate the current page#
			r = copy.copy(p)
			r.mediaBox = copy.copy(p.mediaBox)			
			r.mediaBox.upperRight = (x3, b)
			r.mediaBox.lowerLeft = (x1, x2)

			#cropping the bottom page#
			r.artBox = r.mediaBox
			r.bleedBox = r.mediaBox
			r.cropBox = r.mediaBox
			if i>0:
				r.rotateClockwise(180)

			#adding the bottom page#
			pdf_pages.addPage(r)
			break
	
	#write the all pages#
	pdf_pages.write(w_file)
	r_file.close()
	w_file.close()

if __name__=='__main__':
	split_pages('input.pdf','output-A5.pdf')
