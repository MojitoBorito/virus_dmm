#!/usr/bin/env bash -C -e -u -o pipefail
save_modules.py -m "corona_expansion_filter.ppi_plus_virus_intact.corona_standard.no_tool.gt" -p "corona_expansion_filter.ppi_plus_virus_intact.corona_standard.no_tool" -l DEBUG

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:SAVEMODULES":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
    pandas: "$(python -c "import pandas; print(pandas.__version__)")"
END_VERSIONS
