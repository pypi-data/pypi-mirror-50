import pandas as pd, numpy as np
from numpy import linalg as LA
from numpy.linalg import inv  

def relativeImp(df, outcomeName, driverNames):
    '''   
    Return a dataframe with the raw and relative importance by driver.
    
    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        Raw input data, e.g. survey responses
    
    outcomeName: str
        Name of the outcome variable, e.g. overall satisfaction scores
        
    driverNames: list
        Names of the driver variables, e.g. satisfication drivers such as quality, ease of use etc.  
    
    Returns
    ----------
    pandas.core.frame.DataFrame
        Driver: names of the driver variables
        RawRelaImpt: the raw relative importance whose sum equals R-squared
        NormRelaImpt: the normalized relative importance whose sum equals one    
    '''

    allNames = driverNames.copy()
    allNames.insert(0, outcomeName)
    
    corrALL = df[allNames].apply(pd.to_numeric, errors='coerce').corr() 
    corrXX = corrALL.iloc[1:, 1:].copy()
    corrXY = corrALL.iloc[1:, 0].copy()
    
    w_corrXX, v_corrXX = LA.eig(corrXX)
    
    numX = len(corrXX)
    idx_diag = np.diag_indices(numX)
    diag = np.zeros((numX, numX), float)
    diag[idx_diag] = w_corrXX
    delta = np.sqrt(diag)
    
    coef_xz = v_corrXX @ delta @ v_corrXX.transpose()
    coef_yz = inv(coef_xz) @ corrXY
    
    rsquare = sum(np.square(coef_yz))
    
    rawWeights = np.square(coef_xz) @ np.square(coef_yz)
    normWeights = (rawWeights/rsquare)*100
    
    df_results = pd.DataFrame(data = {'Driver': driverNames,
                                      'RawRelaImpt': rawWeights,
                                      'NormRelaImpt': normWeights})
    return df_results