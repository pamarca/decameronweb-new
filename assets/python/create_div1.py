import logging, os, pprint

from bs4 import BeautifulSoup
import bs4  # for assertions
import helpers

## load up xml-objects --------------------------
english_xml_path = os.path.abspath( '../xml/engDecameron.xml' )
italian_xml_path = os.path.abspath( '../xml/itDecameron.xml' )
english_soup = helpers.load_xml(english_xml_path)
italian_soup = helpers.load_xml(italian_xml_path)


#remove div2+children and pb from div1
def clean_div1(soup):
    for no_div2 in soup.find_all('div2'):
        no_div2.decompose()
    for pb_tag in soup.find_all('pb'):
        pb_tag.decompose()

# add speaker line
def add_speaker_line(div1_variable, soup):
    for d1t in div1_variable:
        add_speaker = soup.new_tag('p')
        add_speaker.string = '[Voice: author]'
        #d1t.insert(2, add_speaker)
        d1t.p.insert_before(add_speaker)
        add_speaker.string.wrap(soup.new_tag('h3'))
    return

# create dict of div1
def add_dict_to_div1(div1_variable):
    div1_data_info = []
    for div1_obj in div1_variable:
        assert type(div1_obj) == bs4.element.Tag
        type_attribute = div1_obj['type']
        id_attribute = div1_obj['id']
        heads = div1_obj.select('head')
        head_text = heads[0].text
        div1_truncated_text = div1_obj.text[0:100]
        dct = {
            'id': id_attribute,
            'type': type_attribute,
            'head_text': head_text,
            'div1_truncated_text': div1_truncated_text + '...'
        }
        div1_data_info.append(dct)
    return div1_data_info

#create md files of div1 with names from id containing md tags + xml text
def create_md_files(div1_results, div1_data_info, outpath, lang):
    for cc, result in enumerate(div1_results):
        filename_md = os.path.abspath('../../{}/'.format(outpath) + lang + div1_data_info[cc]['id'] + '.md')
        with open(filename_md, "w", encoding='utf-8') as file2:
            #md tags
            file2.write('---\n')
            file2.write('title: "' + div1_data_info[cc]['head_text'] +'"\n')
            file2.write('day: "' + div1_data_info[cc]['id'] + '"\n')
            file2.write('layout: "single-xml"\n')
            file2.write('---\n')

            #html structure
            html_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
            html_soup.body.append(result)
            html_output = html_soup.prettify(formatter='html')
            file2.write(html_output)
    return

div1_results_eng = english_soup.select('div1')
div1_results_it = italian_soup.select('div1')

clean_div1_eng = clean_div1(english_soup)
clean_div1__it = clean_div1(italian_soup)

div1_speaker_eng = add_speaker_line(div1_results_eng, english_soup)
div1_speaker_it = add_speaker_line(div1_results_it, italian_soup)

div1_data_info_eng = add_dict_to_div1(div1_results_eng)
div1_data_info_it = add_dict_to_div1(div1_results_it)

create_md_files(div1_results_eng, div1_data_info_eng, '_enDecameron', 'en')
create_md_files(div1_results_it, div1_data_info_it, '_itDecameron', 'it')