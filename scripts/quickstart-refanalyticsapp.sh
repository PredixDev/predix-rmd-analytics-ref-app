#!/bin/bash
set -e
function local_read_args() {
  while (( "$#" )); do
  opt="$1"
  case $opt in
    -h|-\?|--\?--help)
      PRINT_USAGE=1
      QUICKSTART_ARGS="$SCRIPT $1"
      break
    ;;
    -b|--branch)
      BRANCH="$2"
      QUICKSTART_ARGS+=" $1 $2"
      shift
    ;;
    -o|--override)
      QUICKSTART_ARGS=" $SCRIPT"
    ;;
    --skip-setup)
      SKIP_SETUP=true
    ;;
    --skip-pull)
      SKIP_PULL=true
    ;;
    *)
      QUICKSTART_ARGS+=" $1"
      #echo $1
    ;;
  esac
  shift
  done

  if [[ -z $BRANCH ]]; then
    echo "Usage: $0 -b/--branch <branch> [--skip-setup]"
    exit 1
  fi
}

# default settings
BRANCH="master"
PRINT_USAGE=0
SKIP_SETUP=false
SKIP_PULL=false

IZON_SH="https://raw.githubusercontent.com/PredixDev/izon/1.1.0/izon2.sh"
SCRIPT="-script digital-twin.sh -script-readargs digital-twin-readargs.sh"
VERSION_JSON="version.json"
PREDIX_SCRIPTS=predix-scripts
REPO_NAME=predix-rmd-analytics-ref-app
VERSION_JSON="version.json"
APP_DIR="digital-twin-analytics"
APP_NAME="Predix RMD Analytics Application"
SCRIPT_NAME="quickstart-refanalyticsapp.sh"
GITHUB_RAW="https://raw.githubusercontent.com/PredixDev"
TOOLS="Cloud Foundry CLI, Git, Maven, Predix CLI"
TOOLS_SWITCHES="--cf --git --maven --predixcli"
QUICKSTART_ARGS+=" "
QUICKSTART_ARGS+="-pxclimin 0.6.34 -rmq -bindrmq -af -armd -fce $SCRIPT"


# Process switches
local_read_args $@

#variables after processing switches
SCRIPT_LOC="$GITHUB_RAW/$REPO_NAME/$BRANCH/scripts/$SCRIPT_NAME"
VERSION_JSON_URL="$GITHUB_RAW/predix-rmd-analytics-ref-app/$BRANCH/version.json"


function check_internet() {
  set +e
  echo ""
  echo "Checking internet connection..."
  curl "http://google.com" > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Unable to connect to internet, make sure you are connected to a network and check your proxy settings if behind a corporate proxy"
    echo "If you are behind a corporate proxy, set the 'http_proxy' and 'https_proxy' environment variables."
    exit 1
  fi
  echo "OK"
  echo ""
  set -e
}

function init() {
  currentDir=$(pwd)
  if [[ $currentDir == *"scripts" ]]; then
    echo 'Please launch the script from the root dir of the project'
    exit 1
  fi
  
  check_internet
  
  #get the script that reads version.json
  eval "$(curl -s -L $IZON_SH)"
  
  #download the script and cd
  getUsingCurl $SCRIPT_LOC
  chmod 755 $SCRIPT_NAME;
  if [[ ! $currentDir == *"$REPO_NAME" ]]; then
    mkdir -p $APP_DIR
    cd $APP_DIR
  fi

  
  getVersionFile
  getLocalSetupFuncs $GITHUB_RAW
}


if [[ $PRINT_USAGE == 1 ]]; then
  init
  __print_out_standard_usage
else
  if $SKIP_SETUP; then
    init
  else
    init
    __standard_mac_initialization
  fi
fi

getPredixScripts
#clone the repo itself if running from oneclick script
#getCurrentRepo

#cd predix-scripts/$REPO_NAME
# echo "Pulling Submodules"
# if ! $SKIP_PULL; then
#   ./scripts/pullSubModules.sh
# fi
#cd ../..

echo "quickstart_args=$QUICKSTART_ARGS"
source $PREDIX_SCRIPTS/bash/quickstart.sh $QUICKSTART_ARGS

__append_new_line_log "Successfully completed $APP_NAME installation!" "$quickstartLogDir"
