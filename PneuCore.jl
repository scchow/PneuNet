#!/usr/bin/julia

module PneuCore

# use the PyCall package
using PyCall: @pyimport, pyimport, PyVector
# add current folder to list of places to search
unshift!(PyVector(pyimport("sys")["path"]), "")
# search current folder for Output.py
@pyimport Output

# Make data structure used for each interval in the timeline
struct Interval
	start::Int8
	duration::Int8
	amplitude::Int8
end
export Interval


# runs through one cycle of the timeline
function doCycle(timeline::Array{Array{Interval,1},1}, totalTime::Float16)
	const STEPS_IN_TIMELINE = 10

	# set the index on each channel to 1
	currIndex::Array{Int8,1} = ones(length(timeline))

	# run through timeline
	for currTime::Int8 in 1:STEPS_IN_TIMELINE
		# start row with time stamp
		print("$currTime\t")

		amplitudes = []
		
		# find value of each channel
		for channel::Int8 = 1:length(timeline)
			# return value and update channel's current index
			(amp::Int8, currIndex[channel]::Int8) = 
				readChannel(timeline, channel, currIndex[channel], currTime)

			push!(amplitudes, amp)
		end

		# set all values at once
		writeOut(amplitudes);

		sleep(totalTime/STEPS_IN_TIMELINE)
	end
end
export doCycle


# return value on the selected channel given the time
function readChannel(timeline::Array{Array{Interval,1},1}, channelID::Int8, currIndex::Int8, currTime::Int8)
	# while not past last interval
	while currIndex <= length(timeline[channelID])

		# get interval to check
		currInterval::Interval = timeline[channelID][currIndex]

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

	# after last interval in timeline
	return (0, currIndex)
end
export readChannel

# will eventually change PWM pin values through Python function
function writeOut(value)
	# call python function
	Output.print_stuff(value);
end
export writeOut


end
