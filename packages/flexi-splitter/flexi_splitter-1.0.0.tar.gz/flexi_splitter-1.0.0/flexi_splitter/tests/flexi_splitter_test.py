#!/usr/bin/env python3
# -*-coding:Utf-8 -*

"""
This module provides unitary tests for the flexi_splitter project
"""

import unittest
import copy
import yaml
import sys
from .. import flexi_splitter
from . import data_test


class ReadsClassTest(unittest.TestCase):
    """
    all the tests for the Reads class
    """
    def test_init(self):
        """
        all the tests on loading the config yaml file
        """
        self.assertEqual(
            str(data_test.Reads_paired_1),
            data_test.read_paired_1
        )

    def test_write(self):
        """
        all the tests on loading the config yaml file
        """
        self.assertEqual(
            str(data_test.Reads_paired_1),
            data_test.read_paired_1
        )



class ConfigLoadTest(unittest.TestCase):
    """
    all the tests for the fonctions loading the configuration
    """
    def test_loading_file(self):
        """
        all the tests on loading the config yaml file
        """
        self.assertEqual(
            flexi_splitter.load_yaml(
                path="flexi_splitter/tests/data/toy_file.yaml"),
            data_test.CONFIG_TOY
        )

    def test_loading_file_yamlerror(self):
        """
        all the tests on loading the config yaml file
        """
        try:
            flexi_splitter.load_yaml(
                path="flexi_splitter/tests/data/RNA_seq_sub1.fastq")
        except yaml.YAMLError:
            self.assertEqual(1, 1)

    def test_extracting_pos(self):
        """
        test on the adaptator position extraction
        """
        pos_object = {'reads': 0,
                      'start': 6,
                      'start_update': 6,
                      'stop': 13,
                      'stop_update': 13,
                      'header': False}
        self.assertEqual(
            flexi_splitter.extract_pos(
                config=flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file.yaml"),
                adaptator="RT"),
            pos_object
        )

    def test_list_adaptator_barcode(self):
        """
        test the list_adaptator_barcode function
        """
        self.assertEqual(
            flexi_splitter.list_adaptator_barcode(
                config=flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file.yaml"),
                adaptator="RT",
                ntuple=0
            ),
            {"RT1": "TAGTGCC",
             "RT2": "GCTACCC",
             "RT3": "ATCGACC",
             "RT4": "CGACTCC"})

    def test_list_adaptator_barcode_error(self):
        """
        test the list_adaptator_barcode function
        """
        try:
            flexi_splitter.list_adaptator_barcode(
                config=flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file.yaml"),
                adaptator="RT",
                ntuple=3)
        except KeyError:
            self.assertEqual(1, 1)


class ReadsReadTest(unittest.TestCase):
    """
    all the tests for reading the sequences
    """
    def test_adaptator_barcode_error(self):
        """
        test barcode error
        """
        try:
            flexi_splitter.test_adaptator(
                flexi_splitter.load_yaml(
                    "flexi_splitter/tests/data/toy_file.yaml"),
                "PCT",
                1
            )
        except KeyError:
            self.assertEqual(1, 1)

    def test_extract_coords_error(self):
        """
        test extraction of PCR barcode from config
        """
        try:
            flexi_splitter.test_adaptator(
                {
                    'RT': {
                        'coords2': {
                            'reads': 1,
                            'stop': 13,
                            'header': False
                        }
                    }
                },
                "RT",
                0
            )
        except KeyError:
            self.assertEqual(1, 1)

    def test_extract_start_error(self):
        """
        test extraction of PCR barcode from config
        """
        try:
            flexi_splitter.test_adaptator(
                {
                    'RT': {
                        'coords': {
                            'reads': 1,
                            'stop': 13,
                            'header': False
                        }
                    }
                },
                "RT",
                0
            )
        except KeyError:
            self.assertEqual(1, 1)

    def test_extract_stop_error(self):
        """
        test extraction of PCR barcode from config
        """
        try:
            flexi_splitter.test_adaptator(
                {
                    'RT': {
                        'coords': {
                            'reads': 1,
                            'start': 6,
                            'header': False
                        }
                    }
                },
                "RT",
                0
            )
        except KeyError:
            self.assertEqual(1, 1)

    def test_extract_reads_error(self):
        """
        test extraction of PCR barcode from config
        """
        try:
            flexi_splitter.test_adaptator(
                {
                    'RT': {
                        'coords': {
                            'start': 6,
                            'stop': 13,
                            'header': False
                        }
                    }
                },
                "RT",
                0
            )
        except KeyError:
            self.assertEqual(1, 1)

    def test_extract_reads_error_value(self):
        """
        test extraction of PCR barcode from config
        """
        try:
            flexi_splitter.test_adaptator(
                {
                    'RT': {
                        'coords': {
                            'reads': 1,
                            'start': 6,
                            'stop': 13,
                            'header': False
                        }
                    }
                },
                "RT",
                2
            )
        except ValueError:
            self.assertEqual(1, 1)

    def test_extract_barcode_umi(self):
        """
        test extraction of umi
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.extract_barcode_pos(
                reads=reads_test,
                start=0,
                stop=5,
                header=False)['seq'],
            data_test.umi_barcode_single
        )

    def test_extract_barcode_pos_header(self):
        """
        test extraction of umi
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.extract_barcode_pos(
                reads=reads_test,
                start=1,
                stop=3,
                header=True)['seq'],
            "AGT"
        )

    def test_extract_barcode_rt_from_pos(self):
        """
        test extraction of RT barcode from position
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.extract_barcode_pos(
                reads=reads_test,
                start=6,
                stop=13,
                header=False)['seq'],
            data_test.RT_barcode_single
        )

    def test_extract_barcode_pcr_from_pos(self):
        """
        test extraction of PCR barcode from position
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.extract_barcode_pos(reads_test,
                                             0,
                                             5,
                                             True)['seq'],
            data_test.PCR_barcode_single
        )

    def test_extract_barcode_rt(self):
        """
        test extraction of RT barcode from config
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.extract_barcode(
                reads=reads_test,
                config=flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file.yaml"),
                adaptator="RT",
                ntuple=0,
                verbose=True)['seq'],
            data_test.RT_barcode_single
        )

    def test_extract_barcode_pcr(self):
        """
        test extraction of PCR barcode from config
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.extract_barcode(
                reads=reads_test,
                config=flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file.yaml"),
                adaptator="PCR",
                ntuple=0
            )['seq'],
            data_test.PCR_barcode_single
        )

    def test_extract_barcode_error(self):
        """
        test extraction of PCR barcode from config
        """
        try:
            flexi_splitter.extract_pos(
                flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file.yaml"),
                "PCT")
        except KeyError:
            self.assertEqual(1, 1)


class ModifyReadTest(unittest.TestCase):
    """
    all tests that modify the read
    """

    def test_write_umi_in_header(self):
        """
        test writting umi in header
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.write_umi_in_header(
                reads=reads_test,
                config=data_test.CONFIG_TOY,
                adaptator='UMI',
                ntuple=0
            ).header,
            data_test.Reads_umi_single.header
        )

    def test_remove_barcode_umi_pos(self):
        """
        test removing umi with pos
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        reads_test2 = copy.deepcopy(data_test.Reads_single)
        reads_test3 = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcode_pos(
                reads=reads_test,
                start=0,
                stop=5,
                header=False).seq,
            data_test.Reads_single_noumi.seq
        )
        self.assertEqual(
            flexi_splitter.remove_barcode_pos(
                reads=reads_test2,
                start=0,
                stop=5,
                header=False).header,
            data_test.Reads_single_noumi.header
        )
        self.assertEqual(
            flexi_splitter.remove_barcode_pos(
                reads=reads_test3,
                start=0,
                stop=5,
                header=False).qual,
            data_test.Reads_single_noumi.qual
        )

    def test_remove_barcode_rt_pos_seq(self):
        """
        test removing rt with pos
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcode_pos(
                reads=reads_test,
                start=6,
                stop=13,
                header=False).seq,
            data_test.Reads_single_noRT.seq
        )

    def test_remove_barcode_rt_pos_description(self):
        """
        test removing rt with pos
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcode_pos(
                reads=reads_test,
                start=6,
                stop=13,
                header=False).header,
            data_test.Reads_single_noRT.header
        )

    def test_remove_barcode_rt_pos_qual(self):
        """
        test removing rt with pos
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcode_pos(
                reads=reads_test,
                start=6,
                stop=13,
                header=False).qual,
            data_test.Reads_single_noRT.qual
        )

    def test_remove_barcode_pos_header(self):
        """
        test remove of umi
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcode_pos(
                reads=reads_test,
                start=1,
                stop=3,
                header=True).header,
            "K00201:182:HM3TMBBXX:6:2228:17706:1226 1:N:0:NCG"
        )

    def test_remove_barcode(self):
        """
        test removing rt with config
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcode(
                reads=reads_test,
                config=data_test.CONFIG_TOY,
                adaptator="RT",
                ntuple=0
            ).seq,
            data_test.Reads_single_noRT.seq
        )

    def test_update_position(self):
        """
        test update_position function
        """
        config_rt_update = copy.deepcopy(data_test.CONFIG_TOY)
        config_rt_update['RT']['coords']['start_update'] = 0
        config_rt_update['RT']['coords']['stop_update'] = 7
        self.maxDiff = None
        self.assertEqual(
            flexi_splitter.update_position(config = data_test.CONFIG_TOY,
                                         adaptator = 'UMI',
                                         adapt = 'RT',
                                         adaptator_length = 6,
                                         ntuple = 0),
            config_rt_update
        )

    def test_update_config(self):
        """
        test position update after removing a barcode
        """
        config_rt_update = copy.deepcopy(data_test.CONFIG_TOY)
        config_rt_update['RT']['coords']['start_update'] = 0
        config_rt_update['RT']['coords']['stop_update'] = 7
        self.maxDiff = None
        self.assertEqual(
            flexi_splitter.update_positions(
                config=data_test.CONFIG_TOY,
                adaptator="UMI",
                ntuple=0
            ),
            flexi_splitter.load_yaml(
                path="flexi_splitter/tests/data/toy_file.yaml")
        )

    def test_update_config2(self):
        """
        test position update after removing a barcode
        """
        config = flexi_splitter.load_yaml(
            path="flexi_splitter/tests/data/toy_file.yaml")
        barcode_dic = flexi_splitter.create_barcode_dictionaries(
            config=config
        )
        config_rt_update = copy.deepcopy(data_test.CONFIG_TOY)
        config_rt_update['RT']['coords']['start_update'] = 0
        config_rt_update['RT']['coords']['stop_update'] = 7
        self.maxDiff = None
        reads_test = copy.deepcopy(data_test.Reads_single)
        reads_test2 = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.match_barcode(
                reads=reads_test,
                config=flexi_splitter.update_positions(
                    config=data_test.CONFIG_TOY,
                    adaptator="UMI",
                    ntuple=0
                ),
                adaptator="PCR",
                ntuple=0,
                barcode_dictionary=barcode_dic
            ),
            flexi_splitter.match_barcode(
                reads=reads_test2,
                config=data_test.CONFIG_TOY,
                adaptator="PCR",
                ntuple=0,
                barcode_dictionary=barcode_dic
            ),
        )

    def test_remove_barcodes(self):
        """
        test removing rt with config
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcodes(
                reads_test,
                ntuple=0,
                config=data_test.CONFIG_TOY,
            ).seq,
            data_test.Reads_trim_single.seq
        )
    def test_remove_barcodes_full(self):
        """
        test removing rt with config
        """
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.remove_barcodes(
                reads_test,
                ntuple=0,
                config=data_test.CONFIG_TOY,
            ).write(sys.stdout),
            data_test.Reads_fully_trimmed.write(sys.stdout)
        )


class SeachBarcodeTest(unittest.TestCase):
    """
    Tests function that search for barcode in reads
    """
    def test_barcode_search(self):
        """
        test search sample from barcode
        """
        config = flexi_splitter.load_yaml(
            path="flexi_splitter/tests/data/toy_file.yaml")
        barcode_dic = flexi_splitter.create_barcode_dictionaries(
            config=config
        )
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.match_barcode(
                reads=reads_test,
                config=config,
                adaptator="PCR",
                ntuple=0,
                barcode_dictionary=barcode_dic
            ),
            "PCR1"
        )

    def test_barcode_search_error(self):
        """
        test search sample from barcode
        """
        config = flexi_splitter.load_yaml(
            path="flexi_splitter/tests/data/toy_file.yaml")
        barcode_dic = flexi_splitter.create_barcode_dictionaries(
            config=config
        )
        reads_test = copy.deepcopy(data_test.Reads_single)
        try:
            flexi_splitter.match_barcode(
                reads=reads_test,
                config=config,
                adaptator="PCT",
                ntuple=0,
                barcode_dictionary=barcode_dic,
                verbose=True
            )
        except KeyError:
            self.assertEqual(1, 1)
        except ValueError:
            self.assertEqual(1, 1)

    def test_barcodes_search(self):
        """
        test search sample from list of barcode
        """
        config = flexi_splitter.load_yaml(
            path="flexi_splitter/tests/data/toy_file.yaml")
        barcode_dic = flexi_splitter.create_barcode_dictionaries(
            config=config
        )
        reads_test = copy.deepcopy(data_test.Reads_single)
        self.assertEqual(
            flexi_splitter.match_barcodes(
                reads=reads_test,
                config=config,
                ntuple=0,
                barcode_dictionary=barcode_dic
            ),
            ['RT1', 'PCR1']
        )

    def test_barcodes_2_sample(self):
        """
        test converting barcodes to  sample name
        """
        config = flexi_splitter.load_yaml(
            path="flexi_splitter/tests/data/toy_file.yaml")
        self.assertEqual(
            flexi_splitter.barcode_to_sample(
                barcodes=['RT1', 'PCR1'],
                config=config
            ),
            'wt'
        )

    def test_barcodes_2_sample_error(self):
        """
        test converting barcodes to  sample name
        """
        config = flexi_splitter.load_yaml(
            path="flexi_splitter/tests/data/toy_file.yaml")
        self.assertEqual(
            flexi_splitter.barcode_to_sample(
                barcodes=['RT3', 'PCR1'],
                config=config,
                verbose=True
            ),
            'unassigned'
        )


class HandleFastqTest(unittest.TestCase):
    """
    Tests handling fastq inputs
    """
    def test_reads_number(self):
        """
        test computing the list of reads number
        """
        self.assertEqual(
            flexi_splitter.list_reads_number(
                config=data_test.CONFIG_TOY_PAIRED
            ),
            3
        )

    def test_read_reads(self):
        """
        test
        """
        fin = open("flexi_splitter/tests/data/single_read.fastq")
        reads_list = list()
        reads_list.append(flexi_splitter.Reads())
        line_number = 0
        for line in fin :
            reads_list = flexi_splitter.read_reads( fins=[line],
                                                  reads_list=reads_list,
                                                  ntuple=[0],
                                                  line_number= line_number
                          )
            line_number +=1
        self.assertEqual(
            line_number,
            4
        )
        self.assertEqual(
            reads_list[0].header,
            data_test.Reads_single.header
        )
        self.assertEqual(
            reads_list[0].seq,
            data_test.Reads_single.seq
        )
        self.assertEqual(
            reads_list[0].qual,
            data_test.Reads_single.qual
        )
        self.assertEqual(
            reads_list[0].qual_str,
            data_test.Reads_single.qual_str
        )
        self.assertEqual(
            str(reads_list[0]),
            str(data_test.Reads_single)
        )

    def test_assign_reads_single(self):
        """
        test assigning single reads to the right sample
        """
        barcode_dic = flexi_splitter.create_barcode_dictionaries(
            config=flexi_splitter.load_yaml(
                path="flexi_splitter/tests/data/toy_file.yaml")
        )
        self.assertEqual(
            flexi_splitter.assign_reads(
                reads_list=[data_test.Reads_single],
                config=flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file.yaml"),
                barcode_dictionary=barcode_dic,
                verbose=True
            ),
            'wt'
        )

    def test_assign_reads_paired(self):
        """
        test assigning triplet of reads to the right sample
        """
        barcode_dic = flexi_splitter.create_barcode_dictionaries(
            config=flexi_splitter.load_yaml(
                path="flexi_splitter/tests/data/toy_file_paired.yaml")
        )
        self.assertEqual(
            flexi_splitter.assign_reads(
                reads_list=[data_test.Reads_paired_1,
                            data_test.Reads_paired_2,
                            data_test.Reads_paired_3],
                config=flexi_splitter.load_yaml(
                    path="flexi_splitter/tests/data/toy_file_paired.yaml"),
                barcode_dictionary=barcode_dic,
                verbose=True
            ),
            'sample_paired'
        )

    def test_parsing_reads(self):
        """
        test search sample from list of barcode
        """
        flexi_splitter.parse_ntuples_fastqs(
            fastqs=["flexi_splitter/tests/data/RNA_seq_sub1.fastq",
                    "flexi_splitter/tests/data/RNA_seq_sub2.fastq",
                    "flexi_splitter/tests/data/RNA_seq_Index.fastq"],
            config=flexi_splitter.load_yaml(
                path="flexi_splitter/tests/data/toy_file_paired.yaml"),
            results_path="../results/",
            ntuple_param=3,
            verbose=False
        )
        self.assertEqual(1, 1)

class ReadsClassTest(unittest.TestCase):
    """
    Tests Reads object
    """
    def readReads_header_test(self):
        """
        test assign header
        """
        self.assertEqual(
        data_test.Reads_single.header,
        "K00201:182:HM3TMBBXX:6:2228:17706:1226 1:N:0:NCAGTG"
        )

    def readReads_seq_test(self):
        """
        test assign seq
        """
        self.assertEqual(
        data_test.Reads_single.seq,
        "NTTCTCTAGTGCCTCGCCGCTGGTGTAGTGGTATCATGCGAGAAGAGATG"
        )

    def readReads_qual_str_test(self):
        """
        test assign seq
        """
        self.assertEqual(
        data_test.Reads_single.qual_str,
        "#AAFFJJJJJJAAAFFJJJJJJJFFJJJJJJJJJJJJJJFJJJJFFFFJ-"
        )

    def readReads_str2qual_test(self):
        """
        test assign seq
        """
        self.assertEqual(
        data_test.Reads_single.qual,
        [-29, 1, 1, 6, 6, 10, 10, 10, 10, 10, 10, 1, 1, 1, 6, 6, 10, 10, 10, 10, 10, 10, 10, 6, 6, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 6, 10, 10, 10, 10, 6, 6, 6, 6, 10, -19]
        )

if __name__ == '__main__':
    unittest.main()
