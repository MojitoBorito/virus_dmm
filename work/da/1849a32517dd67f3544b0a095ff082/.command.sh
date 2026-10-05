#!/usr/bin/env bash -C -e -u -o pipefail
module_parser.py ppi_plus_virus_intact.top_50.gt -t firstneighbor -l DEBUG -m virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.firstneighbor.gt -s virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.tsv -o virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.firstneighbor.gt -b blacklist_intact.top_50.txt

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:NETWORKEXPANSION:MODULEPARSER":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
END_VERSIONS
