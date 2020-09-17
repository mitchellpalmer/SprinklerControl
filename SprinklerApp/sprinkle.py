import sys, os, time

if len(sys.argv) != 3:
    print "Give correct number of arguments: python sprinkle.py [sprinkler id] [time to run in minutes]"
    raise SystemExit

mapIDtoWiringPi = [-1, 4, 5, 6, 27, 0, 2, 3, 21]

id = int(sys.argv[1])
timeOn = float(sys.argv[2]) * 60 # from minutes into seconds

print("turning on sprinkler {0}".format(str(id)))

os.system("gpio mode {0} out".format(str(mapIDtoWiringPi[id])))  
os.system("gpio write {0} 1".format(str(mapIDtoWiringPi[id])))  

time.sleep(timeOn)

os.system("gpio write {0} 0".format(str(mapIDtoWiringPi[id])))  
