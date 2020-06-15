from ubuntu:20.04
run apt-get update -qq
run DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
run apt-get install -y vim clang-format sudo python cmake g++ g++-9 git clang++-9
run gcc --version
run cmake --version
run python3 --version
run git clone https://github.com/yoannlr/simdjson_benchmark_docker
