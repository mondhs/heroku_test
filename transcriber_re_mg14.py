#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
trancriber mg1.4
'''

import sys, re
import collections

class TranscriberRegexp:

# http://cmusphinx.sourceforge.net/wiki/tutorialam
#   Do not use case-sensitive variants like “e” and “E”. Instead, all your phones must be different even in case-insensitive variation. Sphinxtrain doesn't support some special characters like '*' or '/' and supports most of others like ”+” or ”-” or ”:” But to be safe we recommend you to use alphanumeric-only phone-set. Replace special characters in the phone-set, like colons or dashes or tildes, with something alphanumeric. For example, replace “a~” with “aa” to make it alphanumeric only.


# 1 - nosinė, 2 - šnipštimas(ž,š), e3 ė _-ilgumas($/:) .-minkštumas(')
    graphemeToPhonemeMap = [
        ( u"iu", u"IU"),#Svarbu jei be minkštumo
        ( u"ių", u"IU_"),#Svarbu jei be minkštumo
        ( u"io", u"IO_"),#Svarbu jei be minkštumo
        #( u"ui", u"UI"),
        #( u"uo", u"UO"),
        ( u"ia", u"E"),
        ( u"ią", u"E_"),
        #( u"tst", u"T S T"), #atstatyk# nebėra versijoje z1.3
        #( u"ts", u"C"),#atsakymą,atsiųsk# nebėra versijoje z1.3
        ( u"iau", u"E U"),
        ( u"ja", u"J. E"), #jau, japonas
        ( u"ją", u"J. E_"), #naują
        

        #Dantiniai priebalsiai {S, Z, C, DZ} prieš alveolinius {S2, Z2, C2, DZ2} keičiami atitinkamai į alveolinius {S2, Z2, C2, DZ2} (slenksčiai -> S L E N K S2 C2 E I).
        ( u"sž", u"S2 Z2"),#?
        ( u"sč", u"S2 C2"),#kunigaikštysčiu
        ( u"zdž", u"Z2 DZ2"),#vabzdžiai
        
        #vyKdyk duslieji prieš skardžiuos g                
        ( u"gk", u"K K"),#angkoras -> A N K K O_ R A S
        ( u"gt", u"K T"),#vašingtonas, jungtinių
        ( u"tb", u"D B"),#atbaidyti
        ( u"šb", u"Z2 B"),#išbandyti                
        ( u"kd", u"G D"),#atlikdavo
        ( u"sd", u"Z D"),#kasdami
        ( u"šd", u"Z2 D"),#neišdildoma
        ( u"pg", u"B G"),#apgadintas
        ( u"tg", u"D G"),#atgabenti
        ( u"šg", u"Z2 G"),#išgaubti
        ( u"tž", u"D Z2"),#atžvilgiu
        ( u"žk", u"S2 K"),#grįžk
        ( u"zt", u"S T"),#megztinis
        

        ( u"ch", u"CH"),
        ( u"dž", u"DZ2"),
        ( u"dz", u"DZ"),

                
        #grafemos
        ( u"a", u"A"),
        ( u"ą", u"A_"),
        ( u"b", u"B"),
        ( u"c", u"C"),
        ( u"č", u"C2"),
        ( u"d", u"D"),
        ( u"e", u"E"),
        ( u"ę", u"E_"),
        ( u"ė", u"E3_"),
        ( u"f", u"F"),
        ( u"g", u"G"),
        ( u"h", u"H"),
        ( u"i", u"I"),
        ( u"į", u"I_"),
        ( u"y", u"I_"),
        ( u"j", u"J."),
        ( u"k", u"K"),
        ( u"l", u"L"),
        ( u"m", u"M"),
        ( u"n", u"N"),
        ( u"o", u"O_"),
        ( u"p", u"P"),
        ( u"r", u"R"),
        ( u"s", u"S"),
        ( u"š", u"S2"),
        ( u"t", u"T"),
        ( u"u", u"U"),
        ( u"ų", u"U_"),
        ( u"ū", u"U_"),
        ( u"v", u"V"),
        ( u"w", u"V"),
        ( u"z", u"Z"),
        ( u"ž", u"Z2"),
        ]

        #daug gale b,d,g,z,ž(skardieji) kaip p,t,k,s,š(duslieji)+
        #grįžk skardieji prieš duslieji š
        #minkštumas: džiaugsmas prieš e, i, ė yra minkšti
        #minkštumas: ankstenė - k ir g sustabdomas minkšumas anks't'enė
        #!Neitraukiant minkšrumo! tai butinai reikia iu ir io kaip atskiros fonemos. 

    preprocesorMap = [
        ( u"^ie", u"jie"),
        ( u"g$", u"k"),
        ( u"d$", u"t"),
        ( u"ž$", u"š"),
        ( u"z$", u"s"),
        ( u"facebookas", u"feisbukas"),
        ( u"unesco", u"junesko"),
    ]

    def __init__(self):
        transcribation_keys = map(lambda x: x[0], self.graphemeToPhonemeMap)
        self.transcribation_rulesDict = dict(self.graphemeToPhonemeMap)
        transcribation_regexStr = u"(%s)" % u"|".join(map(re.escape, transcribation_keys))
        # Create a regular expression  from the dictionary keys
        self.transcribation_regex = re.compile(transcribation_regexStr)

        preprocess_keys = map(lambda x: x[0], self.preprocesorMap)
        self.preprocess_rulesDict = dict(self.preprocesorMap)
        preprocess_regexStr = u"(%s)" % u"|".join(map(re.escape, preprocess_keys))
        # Create a regular expression  from the dictionary keys
        self.preprocess_regex = re.compile(preprocess_regexStr)


    def multiple_replace(self,  text):
        preprocesedText = self.preprocess_regex.sub(lambda mo: u" " + self.preprocess_rulesDict[mo.string[mo.start():mo.end()]] + u" ", text)
        
        #print "["+text+"]"
        # For each match, look-up corresponding value in dictionary
        return self.transcribation_regex.sub(lambda mo: u" " + self.transcribation_rulesDict[mo.string[mo.start():mo.end()]] + u" ", preprocesedText)

    def transcribe(self, word):
        #lowerWord = word.decode('utf-8').lower().encode('utf-8')
        lowerWord = word.lower()
        transcibedWord = self.multiple_replace(lowerWord)
        transcibedWord = re.sub(ur'\s+', ' ', transcibedWord)
        transcibedWord = transcibedWord.upper().strip()
        return transcibedWord;

    def transcribeDictionary(self, text):
        translatedMap = {}
        #lowerText = text.decode('utf-8').lower().encode('utf-8')
        lowerText = text.lower()
        lowerText = re.sub(ur"[\.\,\?\!\"\/\_><]+", r" ", lowerText)
        for wortEntry in lowerText.split():
            wordTranslated = self.transcribe(wortEntry)
            translatedMap[wortEntry] = wordTranslated
        translatedMap = collections.OrderedDict(sorted(translatedMap.items(), key=lambda t: t[0]))
        return translatedMap





import argparse

def processWords(words):
    transcriber = TranscriberRegexp()
    sphinx_dictionary = transcriber.transcribeDictionary(words)
    return sphinx_dictionary

def processFile(input_file):
    sphinx_dictionary = collections.OrderedDict()
    for line in input_file:
        loop_dictionary = processWords(line)
        sphinx_dictionary.update(loop_dictionary)
    sphinx_dictionary = collections.OrderedDict(sorted(sphinx_dictionary.items(), key=lambda t: t[0]))
    return sphinx_dictionary

        
def writeToFile(sphinx_dictionary, output_file):
    for key, value in sphinx_dictionary.iteritems():
        output_file.write( u"{}\t{}\n".format(key, value))
        
def writeToConsole(sphinx_dictionary):
    for key, value in sphinx_dictionary.iteritems():
        print u"{}\t{}".format(key, value)


def main():
    usage='%(prog)s --help'
    description='''Transcription text to phone for CMU Sphinx recognition. Example: %(prog)s -i zodziai.txt -o zodziai.dict
    '''
    parser = argparse.ArgumentParser(usage=usage,description=description)    
    parser.add_argument('-o', '--output_file', help='Output text dictionary file: word   W O R D', metavar='out-file', type=argparse.FileType('wt'))
    parser.add_argument('-v', '--verbose', action='store_true',help='Verbose output for debuging')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("input_words",  nargs='?', help="echo the string you use here")
    group.add_argument('-i', '--input_file', help='Input text file one word per line, \'-\' for standard input', metavar='in-file', type=argparse.FileType('rt'))

    
    args = parser.parse_args()
    if args.verbose: print args
    sphinx_dictionary = {}
    
    if args.input_file:
        sphinx_dictionary = processFile(args.input_file)
    elif args.input_words:
        sphinx_dictionary = processWords(args.input_words)
    else:
        sphinx_dictionary = processWords("bandom besikiškiakopūstaudavome")
        
    if args.output_file:
        writeToFile(sphinx_dictionary, args.output_file)
    else:
        writeToConsole(sphinx_dictionary)

if __name__ == "__main__":
    main()


