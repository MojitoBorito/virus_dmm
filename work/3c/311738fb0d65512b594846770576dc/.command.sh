#!/usr/bin/env bash -C -e -u -o pipefail
topology.py --module "virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.human_int.firstneighbor.gt" --id "virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.human_int.firstneighbor" --out "virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.human_int.firstneighbor.topology.tsv"

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:TOPOLOGY":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
END_VERSIONS
