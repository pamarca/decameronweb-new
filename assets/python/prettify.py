import os, pprint
import glob
from bs4 import BeautifulSoup
import bs4  # for assertions
import helpers

for xml_file in glob.glob('../xml/enDecameron/*.xml'):
    bs = BeautifulSoup(open(xml_file), 'xml')
    pretty = bs.prettify()

    pretty_xml = open(xml_file, 'w')
    pretty_xml.write(pretty)
    pretty_xml.close()

for xml_file in glob.glob('../xml/itDecameron/*.xml'):
    bs = BeautifulSoup(open(xml_file), 'xml')
    pretty = bs.prettify()

    pretty_xml = open(xml_file, 'w')
    pretty_xml.write(pretty)
    pretty_xml.close()

#bs = BeautifulSoup(open('output_files/prettyEng/d01conclu.xml'), 'xml')
#print(bs.prettify())