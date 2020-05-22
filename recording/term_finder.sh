#!/bin/sh

entire=false
x=0
y=0
w=0
h=0
b=0  # b for border
t=0  # t for title (or top)


eval $(xwininfo -id $(xdotool getactivewindow) |
	sed -n -e "s/^ \+Absolute upper-left X: \+\([0-9]\+\).*/x=\1/p" \
	-e "s/^ \+Absolute upper-left Y: \+\([0-9]\+\).*/y=\1/p" \
	-e "s/^ \+Width: \+\([0-9]\+\).*/w=\1/p" \
	-e "s/^ \+Height: \+\([0-9]\+\).*/h=\1/p" \
	-e "s/^ \+Relative upper-left X: \+\([0-9]\+\).*/b=\1/p" \
	-e "s/^ \+Relative upper-left Y: \+\([0-9]\+\).*/t=\1/p" )
if [ "$entire" = true ]
then                     # if user wanted entire window, adjust x,y,w and h
	let x=$x-$b
	let y=$y-$t
	let w=$w+2*$b
	let h=$h+$t+$b
fi
echo "$w"x"$h" $x,$y
