#!/usr/bin/julia

module Input

# Must have an include() call before this.
using PneuCore: Interval

# reads timeline from file. Check README.md for more details.
function readTimeline(filename::String, verbose::Bool = false)
	# make timeline array
	timeline::Array{Array{Interval,1},1} = []

	f = open(filename);
	f = readlines(f);
	c::Int8 = 1
	total::Int8 = 0

	for line in f
		if verbose
			println("reading line > \"$line\"")
		end
		
		intvs = split(line, ",");
		push!(timeline, Interval[])

		for intv in intvs
			if length(intv) < 5
				if verbose
					print("\033[30;1m    invalid length > \033[0m")
					println("\"$intv\"")
				end
				continue
			end

			if verbose
				print("\033[36m    possible interval > \033[0m")
				println("\"$intv\"")
			end

			if intv[end] == ","
				intv = intv[1:intv.length-1]
			end

			params = split(strip(intv, [',', '\n']))

			if length(params) != 3
				if verbose
					print("\033[35;1m        invalid parameter count\033[0m\n")
				end
				continue
			end

			bad = false
			for param in params
				if isnull(tryparse(Int8, param))
					if verbose
						print("\033[31m        invalid integer > \033[0m")
						println("\"$param\"")
					end
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

			if verbose
				print("\033[32m        interval > \033[0m")
				println(newIntv)
				total = total + 1
			end
			push!(timeline[c], newIntv)
		end

		if length(timeline[c]) == 0
			if verbose
				print("\033[33mno intervals found. Skipping line.\033[0m\n")
			end
			pop!(timeline)
		else
			c = c + 1
		end
		if verbose
			println()
		end
	end

	if verbose
		println("reached end of file.")
		println("found $total intervals across $(length(timeline)) channels.\n")
	end

	return timeline::Array{Array{Interval,1},1}
end
export readTimeline

# Returns a statically-defined 
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
