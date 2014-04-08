import os
import unittest
import pandas as pd

from consensus_tools_mod import *

class exerciseImports(unittest.TestCase):
    
    import consensus_tools_mod
    import pandas as pd
    from collections import defaultdict
    import itertools
    import numpy as np
    # import Levneshtein
    # import maptplotlib.pyplot as plt

class exerciseDirectoryLayout(unittest.TestCase):

    "test the layout"
 
    def testDataDirectory(self):
        assert(os.stat(data_dir));

    def testTmpDirectory(self):
        assert(os.stat(tmp_dir));

class exerciseNfNData(unittest.TestCase):
    "test the csv"

    def testReadRCSV(self):
        NfNcsv = os.path.join(data_dir, 'Herbarium_NfN.csv')
        df = pd.read_csv(NfNcsv);
        assert(not df.empty)

def legacy(datadir):

    # DEPENDENCIES
    import pandas as pd
    from collections import defaultdict
    import itertools

    import numpy as np
    import Levenshtein
    import matplotlib.pyplot as plt

    ## FIXME
    data_dir    = datadir;
    
    # TEST EXAMPLE
    test_example = ["12 mi. W. Oakland, Cal", "12 mi West Oakland", "12 mi. W. Oakland", "12 miles W Oakland"]
    token_example = token_consensus(test_example, data_dir)
    character_example = character_consensus(test_example, wdir = data_dir)

    nfn_data = pd.read_csv(os.path.join(data_dir,"Herbarium_NfN.csv"))
    nfn_data = nfn_data.fillna(np.nan) # tweaks conversion

    gold_data = pd.read_csv(os.path.join(data_dir,"Herbarium_Gold.csv"))
    gold_data = gold_data.fillna(np.nan) # tweaks conversion

    # Finding consensus
    character_coll = variant_consensus(accession = "filename", field = "Collected by", method = "character", data = nfn_data, wdir = data_dir)
    character_loc = variant_consensus(accession = "filename", field = "Location", method = "character", data = nfn_data, wdir = data_dir)

    token_coll = variant_consensus(accession = "filename", field = "Collected by", method = "token", data = nfn_data, wdir = data_dir)
    token_loc = variant_consensus(accession = "filename", field = "Location", method = "token", data = nfn_data, wdir = data_dir)

    # Compiling results
    character_results = pd.merge(gold_data, character_coll, on = "filename", suffixes = ("_gold", "_consensus"))
    character_results = pd.merge(character_results, character_loc, on = "filename", suffixes = ("_gold", "_consensus"))

    token_results = pd.merge(gold_data, token_coll, on = "filename", suffixes = ("_gold", "_consensus"))
    token_results = pd.merge(token_results, token_loc, on = "filename", suffixes = ("_gold", "_consensus"))

    print('character_results', character_results.head())

    ## TODO hm
    d1 = pd.DataFrame.from_records(character_results['Collected by_consensus'], index=character_results['Collected by_gold'])
    print ('d1 collectedby__char', d1.head())

    d2 = pd.DataFrame.from_records(character_results['Location_consensus'], index=character_results['Location_gold'])
    print ('d2 location__char', d2.head())

    print('token_results', token_results.head())

    ## TODO wtf
    d3 = pd.DataFrame.from_records(token_results['Collected by_consensus'], index=token_results['Collected by_gold'])
    print ('d3 collected__token', d3.head())

    d4 = pd.DataFrame.from_records(token_results['Location_consensus'], index=token_results['Location_gold'])
    print ('d4 location__token', d4.head())

if __name__ == '__main__':
    
    data_dir    = '../data_dir_'
    tmp_dir     = '../tmp_dir_' 
    
    legacy(data_dir)
    unittest.main()
    raw_input("press any key to quit...")

