#!/bin/bash

#Проверяем существует ли директория NETCRACKER_HOME
if [[ -z ${1} ]]; then
    echo "Please provide NETCRACKER_HOME"
    echo "Example: ./gen.sh /u02/netcracker/toms/u141_dev_6300"
    exit 1
fi

# Устанавливаем директорию NETCRACKER_HOME
NETCRACKER_HOME=${1}

#/u02/netcracker/toms/temp/licgen
TMP_DIR=$(cd $(dirname $0) && pwd);

# Пересоздаем директорию
rm -rf ${TMP_DIR}/lic
mkdir ${TMP_DIR}/lic

#Копируем содержимое папки initvm в NETCRACKER_HOME
cp -r initvm/* ${NETCRACKER_HOME}/
chmod +x ${NETCRACKER_HOME}/initvm.sh

#Проверяем если ip в листе ипишников
if [[ -z "$(cat ip_list.txt)" ]]; then
    echo "ERROR: Please provide ip in file ip_list.txt"
    exit 1
fi

#Формируем массив IP
declare -a IP_LIST
IP_LIST=( `cat "ip_list.txt" | tr '\n' ' ' | tr -d '\r'`)


for IP in ${IP_LIST[@]}
do
    cd ${NETCRACKER_HOME}
    UNIQUE_ID=$(echo ${IP}| awk -F. '{print $3$4}')
    rm -f uniqueid.txt vm_external_ip.txt
    echo "============= ${IP} ============="
    echo "============= ${UNIQUE_ID} ============="
    echo ${UNIQUE_ID} > uniqueid.txt
    ./initvm.sh --dont-apply
    cd ${TMP_DIR}/licensegen
    ./licensegen.sh ${NETCRACKER_HOME}
    if [ $? -ne 0 ]; then
        echo "[Run licensegen.sh] --> FAIL"
        exit 1
    fi

    ISCLUST=$(grep '<cluster>' ${NETCRACKER_HOME}/config/config.xml |wc -l)

    if [[ "$ISCLUST" -eq 0 ]]; then
        if [[ -f "${NETCRACKER_HOME}/license.nc" ]]; then
            cp -f ${NETCRACKER_HOME}/license.nc ${TMP_DIR}/lic/license${UNIQUE_ID}.nc
        fi
    else
        if [[ -n $(find ${NETCRACKER_HOME}/servers/clust*_${UNIQUE_ID} -name "license.nc" 2>/dev/null) ]]; then
            for license_file in $(find ${NETCRACKER_HOME}/servers/clust*_${UNIQUE_ID} -name "license.nc"); do
                CLUSTER_NUM=$(echo $license_file |awk -F/ '{print $(NF-1)}' | awk -F_ '{print $1}')
                cp -f $license_file ${TMP_DIR}/lic/${CLUSTER_NUM}_license${UNIQUE_ID}.nc
            done
        fi
    fi

    if [[ ! -f "${TMP_DIR}/lic/license${UNIQUE_ID}.nc" && -z $(find ${TMP_DIR}/lic/ -name "clust*_license${UNIQUE_ID}.nc") ]]; then
        echo "[license file is not found] --> FAIL"
        exit 1
    fi
done

cd ${TMP_DIR}
cp -a initvm/initvm.sh ./
cp -a initvm/init_customers_sequence.sql ./
cp -a initvm/update_netcracker_url.sql ./

zip -rq lic.zip lic/ initvm.sh init_customers_sequence.sql update_netcracker_url.sql
if [ $? -ne 0 ];then
    echo "[Packing lic.zip] --> FAIL"
    exit 1
else
    echo "[Packing lic.zip] --> DONE"
fi
