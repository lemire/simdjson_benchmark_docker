# A simdjson benchmarking tool


## Setup
* Consider removing `benchmark_results.json` if you want to start anew. If there is a leftover `simdjson` directory, you may remove it as well.
* Execute `python3 commits.py`
* Open `plots.html`. It might be useful to create a local web server (`python3 -m http.server`) and to open it at `http://localhost:8000/plots.html` (for example).

To summarize, you could do:
```
rm -r -f benchmark_results.json simdjson
python3 commits.py 2db4592571bec79a7e91fee1ad0e0e59217b4fde
python3 -m http.server
# open http://localhost:8000/plots.html in your browser
```

After running `python3 commits.py  ...`,  you can also copy the benchmark_results.json file elsewhere together with `plots.html` and `main.js` and load them up in your browser on another machine.


