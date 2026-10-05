#!/usr/bin/env python3

import pandas as pd # type: ignore
import argparse

def get_virfil_data(tax_id, database_name, database_file, human_file, output_dir, threshold=None, percentile=None, top=None, same=False):
    interaction_db = pd.DataFrame()

    if database_name == 'intact':
        interaction_db = parse_intact(database_file, threshold, percentile, top, same)
    elif database_name == 'hvidb':
        interaction_db = parse_hvidb(database_file)
    else:
        raise ValueError(f"Unsupported database name: {database_name}")

    interactions, virus_seeds, human_seeds = get_interacions_and_seeds(interaction_db, tax_id)

    human_ppi = pd.read_csv(human_file, sep='\t', header=None, names=['protein_a', 'protein_b'])

    interactions_to_add = interactions[['virus_protein', 'human_protein']].copy()
    interactions_to_add = interactions_to_add.rename(columns={
        'virus_protein': 'protein_a',
        'human_protein': 'protein_b'
    })
    ppi_plus_virus = pd.concat([human_ppi, interactions_to_add], ignore_index=True)
    
    ppi_plus_virus.to_csv(f"{output_dir}/ppi_plus_virus_{database_name}.csv", index=False, header=False)
    virus_seeds.to_csv(f"{output_dir}/virus_seeds_{database_name}.txt", index=False, header=False)
    human_seeds.to_csv(f"{output_dir}/human_seeds_{database_name}.txt", index=False, header=False)


def parse_intact(database_file, threshold=None, percentile=None, top = None, same=False):
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

    human_intact = human_intact.sort_values(by='miscore', ascending=False).copy()

    human_intact = human_intact.drop_duplicates(
        subset = ['human_protein', 'virus_protein', 'virus_taxid'],
        keep = 'first'
    )

    if percentile is not None: 
        human_intact = filter_intact_by_percentile(human_intact, percentile)
    elif threshold is not None:
        human_intact = human_intact[human_intact["miscore"] >= threshold].copy()
    elif top is not None:
        top_human = (
            human_intact.groupby(['virus_taxid', 'human_protein'])['miscore']
            .max()
            .reset_index()
            .sort_values(['virus_taxid', 'miscore'], ascending=[True, False])
            .groupby('virus_taxid')
            .head(top)
        )

        human_intact = human_intact.merge(
            top_human[['virus_taxid', 'human_protein']],
            on=['virus_taxid', 'human_protein'],
            how='inner'
        )
    elif same:
        human_intact = human_intact.drop_duplicates(
            subset = ['virus_taxid', 'virus_protein'],
            keep = 'first'
        )

    human_intact = human_intact[['virus_taxid', 'virus_protein', 'human_protein']].copy()

    return human_intact


def filter_intact_by_percentile(human_intact, percentile=None):
    if percentile is not None:
        threshold = human_intact.groupby("virus_taxid")["miscore"].transform(
            lambda x: x.quantile(percentile)
        )
        human_intact = human_intact[human_intact["miscore"] >= threshold].copy()
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
    cmd.add_argument('--threshold', type=float, default=None, help='Confidence score threshold for filtering interactions (applicable for IntAct)')
    cmd.add_argument('--percentile', type=float, default=None, help='Percentile for filtering interactions (applicable for IntAct)')
    cmd.add_argument('--top', type=int, default=None, help='Top N human proteins per virus for filtering interactions (applicable for IntAct)')
    cmd.add_argument('--same', action='store_true', help='Flag to extract same number of virus and human seeds')
    args = cmd.parse_args()

    get_virfil_data(args.tax_id, 
                    args.database_name, 
                    args.database_file, 
                    args.human_file, 
                    args.output_dir, 
                    args.threshold, 
                    args.percentile,
                    args.top,
                    args.same)

