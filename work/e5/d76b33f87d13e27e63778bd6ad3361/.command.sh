#!/usr/bin/env bash -C -e -u -o pipefail
graph_tool_parser.py input/ppi_plus_virus_intact.corona_standard.csv -f gt -l DEBUG

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:GRAPHTOOLPARSER":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
END_VERSIONS
