import random
import time
import re

SUBJECT_SYLL_MIN = 2
SUBJECT_SYLL_MAX = 5
VERB_SYLL_MIN = 1
VERB_SYLL_MAX = 4
OBJECT_SYLL_MIN = 2
OBJECT_SYLL_MAX = 5
ADVERB_SYLL_MIN = 1
ADVERB_SYLL_MAX = 4
FILLER_SYLL_MAX = 6

class WordSoup:
    def syll_count(self, word):
        syll = word.count('-') + word.count(' ') + 1
        return syll

    def sentence_syll_count(self):
        syll = 0
        for word in self.sentence_phonetic[1:]:
            syll += self.syll_count(word)
        return syll

    def grw_syll(self, file_path, syll_goal):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            low = 0
            high = len(lines) - 1
            syll = 0
            while syll != syll_goal:
                line_number = random.randint(low, high)
                line = lines[line_number].strip()
                spellings = line.split()
                middle = len(spellings) // 2
                phonetic = " ".join(spellings[middle:]) 
                syll = self.syll_count(phonetic)
                if syll < syll_goal:
                    low = line_number
                elif syll > syll_goal:
                    high = line_number
                elif syll == syll_goal:
                    return line
                file.seek(0)

    def svo_syll(self, words, syll):
        #Map in text files containing words
        subjects = words[0]
        verbs = words[1]
        objects = words[2]
        fillers = words[8]
        og_syll = syll

        # Fetch object first
        if syll <= OBJECT_SYLL_MAX:
            object_syll = OBJECT_SYLL_MIN
        else:
            object_syll = OBJECT_SYLL_MIN
        spellings = self.grw_syll(objects, object_syll).lower().split()
        middle = len(spellings) // 2
        self.object = [" ".join(spellings[:middle]), " ".join(spellings[middle:])]
        syll -= object_syll

        # Fetch verb next
        if syll <= VERB_SYLL_MAX:
            verb_syll = syll
        else:
            verb_syll = VERB_SYLL_MAX
        self.verb = self.grw_syll(verbs, verb_syll).split()
        self.verb[0] = self.verb[0].lower()
        syll -= verb_syll

        # Fetch subject last
        if SUBJECT_SYLL_MAX < (syll // 2):
            subject_syll = random.randint(SUBJECT_SYLL_MIN, SUBJECT_SYLL_MAX)
        else:
            subject_syll = SUBJECT_SYLL_MIN
        spellings = self.grw_syll(subjects, subject_syll).split()
        middle = len(spellings) // 2
        self.subject = [" ".join(spellings[:middle]), " ".join(spellings[middle:])]
        syll -= subject_syll

        #construct pre-filler true and phonetic spelling sentences
        sentence = ['svo', self.subject[0], self.verb[0], self.object[0]]
        self.sentence_phonetic = ['svo', self.subject[1], self.verb[1], self.object[1]]

        syll = og_syll - self.sentence_syll_count()

        #Randomly adding adlibs
        while syll > 0:
            if syll > FILLER_SYLL_MAX:
                spellings = self.grw_syll(fillers, FILLER_SYLL_MAX).split()
                middle = len(spellings) // 2
                self.filler.append(" ".join(spellings[:middle]))
                self.filler.append(" ".join(spellings[middle:]))
            else:
                spellings = self.grw_syll(fillers, syll).split()
                middle = len(spellings) // 2
                self.filler.append(" ".join(spellings[:middle]))
                self.filler.append(" ".join(spellings[middle:]))
            filler_index = random.randint(1, len(sentence))
            sentence.insert(filler_index, self.filler[-2])
            self.sentence_phonetic.insert(filler_index, self.filler[-1])
            syll -= FILLER_SYLL_MAX

        self.sentence = sentence

        return sentence

    def sv_syll(self, words, syll):
        #Map in text files containing words
        subjects = words[0]
        verbs = words[1]
        fillers = words[8]
        og_syll = syll

        # Fetch verb first
        if syll <= VERB_SYLL_MAX:
            verb_syll = syll
        else:
            verb_syll = VERB_SYLL_MAX
        self.verb = self.grw_syll(verbs, verb_syll).split()
        self.verb[0] = self.verb[0].lower()
        syll -= verb_syll

        # Fetch subject next
        if SUBJECT_SYLL_MAX < (syll // 2):
            subject_syll = random.randint(SUBJECT_SYLL_MIN, SUBJECT_SYLL_MAX)
        else:
            subject_syll = SUBJECT_SYLL_MIN
        spellings = self.grw_syll(subjects, subject_syll).split()
        middle = len(spellings) // 2
        self.subject = [" ".join(spellings[:middle]), " ".join(spellings[middle:])]
        syll -= subject_syll

        #construct pre-filler true and phonetic spelling sentences
        sentence = ['sv', self.subject[0], self.verb[0]]
        self.sentence_phonetic = ['sv', self.subject[1], self.verb[1]]

        syll = og_syll - self.sentence_syll_count()

        #Randomly adding adlibs
        while syll > 0:
            if syll > FILLER_SYLL_MAX:
                spellings = self.grw_syll(fillers, FILLER_SYLL_MAX).split()
                middle = len(spellings) // 2
                self.filler.append(" ".join(spellings[:middle]))
                self.filler.append(" ".join(spellings[middle:]))
            else:
                spellings = self.grw_syll(fillers, syll).split()
                middle = len(spellings) // 2
                self.filler.append(" ".join(spellings[:middle]))
                self.filler.append(" ".join(spellings[middle:]))
            filler_index = random.randint(1, len(sentence))
            sentence.insert(filler_index, self.filler[-2])
            self.sentence_phonetic.insert(filler_index, self.filler[-1])
            syll -= FILLER_SYLL_MAX

        self.sentence = sentence

        return sentence

    
    def sva_syll(self, words, syll):
        #Map in text files containing words
        subjects = words[0]
        verbs = words[1]
        adverbs = words[4]
        fillers = words[8]
        og_syll = syll

        # Fetch adverb first
        if syll <= ADVERB_SYLL_MAX:
            adverb_syll = ADVERB_SYLL_MIN
        else:
            adverb_syll = ADVERB_SYLL_MIN
        self.adverb = self.grw_syll(adverbs, adverb_syll).split()
        self.adverb[0] = self.adverb[0].lower()
        syll -= adverb_syll

        # Fetch verb next
        if syll <= VERB_SYLL_MAX:
            verb_syll = syll
        else:
            verb_syll = VERB_SYLL_MAX
        self.verb = self.grw_syll(verbs, verb_syll).split()
        self.verb[0] = self.verb[0].lower()
        syll -= verb_syll

        # Fetch subject last
        if SUBJECT_SYLL_MAX < (syll // 2):
            subject_syll = random.randint(SUBJECT_SYLL_MIN, SUBJECT_SYLL_MAX)
        else:
            subject_syll = SUBJECT_SYLL_MIN
        spellings = self.grw_syll(subjects, subject_syll).split()
        middle = len(spellings) // 2
        self.subject = [" ".join(spellings[:middle]), " ".join(spellings[middle:])]
        syll -= subject_syll

        #construct pre-filler true and phonetic spelling sentences
        sentence = ['sva', self.subject[0], self.verb[0], self.adverb[0]]
        self.sentence_phonetic = ['sva', self.subject[1], self.verb[1], self.adverb[1]]

        syll = og_syll - self.sentence_syll_count()

        #Randomly adding adlibs
        while syll > 0:
            if syll > FILLER_SYLL_MAX:
                spellings = self.grw_syll(fillers, FILLER_SYLL_MAX).split()
                middle = len(spellings) // 2
                self.filler.append(" ".join(spellings[:middle]))
                self.filler.append(" ".join(spellings[middle:]))
            else:
                spellings = self.grw_syll(fillers, syll).split()
                middle = len(spellings) // 2
                self.filler.append(" ".join(spellings[:middle]))
                self.filler.append(" ".join(spellings[middle:]))
            filler_index = random.randint(1, len(sentence))
            sentence.insert(filler_index, self.filler[-2])
            self.sentence_phonetic.insert(filler_index, self.filler[-1])
            syll -= FILLER_SYLL_MAX

        self.sentence = sentence

        return sentence

    def construct_sentence_syll(self, words, syll):
        sent_type = random.randint(1, 3)
        if sent_type == 1:
            self.sentence = self.svo_syll(words, syll)
        elif sent_type == 2:
            self.sentence = self.sv_syll(words, syll)
        elif sent_type == 3:
            self.sentence = self.sva_syll(words, syll)
        else:
            print("Invalid procedure.")

    def another_serving(self, words, syll):
        """
        Reconstructs a sentence of the same type as the current one, using the sentence type at self.sentence[0].
        """
        sent_type = self.sentence[0]
        if sent_type == 'svo':
            self.sentence = self.svo_syll(words, syll)
        elif sent_type == 'sv':
            self.sentence = self.sv_syll(words, syll)
        elif sent_type == 'sva':
            self.sentence = self.sva_syll(words, syll)
        else:
            print("Invalid sentence type for another_serving.")

    def rhym_syll_fetch(self, file_path, syll_goal, phonetic_spelling):
        target = re.split(r"[- ]", phonetic_spelling)[-1]
        syll = 0
        no_rhyme = True
        with open(file_path, 'r') as file:
            lines = file.readlines()
            low = 0
            high = len(lines) - 1
            vowels = ['a', 'e', 'i', 'o', 'u', 'y']
            same_word = True
            while (no_rhyme) or (syll != syll_goal) or same_word:
                line_number = random.randint(low, high)
                rhyming_word = lines[line_number].strip()
                #spellings = re.split(r"[- ]", lines[line_number].strip())
                #print(spellings)
                spellings = rhyming_word.split()
                middle = len(spellings) // 2
                spellings = [" ".join(spellings[:middle]), " ".join(spellings[middle:])]
                syll = self.syll_count(spellings[1])
                if syll < syll_goal:
                    low = line_number
                elif syll > syll_goal:
                    high = line_number
                
                last_syll = re.split(r"[- ]", spellings[1])[-1]

                no_vowel = (last_syll[0] not in vowels)
                i = 0
                while no_vowel and (i < len(last_syll) - 1):
                    i += 1
                    no_vowel = (last_syll[i] not in vowels)

                no_vowel = (target[0] not in vowels)
                i2 = 0
                while no_vowel and (i2 < len(target) - 1):
                    i2 += 1
                    no_vowel = (target[i2] not in vowels)
                #print('first word', target, target[i2:])
                #print('rhyme', last_syll, last_syll[i:])
                no_rhyme = last_syll[i:] != target[i2:]
                #print('ph', phonetic_spelling)
                #print('rh', spellings[1])
                same_word = (phonetic_spelling == spellings[1])
                file.seek(0)
        #print(spellings)
        return spellings
    
    def print_sentence(self):
        printable = ''
        for word in self.sentence[1:]:
            printable += ' ' + word
        printable += '.'
        print(printable)

    def svao_discerner(self, filler_words):
        s = 0
        v = 0
        ao = 0
        i = 1
        while (ao == 0) and (i <  len(self.sentence)):
            if (self.sentence[i] not in filler_words):
                if s == 0:
                    s = i
                elif v == 0:
                    v = i
                else: 
                    ao = i
            i += 1
        return s, v, ao


    def rhyme_replacer(self, index, phonetic):
        filler_words = []
        with open(self.words[8], 'r') as file:
            for line in file:
                line = line.strip().split()
                middle = len(line) // 2
                filler_words.append(" ".join(line[:middle]))
        s, v, ao = self.svao_discerner(filler_words)

        if index == s: #subject
            file = self.words[0]
            max_syll = SUBJECT_SYLL_MAX
            #phonetic_spelling = self.subject[1]
            phonetic_spelling = phonetic
            syll_goal = self.syll_count(self.subject[1])
        elif index == v: #verb
            file = self.words[1]
            max_syll = VERB_SYLL_MAX
            phonetic_spelling = phonetic
            syll_goal = self.syll_count(self.verb[1])
        elif index == ao and self.sentence[0] == 'svo':
            file = self.words[2] #object
            max_syll = OBJECT_SYLL_MAX
            phonetic_spelling = phonetic
            syll_goal = self.syll_count(self.object[1])
        elif index == ao and self.sentence[0] == 'sva': #adverb
            file = self.words[4]
            max_syll = ADVERB_SYLL_MAX
            phonetic_spelling = phonetic
            syll_goal = self.syll_count(self.adverb[1])
        else:
            file = self.words[8]
            max_syll = FILLER_SYLL_MAX
            phonetic_spelling = phonetic
            phonetic_filler = self.filler[self.filler.index(self.sentence[index]) + 1]
            syll_goal = self.syll_count(phonetic_filler)

        rhyme = self.rhym_syll_fetch(file, syll_goal, phonetic_spelling)
        middle = len(rhyme) // 2
        rhyme_list = [" ".join(rhyme[:middle]).lower(), " ".join(rhyme[middle:])]    
        self.sentence[index] = rhyme_list[0]
    
    def __init__(self, words, syll):
        self.words = words
        self.subject = "N/A"
        self.verb = "N/A"
        self.object = "N/A"
        #self.adjective = "N/A"
        self.adverb = "N/A"
        #self.noun = "N/A"
        self.filler = []

        #maybe use maybe don't
        self.conjunction = "N/A"
        self.preposition = "N/A"

        self.sentence = "N/A"
        self.sentence_phonetic = "N/A"

        self.construct_sentence_syll(words, syll)

syll = 10
files = ['subjects.txt', 'verbs.txt', 'objects.txt', 
        'adjectives.txt', 'adverbs.txt', 'nouns.txt', 
        'conjunctions.txt', 'prepositions.txt', 'filler.txt']
soup1 = WordSoup(files, syll)
print('\nThis Apple:')
soup1.print_sentence()
soup2 = WordSoup(files, syll)
print(soup1.sentence_phonetic[-1])
print(soup2.sentence[0])
soup2.rhyme_replacer(len(soup2.sentence)-1, soup1.sentence_phonetic[-1])
soup2.print_sentence()

#print('This Apple: ', soup.syll_count(soup.sentence, False))