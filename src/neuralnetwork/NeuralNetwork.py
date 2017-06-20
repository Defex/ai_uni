import numpy as np

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    # print(str(x) + " " + str(1/(1+np.exp(-x))))
    return 1/(1+np.exp(-x))

class NeuralNetwork():
    def __init__(self):
        self.X = np.empty
        self.Y = np.empty
        self.Xtest = np.empty
        self.Ytest = np.empty
        self.results = np.empty
        np.random.seed(1)
        # np.seterr(over='raise')
        self.syn0 = 0.5*np.random.random((136*2,500)) - 0.25
        self.syn1 = 0.5*np.random.random((500,1)) - 0.25
        self.firstInput = True
        self.firstTestInput = True

    def load_test_match(self, training_data):
        if(self.firstTestInput):
            self.Xtest = np.array([training_data[0:136*2:1]])
            self.Ytest = np.array([[training_data[136*2]]])
            self.results = self.Ytest
            self.firstTestInput = False
        else:
            self.Xtest = np.append(self.Xtest, [training_data[0:136*2:1]], axis=0)
            self.Ytest = np.append(self.Ytest, [[training_data[136*2]]], axis=0)
            self.results = self.Ytest

    def clear_test_match(self, training_data):
        self.Xtest = np.empty
        self.Ytest = np.empty
        self.results = np.empty
        self.firstTestInput = True

    def test(self):
        l0 = self.Xtest
        l1 = nonlin(np.dot(l0,self.syn0))
        l2 = nonlin(np.dot(l1,self.syn1))

        l2_error = self.Ytest - l2
        self.results = l2_error

        # for i in range(self.Ytest.size):
        #     print("expected: " + str(self.Ytest[i][0]) + " got " + str(l2[i][0]) + " dif " + str("{0:.5f}".format(l2_error[i][0])))
        
        mse = (l2_error ** 2).mean(axis=0)
        print("test mse: " + str("{0:.5f}".format(mse[0])))
        return self.results

    def load_one_match(self, training_data):
        if(self.firstInput):
            self.X = np.array([training_data[0:136*2:1]])
            self.Y = np.array([[training_data[136*2]]])
            self.firstInput = False
        else:
            self.X = np.append(self.X, [training_data[0:136*2:1]], axis=0)
            self.Y = np.append(self.Y, [[training_data[136*2]]], axis=0)
    
    def train_times(self, n):
        for j in range(n):
            l0 = self.X
            l1 = nonlin(np.dot(l0,self.syn0))
            l2 = nonlin(np.dot(l1,self.syn1))

            l2_error = self.Y - l2

            if (j%1 == 0):
                mse = (l2_error ** 2).mean(axis=0)
                # for i in range(self.Y.size):
                #     print("expected: " + str(self.Y[i][0]) + " got " + str(l2[i][0]) + " dif " + str("{0:.5f}".format(l2_error[i][0])))
                print("All champs mse: " + str("{0:.5f}".format(mse[0])))
                # print("Error:" + str(np.abs(l2_error)))
        
            l2_delta = l2_error*nonlin(l2,deriv=True)

            l1_error = l2_delta.dot(self.syn1.T)

            l1_delta = l1_error*nonlin(l1,deriv=True)

            self.syn1 += 0.0003*l1.T.dot(l2_delta)
            self.syn0 += 0.0003*l0.T.dot(l1_delta)