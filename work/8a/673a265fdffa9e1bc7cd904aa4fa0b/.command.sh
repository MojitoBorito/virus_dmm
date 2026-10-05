#!/usr/bin/env bash -C -e -u -o pipefail
save_modules.py -m "virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.human_int.no_tool.gt" -p "virus_seeds_intact.top_50.ppi_plus_virus_intact.top_50.human_int.no_tool" -l DEBUG

cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:SAVEMODULES":
    python: "$(python --version | sed 's/Python //g')"
    graph-tool: "$(python -c "import graph_tool; print(graph_tool.__version__)" | cut -d' ' -f1)"
    pandas: "$(python -c "import pandas; print(pandas.__version__)")"
END_VERSIONS
