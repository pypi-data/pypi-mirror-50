#!/usr/bin/env python3
# -*-coding:Utf-8 -*

"""
This module provides unitary tests for the suffixtree project
"""

import unittest
from .. import suffix_tree


class BuildingTreeTest(unittest.TestCase):
    """
    all the tests for the fonctions building a tree
    """
    def test_add_nt(self):
        """
        test Node creation
        """
        node = suffix_tree.Node()
        node.add_child("A").barcode = 5
        self.assertEqual(
            str(node),
            "A"
        )

    def test_get_nt(self):
        """
        test Node creation
        """
        node = suffix_tree.Node()
        node.add_child("A").barcode = 5
        self.assertEqual(
            node["B"],
            None
        )

    def test_add_sequence_node(self):
        """
        all the tests on loading the config yaml file
        """
        node = suffix_tree.Node()
        curr_node = node.add_child("A")
        curr_node = curr_node.add_child("C")
        curr_node = curr_node.add_child("T")
        curr_node = curr_node.add_child("G")
        curr_node.barcode = 5
        sequence = "ACTG"
        # contig_toy -> "data/toy_file.yaml"
        self.assertEqual(
            str(node),
            sequence
        )

    def test_add_sequence(self):
        """
        all the tests on loading the config yaml file
        """
        sequence = "ACTG"
        tree = suffix_tree.Tree()
        tree.add_sequence(sequence, 5)
        # contig_toy -> "data/toy_file.yaml"
        self.assertEqual(
            str(tree),
            sequence
        )

    def test_search_sequence_node(self):
        """
        all the tests on loading the config yaml file
        """
        sequence = "ACTG"
        tree = suffix_tree.Tree()
        tree.add_sequence(sequence, "barcode1")
        # contig_toy -> "data/toy_file.yaml"
        self.assertEqual(
            tree.root.get_barcode(sequence),
            ("barcode1", 3, None)
        )

    def test_search_sequence(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        # contig_toy -> "data/toy_file.yaml"
        self.assertEqual(
            tree.search_reads("ACTG", [30, 12, 30, 40]),
            "barcode1"
        )


class SearchingTreeTest(unittest.TestCase):
    """
    all the tests for the fonctions searching a tree
    """

    def test_search_sequence_mismatch(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        self.assertEqual(
            tree.search_reads("AGTG", [30, 2, 30, 40], verbose=True),
            "barcode1"
        )

    def test_search_sequence_error_seq_len(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        try:
            tree.search_reads("AGTGC", [30, 2, 30, 40], verbose=True)
        except IndexError:
            self.assertEqual(1, 1)

    def test_search_sequence_error_seq_qual(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        try:
            tree.search_reads("AGTG", [30, 2, 30, 40, 41], verbose=True)
        except IndexError:
            self.assertEqual(1, 1)

    def test_search_multiple_sequence_mismatch_a(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        tree.add_sequence("ATAG", "barcode2")
        tree.add_sequence("ACAC", "barcode3")
        self.assertEqual(
            tree.search_reads("TGAG", [12, 12, 30, 40], verbose=True),
            "barcode2"
        )

    def test_search_multiple_sequence_mismatch_b(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        tree.add_sequence("ATAG", "barcode2")
        tree.add_sequence("ACAC", "barcode3")
        self.assertEqual(
            tree.search_reads("AGCC", [30, 2, 30, 40], verbose=True),
            "barcode3"
        )

    def test_search_multiple_sequence_mismatch_c(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        tree.add_sequence("ATAG", "barcode2")
        tree.add_sequence("ACAC", "barcode3")
        self.assertEqual(
            tree.search_reads("AGTC", [30, 12, 12, 40], verbose=True),
            "barcode3"
        )

    def test_search_multiple_sequence_mismatch_d(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        tree.add_sequence("ATAG", "barcode2")
        tree.add_sequence("ACAC", "barcode3")
        self.assertEqual(
            tree.search_reads("AGTC", [30, 30, 13, 40], verbose=True),
            "barcode3"
        )

    def test_search_multiple_sequence_mismatch_e(self):
        """
        all the tests on loading the config yaml file
        """
        tree = suffix_tree.Tree()
        tree.add_sequence("ACTG", "barcode1")
        tree.add_sequence("ATAG", "barcode2")
        tree.add_sequence("ACAC", "barcode3")
        self.assertEqual(
            tree.search_reads("AGTC", [30, 30, 40, 13], verbose=True),
            "barcode3"
        )

    def test_forest_search_multiple_sequence_mismatch_a(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("RT", "ATTG", [30, 12, 12, 40], verbose=True),
            "barcode2"
        )

    def test_forest_search_multiple_sequence_mismatch_b(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("PCR", "ACTG", [30, 17, 12, 40], verbose=True),
            "barcode3"
        )

    def test_forest_search_multiple_sequence_mismatch_c(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("PCR", "AGTG", [2, 1, 3, 4], verbose=True),
            "barcode3"
        )

    def test_forest_search_multiple_sequence_mismatch_d(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("PCR", "AGTG", [30, 30, 13, 40],
                                verbose=True),
            "barcode3"
        )

    def test_forst_search_sequence_error_barcode(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        try:
            forest.search_reads("RG", "FFFFF", [30, 12, 12, 40], verbose=True)
        except KeyError:
            self.assertEqual(1, 1)

    def test_forst_search_sequence_error_seq_len(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        try:
            forest.search_reads("RT", "FFFFF", [30, 12, 12, 40], verbose=True)
        except IndexError:
            self.assertEqual(1, 1)

    def test_forest_unassigned_a(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("RT", "FFFF", [30, 12, 12, 40], verbose=True),
            "unassigned"
        )

    def test_forest_unassigned_b(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest()
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("RT", "FFFG", [30, 12, 12, 40], verbose=True),
            "barcode"
        )

    def test_forest_unassigned_mismatch_2(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest(mismatch=2)
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("RT", "FFFG", [30, 12, 12, 40],
                                verbose=True),
            "unassigned"
        )

    def test_forest_unassigned_mismatch_3(self):
        """
        all the tests on loading the config yaml file
        """
        forest = suffix_tree.Forest(mismatch=3)
        forest.add_sequence("RT", "ACAG", "barcode")
        forest.add_sequence("RT", "ATAG", "barcode2")
        forest.add_sequence("PCR", "ACAG", "barcode3")
        forest.add_sequence("PCR", "ATAG", "barcode4")
        self.assertEqual(
            forest.search_reads("RT", "FFFG", [30, 12, 12, 40],
                                verbose=True),
            "unassigned"
        )


if __name__ == '__main__':
    unittest.main()
