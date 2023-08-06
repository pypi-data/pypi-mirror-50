import math

class Range:
    def __init__(self, _min, _max):
        self._min = int(_min)
        self._max = int(_max)
        assert self._min < self._max, "%s < %s" % (_max, _min)

    @property
    def serialize(self):
        return self.regex_for_range(self._min, self._max)

    def bounded_regex_for_range(self, min_, max_):
        return r'\b({})\b'.format(regex_for_range(min_, max_))

    def regex_for_range(self, min_, max_):
        """
        > regex_for_range(12, 345)
        '1[2-9]|[2-9]\d|[1-2]\d{2}|3[0-3]\d|34[0-5]'
        """
        positive_subpatterns = []
        negative_subpatterns = []
        if min_ < 0:
            min__ = 1
            if max_ < 0:
                min__ = abs(max_)
            max__ = abs(min_)
            negative_subpatterns = self.split_to_patterns(min__, max__)
            min_ = 0
        if max_ >= 0:
            positive_subpatterns = self.split_to_patterns(min_, max_)
        negative_only_subpatterns = ['-' + val for val in negative_subpatterns if val not in positive_subpatterns]
        positive_only_subpatterns = [val for val in positive_subpatterns if val not in negative_subpatterns]
        intersected_subpatterns = ['-?' + val for val in negative_subpatterns if val in positive_subpatterns]
        subpatterns = negative_only_subpatterns + intersected_subpatterns + positive_only_subpatterns
        return '|'.join(subpatterns)

    def split_to_patterns(self, min_, max_):
        subpatterns = []
        start = min_
        for stop in self.split_to_ranges(min_, max_):
            subpatterns.append(self.range_to_pattern(start, stop))
            start = stop + 1
        return subpatterns

    def split_to_ranges(self, min_, max_):
        stops = {max_}
        nines_count = 1
        stop = self.fill_by_nines(min_, nines_count)
        while min_ <= stop < max_:
            stops.add(stop)
            nines_count += 1
            stop = self.fill_by_nines(min_, nines_count)
        zeros_count = 1
        stop = self.fill_by_zeros(max_ + 1, zeros_count) - 1
        while min_ < stop <= max_:
            stops.add(stop)
            zeros_count += 1
            stop = self.fill_by_zeros(max_ + 1, zeros_count) - 1
        stops = list(stops)
        stops.sort()
        return stops

    def fill_by_nines(self, integer, nines_count):
        return int(str(integer)[:-nines_count] + '9' * nines_count)

    def fill_by_zeros(self, integer, zeros_count):
        return integer - integer % 10 ** zeros_count

    def range_to_pattern(self, start, stop):
        pattern = ''
        any_digit_count = 0
        for start_digit, stop_digit in zip(str(start), str(stop)):
            if start_digit == stop_digit:
                pattern += start_digit
            elif start_digit != '0' or stop_digit != '9':
                pattern += '[{}-{}]'.format(start_digit, stop_digit)
            else:
                any_digit_count += 1
        if any_digit_count:
            pattern += r'\d'
        if any_digit_count > 1:
            pattern += '{{{}}}'.format(any_digit_count)
        return pattern

def match(_min, _max):
    ch = Range(_min, _max)
    return ch.serialize

if __name__ == "__main__":
    import sys
    print(match(sys.argv[1], sys.argv[2]))

