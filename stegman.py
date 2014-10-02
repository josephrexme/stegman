#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Joseph Rex
# @blog: http://josephrex.me
# @twitter: @joerex101
# http://resources.infosecinstitute.com
import sys, re, binascii, string

def gethex(image):
	f = open(image, 'rb')
	data = f.read()
	f.close()
	hexcode = binascii.hexlify(data)
	return hexcode
def embed(embedFile, coverFile, stegFile):
	filetype = coverFile[-3:]
	stegtype = stegFile[-3:]
	if filetype != 'png' and filetype != 'jpg':
		print 'Invalid format'
	elif filetype != stegtype:
		print 'Output file has to be in the same format as cover image (%s)' % string.swapcase(filetype)
	else:
		data = open(embedFile, 'r').read()
		info = gethex(coverFile)
		if extradatacheck(info, filetype):
			print 'File already contains embedded data'
		else:
			info += data.encode('hex')
			f = open(stegFile, 'w')
			f.write(binascii.unhexlify(info))
			f.close()
			print 'Storing data to', stegFile
def extract(stegFile, outFile):
	filetype = stegFile[-3:]
	data = gethex(stegFile)
	if extradatacheck(data, filetype):
		store = open(outFile, 'w')
		store.write( binascii.unhexlify(extradatacheck(data, filetype)) )
		store.close()
		print 'Extracted data stored to', outFile
	else:
		print 'File has no embedded data in it'
def extradatacheck(data, type):
	if type == 'png':
		pattern = r'(?<=426082)(.*)'
	elif type == 'jpg':
		pattern == r'(?<=FFD9)(.*)'
	match = re.search(pattern, data)
	if match:
		return match.group(0)
	else:
		false
def usage():
	print """
Usage:
Embeding
stegman -s embedfile.txt coverfile.jpg output.jpg

Extracting
stegman -e stegfile.jpg output.txt

Valid Formats:
JPG, PNG
	"""
def args():
	if sys.argv[1] == '-s':
		embed(sys.argv[2], sys.argv[3], sys.argv[4])
	elif sys.argv[1] == '-e':
		extract(sys.argv[2], sys.argv[3])
	else:
		usage()
def main():
	if len(sys.argv) > 1:
		args()
	else:
		usage()

if __name__ == '__main__':
	main()