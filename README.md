# ST3 - HL7 plug-in and syntax highlighter

HL7 Sublime Text 3 plug-in and syntax highlighter to make the life of those who work in the Health Integration field easier.

## Funcionalities


### Enhanced syntax highlighter
![Syntax Highlighter Image](Misc/syntaxhighlighter.gif)


### Segment inspector
Gives a description of the segment and parses it.

![Segment Inspector Image](Misc/segmentinspector.gif)


### Segment / Event search
Searches on Caristix web site the given segment (e.g. PID, OBX, ...) or event (e.g. ADT^A01, ADT_A04). Notice that events separated with both ^ and _ are valid searches.

![Segment Event Searcher Image](Misc/segmenteventsearcher.gif)

### Message Cleaner
Cleans an HL7 message from unwanted escape characters such as "^M". It also cleans every unnecessary "|" and "^" to improve readability.

![Message Cleaner Image](Misc/messagecleaner.gif)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Change Log

* 15-04-2018 - Sub-component separator support
* 01-02-2018 - First version


## Acknowledgments

* Syntax Highlighter based on the one from @craighurley (https://github.com/craighurley/sublime-hl7-syntax)

