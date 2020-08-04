import os

os.chdir("./benchmark")
result = os.popen("./parse -t ../../jsonexamples/gsoc-2018.json ").read().replace("\n", "").split("\t")
print(result[5])
