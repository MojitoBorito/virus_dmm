#!/usr/bin/env python3

import pandas as pd
import argparse

def get_virfil_data(tax_id, database_name, database_file, human_file, output_dir):
    interaction_db = pd.DataFrame()

    if database_name == 'intact':
        interaction_db = parse_intact(database_file)
    elif database_name == 'hvidb':
        interaction_db = parse_hvidb(database_file)
    else:
        raise ValueError(f"Unsupported database name: {database_name}")

    interactions, virus_seeds, human_seeds = get_interacions_and_seeds(interaction_db, tax_id)

    human_ppi = pd.read_csv(human_file, sep='\t', header=None, names=['protein_a', 'protein_b'])

    interactions_to_add = interactions[['virus_protein', 'human_protein']].copy()
    interactions_to_add = interactions_to_add.rename(columns={
        'virus_protein': 'protein1',
        'human_protein': 'protein2'
    })
    ppi_plus_virus = pd.concat([human_ppi, interactions_to_add], ignore_index=True)
    
    ppi_plus_virus.to_csv(f"{output_dir}/ppi_plus_virus.tsv", sep='\t', index=False)
    virus_seeds.to_csv(f"{output_dir}/virus_seeds.tsv", sep='\t', index=False, header=False)
    human_seeds.to_csv(f"{output_dir}/human_seeds.tsv", sep='\t', index=False, header=False)



def parse_intact(database_file):
    intact = pd.read_csv(database_file, sep='\t')

    intact = intact[intact['Taxid interactor A'] != intact['Taxid interactor B']].copy()

    intact['taxid_a'] = intact['Taxid interactor A'].str.extract(r'^taxid:(\d+)')
    intact['taxid_b'] = intact['Taxid interactor B'].str.extract(r'^taxid:(\d+)')

    mask = ((intact['taxid_a'] == '9606') ^ (intact['taxid_b'] == '9606'))
    human_intact = intact[mask].copy()
    human_intact['virus_taxid'] = human_intact.apply(
        lambda x : x['taxid_b'] if x['taxid_a'] == '9606' else x['taxid_a'], axis=1
    )
    human_intact['virus_protein'] = human_intact.apply(
        lambda x : x['ID(s) interactor B'] if x['taxid_a'] == '9606' else x['#ID(s) interactor A'], axis=1
    )
    human_intact['human_protein'] = human_intact.apply(
        lambda x : x['#ID(s) interactor A'] if x['taxid_a'] == '9606' else x['ID(s) interactor B'], axis=1
    )

    human_intact = human_intact[human_intact['virus_protein'].str.startswith('uniprotkb:') & 
                                human_intact['human_protein'].str.startswith('uniprotkb:')].copy()
    
    human_intact['virus_protein'] = human_intact['virus_protein'].str.replace(r'^uniprotkb:', '', regex=True)
    human_intact['human_protein'] = human_intact['human_protein'].str.replace(r'^uniprotkb:', '', regex=True)
    human_intact['virus_protein'] = human_intact['virus_protein'].str.replace(r'-PRO_.*$', '', regex=True)
    human_intact['human_protein'] = human_intact['human_protein'].str.replace(r'-PRO_.*$', '', regex=True)

    human_intact['miscore'] = (
        human_intact['Confidence value(s)']
        .str.extract(r'(?<=intact-miscore:)(\d+\.\d+)')
        .astype(float)
    )

    human_intact = human_intact.drop_duplicates(
        subset = ['human_protein', 'virus_protein', 'virus_taxid'],
        keep = 'first'
    )

    human_intact = human_intact[['virus_taxid', 'virus_protein', 'human_protein']].copy()

    return human_intact


def parse_hvidb(database_file):
    hvidb = pd.read_csv(database_file, sep='\t')
    hvidb['virus_taxid'] = hvidb['Organism_Interactor_virus'].astype(str)

    hvidb['virus_protein'] = hvidb['Uniprot_virus'].str.replace(r'-PRO_.*$', '', regex=True)
    hvidb['human_protein'] = hvidb['Uniprot_human'].str.replace(r'-PRO_.*$', '', regex=True)

    hvidb = hvidb[['virus_taxid', 'virus_protein', 'human_protein']]

    return hvidb

def get_interacions_and_seeds(df, taxid):
    interactions = df[df['virus_taxid'] == taxid]
    virus_seeds = interactions['virus_protein'].unique()
    human_seeds = interactions['human_protein'].unique()

    virus_seeds = pd.Series(virus_seeds)
    human_seeds = pd.Series(human_seeds)

    return interactions, virus_seeds, human_seeds


if __name__ == "__main__":
    cmd = argparse.ArgumentParser(description="Extract virus-host interactions and seeds for viral DMMM")
    cmd.add_argument('--tax_id', type=str, required=True, help='Taxonomy ID of the virus')
    cmd.add_argument('--database_name', type=str, required=True, choices=['intact', 'hvidb'], help='Name of the interaction database (intact or hvidb)')
    cmd.add_argument('--database_file', type=str, required=True, help='Path to the interaction database file')
    cmd.add_argument('--human_file', type=str, required=True, help='Path to the human PPI file')
    cmd.add_argument('--output_dir', type=str, required=True, help='Directory to save the output files')
    args = cmd.parse_args()

    get_virfil_data(args.tax_id, args.database_name, args.database_file, args.human_file, args.output_dir)

"""get_virfil_data("10298", 
                "intact", 
                "data/intact.tsv", 
                "tests/pipeline_results/input/networks/string.human_physical_links_v12_0_min700.UniProtKB-AC.robust.tsv", 
                "test_cache")"""
