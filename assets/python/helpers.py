import logging, os

from bs4 import BeautifulSoup
import bs4  # for assertions


log = logging.getLogger(__name__)


def load_xml( filepath ):
    assert type(filepath) == str
    log.debug( f'filepath, ``{filepath}``' )
    assert os.path.exists( filepath )
    xml = None
    with open( filepath, encoding='utf-8' ) as f:
        xml = f.read()
    assert type(xml) == str
    soup = BeautifulSoup( xml, 'xml' )
    assert type(soup) == bs4.BeautifulSoup
    return soup
