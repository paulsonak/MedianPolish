import numpy as np

class MedianPolish:
    """Fits an additive model using Tukey's median polish algorithm"""

    def __init__(self, array): 
        """Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org"""
        if isinstance(array, np.ndarray):
            self.tbl_org = array
            self.tbl = self.tbl_org.copy()
        else:
            raise TypeError('Expected the argument to be a numpy.ndarray.')

    @staticmethod            
    def csv_to_ndarray(fname): 
        """ Utility method for loading ndarray from .csv file""" 
        try:
            return np.genfromtxt(fname, delimiter=",")    
        except e:
            print("Error loading file %s:" % fname)
            raise

    def median_polish(self, max_iterations=10, method='median'):
        """
            Implements Tukey's median polish alghoritm for additive models
            method - default is median, alternative is mean. That would give us result equal ANOVA.
        """
        

        grand_effect = 0
        median_row_effects = 0
        median_col_effects = 0
        row_effects = np.zeros(shape=self.tbl.shape[0])
        col_effects = np.zeros(shape=self.tbl.shape[1])

        for i in range(max_iterations):
            if method == 'median':
                row_medians = np.median(self.tbl  ,1) 
                row_effects += row_medians
                median_row_effects = np.median(row_effects)
            elif method == 'average':
                row_medians = np.average(self.tbl  ,1) 
                row_effects += row_medians
                median_row_effects = np.average(row_effects)
            grand_effect += median_row_effects
            row_effects -= median_row_effects
            self.tbl -= row_medians[:,np.newaxis] 

            if method == 'median':
                col_medians = np.median(self.tbl,0) 
                col_effects += col_medians
                median_col_effects = np.median(col_effects)
            elif method == 'average':
                col_medians = np.average(self.tbl,0) 
                col_effects += col_medians
                median_col_effects = np.average(col_effects)

            self.tbl -= col_medians 

            grand_effect += median_col_effects

        return grand_effect, col_effects, row_effects , self.tbl, self.tbl_org



if __name__ == "__main__":    
    
    # Example and data on volume of rubber taken from chapter 6 of 
    # William N. Venables and Brian D. Ripley (2002). Statistics Complements to Modern Applied Statistics with S, ISBN 0-387-95457-0.
    #data_file='ripley.csv'
    #arr = MedianPolish.csv_to_ndarray(data_file) * 10000 
    
    # Example and data on Arisona state temperature taken from 
    # Chapter 10 of Tukey, John W (1977). Exploratory Data Analysis. Addison-Wesley. ISBN 0-201-07616-0.
    data_file = "ArizonaTmp.csv"
    arr = MedianPolish.csv_to_ndarray(data_file) 
    
    mp = MedianPolish(arr) 
    ge, ce, re , resid, tbl_org =  mp.median_polish(4) 
    print("median polish:")
    print("grand effect = ", ge)
    print("column effects = ", ce )
    print("row effects = ", re )
    print("-----Table of Residuals-------" )
    print(resid)
    print("-----Original Table-------")
    print(tbl_org)

    ge, ce, re , resid, tbl_org =  mp.median_polish(4 , "average")
    print('\n')
    print("average polish:" )
    print("grand effect = ", ge)
    print("column effects = ", ce )
    print("row effects = ", re )
    print("-----Table of Residuals-------" )
    print(resid)
    print("-----Original Table-------")
    print(tbl_org)

