SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

export PYTHONPATH="$PYTHONPATH:$DIR/third-party/lib/python2.7/site-packages"
