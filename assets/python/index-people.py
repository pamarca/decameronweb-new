import logging, os, pprint

from bs4 import BeautifulSoup
import bs4  # for assertions
import helpers

## load up xml-objects --------------------------
english_xml_path = os.path.abspath( '../xml/engDecameron.xml' )
italian_xml_path = os.path.abspath( '../xml/itDecameron.xml' )
english_soup = helpers.load_xml(english_xml_path)
italian_soup = helpers.load_xml(italian_xml_path)

#create index page for people
html_soup = BeautifulSoup('', 'html.parser')
for people in italian_soup.particDesc.find_all('person'):
    rel_tag = people.rel
    disguise_tag = people.disguise

    #create each entry
    for entry in people:
        item_soup = BeautifulSoup('<div></div>', 'html.parser')
        p_name_tag = item_soup.new_tag('p')
        item_soup.div.append(p_name_tag)
        a_name_tag = item_soup.new_tag('a')
        a_name_tag['id'] = people['id']
        try:
            a_name_tag['brigata'] = people['brigata']
        except:
            pass
        try:
            a_name_tag['religion'] = people['religion']
        except:
            pass
        try:
            a_name_tag['sex'] = people['sex']
        except:
            pass
        try:
            a_name_tag['age'] = people['age']
        except:
            pass
        try:
            a_name_tag['role'] = people['role']
        except:
            pass
        try:
            a_name_tag['status'] = people['status']
        except:
            pass
        try:
            a_name_tag['condition'] = people['condition']
        except:
            pass
        try:
            a_name_tag['estate'] = people['estate']
        except:
            pass
        try:
            a_name_tag['origin'] = people['origin']
        except:
            pass
        item_soup.p.append(a_name_tag)
        a_name_tag.string = people.text
        try:
            item_soup.a.append(rel_tag)
        except:
            pass
        try:
            item_soup.a.append(disguise_tag)
        except:
            pass

        hr_tag = item_soup.new_tag('hr')
        item_soup.div.append(hr_tag)

        html_soup.append(item_soup)

html_output = html_soup.prettify(formatter='html')

index_people = os.path.abspath('../../_pages/index_people.md')
with open(index_people, "w", encoding='utf-8') as f:
    # md tags
    f.write('---\n')
    f.write('layout: "single"\n')
    f.write('permalink: /index_people/' + '\n')
    f.write('title: "Index of People"' + '\n')
    f.write('---\n')
    f.write(html_output)

#finding people in the text
div2_person_tag = italian_soup.find_all('name', {"type" : "person"})
