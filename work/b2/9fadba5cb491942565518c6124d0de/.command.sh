#!/usr/bin/env bash -C -e -u -o pipefail
topology.py --module "corona_expansion_filter.ppi_plus_virus_intact.corona_standard.no_tool.gt" --id "corona_expansion_filter.ppi_plus_virus_intact.corona_standard.no_tool" --out "corona_expansion_filter.ppi_plus_virus_intact.corona_standard.no_tool.topology.tsv"

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:TOPOLOGY":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
END_VERSIONS
