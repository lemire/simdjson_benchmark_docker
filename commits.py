import os
import os.path
import json
import shutil
import ftplib

#
#	config
#

gitlog_cmd = "git log --date=unix --pretty='format:%H %ad' {}..HEAD"
gitclone_cmd = "git clone {} {}"

distant_repo = "https://github.com/simdjson/simdjson.git"

basedir = "{}/".format(os.getcwd()) + "{}"

local_repo = basedir.format("simdjson")
bench_scripts = basedir.format("/benchmark_scripts/")
bench_results = basedir.format("/benchmark_results/")
lastcommit_file = basedir.format("lastcommit")

uploadFTP = True

#
#	main code
#

# 0. initialize/load benchmarks results files

benchmarks = os.listdir(bench_scripts)
result_objects = {}

for bench in benchmarks:
	resfile = bench_results + bench + ".json"
	if not os.path.isfile(resfile):
		with open(resfile, 'w') as rf:
			rf.write("{}")
			rf.close()
	with open(resfile, 'r') as rf:
		result_objects[bench] = json.load(rf)
		rf.close()

# write files when we quit
def clean_exit():
	print(":: Writing results...")
	for bench in benchmarks:
		resfile = bench_results + bench + ".json"
		with open(resfile, 'w') as rf:
			json.dump(result_objects[bench], rf)
			rf.close()
			print(":: Wrote results for {} to {}".format(bench, resfile))

# 1. if we can't find the local repo, we clone it from the distant repo

if not os.path.exists(local_repo):
	print(":: Local repo not found, cloning from {}".format(distant_repo))
	os.system(gitclone_cmd.format(distant_repo, local_repo))


# 2. we get the latest commit we performed benchmarks on

with open(lastcommit_file, 'r') as lcf:
	lastcommit = lcf.read().replace("\n", "")
	lcf.close()

print(":: Resume benchmarks from commit " + lastcommit)


# 3. we pull and get a list of the new commits

os.chdir(local_repo)
print(":: Pull")
os.system("git pull")
commits = os.popen(gitlog_cmd.format(lastcommit)).read().split("\n")
remaining_commits = len(commits)
print(":: Will peform benchmarks on {} commits".format(str(remaining_commits)))

# 4. perform all benchmarks for each commit

for i in range(len(commits) - 1, -1, -1):
	commit = commits[i].split(" ")
	print(":: Perform benchmarks on commit {} ({} commits remaining).. building..".format(commit[0], str(remaining_commits)))

	if os.path.exists("./build"):
		shutil.rmtree("./build")

	os.system("git checkout " + commit[0])
	os.mkdir("./build")
	os.chdir("./build")
	os.system("cmake ..")
	os.system("make")

	for bench in benchmarks:
		out = os.popen("python " + bench_scripts + bench).read().replace("\n", "")
		result_objects[bench][commit[0]] = {'date': commit[1], 'speed': float(out)}

	os.chdir(local_repo)
	remaining_commits = remaining_commits - 1

os.system("git checkout master")
os.chdir(basedir.format(""))

clean_exit()

print(":: Benchmarks performed on {} commits".format(str(len(commits))))

with open(lastcommit_file, 'w') as lcf:
	lcf.write(commits[len(commits) - 1].split(" ")[0])
	lcf.close()

# 5. upload the results to the web server

if uploadFTP:
	ftpaddr = '35.206.98.224'
	ftpuser = 'simdjson@lemire.me'

	with open('ftppass', 'r') as passfile:
		ftppass = passfile.read().replace("\n", "")
		passfile.close()

	print(":: Uploading the results to the server")
	session = ftplib.FTP(ftpaddr, ftpuser, ftppass)

	for bench in benchmarks:
		jsonname = bench + ".json"
		f = open(bench_results + jsonname, 'rb')
		print(":: Upload {} to the server".format(jsonname))
		session.storbinary("STOR benchmark_results/{}".format(jsonname), f)
		f.close()

	session.close()
	print(":: All results uploaded")
