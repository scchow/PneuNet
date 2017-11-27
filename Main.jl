#!/usr/bin/julia

print("loading modules...")

tic() # start timer

# bring in modules from other files. Order matters.
include("./PneuCore.jl")
include("./Input.jl")
using Input: readTimeline
using PneuCore: Interval, doCycle, writeOut

println("done!")
toc() # print timer value

#@time writeOut("Python loaded")
println()

# Broken into a function to allow setting type of timeline
function start()
	timeline = Input.readTimeline()
	println(timeline)
	# choose how long to spend on one cycle, in seconds
	cycleTime::Float16 = 1

	for a = 1:3
		# label the output
		println("Cycle $a:");
		# extra time is approximately constant,
		#  independent of the cycle length.
		@time PneuCore.doCycle(timeline, cycleTime);
	end
end

start()
