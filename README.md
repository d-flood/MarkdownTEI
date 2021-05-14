# Markdown for TEI Transcriptions

Project Goals
1. Define a modified subset of markdown syntax
2. Converts the markdown transcription into a TEI XML encoded document that is compatible with the ITSEE/INTF [Online Transcription Editor](https://itsee-wce.birmingham.ac.uk/ote/transcriptiontool).
3. Produce JSON transcription files for use with the ITSEE [Collation Editor](https://github.com/itsee-birmingham/standalone_collation_editor)

This utility uses [lxml](https://pypi.org/project/lxml/) and it extends and abuses [Python-Markdown](https://pypi.org/project/Markdown/)

## Repurposed and Modified Syntax | Example
### markdown text
```markdown
# A Transcription of ZZZZ {n='ZZZZ'}
## Talitha Mackenzie
### 2021-05-12
................................... <!-- marks end of header -->
#### Romans <!-- Full or SBL abbreviated book title is converted to IGNTP/INTF format  -->
##### 11   <!-- numerical chapter is converted to IGNTP/INTF format  -->
<pb n="323v"/> <!-- regular XML tags work and are useful --> 
<lb/> words are tokenized
<lb/><v n="5">shortcut tag for verse unit
<lb/>[supp]lied [text] in brackets
<lb/>unclear `text` in back`ticks`
<lb/>**marginalia in double-asterisks**{subtype='lineleft'}
<lb/>a word bro-
<lb/>/ken by a break
<lb/>{unencoded notes in braces}
<lb/>*encoded editer's note in single asterisks*
<lb/> ++ correcdet txet | corrected text ++
<lb/> add attributes to an `element`{reason='damage to page'}</v>
<!-- close out the chapter and book -->
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
                <title n="ZZZZ" type="document">A Transcription of ZZZZ</title>
                <respStmt>
                    <resp when-iso="2021-05-12">Transcribed by</resp>
                    <name type="person">Talitha Mackenzie</name>
                </respStmt>
            </titleStmt>
        </fileDesc>
    </teiHeader>
    <text xml:lang="grc">
        <body>
            <div type="book" n="B06">
                <div type="chapter" n="B06K11">
                    <pb n="323v"/>
                    <lb/><w>words</w><w>are</w><w>tokenized</w>
                    <lb/>
                    <ab n="B06K11V5"><w>shortcut</w><w>tag</w><w>for</w><w>verse</w><w>unit</w>
                        <lb/><w><supplied>supp</supplied>lied</w><w><supplied>text</supplied></w><w>in</w><w>brackets</w>
                        <lb/><w>unclear</w><w><unclear>text</unclear></w><w>in</w><w>back<unclear>ticks</unclear></w>
                        <lb/><seg type="margin" subtype="lineleft">marginalia in double-asterisks</seg>
                        <lb/><w><w>a</w></w><w>word</w><w>bro</w><lb/><w>/ken</w><w>by</w><w><w>a</w></w>bre<w><w>a</w></w>k
                        <lb/>{unencoded notes in braces}
                        <lb/><note type="local">encoded editer's note in single asterisks</note>
                        <lb/><app>
                            <rdg type="orig" hand="firsthand"><w>correcdet</w><w>txet</w></rdg>
                            <rdg type="corr" hand="corrector"><w>corrected</w><w>text</w></rdg>
                            </app>
                        <lb/><w>add</w><w>attributes</w><w>to</w><w>an</w><w><unclear reason="damage to page">element</unclear></w>
                    </ab>
                </div>
            </div>
        </body>
    </text>
</TEI>
```
