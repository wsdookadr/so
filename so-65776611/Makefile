bench:
	./bench.sh bininssort.py reversed    3000 3000 $$((3000 * 30)) > bench_reversed.txt
	./bench.sh bininssort.py alternating 3000 3000 $$((3000 * 30)) > bench_alternating.txt

plot:
	match-growth.py --infile bench_alternating.txt --outfile time_alternating.png --col1 N --col2 time --top 1
	match-growth.py --infile bench_reversed.txt    --outfile time_reversed.png    --col1 N --col2 time --top 1
	convert +append time_reversed.png time_alternating.png time_all.png

.PHONY: bench plot
