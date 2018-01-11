#!/usr/bin/julia

print("loading modules...")

tic() # start timer

# bring in modules from other files. Order matters.
include("./PneuCore.jl")
include("./Visualize.jl")
include("./Input.jl")
using PneuCore: Interval, doCycle, writeOut, readChannel
using Input: readTimeline
using Visualize: drawTimeline

println("done!")
toc() # print timer value

@time writeOut([])
@time writeOut("Python loaded")
println()

function start()
	timeline = Input.readTimeline("mynums.txt", true)
	Visualize.drawTimeline(timeline)
	println()

	# choose how long to spend on one cycle, in seconds
	cycleTime::Float16 = 1

	for a = 1:2
		println("Cycle $a:");
		# extra time is approximately constant,
		#  independent of the cycle length.
		@time PneuCore.doCycle(timeline, cycleTime);
	end
end

start()
