import unittest
from .preprocess import *


class TestPreprocessMethods(unittest.TestCase):

    def test_normalize_text(self):
        case1 = (' afd  hgf\n adfad\n\nfad\n \nadf',
                 'afd hgf\nadfad\nfad\nadf')
        self.assertEqual(normalize_text(case1[0]), case1[1])

    def test_segment_sentence(self):
        doc1 = spacy_nlp('In unanesthetized, spontaneously hypertensive '
                         'rats the decrease in blood pressure and heart rate '
                         'produced by intravenous clonidine, 5 to 20 '
                         'micrograms/kg, was inhibited or reversed by '
                         'nalozone, 0.2 to 2 mg/kg. The hypotensive '
                         'effect of 100 mg/kg alpha-methyldopa was '
                         'also partially reversed by naloxone. Naloxone '
                         'alone did not affect either blood pressure or'
                         ' heart rate. In brain membranes from spontaneously'
                         ' hypertensive rats clonidine, 10(-8) to 10(-5) M,'
                         ' did not influence stereoselective binding of '
                         '[3H]-naloxone (8 nM), and naloxone, 10(-8) to '
                         '10(-4) M, did not influence clonidine-suppressible'
                         ' binding of [3H]-dihydroergocryptine (1 nM). '
                         'These findings indicate that in spontaneously '
                         'hypertensive rats the effects of central '
                         'alpha-adrenoceptor stimulation involve activation '
                         'of opiate receptors. As naloxone and clonidine do '
                         'not appear to interact with the same receptor site,'
                         ' the observed functional antagonism suggests the '
                         'release of an endogenous opiate by clonidine or '
                         'alpha-methyldopa and the possible role of the opiate'
                         ' in the central control of sympathetic tone.')
        case1 = ([sent.text for sent in doc1.sents],
                 [
                     'In unanesthetized, spontaneously hypertensive rats the '
                     'decrease in blood pressure and heart rate produced by '
                     'intravenous clonidine, 5 to 20 micrograms/kg, was inhib'
                     'ited or reversed by nalozone, 0.2 to 2 mg/kg.',

                     'The hypotensive effect of 100 mg/kg alpha-methyldopa was'
                     ' also partially reversed by naloxone.',

                     'Naloxone alone did not affect either blood pressure or '
                     'heart rate.',

                     'In brain membranes from spontaneously hypertensive rats'
                     ' clonidine, 10(-8) to 10(-5) M, did not influence stere'
                     'oselective binding of [3H]-naloxone (8 nM), and naloxone'
                     ', 10(-8) to 10(-4) M, did not influence clonidine-suppr'
                     'essible binding of [3H]-dihydroergocryptine (1 nM).',

                     'These findings indicate that in spontaneously hypertensi'
                     've rats the effects of central alpha-adrenoceptor stimul'
                     'ation involve activation of opiate receptors.',

                     'As naloxone and clonidine do not appear to interact with'
                     ' the same receptor site, the observed functional antagon'
                     'ism suggests the release of an endogenous opiate by clon'
                     'idine or alpha-methyldopa and the possible role of the o'
                     'piate in the central control of sympathetic tone.'
                 ]
                 )
        self.assertEqual(case1[0], case1[1])

        doc2 = spacy_nlp('He said:" This should be a tough issue. Isn\'t it?"')
        case2 = (
            ['He said:" This should be a tough issue. Isn\'t it?"'],
            [sent.text for sent in doc2.sents]
        )
        self.assertEqual(case2[0], case2[1])


if __name__ == '__main__':
    unittest.main()
