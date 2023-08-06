#!/usr/bin/env gnuplot
# set loadpath
load "plots/common.plot"

# datafile = 'mappings.multi.csv'
# datafile = 'test.dat'




set xlabel 'Time (ms)' font ",16"
set ylabel '# DSN' font ",16"

# nooutput
# STATS_min/STATS_max/STATS_blocks
stats datafile every ::2

# plot for [i=1:STATS_blocks] datafile index (i-1) pt 7 ps 2 title 'record '.i
# plot for [IDX=1:STATS_blocks] datafile index IDX u 1:2 w lines title "hello"

# splot '< sqlite3 healy.db3 "SELECT lon,lat,-depth FROM healy_summary WHERE depth IS NOT NULL;" | tr "|" " "' t 'depth'
# we remove 1 because our script adds 2 lines 
# pt = point type
# ps 

# show style arrow

# large / small / <size>
set bars fullwidth
# set grid lt 0 lw 0.5 lc rgb "#ff0000"

set style line 1 lt rgb "cyan" lw 3 pt 6
set style line 1 lt rgb "red" lw 3 pt 6

# 2 'pink', 3 'green',
# http://www.gnuplotting.org/defining-a-palette-with-discrete-colors/
set palette maxcolors 3
set palette defined ( 0 'green', \
					  1 'red', \
					  2 'blue' )

# unset key
unset colorbox
set colorbox
show palette
set key autotitle columnhead

#http://stackoverflow.com/questions/8717805/vary-point-color-in-gnuplot-based-on-value-of-one-column
# column(-2) returns the dataset id
# filename screen
# TODO display acks

#palette cb 

# The `set cbrange` command sets the range of values which are colored using
# the current `palette` by styles `with pm3d`, `with image` and `with palette`.
# Values outside of the color range use color of the nearest extreme
set cbrange[0:STATS_blocks-1]

print("hello world")

# http://stackoverflow.com/questions/27901349/different-color-per-dataset
# `lc variable` tells the program to use the value read from one column of the
# input data as a linetype index, and use the color belonging to that linetype

# WARN: column(-2) does not work outside of using
plot for [idx=0:STATS_blocks-1] \
	datafile index idx using "packetid":'mapping_dsn':(0):"mapping_length":(idx+1) with vectors filled head size screen 0.008,145 lt idx title sprintf("Mappings from dataset %d", idx)
	# , \
	# datafile index idx using 'packetid':"dataack":(column(-2))  with points pt 5 lc palette z title sprintf("DACKs from dataset %d", idx)



#A blank filename (’ ’) specifies that the previous filename should be reused.
	# plot "" using (0):(column('mapping_dsn')):(400):(0) with vectors filled nohead lw 5
	# plot "" every 1:1 using (column("packetid")):(column('mapping_dsn')):(50) with xerrorbars ls 1 lw 4
		

		# notitle
# plot datafile index (IDX) using (column("packetid")):(column('mapping_dsn')):(0):(column("mapping_length")) with vectors arrowstyle 1 ls (IDX+1) 
# };
