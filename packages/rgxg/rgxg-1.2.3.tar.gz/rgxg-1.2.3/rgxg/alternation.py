import collections
import shlex
import copy
import re
import itertools

def escape(s):
    return re.escape(s).replace("\ ", " ")

class StringSet:
    '''
    a set of strings
    instead of using a list of strings everywhere, condense duplicates and preserve additional
    statistics so we can use less memory, avoid repetitive calculations and make better decisions
    '''

    def __init__(self, strings=None):
        self.strings = collections.Counter(shlex.split(strings))

    def __iter__(self):
        return iter(self.strings.keys())

class Rgxg:
    @classmethod
    def build(self, t):
        '''
        Directed Acyclic Word Graph
        like a Trie, but we condense substrings and share substrings/suffixes where possible
        ref: https://en.wikipedia.org/wiki/Deterministic_acyclic_finite_state_automaton
        '''
        made = {}
        for k, v in t.items():
            v = Rgxg.build(v)
            # merge substrings
            if k and len(v) == 1 and '' not in v:
                k2, v2 = list(v.items())[0]
                made[k + k2] = v2
            else:
                made[k] = v

        return made

    @classmethod
    def Trie(self, strings):
        '''
        Trie
        an n-ary string character tree
        ref: https://en.wikipedia.org/wiki/Trie
        '''
        root = {}
        for word in strings:
            d = root
            for token in self.tokenize(word):
                d = d.setdefault(token, {})
            d[''] = {}
        return root

    @classmethod
    def tokenize(self, word):
        return iter(list(word))

class Serialize:
    def __init__(self, dawg):
        self.dawg = dawg

    @property
    def serialize(self):
        return self.serialize_regex(self.dawg)

    def serialize_regex(self, d, level=0):
        if d and self.is_char_class(d):
            s = self.as_char_class(d.keys())
        elif d and self.all_suffixes_identical(d):
            v = list(d.values())[0]
            if self.all_len1(d):
                s = self.as_charclass(d.keys())
            elif self.is_optional_char_class(d):
                s = self.as_opt_charclass(d.keys())
            elif self.is_optional(d):
                s = self.as_optional_group(d.keys())
            else:
                s = self.as_group(d.keys())
            s += self.serialize_regex(v, level=level + 1)
        elif self.is_optional_char_class(d):
            s = self.as_opt_charclass(d.keys())
        elif self.is_optional(d):
            s = self.opt_group(escape(sorted(list(d.keys()))[1])) + '?'
        else:
            bysuff = self.suffixes(d)
            if len(bysuff) < len(d):
                suffixed = [self.repr_keys(k, do_group=(level > 0)) +
                            self.serialize_regex(v, level=level + 1)
                            for v, k in bysuff]
                s = self.group(suffixed)
            else:
                grouped = [k + (self.serialize_regex(v, level=level + 1) if v else '')
                           for k, v in sorted(d.items())]
                s = self.group(grouped)
        return s

    def repr_keys(self, l, do_group=True):
        if self.all_len1(l):
            return self.as_charclass(l)
        if self.all_len01(l):
            return self.as_opt_charclass(l)
        return self.as_group(l, do_group=do_group)

    def suffixes(self, d):
        return sorted(((k, [a for a, _ in v])
                        for k, v in itertools.groupby(sorted(d.items(),
                                            key=lambda x: repr(self.emptyish(x[0]))),
                                            key=lambda x: self.emptyish(x[1]))),
                        key=lambda x: (repr(x[1]), repr(x[0])))

    def emptyish(self, x):
        if not x or x == {'': {}}:
            return {}
        return x

    def group(self, strings, do_group=True):
        if self.is_optional_strings(strings):
            return self.as_optional_group(strings)
        s = '|'.join(strings)
        if do_group and (len(strings) > 1 or ('|' in s and '(?:' not in s)):
            s = ('(?:' if len(strings) > 1 else '(') + s + ')'
        return s

    def opt_group(self, s):
        if len(s) - s.count('\\') > 1:
            s = ('(?:' if len(s.split()) > 1 else '(') + s + ')'
        return s

    def as_group(self, l, do_group=True):
        l = sorted(l)
        suffix = self.longest_suffix(l) if len(l) > 1 else ''
        if suffix:
            lensuff = len(suffix)
            prefixes = [x[:-lensuff] for x in l]
            if self.all_len1(prefixes):
                s = self.as_char_class(prefixes)
            else:
                s = self.group(prefixes)
            s += suffix
        else:
            s = self.group(l, do_group=do_group)
        return s

    def longest_prefix_2strings(self, x, y, longest):
        length = min(min(len(x), len(y)), longest)
        for i in range(1, length + 1):
            if x[:i] != y[:i]:
                return i - 1
        return length

    def longest_suffix(self, strings):
        return self.longest_prefix([s[::-1] for s in copy.copy(strings)])

    def longest_prefix(self, strings):
        if not strings:
            return ''
        prefix = strings[0]
        longest = min(len(s) for s in strings)
        for i in range(1, len(strings)):
            longest = self.longest_prefix_2strings(prefix, strings[i], longest)
            if longest == 0:
                return ''
        return prefix[:longest][::-1]

    def as_optional_group(self, strings):
        strings = sorted(strings)
        assert strings[0] == ''
        j = strings[1:]
        if not j:
            return ''
        s = '|'.join(j)
        if len(j) > 1 or len(j[0]) > 1 or s.endswith('?') or '|' in s or '(?:' in s:
            s = ('(?:' if len(j) > 1 else '(') + s + ')'
        return s + "?"

    def is_optional(self, d):
        if len(d) == 2:
            items = sorted(list(d.items()))
            return (not items[0][0] and (
                    not items[1][1] or items[1][1] == {'': {}}))
        return False

    def is_optional_char_class(self, d):
        return (self.all_len01(d.keys()) and
                self.all_values_not(d))

    def is_char_class(self, d):
        return (self.all_len1(d.keys()) and
                self.all_values_not(d))

    def is_optional_strings(self, strings):
        return not all(s for s in strings)

    def as_char_class(self, strings):
        s = ''.join(sorted(strings))
        if len(s) > 1:
            s = '[' + s + ']'
        return s

    def all_len1(self, l):
        return all(len(k) == 1 for k in l)

    def all_len01(self, l):
        return set(map(len, l)) == {0, 1}

    def all_values_not(self, d):
        return all(not v or v == {'': {}} for v in d.values())

    def all_suffixes_identical(self, d):
        vals = list(d.values())
        return len(vals) > 1 and len(set(map(str, vals))) == 1

    def as_charclass(self, l):
        s = self.condense_range(l)
        if len(l) > 1:
            s = '[' + s + ']'
        return s

    def as_opt_charclass(self, l):
        s = self.condense_range(l)
        if len(l) > 2:
            s = '[' + s + ']'
        else:
            s = escape(s)
        return s + "?"

    def condense_range(self, chars):
        chars = sorted([c for c in chars if c])
        l = []
        while chars:
            i = 1
            while i < len(chars):
                if chars[i] != chr(ord(chars[i - 1]) + 1):
                    break
                i += 1
            if i <= 1:
                l.append(str(chars[0]))
            elif i == 2:
                l.append('{}{}'.format(chars[0], chars[1]))
            else:
                l.append('{}-{}'.format(chars[0], chars[i - 1]))
            if i == len(chars):
                chars = []
            else:
                del chars[:i]
        return ''.join(l)

def match(strings):
    '''
    convenience wrapper for generating one regex from a list of strings
    '''

    if not isinstance(strings, list):
        strings = StringSet(strings)
    strings = map(escape, strings)

    trie = Rgxg.Trie(strings)
    dawg = Rgxg.build(trie)
    return Serialize(dawg).serialize

if __name__ == "__main__":
    import sys
    print(match(sys.argv[1:]))
