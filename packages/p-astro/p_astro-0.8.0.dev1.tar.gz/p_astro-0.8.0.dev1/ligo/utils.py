# Copyright (C) 2018 Shaon Ghosh, Shasvath Kapadia, Deep Chatterjee
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import os
import pickle

from argparse import ArgumentParser
from configparser import ConfigParser
import glob
import sqlite3

import numpy as np
import pandas as pd
from astropy.table import Column, Table, vstack
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


def join():
    """
    Joins the extracted sim-coinc data from GstLAL injection
    campaigns into a single Astropy table
    """
    parser = ArgumentParser(
        "Join extracted GstLAL sim-coinc parameters as astropy table")
    parser.add_argument("-i", "--input", required=True,
                        help="Directory storing extracted sim-coinc flat files")
    parser.add_argument("-c", "--config", required=True,
                        help="Name of the config file")
    parser.add_argument("-o", "--output", required=True,
                        help="Name of the output file")
    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)
    extract_prefix = config.get('output_filenames',
                                'em_bright_extract_prefix')
    extract_suffix = config.get('output_filenames',
                                'em_bright_extract_suffix')
    cols = config.get('core',
                      'sqlite_cols')
    list_of_files = glob.glob(
        os.path.join(args.input, '{}*{}'.format(extract_prefix,
                                                extract_suffix)))
    cols = cols.split(',')
    print(list_of_files)
    # FIXME delimited '|' is a fragile piece
    data = vstack(
        [Table.read(f, format='ascii', delimiter='|', names=cols)
         for f in list_of_files]
    )
    ID = Column(np.arange(len(data)), name='id')
    data.add_column(ID, index=0)
    data.write(args.output, format='ascii', delimiter='\t')


def extract():
    """
    Ingests a GstLAL injection campaign sqlite database and
    outputs the list of coinc parameters in a flat file
    """
    parser = ArgumentParser(
        "Get sim-coinc maps for LIGO GstLAL injection sqlite database")
    parser.add_argument("-i", "--input", required=True,
        help="sqlite database")
    parser.add_argument("-o", "--output", required=True,
        help="Output file, stored as numpy array")
    args = parser.parse_args()

    cur = sqlite3.connect(args.input).cursor()
    cur.execute("""
	    CREATE TEMPORARY TABLE
	    sim_coinc_map_helper
	    AS
	    SELECT a.event_id as sid,
	    coinc_event.coinc_event_id as cid,
	    coinc_event.likelihood as lr
	    FROM coinc_event_map as a
	    JOIN coinc_event_map AS b ON (b.coinc_event_id == a.coinc_event_id)
	    JOIN coinc_event ON (coinc_event.coinc_event_id == b.event_id)
	    WHERE a.table_name == 'sim_inspiral'
	    AND b.table_name == 'coinc_event'
	    AND NOT EXISTS (
	        SELECT * FROM time_slide WHERE
	        time_slide.time_slide_id == coinc_event.time_slide_id
	        AND time_slide.offset != 0
	    )"""
    )

    cur.execute("""
	    CREATE INDEX IF NOT EXISTS
	    sim_coinc_map_helper_index ON sim_coinc_map_helper (sid, cid)
	    """
    )

    cur.execute("""
	    CREATE TEMPORARY TABLE
		    sim_coinc_map
	    AS
		    SELECT
			    sim_inspiral.simulation_id AS simulation_id,
			    (
				    SELECT cid FROM
	                sim_coinc_map_helper
				    WHERE sid = simulation_id
				    ORDER BY lr DESC
				    LIMIT 1
			    ) AS coinc_event_id
		    FROM sim_inspiral
		    WHERE coinc_event_id IS NOT NULL
        """
    )

    cur.execute("""DROP INDEX sim_coinc_map_helper_index""")

    query = """
	SELECT 
	sim_inspiral.mass1,
	sim_inspiral.mass2,
	sim_inspiral.spin1z,
	sim_inspiral.spin2z,
	sngl_inspiral.mass1,
	sngl_inspiral.mass2,
	sngl_inspiral.spin1z,
	sngl_inspiral.spin2z,
	sngl_inspiral.Gamma1,
	coinc_inspiral.combined_far,
	coinc_inspiral.snr
	FROM
	sim_coinc_map 
	JOIN
	sim_inspiral 
	ON 
	sim_coinc_map.simulation_id==sim_inspiral.simulation_id 
	JOIN
	coinc_event_map 
	ON
	sim_coinc_map.coinc_event_id == coinc_event_map.coinc_event_id 
	JOIN
	coinc_inspiral 
	ON
	sim_coinc_map.coinc_event_id == coinc_inspiral.coinc_event_id 
	JOIN
	sngl_inspiral 
	ON
	(coinc_event_map.table_name == 'sngl_inspiral' AND coinc_event_map.event_id == sngl_inspiral.event_id) 
	WHERE
	sngl_inspiral.ifo=='H1';    
	"""
    np.savetxt(args.output, np.array(cur.execute(query).fetchall()),
               fmt='%f|%f|%f|%f|%f|%f|%f|%f|%d|%e|%f')


def train():
    parser = ArgumentParser(
        description='Executable to train source classifier from injections')

    parser.add_argument(
        '-i', '--input',
        help='Pickled dataframe containing source categorized data')
    parser.add_argument(
        '-o', '--output',
        help='Pickled object storing the trained classifiers')
    parser.add_argument(
        '-c', '--config', required=True,
        help='Config file with additional parameters')

    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)
    # compulsory sections in config
    required_sections = ['core',
                         'em_bright']
    assert all(config.has_section(s) for s in required_sections), \
        'Config file must have sections %s'%(required_sections,)

    # get column names and values from config
    feature_cols = config.get('em_bright',
                              'feature_cols').split(',')
    category_cols = config.get('em_bright',
                               'category_cols').split(',')
    threshold_cols = config.get('em_bright',
                                'threshold_cols').split(',')
    all_cols = feature_cols + category_cols + threshold_cols

    threshold_values = map(
        eval, config.get(
            'em_bright',
            'threshold_values').split(',')
        )
    threshold_type = config.get('em_bright',
                                'threshold_type').split(',')
    # read dataframe, check sanity
    with open(args.input, 'rb') as f:
        df = pickle.load(f)

    assert all(col in df.keys() for col in all_cols), \
        'Dataframe must contain columns %s'%(all_cols,)

    # create masked array based on threshold values, extract features and targets
    mask = np.ones(len(df)).astype(bool)
    for col, value, typ in zip(threshold_cols, threshold_values, threshold_type):
        mask &= df[col] < value if typ == 'lesser' else \
            df[col] > value if typ == 'greater' else True
    features = df[feature_cols][mask]
    targets = df[category_cols][mask]
    # train RF classifier for each category
    rf_kwargs = eval(config.get('em_bright',
                                'rf_kwargs'))
    scaler = StandardScaler().fit(features)
    clfs = []
    for category, target_value in targets.iteritems():
        clf = RandomForestClassifier(**rf_kwargs)
        clf.fit(features, target_value)
        clfs.append(clf)
    # append the Standard scaler object
    clfs.extend([scaler])
    # append the output filename of the classifier
    clfs.extend([args.output])
    with open(args.output, 'wb') as f:
        pickle.dump(clfs, f)

#FIXME This function is not used
def histogram_by_bin():

    parser = ArgumentParser(
        description='Executable to histogram triggers by SVD bin number')

    parser.add_argument(
        '--bns-file',
        help='Text file containing data extracted from BNS database')
    parser.add_argument(
        '--nsbh-file',
        help='Text file containing data extracted from NSBH database')
    parser.add_argument(
        '--bbh-file',
        help='Text file containing data extracted from BBH database')
    parser.add_argument(
        '-o', '--output',
        help='Text file to store activation counts per bin and source category')
    parser.add_argument(
        '-c', '--config', required=True,
        help='Config file with additional parameters')

    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    cfar_threshold = config.get('cfar_threshold')
    num_svds = config.get('total_svd_bins')
    
    data_bns = np.loadtxt(args.bns_file,delimter="|")
    data_nsbh = np.loadtxt(args.nsbh_file,delimter="|")
    data_bbh = np.loadtxt(args.bbh_file,delimter="|")

    cfar_bns = data_bns[:,11]
    cfar_nsbh = data_nsbh[:,11]
    cfar_bbh = data_bbh[:,11]

    bns_act_counts = data_bns[:,10][cfar_bns < cfar_threshold]
    nsbh_act_counts = data_nsbh[:,10][cfar_nsbh < cfar_threshold]
    bbh_act_counts = data_bbh[:,10][cfar_bbh < cfar_threshold]

    a_bns = np.array([len(bns_act_counts[bns_act_counts == svd]) for svd in range(num_svds)])
    a_nsbh = np.array([len(nsbh_act_counts[nsbh_act_counts == svd]) for svd in range(num_svds)])
    a_bbh = np.array([len(bbh_act_counts[bbh_act_counts == svd]) for svd in range(num_svds)])
    
    np.savetxt(args.output,np.c_[a_bns,a_nsbh,a_bbh],fmt="%d\t%d\t%d")
