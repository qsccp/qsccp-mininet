function do_compress() {
    scenario=$1
    for i in {1..10}
    do
        for ms in 30 50 100 150 200 250 300
        do
            ls ${scenario}_${ms}ms/${i}
            find ${scenario}_${ms}ms/${i} -mindepth 1 -maxdepth 1 -not \( -name 'c1' -or -name 'c2' \) -exec rm -rf {} \;
            # 遍历 ${scenario}_${ms}ms/1-10 目录，删除里面所有不为 c1 或者 c2 的文件和目录
            # find ${scenario}_${ms}ms/${i} -maxdepth 1 -not \( -name 'c1' -or -name 'c2' \) -exec rm -rf {} \;
        done

	for bd in 1 5 10 15 20 40 80 120 160
	do
            ls ${scenario}_${bd}M/${i}
            find ${scenario}_${bd}M/${i} -mindepth 1 -maxdepth 1 -not \( -name 'c1' -or -name 'c2' \) -exec rm -rf {} \;
            # 遍历 ${scenario}_${ms}ms/1-10 目录，删除里面所有不为 c1 或者 c2 的文件和目录
            # find ${scenario}_${ms}ms/${i} -maxdepth 1 -not \( -name 'c1' -or -name 'c2' \) -exec rm -rf {} \;
	done
    done
}

do_compress "compare_data/cubic_qsccp"
do_compress "compare_data/cubic_reno"
do_compress "compare_data/cubic_bic"
do_compress "compare_data/cubic_bbr"
do_compress "compare_data/cubic_cubic"
do_compress "compare_data/reno_reno"
do_compress "compare_data/bic_bic"
do_compress "compare_data/bbr_bbr"
do_compress "compare_data/qsccp_qsccp"
