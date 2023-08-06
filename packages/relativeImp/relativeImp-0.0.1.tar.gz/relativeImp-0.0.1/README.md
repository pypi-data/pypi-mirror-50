# Relative Importance Calculator

## Introduction

Key driver analysis is a popular and powerful tool in marketing research to quantify the relative importance of individual drivers in predicting an outcome variable. For example, marketing researchers conduct key driver analysis using customer experience survey responses to understand which aspects of the customer experience would drive the customer overall satisfaction the most.

As drivers are often highly correlated with each other, typical multiple regression analysis would produce flawed indicators of driver importance. Instead, we adopt the [relative weight analysis](https://relativeimportance.davidson.edu/Tonidandel&LeBreton(2011)_JBP_Relative%20Weights.pdf) approach which accurately partitions variance among the correlated drivers.

The Relative Importance Calculator produces the raw and normalized relative importance by driver for a specified outcome variable. The sum of the raw relative importance equals R-squared (i.e. the total proportion of variation in the outcome variable that can be explained by all the drivers) and the sum of the normalized relative importance equals one.

## Prerequisite

To use the Relative Importance Calculator, you need to have pandas and NumPy installed.

## Installation

Install the Relative Importance Calculator from [PyPI](https://pypi.org/):

```pip install relativeImp```

## Input and Output

The Relative Importance Calculator takes three mandatory input parameters and returns a pandas DataFrame:

    **Input Parameters:**
    ----------
    df: pandas.core.frame.DataFrame
        Raw input data, e.g. survey responses
    
    outcomeName: str
        Name of the single outcome variable, e.g. overall satisfaction scores
        
    driverNames: list
        Names of the driver variables, e.g. satisfication drivers such as quality, ease of use etc.  
    
    **Output Returns:**
    ----------
    pandas.core.frame.DataFrame with three columns:
        Driver: names of the driver variables
        RawRelaImpt: the raw relative importance whose sum equals R-squared
        NormRelaImpt: the normalized relative importance whose sum equals one    

## Example Code

```python
import pandas as pd
from relativeImp import relativeImp

df = pd.read_excel("raw_survey_responses.xlsx")
outcomeName = 'Overall Satisfaction'
driverNames = ['Response Time to the Service Call',
            'Efficiency of Handling the Service Call',
            'Answer/Solution Provided',
            'Knowledge of the Service Personnel',
            'Communication Skills of the Service Personnel',
            'Professionalism of the Service Personnel']

df_results = relativeImp(df, outcomeName, driverNames)
```

## Creator

Copyright &copy 2019 Dan Yang
