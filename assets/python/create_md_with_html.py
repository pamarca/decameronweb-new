import logging, os, pprint

from bs4 import BeautifulSoup
import bs4  # for assertions
import helpers

## load up xml-objects --------------------------
english_xml_path = os.path.abspath( './source_xml_files/engDecameron.xml' )
italian_xml_path = os.path.abspath( './source_xml_files/itDecameron.xml' )
english_soup = helpers.load_xml( english_xml_path )
italian_soup = helpers.load_xml( italian_xml_path )

#changing div2 into 'div'
divs_eng = english_soup.find_all('div2')
for div_eng in divs_eng:
    div_eng.name = 'div'
divs_it = italian_soup.find_all('div2')
for div_it in divs_it:
    div_it.name = 'div'

#create dict
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

#create md files with names from id containing md tags + xml text
def create_md_files(div2_results, div2_data_info, outpath):
    for cc, result in enumerate(div2_results):
        filename_md = os.path.abspath('./output_files/{}/'.format(outpath) + div2_data_info[cc]['id'] + '.md')
        with open(filename_md, "w", encoding='utf-8') as file2:
            file2.write('---\n')
            file2.write('title: "' + div2_data_info[cc]['head_text'] +'"\n')
            file2.write('day: "' + div2_data_info[cc]['id'] + '"\n')
            file2.write('layout: "single-xml"\n')
            file2.write('---\n')
            html_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
            html_soup.body.append(result)
            html_output = html_soup.prettify(formatter='html')
            file2.write(html_output)
    return



div2_results_eng = english_soup.select('div')
div2_results_it = italian_soup.select('div')

div2_data_info_eng = add_dict_to_div2(div2_results_eng)
div2_data_info_it = add_dict_to_div2(div2_results_it)

create_md_files(div2_results_eng, div2_data_info_eng, 'engDecameron_md')
create_md_files(div2_results_it, div2_data_info_it, 'itDecameron_md')


