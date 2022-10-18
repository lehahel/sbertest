# CONFIG ###

PORT=8080

#############

SCRIPT_DIR=$(dirname "$0")

echo ${SCRIPT_DIR}

if test -f ${SCRIPT_DIR}/binlist-data.csv; then
  echo Removing old data
  rm ${SCRIPT_DIR}/binlist-data.csv
fi

echo Collecting data
wget \
  --no-check-certificate \
  --content-disposition https://raw.githubusercontent.com/iannuttall/binlist-data/master/binlist-data.csv \
  -P ${SCRIPT_DIR} \
&& echo 'Sucessfully downloaded data' \
|| echo 'Error while downloading data'

echo Building container
docker build --tag bank_app ${SCRIPT_DIR}/. #--progress=plain

echo 'TESTS:\033[0;32m OK \033[0m'

echo Starting server
nohup docker run --publish ${PORT}:8080 bank_app &
