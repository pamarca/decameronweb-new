import logging, os, pprint

from bs4 import BeautifulSoup, Comment
import bs4  # for assertions
import helpers

## load up xml-objects --------------------------
english_xml_path = os.path.abspath( '../xml/engDecameron.xml' )
italian_xml_path = os.path.abspath( '../xml/itDecameron.xml' )
english_soup = helpers.load_xml(english_xml_path)
italian_soup = helpers.load_xml(italian_xml_path)

#remove div2+children and pb from div1
def clean_div(soup):
    #remove pb
    for pb_tag in soup.find_all('pb'):
        pb_tag.decompose()

    #remove comments
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    #changing milestones
    # milestones = soup.select('milestone')
    # for milestone in milestones:
    #     try:
    #         mstone_id = milestone['id']
    #     except:
    #         mstone_id = 'None'
    #
    #     milestone.name = "a"
    #     milestone['name'] = mstone_id
    #     milestone.string = '[' + mstone_id[-3:] + ']'
    #     del milestone['id']

    # change head tag to h1
    div_head = soup.select('head')
    for head_tag in div_head:
        head_tag.name = "h1"

    #change <title></title> to <i><i>
    title_tags = soup.select('title')
    for title_tag in title_tags:
        title_tag.name = "i"

# add speaker line
def add_speaker_line(soup):
    #add speaker to proem
    sp_tag_prol = soup.find('prologue')
    add_speaker_prol = soup.new_tag('p')
    add_speaker_prol.string = '[Voice: author]'
    #sp_tag_prol.insert(1, add_speaker_prol)
    sp_tag_prol.h1.insert_after(add_speaker_prol)
    add_speaker_prol.string.wrap(soup.new_tag('h2'))

    #add speaker to epologue
    sp_tag_epil = soup.find('epilogue')
    add_speaker_epil = soup.new_tag('p')
    add_speaker_epil.string = '[Voice: author]'
    sp_tag_epil.h1.insert_after(add_speaker_epil)
    #sp_tag_epil.p.insert_before(add_speaker_epil)
    add_speaker_epil.string.wrap(soup.new_tag('h2'))

    return

#create prologue md file
def prologue_md_file(soup, outpath, mstone_dir):
    front = soup.find('front')
    front.name = "div"
    prologue = soup.find('prologue')
    prologue.name = "div"
    #prologue.string = "Proem"
    prologue_md = os.path.abspath('../../{}/'.format(outpath) + prologue['id'] + '.md')
    #pretty_prologue = soup.front.prettify()
    with open(prologue_md, "w", encoding='utf-8') as file2:
            #md tags
            file2.write('---\n')
            file2.write('title: Proem' + '\n')
            file2.write('day: "' + prologue['id'] + '"\n')
            file2.write('layout: "single"\n')
            file2.write('---\n')

            #html structure
            html_soup = BeautifulSoup('', 'html.parser')
            html_soup.append(front)
            html_soup.append(prologue)

            # changing milestones
            milestones = html_soup.select('milestone')
            for milestone in milestones:
                try:
                    mstone_id = milestone['id']
                except:
                    mstone_id = 'None'

                milestone.name = "a"
                milestone['href'] = '{{ site.baseurl }}' + mstone_dir + '/' + 'proem' + '#' + mstone_id
                milestone.string = '[' + mstone_id[-3:] + ']'
                #del milestone['id']

            html_output = html_soup.prettify(formatter='html')
            file2.write(html_output)
    return

#create epilogue md file
def epilogue_md_file(soup, outpath, mstone_dir):
    epilogue = soup.find('epilogue')
    epilogue.name = "div"
    trailer = soup.find('trailer')
    trailer.name = "div"
    epilogue_md = os.path.abspath('../../{}/'.format(outpath) + epilogue['id'] + '.md')
    #pretty_prologue = soup.front.prettify()
    with open(epilogue_md, "w", encoding='utf-8') as file2:
            #md tags
            file2.write('---\n')
            file2.write('title: Epilogue' + '\n')
            file2.write('day: "' + epilogue['id'] + '"\n')
            file2.write('layout: "single"\n')
            file2.write('---\n')

            #html structure
            html_soup = BeautifulSoup('', 'html.parser')
            html_soup.append(epilogue)
            html_soup.append(trailer)

            # changing milestones
            milestones = html_soup.select('milestone')
            for milestone in milestones:
                try:
                    mstone_id = milestone['id']
                except:
                    mstone_id = 'None'

                milestone.name = "a"
                milestone['href'] = '{{ site.baseurl }}' + mstone_dir + '/' + 'epilogue' + '#' + mstone_id
                milestone.string = '[' + mstone_id[-3:] + ']'

            html_output = html_soup.prettify(formatter='html')
            file2.write(html_output)
    return

clean_div_eng = clean_div(english_soup)
clean_div_it = clean_div(italian_soup)

speaker_eng = add_speaker_line(english_soup)
speaker_it = add_speaker_line(italian_soup)

prologue_md_eng = prologue_md_file(english_soup, '_enDecameron', 'itDecameron')
prologue_md_it = prologue_md_file(italian_soup, '_itDecameron', 'enDecameron')

epilogue_md_eng = epilogue_md_file(english_soup, '_enDecameron', 'itDecameron')
epilogue_md_it = epilogue_md_file(italian_soup, '_itDecameron', 'enDecameron')

# #print epilogue
# english_epilogue = english_soup.epilogue.prettify()
# english_trailer = english_soup.trailer.prettify()
#
# epilogue_path = os.path.abspath( './output_files/epilogue.txt' )
# with open(epilogue_path, 'w') as f:
#     f.write(str(english_epilogue))
#     f.write(str(english_trailer))
