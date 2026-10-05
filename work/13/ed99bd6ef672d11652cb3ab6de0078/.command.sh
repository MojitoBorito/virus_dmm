#!/usr/bin/env bash -C -e -u -o pipefail
firstneighbor_tool.py -n ppi_plus_virus_intact.top_50.gt -s virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.tsv -o "virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.firstneighbor.gt"

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:NETWORKEXPANSION:GT_FIRSTNEIGHBOR:FIRSTNEIGHBOR":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
END_VERSIONS
