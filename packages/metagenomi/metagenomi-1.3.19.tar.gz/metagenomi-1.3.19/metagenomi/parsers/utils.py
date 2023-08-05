import re
import collections
# import sys
# import os
import subprocess
import pcdhit

from statistics import mean


def get_length_deviation(seqs):
    most_common_length = get_most_common_length(seqs)
    deviations = [abs(most_common_length-len(i)) for i in seqs]
    return sum(deviations)/len(seqs)


def get_most_common_length(seqs):
    lengths = [len(i) for i in seqs]

    common = collections.Counter(lengths).most_common()
    if len(common) > 1:
        return mean([i[0] for i in common])
    else:
        return common[0][0]


def cluster_seqs(seqs, threshold=0.8, verbose=False):
    records = [('>fake_header', i) for i in seqs]
    if verbose is False:
        filtered_records = pcdhit.filter(records, threshold)

    clusters = []
    for i in filtered_records:
        seq = i[1]
        clusters.append(seq)
    return clusters


class MgError(Exception):
    """Base class for mg exceptions."""


class MuscleNotFoundError(MgError):
    """cdhit not installed."""

    def __init__(self):
        message = 'Check if muscle is installed.'
        super().__init__(message)


def align(seqs, output=None, verbose=False):
    '''
    TODO: Verbosity not implemented
    '''
    from Bio import AlignIO
    muscle_exe = pcdhit.is_command(['muscle', '/tmp/muscle'])
    if muscle_exe is None:
        raise MuscleNotFoundError

    records = [('>fake_header', i) for i in seqs]
    with pcdhit.opentf() as fin, pcdhit.opentf() as fout:
        pcdhit.print_input_fasta(records, fin)
        call_muscle(muscle_exe, fin, fout)

        aln = AlignIO.read(fout, "fasta")
    return aln


def call_muscle(muscle_exe, fin, fout):
    command = '%s -in %s -out %s' % (muscle_exe, fin.name, fout.name)
    proc = subprocess.Popen(command, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return


def avg_perc_identity(aln):
    avgs = []
    for a in range(0, len(aln[0])):
        s = aln[:, a]
        consensus = collections.Counter(s).most_common(1)[0]
        perc_consensus = consensus[1]/len(s)
        avgs.append(perc_consensus)
    return sum(avgs)/len(avgs)


def perc_identity(aln):
    i = 0
    for a in range(0, len(aln[0])):
        s = aln[:, a]
        if s == len(s) * s[0]:
            i += 1
    return 100*i/float(len(aln[0]))


def orient_repeat(repeat):
    # Y = C | T
    repeat_GYYfwd = re.compile(r'^G[CT][CT]')
    repeat_GYYrev = re.compile(r'[AG][AG]C$')
    motif_fwd = re.compile(r'ATTGAAA[ATGC]$')
    motif_rev = re.compile(r'^[ATGC]TTTCAAT')

    direction = None
    forward = None
    reverse = None
    score = 0

    # LEVEL 1
    bits = []
    if repeat.startswith("G"):
        forward = True
        direction = '+'
        bits.append(1)
        score = 1
    else:
        bits.append(0)

    if repeat.endswith("C"):
        reverse = True
        direction = '-'
        bits.append(1)
        score = 1
    else:
        bits.append(0)

    if forward and reverse:
        direction = None
        score = 0


    # LEVEL 2
    forward = None
    reverse = None
    if re.search(repeat_GYYfwd, repeat):
        forward = True
        direction = '+'
        bits.append(1)
        score = 2
    else:
        bits.append(0)

    if re.search(repeat_GYYrev, repeat):
        reverse = True
        direction = '-'
        bits.append(1)
        score = 2
    else:
        bits.append(0)

    if forward and reverse:
        direction = None
        score = 0

    # LEVEL 3
    forward = None
    reverse = None
    if repeat.startswith("GTT"):
        forward = True
        direction = '+'
        bits.append(1)
        score = 3
    else:
        bits.append(0)

    if repeat.endswith("AAC"):
        reverse = True
        direction = '-'
        bits.append(1)
        score = 3
    else:
        bits.append(0)

    if forward and reverse:
        direction = None
        score = 0

    # LEVEL 4
    forward = None
    reverse = None
    if re.search(motif_fwd, repeat):
        direction = '+'
        forward = True
        bits.append(1)
        score = 4
    else:
        bits.append(0)

    if re.search(motif_rev, repeat):
        reverse = True
        direction = '-'
        bits.append(1)
        score = 4
    else:
        bits.append(0)

    if forward and reverse:
        score = 0
        return (None, 0, bits)
    if forward or reverse:
        return (direction, score, bits)

    return (direction, score, bits)
