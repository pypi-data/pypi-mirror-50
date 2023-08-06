#!/usr/bin/env python3

import os, sys
from argparse import ArgumentParser
from pkg_resources import resource_string
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from punsy import log
from punsy.structs.suffix_trie import SuffixTrie

import tqdm

LOG = log.get_logger('punsy')

class CMU:
    def __init__(self, cmu_fpath):
        self.fpath = cmu_fpath
        self.phonemes = SuffixTrie()
        self.mapping = {}
        self.n_lines = CMU.count_lines(self.fpath)

    def run(self):
        LOG.info(f'Parsing & loading {self.n_lines} entries from CMU dictionary file')
        with tqdm.tqdm(total=self.n_lines) as pbar:
            for word, phonemes in CMU.parse(self.fpath):
                phonemes = phonemes.split(' ')
                self.phonemes.insert(phonemes, word)
                self.mapping[word] = phonemes
                pbar.update(1)

    def rhymes_for(self, suffix, offset=3, max_depth=10):
        pron = self.mapping[suffix]
        LOG.info(f'Pronunciation of "{suffix}" is "{"-".join(pron)}"')
        LOG.info(f'Fetching rhymes, applying offset={offset}: "{"-".join(pron[offset:])}"')
        rhymes = self.phonemes.rhymes_for_suffix(
            pron,
            offset=offset,
            max_depth=10
        )
        LOG.info(f'Rhymes for {suffix}: {rhymes}')
        return rhymes

    @staticmethod
    def parse(fpath='', delimiter='|'):
        for line in CMU.__iter_file(fpath):
            yield line.strip().split(delimiter)

    @staticmethod
    def count_lines(fpath=''):
        for i, _ in enumerate(CMU.__iter_file(fpath)):
            pass
        else:
            return i

    @staticmethod
    def __iter_file(fpath=''):
        if fpath:
            with open(fpath, 'r') as istream:
                yield from istream
        else:
            for line in resource_string('punsy', 'cmudict-0.7b.utf8').decode().split('\n'):
                if line:
                    yield line


class POC:
    def __init__(self, cmu_fpath):
        self.cmu = CMU(cmu_fpath)
        self.cmu.run()

    def run(self, sentence, offset=1, max_depth=10):
        import random
        parts = sentence.split(' ')
        word = parts[-1].upper()
        rhyme = random.choice(self.cmu.rhymes_for(
            word, offset=offset, max_depth=max_depth
        ))
        parts[-1] = rhyme
        result = ' '.join(parts)
        LOG.info(f'Generated pun for {sentence}: {result} ({word} -> {rhyme})')

        return result


def poc():
    parser = ArgumentParser(prog='punsy')

    parser.add_argument('--sentence', type=str, required=True, help='The sentence to punnify')
    parser.add_argument('--cmu-file', type=str, help='(optional) the path of the cmu rhyming dictionary')
    parser.add_argument('--offset', type=int, default=2, help='The number of syllables to match')
    parser.add_argument('--max-depth', type=int, default=10, help='The maximum length of a matched rhyming word')
    args = parser.parse_args()

    LOG.info(
        POC(args.cmu_file).run(
            sentence=args.sentence,
            offset=args.offset
        )
    )

if __name__ == '__main__':
    poc()
