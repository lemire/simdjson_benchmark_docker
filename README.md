# A simdjson benchmarking tool


## Setup
* Consider removing `benchmark_results.json` if you want to start anew.
* Execute `python3 commits.py`
* Open `plots.html`. It might be useful to create a local web server (`python3 -m http.server`) and to open it at `http://localhost:8000/plots.html` (for example).

To summarize, you could do:
```
rm benchmark_results.json
python3 commits.py 5f0b35b2c5ec8aaf9302e4a5abad3323893ce1f0
python3 -m http.server
# open http://localhost:8000/plots.html in your browser
```

After running `python3 commits.py  ...`,  you can also copy the benchmark_results.json file elsewhere together with `plots.html` and `main.js` and load them up in your browser on another machine.


