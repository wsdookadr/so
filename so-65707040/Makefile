modif_1:
	bash -c "time ./modif1.py"

modif_2:
	bash -c 'time python3 ./modif2.py'

modif_2_p1:
	python3 -m cProfile -o modif2.prof ./modif2.py
	gprof2dot -f pstats modif2.prof  | dot -Tsvg -o modif2.svg

modif_2_p2:
	python3 -m viztracer --ignore_c_function --include_files  ~/.local/lib/python3.7/site-packages/sympy modif2.py --save_flamegraph --output_file modif2.html modif2.py

modif_2_p3:
	pyprof2calltree -o modif2.kgrind -r ./modif2.py

modif_3_p1:
	python3 -m cProfile -o modif3.prof ./modif3.py
	pyprof2calltree -k -i ./modif3.prof

modif_3_p2:
	py-spy record -o modif3_flame.svg -- python3 ./modif3.py

modif_3_p3:
	python3 -m viztracer --ignore_c_function --include_files  ~/.local/lib/python3.7/site-packages/sympy modif3.py --save_flamegraph --output_file modif3.html modif3.py

modif_4_p1:
	py-spy record -o modif4_flame.svg -- python3 ./modif4.py

diff_opt_s1:
	python3 -m cProfile -o diff_opt/s1.prof ./diff_opt/s1.py
	gprof2dot -f pstats diff_opt/s1.prof  | dot -Tsvg -o diff_opt/s1.svg

bench6:
	./bench.sh "modif6_bench.py" 2 42 > modif6_bench.txt

bench7:
	./bench.sh "modif7_bench.py" 2 68 > modif7_bench.txt

plot6:
	./plot.sh "plot.gnuplot" "modif6_bench.txt" "modif6_bench.png"
	./plot.sh "plot-log.gnuplot" "modif6_bench.txt" "modif6_bench_log.png"

plot7:
	./plot.sh "plot.gnuplot" "modif7_bench.txt" "modif7_bench.png"
	./plot.sh "plot-log.gnuplot" "modif7_bench.txt" "modif7_bench_log.png"

orig:
	bash -c "time ./orig.py"

.PHONY: modif_1 modif_2 orig
