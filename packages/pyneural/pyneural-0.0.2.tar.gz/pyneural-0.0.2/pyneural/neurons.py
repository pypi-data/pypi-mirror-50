class n_input(object):
    #input neuron--takes a value and send it to other neurons it is connected to
    def __init__(self,out):
        self.out = out #what neurons the input should go out to
        for each in self.out:
            each.incoming.append(self) #tell those neurons that it is attatched to them
        self.brain = None #establish a varibale for the parent
        self.id = None

    def inp(self,stren):#function takes a value input and "fires" that value to all ocnnected neurons
        self.stren = stren#value to send
        self.fire()

    def fire(self):
        for each in self.out:
            each.inp(self.stren,str(self))#sends that value out to each connection

class n_output(object):
    def __init__(self,action):
        self.set_action(action)
        self.ins = 0 #the current total value
        self.incoming = [] #list of all incoming connections
        self.posi = 0 #number of possible connections that have fired
        self.brain = None#make value for parent
        self.id = None

    def set_action(self,action):
        #compile assigned action into executable command
        comdict = {'p':"print("}#all possible commands. just print for now
        com = comdict[action[0]]#add command
        for i in range(1,len(action)):
            com = com+str(action[i])+',' #add arguments
        com = com[:-1]+"')"#remove the last comma
        self.action = com#set as the attribute

    def get_weights(self):
        self.weights = {} #this sets up the initial weights for
        for each in self.incoming:
            self.weights[str(each)] = 1/len(self.incoming)#set an equal weight for each incoming connection

    def inp(self,value,sender):
        #take an input from a connected neuron
        self.ins+=value*(self.weights[sender])*len(self.incoming) #increase the runnung total by the weighted values
        self.posi += 1#incraese number of fired neurons
        if self.posi == len(self.incoming):#check if connected neurons have fired
            self.fire()
            self.posi = 0#reset
            self.ins = 0#reset ------------maybe change this--------------

    def fire(self):
        if self.ins > 0:
            exec(self.action)
        else:
            print(False)#------------------change this-----------------

class neuron(object):
    def __init__(self,out):
        self.out = out #all outgoing connections
        for each in self.out:
            each.incoming.append(self) #tell those neurons that it is attatched to them
        self.ins = 0 #running total of input values
        self.incoming = [] #list of incoming connections
        self.posi = 0 #how many possible incoming connections have "fired"
        self.pol = 1 #whether positive or negative impulses trigger the neuron
        self.reins = [] #list of reinforce keys asoociated with the node
        self.brain = None #attribute for parent
        self.id = None

    def get_weights(self):
        hold = {}
        for each in self.incoming:#assign an equal weight to each incoming node to start. this craetes a weighted summation effect
            hold[str(each)] = 1/len(self.incoming)
        self.weights = hold

    def flip_pol(self):
        self.pol *= -1#flip whether or not negative or positive values trigger the node

    def inp(self,value,sender):
        #take an input from a connected neuron
        self.ins+=value*self.weights[sender] #increase the runnung total
        self.posi += 1
        if self.posi == len(self.incoming):#check if connected neurons have fired
            self.fire()
            self.posi = 0#reset
            self.ins = 0#rest---------------------------------maybe----------------------------------

    def fire(self):
        if self.ins*self.pol > 0 :#check if the inputs are enough
            send = self.ins #send out its value to outgoing connections
            for each in self.reins:
                self.brain.reinforce(each)
        else:
            send = 0 #do not change outgoing connections if the threshold has not been reached
        for each in self.out:
            each.inp(send,str(self)) #send the outputs to outgoing connections
