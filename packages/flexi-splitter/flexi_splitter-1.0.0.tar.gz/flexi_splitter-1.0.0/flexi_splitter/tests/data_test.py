#!/usr/bin/env python3
# -*-coding:Utf-8 -*

"""
This module provides data for the unitary tests for the flexi_splitter project
"""
from io import StringIO
from Bio import SeqIO
from .. import flexi_splitter
# code to create yaml toy

"""
single end
"""

CONFIG_TOY = {
    'RT': {
        'coords': {
            'reads': 0,
            'start': 6,
            'stop': 13,
            'header': False,
            'start_update': 6,
            'stop_update': 13,
        },
        'samples': [
            {'name': "RT1", 'seq': "TAGTGCC"},
            {'name': "RT2", 'seq': "GCTACCC"},
            {'name': "RT3", 'seq': "ATCGACC"},
            {'name': "RT4", 'seq': "CGACTCC"}
        ]
    },
    'PCR': {
        'coords': {
            'reads': 0,
            'start': 0,
            'stop': 5,
            'header': True,
            'start_update': 0,
            'stop_update': 5,
        },
        'samples': [
            {'name': "PCR1", 'seq': "NCAGTG"},
            {'name': "PCR2", 'seq': "CGATGT"},
            {'name': "PCR3", 'seq': "TTAGGC"},
            {'name': "PCR4", 'seq': "TGACCA"},
            {'name': "PCR5", 'seq': "NGAACG"}
        ]
    },
    'UMI': {
        'coords': {
            'reads': 0,
            'start': 0,
            'stop': 5,
            'header': False,
            'start_update': 0,
            'stop_update': 5,
        },
    },
    'conditions': {
        'wt': ['RT1', 'PCR1'],
        'ko': ['RT2', 'PCR2'],
        'unassigned': None
        }
}

RT_barcode_single = 'TAGTGCC'
PCR_barcode_single = 'NCAGTG'
umi_barcode_single = 'NTTCTC'
read_single = "@K00201:182:HM3TMBBXX:6:2228:17706:1226 1:N:0:NCAGTG\n\
NTTCTCTAGTGCCTCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
#AAFFJJJJJJAAAFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
read_trim_single = "@K00201:182:HM3TMBBXX:6:2228:17706:1226 1:N:0:NCAGTG \n\
TCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
AFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
SeqIO_single = SeqIO.read(StringIO(read_single), "fastq")
Reads_single = flexi_splitter.Reads(StringIO(read_single))
SeqIO_trim_single = SeqIO.read(StringIO(read_trim_single), "fastq")
Reads_trim_single = flexi_splitter.Reads(StringIO(read_trim_single))

umi_readnoumi = "@K00201:182:HM3TMBBXX:6:2228:17706:1226 1:N:0:NCAGTG\n\
TAGTGCCTCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
JJJJJAAAFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
SeqIO_single_noumi = SeqIO.read(StringIO(umi_readnoumi), "fastq")
Reads_single_noumi = flexi_splitter.Reads(StringIO(umi_readnoumi))

umi_readnoRT = "@K00201:182:HM3TMBBXX:6:2228:17706:1226 1:N:0:NCAGTG\n\
NTTCTCTCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
#AAFFJAFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
SeqIO_single_noRT = SeqIO.read(StringIO(umi_readnoRT), "fastq")
Reads_single_noRT = flexi_splitter.Reads(StringIO(umi_readnoRT))

umi_read = "@K00201:182:HM3TMBBXX:6:2228:17706:1226_NTTCTC 1:N:0:NCAGTG\n\
NTTCTCTAGTGCCTCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
#AAFFJJJJJJAAAFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
SeqIO_umi_single = SeqIO.read(StringIO(umi_read), "fastq")
Reads_umi_single = flexi_splitter.Reads(StringIO(umi_read))

umi_readnoumi = "@K00201:182:HM3TMBBXX:6:2228:17706:1226_NTTCTC 1:N:0:NCAGTG\n\
TAGTGCCTCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
JJJJJAAAFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
SeqIO_umi_single_noumi = SeqIO.read(StringIO(umi_readnoumi), "fastq")
Reads_umi_single_noumi = flexi_splitter.Reads(StringIO(umi_readnoumi))

umi_readnoRT = "@K00201:182:HM3TMBBXX:6:2228:17706:1226_NTTCTC 1:N:0:NCAGTG\n\
NTTCTCTCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
#AAFFJAFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
SeqIO_umi_single_noRT = SeqIO.read(StringIO(umi_readnoRT), "fastq")
Reads_umi_single_noRT = flexi_splitter.Reads(StringIO(umi_readnoRT))

fully_trimmed = "@K00201:182:HM3TMBBXX:6:2228:17706:1226_NTTCTC 1:N:0:NCAGTG\n\
TCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG\n\
+\n\
AFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-\n"
SeqIO_umi_single_noRT = SeqIO.read(StringIO(fully_trimmed), "fastq")
Reads_fully_trimmed = flexi_splitter.Reads(StringIO(fully_trimmed))

"""
paired-end
"""

CONFIG_TOY_PAIRED = {
    'RT': {
        'coords': {
            'reads': 0,
            'start': 6,
            'stop': 13,
            'header': False
        },
        'samples': [
            {'name': "RT1", 'seq': "TAGTGCC"},
            {'name': "RT2", 'seq': "GCTACCC"},
            {'name': "RT3", 'seq': "ATCGACC"},
            {'name': "RT4", 'seq': "CGACTCC"}
        ]
    },
    'PCR': {
        'coords': {
            'reads': 2,
            'start': 0,
            'stop': 5,
            'header': False
        },
        'samples': [
            {'name': "PCR1", 'seq': "NCAGTG"},
            {'name': "PCR2", 'seq': "CGATGT"},
            {'name': "PCR3", 'seq': "TTAGGC"},
            {'name': "PCR4", 'seq': "TGACCA"},
            {'name': "PCR5", 'seq': "NGAACG"},
            {'name': "PCR6", 'seq': "NCAACA"}
        ]
    },
    'UMI': {
        'coords': {
            'reads': 0,
            'start': 0,
            'stop': 5,
            'header': False
        },
    },
    'conditions': {
        'wt': ['RT1', 'PCR1'],
        'ko': ['RT2', 'PCR2'],
        'sample_paired' : ['RT1', 'PCR6']
        }
}

read_paired_1 = "@GWNJ-0842:360:GW1809071399:6:1101:18243:1625 1:N:0:1\n\
ATATCGTAGTGCCATAGAATTCATTTTTGACCCAGATGATGGTTCCTTTACAGAACAATAAAATGGCTGAACATTTTCACAAATAGAGTGTAACGAAGTCTGGATTTCTGATACCTTGTCATTTGGGGGATTTTAGATCGGAAGAGCACA\n\
+\n\
AAAFFJJJJAJJJJJJF<FFJJJ-JJJJJFFFJJJFFJ-FJJAJJ7AJJFJJJAFFJJJJJ-JJ<F7A77<AJJJJFJJJJJJJJJJJJ-JJJJJJJFJAFJJJJJ<-FFFFJA<JJFF-7FJJJJJFJ-FFJJ-<AJFJFFFJ-AFJ<A\n"
read_paired_2 = "@GWNJ-0842:360:GW1809071399:6:1101:18243:1625 2:N:0:1\n\
NTCAGCTTTACCGTCTTTCCAGAAACTGTTCCACGTATCGGCAACAGCGTTATCAATACCATGAAAAATATCAACCACACCAGAAGCAGCATCAGTGACCACATTAGAAATATCCTGTGCAATAGCGCCAATATGAAACGAGCCATACCG\n\
+\n\
#AAFFJFJ<JJJFJJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJJ<JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJJFF7AJAFJAFJJJJ\n"
read_paired_3 = "@GWNJ-0842:360:GW1809071399:6:1101:18243:1625 2:N:0:1\n\
NCAACA\n\
+\n\
#AAFF-\n"

SeqIO_paired_1 = SeqIO.read(StringIO(read_paired_1), "fastq")
SeqIO_paired_2 = SeqIO.read(StringIO(read_paired_2), "fastq")
SeqIO_paired_3 = SeqIO.read(StringIO(read_paired_3), "fastq")
Reads_paired_1 = flexi_splitter.Reads(StringIO(read_paired_1))
Reads_paired_2 = flexi_splitter.Reads(StringIO(read_paired_2))
Reads_paired_3 = flexi_splitter.Reads(StringIO(read_paired_3))

RT_barcode_paired = 'TAGTGCC'
PCR_barcode_paired = 'NCAACA'
umi_barcode_paired = 'ATATCG'

results_read_paired_1 = "@GWNJ-0842:360:GW1809071399:6:1101:18243:1625_ATATCG 1:N:0:1\n\
ATAGAATTCATTTTTGACCCAGATGATGGTTCCTTTACAGAACAATAAAATGGCTGAACATTTTCACAAATAGAGTGTAACGAAGTCTGGATTTCTGATACCTTGTCATTTGGGGGATTTTAGATCGGAAGAGCACA\n\
+\n\
JJJF<FFJJJ-JJJJJFFFJJJFFJ-FJJAJJ7AJJFJJJAFFJJJJJ-JJ<F7A77<AJJJJFJJJJJJJJJJJJ-JJJJJJJFJAFJJJJJ<-FFFFJA<JJFF-7FJJJJJFJ-FFJJ-<AJFJFFFJ-AFJ<A\n"
results_read_paired_2 = "@GWNJ-0842:360:GW1809071399:6:1101:18243:1625 2:N:0:1\n\
NTCAGCTTTACCGTCTTTCCAGAAACTGTTCCACGTATCGGCAACAGCGTTATCAATACCATGAAAAATATCAACCACACCAGAAGCAGCATCAGTGACCACATTAGAAATATCCTGTGCAATAGCGCCAATATGAAACGAGCCATACCG\n\
+\n\
#AAFFJFJ<JJJFJJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJJ<JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJJFF7AJAFJAFJJJJ\n"
results_read_paired_3 = "@GWNJ-0842:360:GW1809071399:6:1101:18243:1625 2:N:0:1\n\
\n\
+\n\
\n"
SeqIO_results_paired_1 = SeqIO.read(StringIO(read_paired_1), "fastq")
SeqIO_results_paired_2 = SeqIO.read(StringIO(read_paired_2), "fastq")
SeqIO_results_paired_3 = SeqIO.read(StringIO(read_paired_3), "fastq")
Reads_results_paired_1 = flexi_splitter.Reads(StringIO(read_paired_1))
Reads_results_paired_2 = flexi_splitter.Reads(StringIO(read_paired_2))
Reads_results_paired_3 = flexi_splitter.Reads(StringIO(read_paired_3))
