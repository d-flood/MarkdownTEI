# Markdown for TEI Transcriptions - v 0.1

### Project Goals
1. Define a modified subset of markdown syntax
2. Converts the markdown transcription into a TEI XML encoded document that is compatible with the ITSEE/INTF [Online Transcription Editor](https://itsee-wce.birmingham.ac.uk/ote/transcriptiontool).
3. Produce JSON transcription files for use with the ITSEE [Collation Editor](https://github.com/itsee-birmingham/standalone_collation_editor)

### Requirements
- Python 3.6+ (tested on 3.9)
- [lxml](https://pypi.org/project/lxml/) 
- [Python-Markdown](https://pypi.org/project/Markdown/)
- [markdown-del-ins](https://pypi.org/project/markdown-del-ins/)
- [pytest](https://pypi.org/project/pytest/) (only needed if you intend to run the tests on the source code) 

### Using this Tool
- Clone or download this repository and navigate to the root folder in a console window.
- to convert the simple example, execute execute `python -m markdown_to_tei.py examples/simple_example.md`
This will use the default settings: the output file has the same name as the input file but the extension is changed to `.xml` and it is pretty printed.
- Use the -o flag and add an output location, e.g. `python -m markdown_to_tei.py examples/simple_example.md -o my_file.xml`
- Use the -l flag to signal that the output file should be formatted according to the transcription lines, one transcription line per line in the file.
- Use the -p flag to make remove unimportant whitespace (ideal for storage, not for reading).
- To run the tests, execute `python -m pytest` from the root folder.

## Repurposed and Modified Syntax | Simple Example
### markdown text
```markdown
# A Simple Transcription Example
## FirstName LastName
### 2021-05-12
...................................
#### Romans
##### 11
<pb n="323v"/>
<lb/> words are tokenized
<lb/><v n="5">shortcut tag for verse unit
<lb/> [supp]lied [text] in brackets
<lb/> unclear `text` in back`ticks`
<lb/> some text followed by commentary <comm/>
<comm lines="3"/>
<lb/> **marginalia in double-asterisks**
<lb/> a word bro-
<lb n="8"/>ken over two lines
<lb/> {unencoded notes in braces}
<lb/> *encoded editer's note in single asterisks*
<lb/> ++ corrcdet tetx | corrected text ++
<lb/> add attributes to an `element`{reason='damage to page'}</v>
#####
####
```
### rendered TEI
```xml
<!DOCTYPE TEI>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title type="document">A Simple Transcription Example</title>
                <respStmt>
                    <resp when-iso="2021-05-12">Transcribed by</resp>
                    <name type="person">FirstName LastName</name>
                </respStmt>
            </titleStmt>
        </fileDesc>
    </teiHeader>
    <text xml:lang="grc">
        <body>
            <div type="book" n="B06">
                <div type="chapter" n="B06K11">
                    <pb n="323v" type="folio"/>
                    <lb/><w>words</w><w>are</w><w>tokenized</w>
                    <lb/><ab n="B06K11V5"><w>shortcut</w><w>tag</w><w>for</w><w>verse</w><w>unit</w>
                    <lb/><w><supplied>supp</supplied>lied</w><w><supplied>text</supplied></w><w>in</w><w>brackets</w>
                    <lb/><w>unclear</w><w><unclear>text</unclear></w><w>in</w><w>back<unclear>ticks</unclear></w>
                    <lb/><w>some</w><w>text</w><w>followed</w><w>by</w><w>commentary</w><note type="commentary">untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><seg type="margin">marginalia in double-asterisks</seg>
                    <lb/><w>a</w><w>word</w><w>bro
                    <lb n="8"/>ken</w><w>over</w><w>two</w><w>lines</w>
                    <lb/>{unencoded notes in braces}
                    <lb/><note type="local">encoded editer's note in single asterisks</note>
                    <lb/><app><rdg type="orig" hand="firsthand"><w>corrcdet</w><w>tetx</w></rdg><rdg type="corr" hand="corrector"><w>corrected</w><w>text</w></rdg></app>
                    <lb/><w>add</w><w>attributes</w><w>to</w><w>an</w><w><unclear reason="damage to page">element</unclear></w></ab>
                </div>
            </div>
        </body>
    </text>
</TEI>
```

## A Real Example
### markdown text
```markdown
# A Transcription of GA 1506 {n='31506'} 
## David A Flood, II
### 2020-09-12
...................................
#### Romans
##### 11
<pb n="323v"/>
<comm lines="8"/>
<lb n="9"/><comm/><v n="4">???????? ???? ?????????? ???????? ?? ????[??]????-
<lb n="10"/>???????????? . ???????????????? ???????????? ???????????????????????????? ???????????? ?????????????? ?????? ??-
<lb n="11"/>???????????? ?????????? ???? ?????? *expected ????????*</v><v n="5">?????????? ?????? ?????? ???? ???? ?????????? ?????????? ?????????? 
<lb n="12"/>?????? ????????????`??` [????????]?????? ??????????????</v>
<comm lines="5"/>
<lb n="18"/><v n="6">`??`?? ???? ??`????`??`??`?? ??????`??`???? ??`??`{reason="see note"} ??????[??]?? ????[????] [??] ??`??`?????? [????]?? `??`???? ??????[??]??[????] ?????????? *this line is difficult to read because the reverse-side commentary is more visible than the front-facing lemma*
<comm lines="4"/>
<comm/></v>
#####
####
```

### rendered TEI
```xml
<!DOCTYPE TEI>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title n="31506" type="document">A Transcription of GA 1506</title>
                <respStmt>
                    <resp when-iso="2020-09-12">Transcribed by</resp>
                    <name type="person">David A Flood, II</name>
                </respStmt>
            </titleStmt>
        </fileDesc>
    </teiHeader>
    <text xml:lang="grc">
        <body>
            <div type="book" n="B06">
                <div type="chapter" n="B06K11">
                    <pb n="323v" type="folio"/>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb n="9"/><note type="commentary">untranscribed commentary text</note><ab n="B06K11V4"><w>????????</w><w>????</w><w>??????????</w><w>????????</w><w>??</w><w>????<supplied>??</supplied>????
                    <lb n="10"/>????????????</w><pc><w>.</w></pc><w>????????????????</w><w>????????????</w><w>????????????????????????????</w><w>????????????</w><w>??????????????</w><w>??????</w><w>??
                    <lb n="11"/>????????????</w><w>??????????</w><w>????</w><w>??????</w><note type="local">expected ????????</note></ab><ab n="B06K11V5"><w>??????????</w><w>??????</w><w>??????</w><w>????</w><w>????</w><w>??????????</w><w>??????????</w><w>??????????</w>
                    <lb n="12"/>??????<w>????????????<unclear>??</unclear></w><w><supplied>????????</supplied>??????</w><w>??????????????</w></ab>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb n="18"/><ab n="B06K11V6"><w><unclear>??</unclear>??</w><w>????</w><w>??<unclear>????</unclear>??<unclear>??</unclear>??</w><w>??????<unclear>??</unclear>????</w><w>??<unclear reason="see note">??</unclear></w><w>??????<supplied>??</supplied>??</w><w>????<supplied>????</supplied></w><w><supplied>??</supplied></w><w>??<unclear>??</unclear>??????</w><w><supplied>????</supplied>??</w><w><unclear>??</unclear>????</w><w>??????<supplied>??</supplied>??<supplied>????</supplied></w><w>??????????</w>
                        <note type="local">
                            this line is difficult to read because the reverse-side commentary is more visible than the front-facing lemma
                        </note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note>
                    <lb/><note type="commentary">One line of untranscribed commentary text</note><note type="commentary">untranscribed commentary text</note></ab>
                </div>
            </div>
        </body>
    </text>
</TEI>
```
________________
## Rendered TEI is valid and can be uploaded to the ITSEE [Online Transcription Editor](https://itsee-wce.birmingham.ac.uk/ote/transcriptiontool)
______
This is above example loaded into the ITSEE Transcription Editor
![itsee online transcription editor screenshot](images/example_file_in_itsee_ote.png)
