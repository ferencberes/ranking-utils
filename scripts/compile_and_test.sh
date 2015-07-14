#!/bin/bash -eu

thisDir="$(dirname $0)"
thisDir="$(readlink -f "$thisDir")"

pushd "$thisDir"

pushd ../trunk
# compile learning to rank source
ant
popd

# run pytests
#../run_pytests.sh
popd
