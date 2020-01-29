from pmod import mathops as mops

x = [0.1,0.2,0.3,0.4,0.5,0.6]
y = [1.4,4.2,8.3,13.4,21.5,36.6]

nx = [0.15,0.2,0.25,0.33]

nspl = mops.spline(x,y)

nspl.pass_spline()

sp = nspl.get_spline(nx)
print(sp)