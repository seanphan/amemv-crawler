
digg_count = "1000.4w"
if 'w' in digg_count:
	digg_count = int(float(digg_count.split('w')[0])*10000)
	print(digg_count)

print(digg_count)