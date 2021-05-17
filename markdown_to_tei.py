import argparse

import lxml.etree as et
from markdown import Markdown
from md_tei_extension import TEI, postprocess_xml, preprocess_md, postprocess_markup # pylint: disable=import-error


def convert_md_to_tei(md_file, xml_file, plain: bool, lines: bool):
    M = Markdown(extensions=['attr_list', TEI(), 'markdown_del_ins'])
    with open(md_file, 'r', encoding='utf-8') as file:
        md = file.read()

    md = preprocess_md(md)
    markup = M.convert(md)
    markup = postprocess_markup(markup)

    parser = et.XMLParser(remove_blank_text=True, encoding='UTF-8')
    xml = et.fromstring(markup, parser)
    xml = postprocess_xml(xml)

    xml = xml.getroottree()
    if plain:
        xml.write(xml_file, encoding='utf-8')
    elif lines:
        xml_str = et.tostring(xml, encoding='unicode')
        xml_str = xml_str.replace('\n', '')
        xml_str = xml_str.replace('<pb', '\n<pb')
        xml_str = xml_str.replace('<lb', '\n    <lb')
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(xml_str)
    else:
        et.indent(xml, '    ')
        xml.write(xml_file, encoding='utf-8', pretty_print=True)

def main():
    parser = argparse.ArgumentParser(description='''
    Convert a subset of Markdown into TEI XML which can be
    loaded into the ITSEE Online Transcription Editor.
    ''')
    parser.add_argument('-o', metavar='output', type=str, help='Output file address (default is same as input with a .xml file extension.')
    parser.add_argument('input', type=str, help='markdown (.md) file to convert')
    parser.add_argument('-l', action='store_true', help='format output according to transcription lines')
    parser.add_argument('-p', action='store_true', help='do not apply any formatting (defaults to pretty printing)')
    args = parser.parse_args()
    md_file = args.input
    if args.o is None:
        xml_file = md_file.replace('.md', '.xml')
    else:
        xml_file = args.o
        if not xml_file.endswith('.xml'):
            xml_file = f'{xml_file}.xml'
    try:
        convert_md_to_tei(md_file, xml_file, args.p, args.l)
    except et.XMLSyntaxError:
        print('''\nFailed to parse the XML file during final touches.\n\
Make sure that all opened tags are closed;\n\
this includes book closing tags i.e. "####"\n\
and chapter closings e.g. "#####", and verse\n\
verse units e.g. "</v>".\n\
You also may have found a bug, so don't hesitate\n\
to report it so it can be addressed.\n''')
    print(f'{md_file} converted and saved as {xml_file}')

if __name__ == '__main__':
    main()
