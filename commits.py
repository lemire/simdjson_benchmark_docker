import os
import os.path
import sys
import json
import shutil
import re
import subprocess

#
#       config
#

gitlog_cmd = "git -C {} log --date=unix --topo-order --pretty='format:%H %ad' {}..HEAD"
gitclone_cmd = "git clone {} {}"

distant_repo = "https://github.com/simdjson/simdjson.git"

basedir = "{}/".format(sys.path[0]) + "{}"

local_repo = basedir.format("simdjson")


if len(sys.argv) > 1 :
        lastcommit = sys.argv[1]
        access_commmit_file = False
else:
        access_commmit_file = True


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

lastcommit_file = basedir.format("lastcommit")


#
#       main code
#

# 0. initialize/load benchmarks results files

result_objects = {}
resfile = "benchmark_results.json"
if not os.path.isfile(resfile):
        with open(resfile, 'w') as rf:
                rf.write("{}")
                rf.close()
        with open(resfile, 'r') as rf:
                result_objects = json.load(rf)
                rf.close()

# write files when we quit
def clean_exit():
        print(":: Writing results...")
        with open(resfile, 'w') as rf:
                json.dump(result_objects, rf)
                rf.close()
                print(":: Wrote results  to {}".format(resfile))

# 1. if we can't find the local repo, we clone it from the distant repo

if not os.path.exists(local_repo):
        print(":: Local repo not found, cloning from {}".format(distant_repo))
        os.system(gitclone_cmd.format(distant_repo, local_repo))


# 2. we get the latest commit we performed benchmarks on
if access_commmit_file:
  with open(lastcommit_file, 'r') as lcf:
        lastcommit = lcf.read().replace("\n", "")
        lcf.close()

print(":: Resume benchmarks from commit " + lastcommit)

if(len(lastcommit) == 0):
  print(":: WARNING, you have an empty last commit!!!!")
# 3. we pull and get a list of the new commits
os.chdir(local_repo)
print(":: Pull")
os.system("git -C {} remote -v".format(local_repo))
os.system("git -C {} pull  ".format(local_repo))
comm = os.popen(gitlog_cmd.format(local_repo, lastcommit))
commread = comm.read()
err = comm.close()

if(len(commread) == 0):
        print(":: Nothing to do. Bye! ") 
        sys.exit(0)

commits = commread.split("\n")

if(err):
       print("error : ",err)
       sys.exit(err)
remaining_commits = len(commits)
print(":: Will peform benchmarks on {} commits".format(str(remaining_commits)))

if(remaining_commits == 0):
       print(":: Nothing to do. Bye! ")
       sys.exit(0)
# 4. perform all benchmarks for each commit

for i in range(len(commits) - 1, -1, -1):
        commit = commits[i].split(" ")
        print(":: Perform benchmarks on commit {} ({} commits remaining).. building..".format(commit[0], str(remaining_commits)))
        os.system("git -C {} checkout {}".format(local_repo, commit[0]))
        this_build_directory = os.path.abspath("./build"+commit[0])
        os.chdir(local_repo)
        print(":: Creating directory "+this_build_directory)
        retcode = subprocess.call(["cmake", "--parallel", "-S", local_repo, "-B", this_build_directory, "-DSIMDJSON_DEVELOPER_MODE=ON" ])
        if(retcode) :
                sys.exit(0)
        print(":: Building into directory "+this_build_directory)
        print("cmake --build {}  --target bench_ondemand --parallel".format(this_build_directory))
        retcode = os.system("cmake --build {}  --target bench_ondemand --parallel".format(this_build_directory))
        if(retcode) :
                sys.exit(0)
        print(":: Done building into directory "+this_build_directory)
        result = os.popen("{}/benchmark/bench_ondemand --benchmark_filter=\"<simdjson_ondemand>\" ".format(this_build_directory)).read()
        for line in result.split("\n"):
           name = line.split("<")[0]
           speed = re.search("(\d+\.\d+)\sGB", line)
           if(speed):
             if(not name in result_objects):
                     result_objects[name] = {}
             result_objects[name][commit[0]] = {'date': commit[1], 'speed': float(speed[1])}
        remaining_commits = remaining_commits - 1

os.system("git -C {} checkout master".format(local_repo))
os.chdir(basedir.format(""))

clean_exit()

print(":: Benchmarks performed on {} commits".format(str(len(commits))))
if access_commmit_file:
  with open(lastcommit_file, 'w') as lcf:
        lcf.write(commits[len(commits) - 1].split(" ")[0])
        lcf.close()
