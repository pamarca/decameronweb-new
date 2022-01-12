import os, pprint

from bs4 import BeautifulSoup, Comment
import bs4  # for assertions
import helpers

## load up xml-objects --------------------------
english_xml_path = os.path.abspath( '../xml/engDecameron.xml' )
italian_xml_path = os.path.abspath( '../xml/itDecameron.xml' )
english_soup = helpers.load_xml(english_xml_path)
italian_soup = helpers.load_xml(italian_xml_path)

#remove div2+children and pb from div1
def clean_div2(soup):
    #remove pb
    for pb_tag in soup.find_all('pb'):
        pb_tag.decompose()

    #remove comments
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    #changing milestones
    milestones = soup.find_all('milestone')
    for milestone in milestones:
        try:
            mstone_id = milestone['id']
        except:
            mstone_id = 'None'

        milestone.name = "a"
        milestone['name'] = mstone_id
        milestone.string = '[' + mstone_id[-3:] + ']'
        del milestone['id']

    #change div1 into div
    for div_tag in soup.find_all('div2'):
        div_tag.name = 'div'

    #change <title></title> to <i><i>
    title_tags = soup.select('title')
    for title_tag in title_tags:
        title_tag.name = "i"

# adding speaker line
def add_speaker_line(div2_variable, soup):
    for d2t in div2_variable:
        speaker = d2t['who']

        add_speaker = soup.new_tag('p')
        add_speaker.string = '[Voice: ' + speaker + ']'
        #d2t.insert(2, add_speaker)
        d2t.head.insert_after(add_speaker)
        add_speaker.string.wrap(soup.new_tag('h2'))
    return

#create dict
def add_dict_to_div2(div2_variable):
    div2_data_info = []
    for div2_obj in div2_variable:
        assert type(div2_obj) == bs4.element.Tag
        type_attribute = div2_obj['type']
        who = div2_obj['who']
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
def create_md_files(div2_results, div2_data_info, outpath, lang):
    for cc, result in enumerate(div2_results):
        filename_md = os.path.abspath('../../{}/'.format(outpath) + lang + div2_data_info[cc]['id'] + '.md')
        with open(filename_md, "w", encoding='utf-8') as file2:
            #md tags
            file2.write('---\n')
            file2.write('title: "' + div2_data_info[cc]['head_text'] +'"\n')
            file2.write('day: "' + lang + div2_data_info[cc]['id'] + '"\n')
            file2.write('layout: "single"\n')
            file2.write('---\n')

            #html structure
            html_soup = BeautifulSoup('', 'html.parser')
            html_soup.append(result)

            # change head tag to h1
            div_head = html_soup.find_all('head')
            for head_tag in div_head:
                head_tag.name = "h1"

            #outputting html
            html_output = html_soup.prettify(formatter='html')
            file2.write(html_output)
    return

div2_results_eng = english_soup.select('div2')
div2_results_it = italian_soup.select('div2')

clean_div2_eng = clean_div2(english_soup)
clean_div2_it = clean_div2(italian_soup)

div2_speaker_eng = add_speaker_line(div2_results_eng, english_soup)
div2_speaker_it = add_speaker_line(div2_results_it, italian_soup)

div2_data_info_eng = add_dict_to_div2(div2_results_eng)
div2_data_info_it = add_dict_to_div2(div2_results_it)

create_md_files(div2_results_eng, div2_data_info_eng, '_enDecameron', 'en')
create_md_files(div2_results_it, div2_data_info_it, '_itDecameron', 'it')

# with open(english_xml_path, 'r') as md_file:
#     content = md_file.read()
#
#     soup = BeautifulSoup(content, 'lxml')
#     div2_tags = soup.div2
#     div2_tags.name = 'div'
