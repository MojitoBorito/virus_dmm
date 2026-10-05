#!/usr/bin/env bash -C -e -u -o pipefail
multiqc_formatter.py -i input/ppi_plus_virus_intact.top_50.node_degree_distribution.yaml input/ppi_plus_virus_intact.corona_standard.node_degree_distribution.yaml input/ppi_plus_virus_intact.top_50.human_int.node_degree_distribution.yaml -H network_node_degree_distribution_header.yaml
cat <<-END_VERSIONS > versions.yml
"NFCORE_DISEASEMODULEDISCOVERY:DISEASEMODULEDISCOVERY:MULTIQCFORMATTER":
    python: "$(python --version | sed 's/Python //g')"
END_VERSIONS
