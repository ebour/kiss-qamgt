# kiss-qamgt
Keep It Simple Stupid QA Management

This project allows to query csv files from jinja template and render it for QA Management purposes.

python -m kiss_qamngt -i tests/resources/data -qd tests/resources/queries -td tests/resources/templates -t template.html -o target/report.html