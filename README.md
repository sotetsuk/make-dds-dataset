### How to make dds dataset used in Pgx

1. build `libdds.so`
    * clone [dds-bridge/dds](https://github.com/dds-bridge/dds) 
    * follow `INSTALL` instruction. In ubuntu 20.04, I used `Makefile_Mac_gcc_shared` and changed threading and link option to remove boost dpendency: 
        * `THREADING	= $(THR_OPENMP) $(THR_STL)`
        * `THREAD_LINK	= -fopenmp`
    * copy `libdds.so` here
2. copy `ddstable.py` from [xrgopher/ddstable](https://gitlab.com/xrgopher/ddstable)
3. install dependencies: `numpy` and `tqdm`
3. run `python3 make_dds_results.py 0 > results.tsv` (specify `seed`)
4. run `to_bytes.py results.tsv`
