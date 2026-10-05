#!/usr/bin/env bash -C -e -u -o pipefail
input_check.py -s check/virus_seeds_intact.top_50.txt -p virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50 -n check/ppi_plus_virus_intact.top_50.gt -b blacklist_intact.top_50.txt -l DEBUG

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:INPUTCHECK":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
END_VERSIONS
