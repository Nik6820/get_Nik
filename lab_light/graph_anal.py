import lightFunctions as lf 
photo=["mercury_1_white", "mercury_1_yellow", "mercury_1_red", "mercury_1_green", "mercury_1_blue",
       "mercury_2_white", "mercury_2_yellow", "mercury_2_red", "mercury_2_green", "mercury_2_blue",
       "warm_white", "warm_yellow", "warm_red", "warm_green", "warm_blue"]
for ph in  photo:
    lamp=ph[:ph.index("_")]
    num=""
    ph=ph[::-1]
    colorreverse=ph[:ph.index("_")]
    color=colorreverse[::-1]
    ph=ph[::-1]
    if lamp=="mercury":
        num=ph[ph.index("_")+1]
        data = lf.readIntensity("photo/"+ ph+".jpg", "spectrum_"+lamp+"_"+num+"_"+color+".jpg", lamp, color)
    else:
        data = lf.readIntensity("photo/"+ ph+".jpg", "spectrum_"+lamp+"_"+color+".jpg", lamp, color)