#!/usr/bin/env bash -C -e -u -o pipefail
network_annotation.py -s input/virus_seeds_intact.top_50.ppi_plus_virus_intact.corona_standard.no_tool.gt -n input/ppi_plus_virus_intact.corona_standard.gt -o ""virus_seeds_intact.top_50.ppi_plus_virus_intact.corona_standard.no_tool.gt""

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:NETWORKANNOTATION":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
END_VERSIONS
