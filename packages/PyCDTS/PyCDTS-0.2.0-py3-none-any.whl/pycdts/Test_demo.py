from Project import Project

P=Project()
#P.inputDataFile='./Cl_0D_750K.mat'
P.inputDataFile='./As0D_process_1em14.mat'
#P.inputDataFile='./Acceptor_0D_ZnTe.mat'
#P.inputDataFile='./DiffTest_2D.mat'
P.numEng.enableDS=1
P.numEng.typeDS=1
P.numEng.enablePS=1
P.numEng.typePS=0
P.numEng.enableRS=1
P.numEng.typeRS=1
P.numEng.debugFlgEnableCorrections=0
P.numEng.debugFlgEnableCorrectionsInsideWhileLoop=0
P.setDataToNumEngine()

P.runRecipe()