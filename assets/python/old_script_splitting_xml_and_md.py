import os, pprint

from bs4 import BeautifulSoup
import bs4  # for assertions
import helpers

## load up xml-objects --------------------------
english_xml_path = os.path.abspath( '../xml/source_files/engDecameron.xml' )
italian_xml_path = os.path.abspath( '../xml/source_files/itDecameron.xml' )
english_soup = helpers.load_xml( english_xml_path )
assert type(english_soup) == bs4.BeautifulSoup
italian_soup = helpers.load_xml( italian_xml_path )
assert type(italian_soup) == bs4.BeautifulSoup



## find all <div2> elements & store dct info for both texts----
def add_dict_to_div2(div2_variable):
    div2_data_info = []
    for div2_obj in div2_variable:
        assert type(div2_obj) == bs4.element.Tag
        type_attribute = div2_obj['type']
        try:
            who = div2_obj['who']
        except:
            who = 'None'
        id_attribute = div2_obj['id']
        heads = div2_obj.select('head')
        head_text = heads[0].text
        div2_truncated_text = div2_obj.text[0:100]
        dct = {
            'id': id_attribute,
            'type': type_attribute,
            'who': who,
            'head_text': head_text,
            'div2_truncated_text': div2_truncated_text + '...'
        }
        div2_data_info.append(dct)
    return div2_data_info

# write separate xml files for each div2
def separate_novella(div2_results, div2_data_info, outpath):
    for cc, result in enumerate(div2_results):
        filename_xml = os.path.abspath('../xml/{}/'.format(outpath) + div2_data_info[cc]['id'] + '.xml')
        with open(filename_xml, "w") as file:
            file.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<TEI xmlns="http://www.tei-c.org/ns/1.0>\n')
            file.write(str(result))
            file.write('\n</TEI>')
    return

# write separate md files for each div2
def create_md_files(div2_results, div2_data_info, outpath, xmlpath):
    for cc, result in enumerate(div2_results):
        filename_md = os.path.abspath('../../{}/'.format(outpath) + div2_data_info[cc]['id'] + '.md')
        with open(filename_md, "w") as file2:
            file2.write('---\n')
            file2.write('title: "' + div2_data_info[cc]['head_text'] + '"\n')
            file2.write('permalink: "/' + xmlpath + '/' + div2_data_info[cc]['id'] + '/"\n')
            file2.write('day: "' + div2_data_info[cc]['id'] + '"\n')
            file2.write('plant-xml: "/assets/xml/' + xmlpath + '/' + div2_data_info[cc]['id'] + '.xml"\n')
            file2.write('layout: "single-xml"\n')
            file2.write('---\n')
    return

# parse div2
div2_results_eng = english_soup.select( 'div2' )
div2_results_it = italian_soup.select('div2')

# parse div1
#div1_results_eng = english_soup.select('div1')
#div1_results_it = italian_soup.select('div1')

# give results for div2
div2_data_info_eng = add_dict_to_div2(div2_results_eng)
div2_data_info_it = add_dict_to_div2(div2_results_it)

# create xml files
separate_novella(div2_results_eng, div2_data_info_eng, 'enDecameron')
separate_novella(div2_results_it, div2_data_info_it, 'itDecameron')

# create md files
create_md_files(div2_results_eng, div2_data_info_eng, '_enDecameron', 'enDecameron')
create_md_files(div2_results_it, div2_data_info_it, '_itDecameron', 'itDecameron')

