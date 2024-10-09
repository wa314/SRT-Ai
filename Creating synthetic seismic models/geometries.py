import numpy as np
import synthetics as syn
import random as rn


impedance_model = syn.create_impedance_strat()

geometry_1 = []
for i in range(100):                                         # Choose hown many models you want to build
    a = rn.randint(90, 100)/100                              # Model Slope
    temp = syn.TwoDGeoModel(depth = (10, 80, 10),            
                            width = (0, 200, 0),             
                            strat = impedance_model[i],      
                            thickness = (1, a),              
                            mode = 'linear',                 
                            conformance = 'none')            
    geometry_1.append(temp.model)


syn_geometry_1 = syn.create_synthetic(geometry_1)
syn_geometry_1 = np.array(syn_geometry_1, dtype='float16')

syn.save_model('name', syn_geometry_1)