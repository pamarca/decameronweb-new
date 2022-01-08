import logging, os, pprint

from bs4 import BeautifulSoup
import bs4  # for assertions
import helpers

## load up xml-objects --------------------------
english_xml_path = os.path.abspath( '../xml/engDecameron.xml' )
italian_xml_path = os.path.abspath( '../xml/itDecameron.xml' )
english_soup = helpers.load_xml(english_xml_path)
italian_soup = helpers.load_xml(italian_xml_path)

# add speaker line
def add_speaker_line(soup):
    sp_tag = soup.find('prologue')
    sp_tag2 = soup.find('epilogue')
    add_speaker = soup.new_tag('p')
    add_speaker.string = '[Voice: author]'
    #sp_tag.insert(2, add_speaker)
    sp_tag.p.insert_before(add_speaker)
    sp_tag2.p.insert_before(add_speaker)
    add_speaker.string.wrap(soup.new_tag('h3'))
    return

#create prologue md file
def prologue_md_file(soup, outpath, lang):
    prologue = soup.find('prologue')
    prologue_md = os.path.abspath('../../{}/'.format(outpath) + lang + prologue['id'] + '.md')
    #pretty_prologue = soup.front.prettify()
    with open(prologue_md, "w", encoding='utf-8') as file2:
            #md tags
            file2.write('---\n')
            file2.write('title: Proem' + '\n')
            file2.write('day: "' + prologue['id'] + '"\n')
            file2.write('layout: "single-xml"\n')
            file2.write('---\n')

            #html structure
            html_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
            html_soup.body.append(prologue)
            html_output = html_soup.prettify(formatter='html')
            file2.write(html_output)
    return

#create epilogue md file
def epilogue_md_file(soup, outpath, lang):
    epilogue = soup.find('epilogue')
    trailer = soup.find('trailer')
    epilogue_md = os.path.abspath('../../{}/'.format(outpath) + lang + epilogue['id'] + '.md')
    #pretty_prologue = soup.front.prettify()
    with open(epilogue_md, "w", encoding='utf-8') as file2:
            #md tags
            file2.write('---\n')
            file2.write('title: Epilogue' + '\n')
            file2.write('day: "' + epilogue['id'] + '"\n')
            file2.write('layout: "single-xml"\n')
            file2.write('---\n')

            #html structure
            html_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
            html_soup.body.append(epilogue)
            html_soup.body.append(trailer)
            html_output = html_soup.prettify(formatter='html')
            file2.write(html_output)
    return


speaker_eng = add_speaker_line(english_soup)
speaker_it = add_speaker_line(italian_soup)

prologue_md_eng = prologue_md_file(english_soup, '_enDecameron', 'en')
prologue_md_it = prologue_md_file(italian_soup, '_itDecameron', 'it')

epilogue_md_eng = epilogue_md_file(english_soup, '_enDecameron', 'en')
epilogue_md_it = epilogue_md_file(italian_soup, '_itDecameron', 'it')

# #print epilogue
# english_epilogue = english_soup.epilogue.prettify()
# english_trailer = english_soup.trailer.prettify()
#
# epilogue_path = os.path.abspath( './output_files/epilogue.txt' )
# with open(epilogue_path, 'w') as f:
#     f.write(str(english_epilogue))
#     f.write(str(english_trailer))
