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
					print_with_color(:light_black, "    invalid length > ")
					println("\"$intv\"")
				end
				continue
			end

			if verbose
				print_with_color(:light_blue, "    possible interval > ")
				println("\"$intv\"")
			end

			if intv[end] == ","
				intv = intv[1:intv.length-1]
			end

			params = split(strip(intv, [',', '\n']))

			if length(params) != 3
				if verbose
					print_with_color(:light_magenta, "        invalid parameter count\n")
				end
				continue
			end

			bad = false
			for param in params
				if isnull(tryparse(Int8, param))
					if verbose
						print_with_color(:red, "        invalid integer > ")
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
				print_with_color(:green, "        interval > ")
				println(newIntv)
				total = total + 1
			end
			push!(timeline[c], newIntv)
		end

		if length(timeline[c]) == 0
			if verbose
				print_with_color(:yellow, "no intervals found. Skipping line.\n")
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
