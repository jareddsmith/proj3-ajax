def test_app():	
	min_limits = [15, 15, 15, 11.428, 13.333]
	max_limits = [34, 32, 30, 28, 26]
	change_list = [200, 400, 600, 1000, 1300]
	st_control = [0, 200/34, 825/68, 3835/204, 47245/1428, 828385/18564]
	end_control = [600/15, 400/11.428, 300/13.333]
	max_spd = 0
	min_spd = 0
	start_time = 0
	end_time = 0
	
	print("Testing is beginning")
	temp = 200/1.609
	t_conv = test_conv(temp, "mi")
	
	if test_conv(temp,"mi") == 200:
		print("Conversion test passed")
	else:
		print("Conversion failed")
		
	max_spd,min_spd = test_spdchk(199, change_list, max_limits, min_limits)
	if max_spd == 34 and min_spd == 15:
		print("Speed check for 199km passed")
	else:
		print("Speed check failed for 199km")
	
	max_spd,min_spd = test_spdchk(200, change_list, max_limits, min_limits)
	if max_spd == 32 and min_spd == 15:
		print("Speed check for 200km passed")
	else:
		print("Speed check failed")
		
	max_spd,min_spd = test_spdchk(400, change_list, max_limits, min_limits)
	if max_spd == 30 and min_spd == 15:
		print("Speed check for 400km passed")
	else:
		print("Speed check failed for 400km")
		
	max_spd,min_spd = test_spdchk(600, change_list, max_limits, min_limits)
	if max_spd == 28 and min_spd == 11.428:
		print("Speed check for 600km passed")
	else:
		print("Speed check failed for 600km")
	
	max_spd,min_spd = test_spdchk(1000, change_list, max_limits, min_limits)
	if max_spd == 26 and min_spd == 13.333:
		print("Speed check for 1000km passed")
	else:
		print("Speed check failed for 1000km")
	
	extra_time = test_extime(200, change_list, 200)
	if extra_time == 10:
		print("Extra time check for -> 200km/1000km passed")
	else:
		print("Extra time check for -> 200km/1000km passed")
		
	extra_time = test_extime(1000, change_list, 1000)
	if extra_time == 10:
		print("Extra time check for 200km/1000km <- passed")
	else:
		print("Extra time check for 200km/1000km <- passed")
		
	extra_time = test_extime(400, change_list, 400)
	if extra_time == 20:
		print("Extra time check for 400km passed")
	else:
		print("Extra time check for 400km passed")
		
	start_time,end_time = test_calc(170, max_limits[0], min_limits[0], st_control, end_control)
	if start_time == 5 and end_time == 170/15:
		print("Time test for 170km passed")
	else:
		print("Time test failed: ", test_calc(170, max_limits[0], min_limits[0], st_control, end_control))
	
	start_time,end_time = test_calc(200, max_limits[1], min_limits[1], st_control, end_control)
	if start_time == 200/34 and end_time == 200/15:
		print("Time test for 200km passed")
	else:
		print("Time test failed: ", test_calc(200, max_limits[1], min_limits[1], st_control, end_control))
	
	
    
def test_conv(dist, dist_unit):
    #Check if the units selected is miles, if so convert to kilometers.
	if dist_unit == "mi":
		dist *= 1.609
	return dist

    
def test_spdchk(dist, change_list, max_limits, min_limits):
    #A for-loop/conditional hybrid to find for the correct speeds to use
	if dist >= 0:
		for change in change_list:
			if dist < change:
				max_spd = max_limits[change_list.index(change)]
				min_spd = min_limits[change_list.index(change)]
				return(max_spd,min_spd)
	return
				
def test_extime(dist, change_list, brev_dist):
    #Calculates the extra time that is need under certain conditions.
	extra_time = 0
	if dist >= 0:
		for change in change_list:
			if brev_dist == dist:
				if dist >= brev_dist:
					dist = brev_dist
					if dist == 200 or dist == 1000:
						extra_time = 10
					elif dist == 400:
						extra_time = 20
	return extra_time

def test_calc(dist,max_spd,min_spd,st_control,end_control):
    #Calculates the times depending on the distance
	if dist in range(0,200):
		start_time = dist/max_spd + st_control[0]
		end_time = dist/min_spd

	elif dist in range(200,400):
		start_time = (dist-200)/max_spd + st_control[1]
		end_time = dist/min_spd

	elif dist in range(400,600):
		start_time = (dist-400)/max_spd + st_control[2]
		end_time = dist/min_spd

	elif dist in range(600,1000):
		start_time = (dist-600)/max_spd + st_control[3]
		end_time = dist/min_spd + end_control[0]

	elif dist in range(1000,1300):
		start_time = (dist-1000)/max_spd + st_control[4]
		end_time = (dist-1000)/min_spd + end_control[0] + end_control[1]

	elif dist > 1300:
		start_time = (dist-1300)/max_spd + st_control[5]
		end_time = (dist-600)/min_spd + end_control[0] + end_control[1] + end_control[2]
		
	return (start_time,end_time)
	
if __name__ == "__main__":
	test_app()