import os

os.chdir("./benchmark")
result = os.popen("./parse -t ../../jsonexamples/canada.json ").read().replace("\n", "").split("\t")
print(result[5])
