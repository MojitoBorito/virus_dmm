#!/usr/bin/env python3

from matplotlib import cm
import pandas as pd
import argparse
import numpy as np

def get_virfil_data(tax_id, database_file, human_file, output_dir, top_interactors = None, same=False, top_interactions=False, suffix='', add_human=False, add_virus=False):
    interactions, human_seeds, virus_seeds, blacklist = parse_intact(database_file, tax_id, top_interactors, same, top_interactions, add_human, add_virus)

    print(f"Found {len(interactions)} interactions for organism with taxid {tax_id}")

    human_ppi = pd.read_csv(human_file, sep='\t', header=None, names=['protein_a', 'protein_b'])    

    ppi_plus_virus = pd.concat([human_ppi, interactions], ignore_index=True)
    
    sorted_pairs = np.sort(ppi_plus_virus[['protein_a', 'protein_b']].values, axis=1)
    ppi_plus_virus['protein_a'] = sorted_pairs[:, 0]
    ppi_plus_virus['protein_b'] = sorted_pairs[:, 1]

    print(f"Found {len(ppi_plus_virus)} interactions in total (including human PPI and virus-host interactions)")
    
    ppi_plus_virus = ppi_plus_virus.drop_duplicates().reset_index(drop=True)
    
    print(f"Found {len(ppi_plus_virus)} unique interactions in total (including human PPI and virus-host interactions)")
    
    ppi_plus_virus.to_csv(f"{output_dir}/ppi_plus_virus_intact.{suffix}.csv", index=False, header=False)
    virus_seeds.to_csv(f"{output_dir}/virus_seeds_intact.{suffix}.txt", index=False, header=False)
    human_seeds.to_csv(f"{output_dir}/human_seeds_intact.{suffix}.txt", index=False, header=False)
    blacklist.to_csv(f"{output_dir}/blacklist_intact.{suffix}.txt", index=False, header=False)


def parse_intact(database_file, tax_id, top_interactors = None, same=False, top_interactions=False, add_human=False, add_virus=False):
    intact = pd.read_csv(database_file, sep='\t')

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

    human_intact = human_intact[human_intact['virus_taxid'] == tax_id]
    
    human_intact = human_intact.drop_duplicates(
        subset = ['human_protein', 'virus_protein'],
        keep = 'first'
    )
    
    
    if top_interactions:
        human_intact = human_intact.nlargest(top_interactions, "miscore")
    
    if top_interactors:
        top_human = get_top_human(human_intact, top_interactors, 'human_protein')
        top_virus = get_top_human(human_intact, top_interactors, 'virus_protein')
        
        human_seeds = pd.Series(top_human['human_protein'].unique())
        virus_seeds = pd.Series(top_virus['virus_protein'].unique())
    elif same:
        viral_unique = human_intact['virus_protein'].unique()
        human_same = get_top_human(human_intact, len(viral_unique), 'human_protein')
        
        human_seeds = pd.Series(human_same['human_protein'].unique())
        virus_seeds = pd.Series(viral_unique)
    else: 
        human_seeds = pd.Series(human_intact['human_protein'].unique())
        virus_seeds = pd.Series(human_intact['virus_protein'].unique())
    
    human_interactions = pd.DataFrame(columns=['protein_a', 'protein_b'])
    virus_interactions = pd.DataFrame(columns=['protein_a', 'protein_b'])
    
    if not top_interactions:
        if add_human:
            human_interactions = get_organism_interactions(intact, "9606")
        if add_virus:
            virus_interactions = get_organism_interactions(intact, tax_id)
    
    interactions = human_intact[['virus_protein', 'human_protein']].copy()
    interactions = interactions.rename(columns={
        'virus_protein': 'protein_a',
        'human_protein': 'protein_b'
    })

    virus_host_virus_proteins = interactions['protein_a'].copy()

    interactions = pd.concat([interactions, human_interactions, virus_interactions], ignore_index=True)
    interactions = interactions[interactions['protein_a'] != interactions['protein_b']].copy()

    blacklist = pd.concat([
        virus_host_virus_proteins,
        virus_interactions['protein_a'] if add_virus else pd.Series(),
        virus_interactions['protein_b'] if add_virus else pd.Series(),
    ], ignore_index=True)

    blacklist = blacklist.drop_duplicates().reset_index(drop=True)
    
    return interactions, human_seeds, virus_seeds, blacklist


def get_organism_interactions(intact, org_taxid):
    interactions = intact[(intact['taxid_a'] == org_taxid) & (intact['taxid_b'] == org_taxid)].copy()
    interactions['protein_a'] = interactions['#ID(s) interactor A']
    interactions['protein_b'] = interactions['ID(s) interactor B']
    
    interactions = interactions[interactions['protein_a'].str.startswith('uniprotkb:') & 
                                interactions['protein_b'].str.startswith('uniprotkb:')].copy()
    
    interactions['protein_a'] = interactions['protein_a'].str.replace(r'^uniprotkb:', '', regex=True)
    interactions['protein_b'] = interactions['protein_b'].str.replace(r'^uniprotkb:', '', regex=True)
    interactions['protein_a'] = interactions['protein_a'].str.replace(r'-PRO_.*$', '', regex=True)
    interactions['protein_b'] = interactions['protein_b'].str.replace(r'-PRO_.*$', '', regex=True)
    
    print(f"Found {len(interactions)} interactions for organism with taxid {org_taxid}")
    
    return interactions[['protein_a', 'protein_b']]

    
def get_top_human(human_intact, cutoff, organism):
    return (
            human_intact.groupby(['virus_taxid', organism])['miscore']
            .max()
            .reset_index()
            .sort_values(['virus_taxid', 'miscore'], ascending=[True, False])
            .groupby('virus_taxid')
            .head(cutoff)
        )


if __name__ == "__main__":
    cmd = argparse.ArgumentParser(description="Extract virus-host interactions and seeds from intact")
    cmd.add_argument('--tax_id', type=str, required=True, help='Taxonomy ID of the virus')
    cmd.add_argument('--database_name', type=str, required=True, choices=['intact', 'hvidb'], help='Name of the interaction database (intact or hvidb)')
    cmd.add_argument('--database_file', type=str, required=True, help='Path to the interaction database file')
    cmd.add_argument('--human_file', type=str, required=True, help='Path to the human PPI file')
    cmd.add_argument('--output_dir', type=str, required=True, help='Directory to save the output files')
    cmd.add_argument('--same', action='store_true', help='Flag to extract same number of virus and human seeds')
    cmd.add_argument('--top_interactors', type=int, default=None, help='Top N human proteins per virus for filtering interactions (applicable for IntAct)')
    cmd.add_argument('--top_interactions', type=int, default=None, help='Top N interactions for filtering interactions (applicable for IntAct)')
    cmd.add_argument('--suffix', type=str, default='', help='Suffix for output files')
    cmd.add_argument('--add_human', action='store_true', help='Flag to add human interactions (applicable for IntAct)')
    cmd.add_argument('--add_virus', action='store_true', help='Flag to add virus interactions (applicable for IntAct)')

    args = cmd.parse_args()
    
    get_virfil_data(args.tax_id, 
                    args.database_file, 
                    args.human_file, 
                    args.output_dir, 
                    args.top_interactors,
                    args.same,
                    args.top_interactions,
                    args.suffix,
                    args.add_human,
                    args.add_virus)
