#def	__pdf2png1(self, src_path, thumb_template, pages):
#	for page in range(pages, 10):
#		img = Wand_Image(filename = src_path + '[%d]' % page, resolution=(150,150))
#		#print img.size
#		if (img.colorspace != 'gray'):
#			img.colorspace = 'gray'		# 'grey' as for bw as for grey (COLORSPACE_TYPES)
#		img.format = 'png'
#		#img.resolution = (300, 300)
#		img.save(filename = thumb_template % page)
