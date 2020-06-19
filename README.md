# Simdjson benchmarking tool

* This script will run benchmarks on each commit of a specific git repo (intended for [simdjson](https://github.com/simdjson/simdjson)).
* It is modular: you can add as much benchmark scripts as you want (these are just python scripts in the `benchmark_scripts` directory).
* The results are stored in JSON files, in the `benchmark_results` directory.
* It should run in a docker container (the container is not finished yet).
* A cron command should ask the container to run `commits.py` once a day, in order to perform the benchmarks on all the new commits on the main repo.
* All variables can be configured by editing `commits.py`.
* If enabled, the script will attempt to upload all the results to a server via FTP. On the FTP home of this server, you should have a `benchmark_results` directory, and the `index.html` and `main.js` files. When accessed from a web browser, the `index.html` file will generate graphics of the results.
