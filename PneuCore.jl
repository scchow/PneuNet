#!/usr/bin/julia

# use the PyCall package
using PyCall
# add current folder to list of places to search
unshift!(PyVector(pyimport("sys")["path"]), "")
# search current folder for Output.py
@pyimport Output

#=
for x in ARGS;
	println(x);
end
=#

# Make data structure used for each interval in the timeline
struct Interval
	start::Int8
	duration::Int8
	amplitude::Int8
end

# runs through one cycle of the timeline
function doCycle(timeline)
	# label the output
	println("Cycle $n:");

	# set the index on each channel to 1
	currIndex::Array{Integer,1} = ones(length(timeline))

	# run through timeline
	for currTime in 1:9
		# start row with time stamp
		print("$currTime\t")

		message = ""
		
		# find value of each channel
		for channel::Integer = 1:length(timeline)
			# return value and update channel's current index
			(amp, currIndex[channel]) = 
				readChannel(timeline, channel, currIndex[channel], currTime)

			# stash retreived value for setting later
			message = message * "$amp "
		end
		# set all values at once
		writeOut(message);
	end
end

# return value on the selected channel given the time
function readChannel(timeline, channelID::Integer, currIndex::Integer, currTime::Integer)
	# while not past last interval
	while currIndex <= length(timeline[channelID])

		# get interval to check
		currInterval = timeline[channelID][currIndex]

		# if we're past the starting point
		if currTime >= currInterval.start
			# if currently in interval duration
			if currTime - currInterval.start < currInterval.duration

				# return the interval's amplitude and index (since it might have incremented)
				return (currInterval.amplitude, currIndex)

			else # not in duration

				# finished one interval; check next interval
				currIndex = currIndex + 1

				# start at the top of the while loop again,
				# but fetching a different interval to test
				continue
			end
		else # not past the starting point
			# between intervals
			return (0, currIndex)
		end
	end

	# after last interval
	return (0, currIndex)
end

# will eventually change PWM pin values through Python function
function writeOut(value)
	# call python function
	Output.printStuff(value);
end

# make timeline as an ambiguous array
timeline = []

# add an array of intervals to the timeline
push!(timeline, Interval[])
# add intervals to that array
push!(timeline[1], Interval(0, 2, 2))
push!(timeline[1], Interval(4, 1, 6))
push!(timeline[1], Interval(8, 2, 8))

# add another array of intervals to the timeline
push!(timeline, Interval[])
# add intervals to that new interval
push!(timeline[2], Interval(0, 2, 2))
push!(timeline[2], Interval(3, 4, 4))
push!(timeline[2], Interval(4, 1, 6))
push!(timeline[2], Interval(8, 4, 8))

# you know the drill.
push!(timeline, Interval[])
push!(timeline[3], Interval(2, 3, 1))
push!(timeline[3], Interval(6, 2, 9))

n = 1
for n in 1:3
	doCycle(timeline);
end
