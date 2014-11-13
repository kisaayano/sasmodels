'''
Created on Nov 13, 2014

@author: rhf

See:
http://web.mit.edu/yamins/www/tabular/

'''

import tabular as tb
import pprint
import numpy as np
from docutils.nodes import row
from pytools.datatable import Row


class Params(object):
    '''
    classdocs
    '''


    def __init__(self, csvFilename="defs.csv"):
        '''
        Constructor
        '''
        self.filename = csvFilename
        self.data = tb.tabarray(SVfile = csvFilename, delimiter=',')
        self.data = self._increaseStringLenght(self.data)
    
    def getOldModelParamValue(self,modelName,ParamName):
        return self.data[ (self.data['model_old']==modelName)  & (self.data['param_old']==ParamName) ]['value']
    
    def getNewModelParamValue(self,modelName,ParamName):
        return self.data[ (self.data['model_new']==modelName)  & (self.data['param_new']==ParamName) ]['value']

    def getOldModelParamNamesAndValues(self,modelName):
        return self.data[ self.data['model_old']==modelName ][['param_old','value']].extract()
    
    def getNewModelParamNamesAndValues(self,modelName):
        return self.data[ self.data['model_new']==modelName ][['param_new','value']].extract()


    def _createNewCsvFileWithPDParams(self, paramsNewToExclude = ['scale', 'background', 'sld', 'solvent_sld' ]):
        """
        Create new CSV file with _pd concatenate to fields
        Save the output file as *_pd_tmp.csv
        """
        outFile = self.filename.split('.')[0]+'_pd_tmp.'+self.filename.split('.')[1]
        paramsToAddPD = np.setdiff1d(self.data['param_new'], paramsNewToExclude)
        
        for row in self.data:
            if row['param_new'] in paramsToAddPD:
                newModelParPD = row['param_new'] + "_pd"
                oldModelParPD = row['param_old'] + "_pd"
                newModelParPDN = row['param_new'] + "_pd_n"
                oldModelParPDN = row['param_old'] + "_pd_n"
                
                newRow = row.copy()
                newRow['param_new'] = newModelParPD
                newRow['param_old'] = oldModelParPD
                self.data = self.data.addrecords(newRow)
    
                newRow = row.copy()
                newRow['param_new'] = newModelParPDN
                newRow['param_old'] = oldModelParPDN
                self.data = self.data.addrecords(newRow)
    
        self.data.sort(order=['model_old','model_new','param_old','param_new'])
        self.data.saveSV(outFile)
    
    
    def _increaseStringLenght(self, nparray):
        """
        CSV to numpy cuts the string field size to the maximum strlen
        This function increases the string witdh to 48 chars
        """ 
        inTypes = nparray.dtype
        outTypes = []        
        for t in inTypes.descr:
            tout = t[1]
            if tout.startswith('|S'):
                tout = 'S48'
            outTypes.append((t[0],tout))
        return nparray.astype(outTypes)
    
    
    
def test():
    p = Params()
    #print p.data
    pprint.pprint(p.getOldModelParamValue('CappedCylinderModel','len_cyl'))
    pprint.pprint(p.getOldModelParamNamesAndValues('CappedCylinderModel'))
    
    p._createNewCsvFileWithPDParams()
    
if __name__ == "__main__":
    test()        