import random
import re
import xml.etree.ElementTree as et
from lxml.etree import _Element # pylint: disable=no-name-in-module
import lxml.etree as ET
from typing import List

from markdown.core import Markdown
from markdown.extensions import Extension
# from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor


def preprocess_md(md: str):
    md = md.replace('-\n', '')
    md = md.replace('[', '~~')
    md = md.replace(']', '~~')
    return md

def postprocess_markup(markup: str):
    markup = re.sub(r'\.\.\.+', '<text xml:lang="grc"><body>', markup)

    # wrap transcription in div book tags
    book_match = re.search(r'<h4>[^<h4>]+</h4>', markup).group(0)
    book = book_match.replace('<h4>', '')
    book = book.replace('</h4>', '')
    book = nt_to_igntp[book]
    book_elem = f'<div type="book" n="{book}">\n'
    markup = markup.replace(book_match, book_elem)

    # wrap chapter section in div tags
    chapter_match = re.search(r'<h5>[^<h5>]+</h5>', markup).group(0)
    chapter = chapter_match.replace('<h5>', '')
    chapter = chapter.replace('</h5>', '')
    chapter_elem = f'<div type="chapter" n="{book}K{chapter}">'
    markup = markup.replace(chapter_match, chapter_elem)

    for x in html_to_tei:
        markup = markup.replace(x[0], x[1])
    markup = f'''<!DOCTYPE TEI><?xml-stylesheet type="text/xsl" href="IGNTP-Rom.xsl"?>
             <TEI xmlns="http://www.tei-c.org/ns/1.0">{markup}</body></text></TEI>'''

    return markup

def postprocess_xml(root: _Element):
    tei_ns = 'http://www.tei-c.org/ns/1.0'
    xml_ns = 'http://www.w3.org/XML/1998/namespace'
    comms = root.xpath(f'//tei:comm', namespaces={'tei': tei_ns}) # type: List[_Element]
    verse_units = root.xpath(f'//tei:ab', namespaces={'tei': tei_ns}) # type: List[_Element]

    # convert abbreviated commentary tags into full TEI compatible elements
    for comm in comms:
        if comm.get('lines'):
            index = comm.getparent().index(comm)
            try:
                lines = int(comm.get('lines'))
            except:
                lines = 1
            for _ in range(lines):
                parent = comm.getparent() #type: _Element
                comm_element = ET.Element('note', type='commentary', nsmap={None: tei_ns, 'xml': xml_ns})
                comm_element.text = 'One line of untranscribed commentary text'
                lb = ET.Element('lb', nsmap={None: tei_ns, 'xml': xml_ns})
                parent.insert(index, lb)
                parent.insert(index+1, comm_element)
            comm.getparent().remove(comm)
        else:
            comm.tag = 'note'
            comm.attrib['type'] = 'commentary'
            comm.text = 'untranscribed commentary text'
    
    # convert abbreviated verse units attributes n="4" to IGNTP ref n="B06K13V4"
    for v in verse_units: #type: _Element
        v.attrib['n'] = f'{v.getparent().get("n")}V{v.get("n")}'

    return root

class TokenizeText(Preprocessor):
    """ wrap individual words in <w> tags """
    def rando_str(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        random_list = [random.choice(chars) for _ in range(5)]
        return ''.join(random_list)

    def tokenize_text(self, text: str):
        breaks_in_word = re.findall(r'<lb[^<>]*/>', text)
        user_markups = re.findall(r'{[^{}]+}', text)
        markups = re.findall(r'<[^<>]+>', text)
        notes = re.findall(r'\*[^*]+\*', text)

        replacements = []
        randos = ['|']
        for m in user_markups:
            rando = self.rando_str()
            text = text.replace(m, f'{rando} ')
            replacements.append((m, rando))
            randos.append(rando)

        for brk in breaks_in_word:
            rando = self.rando_str()
            text = text.replace(brk, f'{rando}')
            replacements.append((brk, rando))
            randos.append(rando)
            
        for a in markups:
            rando = self.rando_str()
            text = text.replace(a, f' {rando} ')
            replacements.append((a, f'{rando}'))
            randos.append(rando)

        for z in notes:
            rando = self.rando_str()
            text = text.replace(z, f'{rando}')
            replacements.append((z, f'{rando}'))
            randos.append(rando)

        new_text = []
        for word in text.split():
            if word not in randos and not word.startswith('*') and not word.startswith('+'):
                # text = text.replace(f'{word}', f' <w>{word.strip()}</w> ')
                word = word.replace(word, f'<w>{word}</w>')
            new_text.append(word)
        text = ''.join(new_text)
        for r in replacements:
            text = text.replace(r[1], r[0])
        return text

    def run(self, lines: list):
        new_lines = []
        for line in lines:
            if line.startswith('#') or line.startswith('...') or line.startswith('>'):
                new_lines.append(line)
            else:
                new_line = self.tokenize_text(line)
                new_lines.append(new_line)
        return new_lines

class RestructureTree(Treeprocessor):
    def create_elements(self):
        return (
            et.Element('teiHeader'),
            et.Element('fileDesc'),
            et.Element('titleStmt'),
            et.Element('respStmt'),
            et.Element('name'),
            et.Element('resp')
        )
    def remove_elements(self, root, elements_to_remove: tuple):
        for elem in elements_to_remove:
            root.remove(elem)
    def get_header_info(self, root):
        return (
            root.find('h1'),
            root.find('h2'),
            root.find('h3'),
        )
    def build_tei_header(self, root, tei_header, file_desc, title_statement, resp_statement, name, resp):
        title, person, date = self.get_header_info(root)
        root.insert(0, tei_header)
        tei_header.append(file_desc)
        file_desc.append(title_statement)
        title_statement.append(title)
        title_statement.append(resp_statement)
        resp_statement.append(resp)
        resp_statement.append(name)
        title.attrib = {'type': 'document'}
        name.text = person.text
        name.attrib = {'type': 'person'}
        resp.text = 'Transcribed by'
        resp.attrib = {'date': date.text}
        self.remove_elements(root, (title, date, person))

    def add_page_break_type(self, root):
        for pb in root.findall('pb'):
            pb.attrib = {'type': 'folio'}

    def run(self, root: et.Element):
        (tei_header, file_desc, title_statement, resp_statement, 
         name, resp) = self.create_elements()
        self.build_tei_header(root, tei_header, file_desc, title_statement, 
                              resp_statement, name, resp)         
        self.add_page_break_type(root)


# class TEIPost(Postprocessor):
#     """ Change tags to be TEI compliant """
#     def run(self, text):
#         text = re.sub(r'\.\.\.+', '<text xml:lang="grc"><body>', text)
#         for x in html_to_tei:
#             text = text.replace(x[0], x[1])
#         return f'<!DOCTYPE TEI><?xml-stylesheet type="text/xsl" href="IGNTP-Rom.xsl"?><TEI xmlns="http://www.tei-c.org/ns/1.0">{text}</body></text></TEI>'

class TEI(Extension):
    def extendMarkdown(self, md: Markdown, key="TEI", index=200):
        # md.postprocessors.register(TEIPost(), key, index)
        md.treeprocessors.register(RestructureTree(md), 'RestructureTree', 200)
        md.preprocessors.register(TokenizeText(md), 'tokenize', 200)


html_to_tei = (
    ('<h1', '<title'),
    ('</h1>', '</title>'),
    ('<h2', '<respStmt'),
    ('</h2>', '</respStmt>'),
    ('<code', '<unclear'),
    ('</code>', '</unclear>'),
    ('·', '<pc>·</pc>'),
    ('date', 'when-iso'),
    ('<v', '<ab'),
    ('</v>', '</ab>'),
    ('<p>', ''),
    ('</p>', ''),
    ('<p/>', ''),
    ('<h4/>', '</div>'),
    ('<h4></h4>', '</div>'),
    ('<h5/>', '</div>'),
    ('<h5></h5>', '</div>'),
    ('<strong', '<seg type="margin" '),
    ('</strong>', '</seg>'),
    ('<del>', '<supplied>'),
    ('</del>', '</supplied>'),
    ('<em', '<note type="local"'),
    ('</em>', '</note>'),
    ('<ins>', '<app><rdg type="orig" hand="firsthand">'),
    ('|', '</rdg><rdg type="corr" hand="corrector">'),
    ('</ins>', '</rdg></app>'),
)

# TODO: complete for at least the 27 NT books
nt_to_igntp = {
    'Romans': 'B06',
    'Rom': 'B06',
    'B06': 'B06',
    '1Cor': 'B07',
    '2Cor': 'B08',
    '1 Corinthians': 'B07',
    '2 Corinthians': 'B08',
    'Galatians': 'B09',
    'Gal': 'B09',
}
