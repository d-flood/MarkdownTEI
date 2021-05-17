import lxml.etree as et
import xml.etree.ElementTree as ET

from md_tei_extension import (preprocess_md, add_text_body_opening_tags, # pylint: disable=import-error
                              h4_to_book_div, h5_to_chapter_div, bulk_replace,
                              add_tei_boilerplate_and_ending_tags, 
                              fill_out_untranscribed_commentary_markup,
                              fill_out_verse_unit_attributes, TokenizeText,
                              RestructureTree, add_page_break_type) # pylint: disable=import-error

###########################################################
###########################################################
# Preprocess markdown

def test_preprocess_md():
    _in = '<lb/> a word bro-\n<lb n="8"/>ken b[y] [a] br[eak]'
    _out = '<lb/> a word bro<lb n="8"/>ken b~~y~~ ~~a~~ br~~eak~~'
    assert preprocess_md(_in) == _out

###########################################################
###########################################################
# Postprocess markup

def test_add_text_body_opening_tags():
    _in = 'header\n....\ntranscription ....\n....'
    _out = 'header\n<text xml:lang="grc"><body>\ntranscription ....\n....'
    assert add_text_body_opening_tags(_in) == _out

def test_h4_to_book_div():
    _in = '<h4>Romans</h4>'
    _out = '<div type="book" n="B06">\n'
    book = 'B06'
    assert h4_to_book_div(_in) == (_out, book)

def test_h5_to_chapter_div():
    _in = '<h5>11</h5>'
    book = 'B06'
    _out = f'<div type="chapter" n="{book}K11">'
    assert h5_to_chapter_div(_in, book) == _out

def test_bulk_replace():
    '''This currently tests a very small part of the strings to be replaced.
    This is basically to ensure that the function is not entirely broken.'''
    _in = '<h4/><h5/>'
    _out = '</div></div>'
    assert bulk_replace(_in) == _out

def test_add_tei_boilerplate_and_ending_tags():
    _in = 'TRANSCRIPTION_BODY'
    _out = f'''<!DOCTYPE TEI><TEI xmlns="http://www.tei-c.org/ns/1.0">{_in}</body></text></TEI>'''
    assert add_tei_boilerplate_and_ending_tags(_in) == _out

###########################################################
###########################################################
# postprocess xml

def test_fill_out_untranscribed_commentary_markup():
    _in = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><text xml:lang="grc"><body><div type="book" n="B06"><div type="chapter" n="B06K11"><ab n="B06K11V5"><comm/><comm lines="3"/></ab></div></div></body></text></TEI>'
    _out = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><text xml:lang="grc"><body><div type="book" n="B06"><div type="chapter" n="B06K11"><ab n="B06K11V5"><note type="commentary">untranscribed commentary text</note><lb/><note type="commentary">One line of untranscribed commentary text</note><lb/><note type="commentary">One line of untranscribed commentary text</note><lb/><note type="commentary">One line of untranscribed commentary text</note></ab></div></div></body></text></TEI>'
    root_in = et.fromstring(_in)
    root_out = fill_out_untranscribed_commentary_markup(root_in)
    root_string = et.tostring(root_out, encoding='unicode')
    assert root_string == _out

def test_fill_out_verse_unit_attributes():
    _in = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><div type="chapter" n="B06K11"><ab n="6">content</ab></div></TEI>'
    _out = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><div type="chapter" n="B06K11"><ab n="B06K11V6">content</ab></div></TEI>'
    parsed = et.fromstring(_in)
    parsed = fill_out_verse_unit_attributes(parsed)
    result = et.tostring(parsed, encoding='unicode')
    print(f'{result=}')
    assert result == _out

###########################################################
###########################################################
# tokenize text

def test_rando_str():
    tokenize = TokenizeText()
    out1 = tokenize.rando_str()
    out2 = tokenize.rando_str()
    assert type(out1) is str and (out1 != out2)

def test_replace_words_with_mid_break():
    _in = '<div>*one two*{key="value"} th<lb n="8"/>ree fo<lb/>ur a an {unencoded note} ++ corrcdet tetx | corrected text ++</div>'
    expected_out = '<div>*one two*{key="value"} th$$$ZZZZZree fo$$$ZZZZZur a an {unencoded note} ++ corrcdet tetx | corrected text ++</div>'
    tokenize = TokenizeText()
    _out, replaced, randos = tokenize.replace_words_with_mid_break(_in, [], ['|'])
    for rando in randos:
        if rando != '|':
            _out = _out.replace(rando, '$$$ZZZZZ')
    if replaced[0][0] == '<lb n="8"/>' and replaced[1][0] == '<lb/>':
        replaced = True
    else:
        replaced = False
    assert _out == expected_out and replaced is True

def test_replace_user_markups():
    _in = '<div>*one two*{key="value"} th$$$ZZZZZree fo$$$ZZZZZur a an {unencoded note} ++ corrcdet tetx | corrected text ++</div>'
    expected_out = '<div>*one two*$$$YYYYY  th$$$ZZZZZree fo$$$ZZZZZur a an $$$YYYYY  ++ corrcdet tetx | corrected text ++</div>'
    tokenize = TokenizeText()
    _out, replaced, randos = tokenize.replace_user_markups(_in, [], ['|'])
    for rando in randos:
        if rando != '|':
            _out = _out.replace(rando, '$$$YYYYY')
    if replaced[0][0] == '{key="value"}' and replaced[1][0] == '{unencoded note}':
        replaced = True
    else:
        replaced = False
    assert _out == expected_out and replaced is True

def test_replace_markups():
    _in = '<div>*one two*$$$YYYYY  th$$$ZZZZZree fo$$$ZZZZZur a an $$$YYYYY  ++ corrcdet tetx | corrected text ++</div>'
    expected_out = ' $$$XXXXX *one two*$$$YYYYY  th$$$ZZZZZree fo$$$ZZZZZur a an $$$YYYYY  ++ corrcdet tetx | corrected text ++ $$$XXXXX '
    tokenize = TokenizeText()
    _out, replaced, randos = tokenize.replace_markups(_in, [], ['|'])
    for rando in randos:
        if rando != '|':
            _out = _out.replace(rando, '$$$XXXXX')
    if replaced[0][0] == '<div>' and replaced[1][0] == '</div>':
        replaced = True
    else:
        replaced = False
    assert _out == expected_out and replaced is True    

def test_replace_notes():
    _in = ' $$$XXXXX *one two*$$$YYYYY  th$$$ZZZZZree fo$$$ZZZZZur a an $$$YYYYY  ++ corrcdet tetx | corrected text ++ $$$XXXXX '
    expected_out = ' $$$XXXXX $$$WWWWW$$$YYYYY  th$$$ZZZZZree fo$$$ZZZZZur a an $$$YYYYY  ++ corrcdet tetx | corrected text ++ $$$XXXXX '

    tokenize = TokenizeText()
    _out, replaced, randos = tokenize.replace_notes(_in, [], ['|'])
    print(f'{replaced=}')
    for rando in randos:
        if rando != '|':
            _out = _out.replace(rando, '$$$WWWWW')
    if replaced[0][0] == '*one two*':
        replaced = True
    else:
        replaced = False
    assert _out == expected_out and replaced is True

def test_build_new_text():
    _in = ' $$$XXXXX $$$WWWWW$$$YYYYY  th$$$ZZZZZree fo$$$ZZZZZur a an $$$YYYYY  ++ corrcdet tetx | corrected text ++ $$$XXXXX '
    expected_out = '$$$XXXXX$$$WWWWW$$$YYYYY<w>th$$$ZZZZZree</w><w>fo$$$ZZZZZur</w><w>a</w><w>an</w>$$$YYYYY++<w>corrcdet</w><w>tetx</w>|<w>corrected</w><w>text</w>++$$$XXXXX'
    randos = ['$$$XXXXX', '$$$YYYYY', '$$$ZZZZZ', '$$$WWWWW']
    tokenized = TokenizeText()
    _out = tokenized.build_new_text(_in, randos)
    assert _out == expected_out

def test_replace_randos():
    _in = '$$$XXXXX$$$WWWWW$$$YYYYY<w>th$$$ZZZZZree</w><w>fo$$$ZZZZZur</w><w>a</w><w>an</w>$$$YYYYY++<w>corrcdet</w><w>tetx</w>|<w>corrected</w><w>text</w>++$$$XXXXX'
    expected_out = 'X1X1W4W4Y2Y2<w>thZ3Z3ree</w><w>foZ3Z3ur</w><w>a</w><w>an</w>Y2Y2++<w>corrcdet</w><w>tetx</w>|<w>corrected</w><w>text</w>++X1X1'
    replacements = [('X1X1', '$$$XXXXX'), ('Y2Y2', '$$$YYYYY'), ('Z3Z3', '$$$ZZZZZ'), ('W4W4', '$$$WWWWW')]
    tokenized = TokenizeText()
    _out = tokenized.replace_randos(_in, replacements)
    print(f'{_out=}')
    assert _out == expected_out
    
def test_tokenize_run():
    _in = ['# should not be tokenized',
           '..... should not be tokenized',
           '> should not be tokenized',
           '<div>*one two*{key="value"} th<lb n="8"/>ree fo<lb/>ur a an {unencoded note} ++ corrcdet tetx | corrected text ++</div>']
    expected_out = ['# should not be tokenized', 
                    '..... should not be tokenized', 
                    '> should not be tokenized',
                    '<div>*one two*{key="value"}<w>th<lb n="8"/>ree</w><w>fo<lb/>ur</w><w>a</w><w>an</w>{unencoded note}++<w>corrcdet</w><w>tetx</w>|<w>corrected</w><w>text</w>++</div>']
    tokenize = TokenizeText()
    _out = tokenize.run(_in)
    assert expected_out == _out

###########################################################
###########################################################
# Restructure Tree

def test_build_tei_header():
    _in = '''
<TEI>
<h1 n="witness">Title</h1>
<h2>transcribor</h2>
<h3>date</h3>
</TEI>
'''
    expected_out = '<TEI><teiHeader><fileDesc><titleStmt><h1 type="document">Title</h1><respStmt><resp when-iso="date">Transcribed by</resp><name type="person">transcribor</name></respStmt></titleStmt></fileDesc></teiHeader></TEI>'
    root = ET.fromstring(_in)
    restructure = RestructureTree()
    _out = restructure.build_tei_header(root)
    _out = ET.tostring(root, encoding='unicode').replace('\n', '')
    assert expected_out == _out

def test_add_page_break_type():
    _in = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><pb n="221r"/></TEI>'
    expected_out = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><pb n="221r" type="folio"/></TEI>'
    root = et.fromstring(_in)
    root = add_page_break_type(root)
    _out = et.tostring(root, encoding='unicode').replace('\n', '')
    print(f'{_out=}')
    assert _out == expected_out
