#!/bin/bash
function do_compare() {
    scenario=$1
    echo "Running $scenario"
    for i in {1..5}
    do
        echo "Running $scenario $i"
        mkdir -p /mini-ndn/compare_data/${scenario}_10ms
        python scenarios/$scenario.py compare_10ms.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_10ms/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_20ms
        python scenarios/$scenario.py compare_20ms.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_20ms/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_40ms
        python scenarios/$scenario.py compare_40ms.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_40ms/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_60ms
        python scenarios/$scenario.py compare_60ms.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_60ms/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_80ms
        python scenarios/$scenario.py compare_80ms.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_80ms/${i}
    done
    echo "Finished $scenario"
}

function do_bd_compare() {
    scenario=$1
    echo "Running $scenario"
    for i in {1..5}
    do
        echo "Running $scenario $i"
        mkdir -p /mini-ndn/compare_data/${scenario}_5M
        python scenarios/$scenario.py compare_100ms_5M.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_5M/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_10M
        python scenarios/$scenario.py compare_100ms_10M.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_10M/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_15M
        python scenarios/$scenario.py compare_100ms_15M.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_15M/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_20M
        python scenarios/$scenario.py compare_100ms_20M.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_20M/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_25M
        python scenarios/$scenario.py compare_100ms_25M.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_25M/${i}
        mkdir -p /mini-ndn/compare_data/${scenario}_30M
        python scenarios/$scenario.py compare_100ms_30M.conf
        mv /tmp/minindn /mini-ndn/compare_data/${scenario}_30M/${i}
    done
    echo "Finished $scenario"
}

do_compare "cubic_reno"
do_compare "cubic_cubic"
do_compare "cubic_bic"
do_compare "cubic_bbr"
#do_compare "cubic_qsccp"
do_compare "reno_reno"
do_compare "bic_bic"
do_compare "bbr_bbr"
#do_compare "qsccp_qsccp"

do_bd_compare "reno_reno"
do_bd_compare "cubic_cubic"
do_bd_compare "bic_bic"
do_bd_compare "bbr_bbr"
#do_bd_compare "qsccp_qsccp"

do_bd_compare "cubic_reno"
do_bd_compare "cubic_bic"
do_bd_compare "cubic_bbr"
#do_bd_compare "cubic_qsccp"
