#!/usr/bin/julia

module Input

# Must have an include() call before this.
using PneuCore: Interval

function readTimeline()
	# make timeline array
	timeline::Array{Array{Interval,1},1} = []

	f = open("mynums.txt");
	f = readlines(f);
	c::Int8 = 1
	for line in f
		println(line)
		intvs = split(line, ",");
		push!(timeline, Interval[])

		for intv in intvs
			if length(intv) < 5
				continue
			end

			if intv[end] == ","
				intv = intv[1:intv.length-1]
			end

			params = split(strip(intv, [',', '\n']))

			if length(params) != 3
				continue
			end
			
			bad = false
			for param in params
				if isnull(tryparse(Int8, param))
					bad = true
				end
			end

			if bad
				continue
			end

			p1 = parse(Int8, params[1])
			p2 = parse(Int8, params[2])
			p3 = parse(Int8, params[3])

			newIntv = Interval(p1,p2,p3)
			println(newIntv)
			push!(timeline[c], newIntv)
		end

		if length(timeline[c]) == 0
			pop!(timeline)
		else
			c = c + 1
		end
	end
	println("end")

	return timeline::Array{Array{Interval,1},1}
end
export readTimeline

function getTestTimeline()
	# make timeline array
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

	return timeline::Array{Array{Interval,1},1}
end
export getTestTimeline

end
