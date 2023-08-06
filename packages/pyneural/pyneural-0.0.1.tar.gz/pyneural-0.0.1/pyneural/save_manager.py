import os

def convert_brain(brain):
    out = [brain.inmap,brain.nmap,brain.outmap]#create a list of maps for recreating the brain
    return out

def convert_neurons(brain):
    weights = {}#dict of all of the weight dicts for each neuron
    for each in brain.nmap.keys():
        thatweight = brain.ns[each].weights #each weight dict
        for every in thatweight.keys():
            for all in brain.ins.keys():
                if str(brain.ins[all]) == every:#change all of the neuron locations to ids
                    thatweight[all] = thatweight.pop(every)
            for all in brain.ns.keys()
                if str(brain.ns[all]) == every::#" "
                    thatweight[all] = thatweight.pop(every)
        weights[each] = thatweight#return this list
    return weights

def export_info(brain,neuron,save_file):
    doc = open(save_file,'w')
    doc.write(str(brain)+'\n')#write everything to a text file with the given title
    doc.write(str(neuron)+'\n')

def save(name,brain):
    master_dir = os.getcwd()#find current directory
    if 'brain_saves' not in os.listdir(master_dir):
        os.mkdir(master_dir+'\\brain_saves')#if the save directory does not exist in the right place create one
    save_file = 'brain_saves\\'+name+'.txt'#save file name
    brain_info = convert_brain(brain)#execute setups
    neuron_info = convert_neurons(brain)
    export_info(brain_info,neuron_info,save_file)#export to file

def load(name):
    save = open('brain_saves\\'+name+'.txt','r')#open the given save
    brain_info = save.readline()#pull out maps
    neuron_info = save.readline()#pull out weights
    exec(
    'global maps'+'''
maps = '''+brain_info#use an execute to convert the strings into variables. thats an interesting pice of code rights there
    )
    exec(
    'global weights'+'''
weights = '''+neuron_info
    )
    return [maps[0],maps[1],maps[2],weights]#return everything
