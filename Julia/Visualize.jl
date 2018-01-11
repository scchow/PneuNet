#!/usr/bin/julia

module Visualize

# Must have an include() call before this.
using PneuCore: Interval, readChannel

function drawTimeline(timeline::Array{Array{Interval,1},1}, useColor::Bool = true)
	const STEPS_IN_TIMELINE = 10

	padLength = length(digits(length(timeline)))

	for channel::Int8 = 1:length(timeline)
		currIdx::Int8 = 1;
		amp::Int8 = 0;
		print(lpad(channel, padLength) * " > ")
		for currTime::Int8 in 1:STEPS_IN_TIMELINE
			(amp, currIdx) = readChannel(timeline, channel, currIdx, currTime)
			if useColor && amp == 0
				print("\033[30;1m$amp \033[0m")
			else
				print("$amp ")
			end
		end
		println()
	end
end
export drawTimeline

end
