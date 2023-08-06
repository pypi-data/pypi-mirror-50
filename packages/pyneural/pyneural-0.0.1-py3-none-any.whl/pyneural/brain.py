from neurons import n_input,n_output,neuron
import save_manager as sama

class Brain(object):
    def __init__(self,inmap,nmap,outmap):
        for each in [inmap,nmap,outmap]: #make sure all entries are dicts
            assert isinstance(each,dict)
        self.inmap = inmap #establish neurons given their connections/actions
        self.outmap = outmap
        self.nmap = nmap
        self.reins = {}
        self.get_connections() #just eye candy. bundles all of the "get" functions


    def get_outs(self):
        self.outs = {}
        for each in self.outmap.keys():
            self.outs[each] = n_output(self.outmap[each])#creates output neurons from output connetion map
            self.outs[each].brain = self#tell neuron that it is part of this brain
            self.outs[each].id = each

    def get_ns(self):
        self.ns = {}
        self.ntons = []#list of neurons conected to other neurons
        for each in self.nmap.keys():
            connections = []#list of connections for each
            for every in self.nmap[each]:
                try: #this try except loop checks if the specified neuron is
                    connections.append(self.outs[every])
                except KeyError:
                    self.ntons.append(each)#if the current neuron has a key that is not in outputs, it moves the current neuron to ntons
                    break
            self.ns[each] = neuron(connections)# creates the actual neuron object
            self.ns[each].brain = self
            self.ns[each].id = each

    def get_ntons(self):#---------------------------fix gating mechanism-----------------------------
        change = True
        while len(self.ntons) > 0:#this one is an experience. this works through nton neurons and tries to get their connections
            if change == False:
                raise KeyError#this is to actually keep the keyerror if keys are actually entered wrong. otherwise the while loop will run infinitely
            change = False
            for each in self.ntons:
                connections = []#this does about the same thing as the last one
                self.ntons.remove(each)#here we remove the current neuron from the list so the list remains not yet found ones only
                for every in self.nmap[each]:
                    if every in self.ns:#check if the value is in ins or ns
                        connections.append(self.ns[every])
                    elif every in self.ins:
                        connections.append(self.ins[every])
                    else:
                        self.ntons.append(each)#if its in neither, readd to the list of unused values
                        break
                self.ns[each] = neuron(connections)#create neurons with the correct connections once they are found
                self.ns[each].brain = self
                self.ns[each].id = each

    def get_ins(self):
        self.ins = {} #this does basically the same thing as the last one just without all of the nasty nton stuff
        for each in self.inmap:
            connections = []
            for every in self.inmap[each]:
                try:
                    connections.append(self.ns[every])
                except KeyError:
                    connections.append(self.outs[every])
            self.ins[each] = n_input(connections)
            self.ins[each].brain = self
            self.ins[each].id = each

    def get_polarities(self):
        for each in self.ns.keys():
            if each[0] == '-':#check if the node is negative and change whether it responds to negative or positive impulses.
                self.ns[each].flip_pol()

    def get_connections(self):
        self.get_outs()#execute all of those lovely functions
        self.get_ns()
        self.get_ntons()
        self.get_ins()
        for each in self.outs.keys():#get initial weights for each after all neurons are added
            self.outs[each].get_weights()
        for each in self.ns.keys():
            self.ns[each].get_weights()
        self.get_polarities()#get the polarities

    def stim(self,inp,value):
        self.ins[inp].inp(value)#brain function for handling inputs

    def add_reinforcement_node(self,target,inp,value):
        key = inp+target
        self.reins[key] = [inp,value,target]#add the key for the reinforceable connection to the brains reins
        self.ns[target].reins.append(key)#add it to the target neuron's reins list

    def reinforce(self,key):
        rein = self.reins[key]#find the right reinforcement node
        value = rein[1] #unpack the values from that node
        target = self.ns[rein[2]]#" "
        if rein[0] in self.ins:#" "
            inp = self.ins[rein[0]]# check if inp is from ins or ns
        elif rein[0] in self.ns:
            inp = self.ns[rein[0]]#" "
        else:
            raise KeyError
        weights = target.weights#set the correct weights list

        for each in weights.keys():
            if each == str(inp):
                weights[each] += value#increase the correct value by the set amount
            else:
                weights[each] -= value/(len(weights)-1)#decrese all other values to compensate
    def save(self,name):
        sama.save(name,self)#use save manager to save the file

def load(name):#load a brain from a specific file
    info = sama.load(name)#get the list of outputs from the save file
    brain = Brain(info[0],info[1],info[2])#create a new brain from the maps
    for every in info[3].keys():#keys for each weight dict
        for all in info[3][every].keys():#keys for each weight
            if all in brain.ins:
                info[3][every][str(brain.ins[all])] = info[3][every].pop(all)#replace id with neuron loaction for each weight
            elif all in brain.ns:
                info[3][every][str(brain.ns[all])] = info[3][every].pop(all)#" "
    for each in brain.ns.keys():
        brain.ns[each].weights = info[3][each]#set the weights for each neuron
    return brain#return loaded brain
