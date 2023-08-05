# import collections
# import pcdhit
from math import log10

from statistics import stdev
from metagenomi.helpers import most_frequent
from metagenomi.parsers import utils


'''
Class used to parse a single entry in a minced output file
along with a script for splitting up a minced file

'''


def split_minced_output(infile):
    '''
    input = minced output file
    returns: two arrays, one containing crispr names and the other containing
    arrays
    '''
    total_crisprs = []
    names = []
    with open(infile, 'r') as file:
        i = 0
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].rstrip()
            if 'Sequence ' in line:
                seq_name = line.split(' ')[1][1:-1]
                seq_line = line

            if 'CRISPR' in line:
                num = line.split(' ')[1]
                name = seq_name + f'_CRISPR_{num}'
                new_array = [seq_line] + [''] + [line]
                j = i+1
                while 'Repeats:' not in lines[j]:
                    new_array.append(lines[j].rstrip())
                    j += 1
                new_array.append(lines[j].rstrip())
                new_array.append('')

                names.append(name)
                total_crisprs.append(new_array)

    # names and arrays are in conserved order
    return(names, total_crisprs)


class ShortFeature:
    '''
    Class used to represent either a spacer or a repeat.

    '''
    def __init__(self, name, start, stop, contig, seq, feature_type, strand=None, score=None, parent=None):
        self.name = name
        self.start = int(start)
        self.stop = int(stop)
        self.contig = contig
        self.strand = strand
        self.seq = seq
        self.mgid = self.name[:22]
        self.score = score
        self.parent = parent
        self.dummy = 'DUMMY'
        self.feature_type = feature_type
        if self.feature_type == 'repeat' and self.strand is None:
            self.strand, self.score, self.bits = utils.orient_repeat(self.seq)
            self.bits = [str(i) for i in self.bits]
            self.bitstring = int(''.join(self.bits), 2)
            self.combined_score = float(f'{self.score}.{self.bitstring}')

    def export_sql(self, source='proprietary', parent_id=None, cluster_id=None):
        # created_at = time.time()
        # updated_at = time.time()
        d = {'name': self.name, 'contig_name': self.contig,
             'feature_start': self.start, 'feature_end': self.stop,
             'strand': self.strand, 'mg_assembly_id': self.mgid,
             'source': source, 'feature_type': self.feature_type,
             'parent': parent_id, 'cluster': cluster_id, 'score': self.combined_score}

        return d

    def get_header(self):
        '''
        returns prodigal style header
        '''

        if self.strand:
            if self.strand == '+':
                strand = 1
            else:
                strand = -1
        else:
            strand = 0
        header = f'>{self.name} # {self.start} # {self.stop} # '
        header += f'{strand} # {self.combined_score} # {self.feature_type}'
        return header


class Crispr:
    '''
    Class used to represent a minced output file.

    '''
    def __init__(self, name, a):
        self.name = name
        self.spacers = []
        self.repeats = []
        self.spacer_seqs = []
        self.repeat_seqs = []
        self.pos = []

        self.parse_crispr(a)

    def parse_crispr(self, a):
        for i in range(len(a)):
            line = a[i]
            # If first line
            if 'Sequence' in line:
                self.seq = line.split(' ')[1][1:-1]
                self.seqlen = int(line.split('(')[1][:-3])
                i += 1
            else:
                if 'CRISPR' in line:
                    self.number = int(line.split(' ')[1])
                    arraystart = int(line.split(': ')[1].split(' -')[0])
                    arrayend = int(line.split('- ')[1].rstrip())
                    self.range = (arraystart, arrayend)

                else:
                    if 'POSITION' in line:
                        start = i+2
                    else:
                        if 'Repeats: ' in line:
                            rl = line.split(': ')[2].split('\t')[0]
                            self.avgRepeatLen = int(rl)
                            sl = line.split(': ')[3].rstrip()
                            self.avgSpacerLen = int(sl)

                            end = i-1
                            array = a[start:end]
                            self.parse_array(array)

    def parse_array(self, array):
        c = 1
        for x in array:
            p = int(x.split('\t')[0])
            self.pos.append(p)

            rseq = x.split('\t')[2]
            rlen = len(rseq)
            repeat_name = f'{self.name}_repeat_{c}'
            rend = p+rlen
            # name, start, stop, contig, strand, seq, feature_type
            r = ShortFeature(repeat_name, p, rend, self.seq, rseq, 'repeat')
            self.repeats.append(r)
            self.repeat_seqs.append(rseq)
            if len(x.split('\t')) > 3:
                sseq = x.split('\t')[3]
                slen = len(sseq)
                sname = f'{self.name}_spacer_{c}'
                send = rend+slen
                s = ShortFeature(sname, rend, send, self.seq, sseq, 'spacer')
                self.spacers.append(s)
                self.spacer_seqs.append(sseq)
            c += 1

    def check_motif_match(self):
        '''
        Does a sequence end with ATTGAAA(N)?
        or does a sequence begin with the reverse complement?
        '''
        motif = 'ATTGAAA'
        rev_motif = 'TTTCAAT'

        for r in self.repeat_seqs:
            if r[:-1].endswith(motif):
                return True
            if r.endswith(motif):
                return True
            if r.startswith(rev_motif):
                return True
            if r[1:].startswith(rev_motif):
                return True
        return False

    def calculate_score(self):
        self.motif = self.check_motif_match()
        aln = utils.align(self.repeat_seqs)
        self.avg_repeat_identity = utils.avg_perc_identity(aln)
        self.spacer_clusters = utils.cluster_seqs(self.spacer_seqs)
        self.repeat_clusters = utils.cluster_seqs(self.repeat_seqs)
        self.repeat_length_deviation = utils.get_length_deviation(self.repeat_seqs)
        self.spacer_length_deviation = utils.get_length_deviation(self.spacer_seqs)
        self.score = self.score_array()

    def score_array(self):
        score = 0
        # 3 : either +3 or 0
        # Repeat has at	least 23 bases and ATTGAAA(N) at the end
        if len(self.repeats) > 22 and self.motif:
            score += 3

        # 4 : range(0, 1)
        # 	Overall repeat identity	within	an	array
        s = (self.avg_repeat_identity*100 - 80)/20
        score += s

        # 5: -1.5 or 0
        # The repeats in the array do not form one sequence similarity cluster
        num_repeat_clusters = len(self.repeat_clusters)
        if num_repeat_clusters > 1:
            score = score - 1.5

        # 6 : range(-3, +1)
        # Scoring the repeat lengths
        s = self.repeat_length_deviation*(-2/5) + 1
        score += s

        # 7 : range(-3, +3)
        # Scoring the spacer lengths
        s = self.spacer_length_deviation*(-1) + 3
        if s < -3:
            s = -3
        score += s

        # 8 : range(-3, +1)
        # Overall spacer identity
        num_spacer_clusters = len(self.spacer_clusters)
        if num_spacer_clusters <= len(self.spacers)/2:
            s = -3
        else:
            s = 0.2*num_spacer_clusters
            if s > 1:
                s = 1

        score += s

        # 9 : range(0, 1)
        # Scoring total number of identical repeats
        total_repeats = len(self.repeats)
        most_frequent_repeat = most_frequent(self.repeat_seqs)
        m = [i for i in self.repeat_seqs if i != most_frequent_repeat]
        total_mutated = len(m)
        if total_mutated > 0:
            s = log10(total_repeats) - log10(total_mutated)
        else:
            s = log10(total_repeats)
        if s > 1:
            s = 1
        score += s

        return score

    def get_consensus_repeat(self):
        pass

    def get_spacers(self):
        return self.spacer_seqs

    def get_range(self):
        return self.range

    def get_num_spacers(self):
        return len(self.spacer_seqs)

    def get_num_repeats(self):
        return len(self.repeat_seqs)

    def get_unique_repeats(self):
        return set(self.repeat_seqs)

    def get_name(self):
        return self.name

    def get_repeats(self):
        return self.repeat_seqs

    def get_seqlen(self):
        return self.seqlen

    def get_seq(self):
        return self.seq

    def get_avg_repeat_length(self):
        return self.avgRepeatLen

    def get_avg_spacer_length(self):
        return self.avgSpacerLen

    def get_spacer_stdev(self):
        slengths = [len(i) for i in self.spacer_seqs]
        return stdev(slengths)

    def get_repeat_stdev(self):
        rlengths = [len(i) for i in self.repeat_seqs]
        return stdev(rlengths)

    def get_longest_spacer(self):
        return max(self.spacer_seqs, key=len)

    def get_shortest_spacer(self):
        return min(self.spacer_seqs, key=len)

    def __str__(self):
        rep = f'{self.name}\nRepeats: {self.repeat_seqs}\n'
        rep += f'Spacers: {self.spacer_seqs}'
        return rep

    def to_dict(self):
        '''
        ['array_name', 'contig', 'contig_length', 'array_start',
         'array_end', 'avg_repeat_len', 'avg_spacer_len', 'num_repeats',
         'repeat_mode_dev', 'spacer_mode_dev', 'min_repeat_len',
         'min_spacer_len', 'max_spacer_len', 'max_repeat_len',
         'array_quality']
         Used to generate minced tsv
        '''
        self.calculate_score()
        spacer_lengths = [len(i) for i in self.spacer_seqs]
        repeat_lengths = [len(i) for i in self.repeat_seqs]

        d = {'name': self.get_name(), 'contig': self.get_seq(),
             'contig_length': self.get_seqlen(), 'start': self.get_range()[0],
             'end': self.get_range()[1],
             'avg_repeat_len': self.get_avg_repeat_length(),
             'avg_spacer_len': self.get_avg_spacer_length(),
             'num_repeats': self.get_num_repeats(),
             'min_repeat_length': min(repeat_lengths),
             'max_repeat_len': max(repeat_lengths),
             'min_spacer_len': min(spacer_lengths),
             'max_spacer_len': max(spacer_lengths),
             'spacer_clusters': len(self.spacer_clusters),
             'repeat_clusters': len(self.repeat_clusters),
             'repeat_length_deviation': self.repeat_length_deviation,
             'spacer_length_deviation': self.spacer_length_deviation,
             'avg_repeat_identity': self.avg_repeat_identity,
             'score': self.score,
             'motif_ATTGAAAN': self.motif
             }

        return d
