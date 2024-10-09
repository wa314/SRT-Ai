import numpy as np
import bruges as bg
import random



# Load impedance and wavelet:
impedance = np.load('path.npy')
wavelet = np.load('path.npy')


# Number of layers in "strat":
def create_strat(nb_rock_types, nb_layers):
    
    rock_layers = []
    rock_types = range(nb_rock_types)
    
    for layer in range(nb_layers):
        if layer == nb_layers - 1:
            thickness = 8 - len(rock_layers)
        else:
            thickness = int((random.random()) * (4)) + 1
               
        rock_type = rock_types[int(random.random() * nb_rock_types)] + 1
        
        if thickness > 0:
            this_layer = np.full(thickness, rock_type)
            rock_layers = rock_layers + this_layer.tolist()
        
    return (tuple(rock_layers))


# Assign acoustic impedance to layers:
def assign_properties(rock_types, impedances=impedance):

    unique_rock_types = set(rock_types) # Remove duplicate rock types
    random.shuffle(impedances)
    
    rt_map = dict(zip(unique_rock_types, impedances[:len(unique_rock_types)]))
    
    
    return tuple((rt_map.get(rt) for rt in rock_types))


def create_impedance_strat():

    # Multiple strat compinations:
    strat = []
    for i in range(100):                                        # Choose the range
        strat.append(create_strat(5, 5))
    
    #Unique strat compinations:
    unique_strat = set(strat)
    unique_stratlist = list(unique_strat)
    
    impedance_strat = []
    for i in range(len(unique_stratlist)):
        temp = assign_properties(unique_stratlist[i])
        impedance_strat.append(temp)

    tuple_impedance_strat = tuple([tuple(item) for item in impedance_strat])

    full_impedance_strat = []
    for item in range(len(tuple_impedance_strat)):
        full = ((random.choice(impedance), random.choice(impedance), random.choice(impedance)),
               tuple_impedance_strat[item],
               (random.choice(impedance), random.choice(impedance), random.choice(impedance)))
        #full = (random.choice(impedance), tuple_impedance_strat[item], random.choice(impedance))
        full_impedance_strat.append(full)
    return (full_impedance_strat)


#Geological Models:
class TwoDGeoModel():
    def __init__(self, depth, width, strat, thickness, mode, conformance):

        self.depth = depth
        self.width = width
        self.strat = strat
        self.thickness = thickness
        self.mode = mode
        self.conformance = conformance
        
        self.model = self.create_model()
    
    
    def create_model(self):
        
        model, *_ = bg.models.wedge(depth = self.depth,
                                    width = self.width,
                                    strat = self.strat,
                                    thickness = self.thickness,
                                    mode = self.mode,
                                    conformance = self.conformance)
        return model


#Synthetic Seismic:
def create_synthetic(model):

    # Reflection Coeffecient:
    rc = [(i[1:,:] - i[:-1,:]) / (i[1:,:] + i[:-1,:]) for i in model]

    # Seismic Synthetic:
    w = wavelet
    synthetic = np.array([np.apply_along_axis(lambda t: np.convolve(t, w, mode = 'same'), axis = 0,
                          arr = r) for r in rc])

    # Adding noise:
    synthetic_noisy = [s + (np.random.lognormal(0.2, 0.5)) * s.std() * np.random.random(s.shape) for s in synthetic]
    return synthetic_noisy


def save_model(fname, model):
    path = '/path'
    np.save(f'{path}/{fname}.npy', model)