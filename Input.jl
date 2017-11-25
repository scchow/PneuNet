#!/usr/bin/julia

module Input

# Must have an include() call before this.
using PneuCore: Interval

function getTimeline()
	# make timeline array
	#timeline = Array{Interval[]}()
	#timeline = []
	timeline::Array{Array{Interval,1},1} = []

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

	return timeline
end
export getTimeline


end
