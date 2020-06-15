import os

os.chdir("./benchmark")
result = os.popen("./parse -t ../../jsonexamples/twitter.json ").read().replace("\n", "").split("\t")
print(result[6])
