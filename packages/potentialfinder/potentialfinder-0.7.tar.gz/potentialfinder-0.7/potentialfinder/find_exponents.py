import os
import pandas as pd
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import sys
import pathlib

def find_exponents(df,
                   fractionToAnalyze=1,
                   outputPath='outputs',
                   outputTable=True,
                   outputPlots=True,
                   timescaling='mon', 
                   outputTablename='Testtable',
                   logToScreen=True,
                   columnFillThreshold=0.5,
                   exp_threshold=0.01,
                   r_s_threshold=0.9,
                   maxrows=5000,
                   debug=False):
    '''
    find and plot plot exponential data in a pandas dataframe 

    :param dataframe df: The dataframe containing date-like and metric columns
    :param str fractionToAnalyze: The last xx percent (0.0-1.0) of data (indexed by the found date columns)
    :param str outputPath: The subfolder to write output table and plots to (created if not existing)
    :param bln outputTable: Write table to outputPath/table (True|False)
    :param bln outputPlots: Plot outputs to outputPath/plots (True|False)
    :param str timescaling: (sec|min|hour|day|mon|year) scaling the exponential factors to the given time unit
    :param str outputTablename: The table name used in the table, and the output plots
    :param bln logToScreen: Print out messages (True|False)
    :param dbl columnFillThreshold: filter out columns with more than xx percent (0.0-1.0) of the data missing
    :param dbl exp_threshold: only show and plot results with an exponent higher than x
    :param dbl r_s_threshold: only show and plot results with an r squared lower than x
    :param int maxrows: specify the maximum number of rows. If df.rowsize > maxrows a random sample of rows is used
    :param bln debug: raise errors instead of continuing if True
    :return: A Pandas dataframe with a list of all date and metric column combinations with their exponential factor and R squared 
    :rtype: dataframe
    '''
    ######################## Functions: #########################
    def is_nan(x):
        return (x is np.nan or x != x)
    
    def printL(text):
        if logToScreen:
            print(text)
            
    def normalize(lst):
        minval=min(lst)
        maxval=max(lst)
        return [(float(i)-minval)/(maxval-minval) for i in lst]

    def powerfit(x, y):
        """line fitting on y-log scale"""

        slope, intercept, r, _, _=linregress(x,np.log(y))
        r_squared=r*r
        printL('slope: '+str(slope))
        printL('intercept:'+str(intercept))
        printL('r_squared:'+str(r))
        #k, m = np.polyfit(x, np.log(y), 1)
        return slope,intercept,r_squared

    def cleanfilename(filename,cleanlist):
        text=filename
        for cleanword in cleanlist:
            text = text.replace(cleanword, '-')
        text=text.replace('-----','-')
        text=text.replace('----','-')
        text=text.replace('---','-')
        text=text.replace('--','-')
        text=text.replace('-','-')
        if text!=filename:
            printL("Warning: Provided filename '"+filename+"' is invalid. Set to '"+text+"'")
        return text
    
    def checkAndGetBool(val):
        if isinstance(val, str):
            return val.lower() in ['true', '1', 't', 'y', 'yes']
        if isinstance(val, (int, float)):
            if val>=1:
                return 1
            else:
                return 0

        
    ############################ Input handling: #############################
    data=df
    ##### Input handling: logToScreen ###
    logToScreen=checkAndGetBool(logToScreen)
    #### Input handling: maxrows ##############  
    if maxrows<=0:
        rownum=df.shape[0]
        maxrows=min(rownum,5000)
        printL("Warning: maxrows cannot be <1. Set to " + str(rownum))
        
    ##### Input handling: df ###################
    if df is None:
        printL("Warning: Dataframe is empty. Returning None")
        return None
    if df.shape[0]==0:
        printL("Warning: Dataframe is empty. Returning None")
        return None    
    if df.shape[0]>maxrows:
        data=data.sample(maxrows)
        
    ##### Input handling: fractionToAnalyze ###  
    ##### ensure that the fraction is between 0 and 1:   
    if fractionToAnalyze>1:
        printL("Warning: Fraction to analyze was specified > 1 ! Set to 1" )
        fractionToAnalyze=1
    if fractionToAnalyze<=0:
        printL("Warning: Fraction to analyze was specified <= 0 ! Set to 0.1" )
        fractionToAnalyze=0.1
        
    ##### Input handling: outputPath ###  
    outputPath=outputPath.replace("//","/")
    outputPath=outputPath.replace("\\","/")
    outputPath=outputPath.replace("\\\\","/")
    if outputPath[:1]==".":
        if outputPath[0:2]!="./":
            outputPath="./"+outputPath[1:]
    elif outputPath[0:1]=="/":
            outputPath="."+outputPath
    else:
        outputPath="./"+outputPath    

    
    ####ensure that output folders exist:
    cwd = pathlib.Path.cwd() #used to handle paths in different environments
    if outputPlots:
         #ensure output folder is existing:
        if not (cwd/outputPath).is_dir():
            pathlib.Path("./"+outputPath+"/").mkdir(parents=True, exist_ok=True)
        if not (cwd/outputPath/"plots").is_dir():
            pathlib.Path("./"+outputPath+"/plots").mkdir(parents=True, exist_ok=True)                
    if outputTable:
       #ensure output folder is existing:
        if not (cwd/outputPath).is_dir():
                pathlib.Path("./"+outputPath+"/").mkdir(parents=True, exist_ok=True)
        if not (cwd/outputPath/"table").is_dir():
                pathlib.Path("./"+outputPath+"/table").mkdir(parents=True, exist_ok=True)


    ##### Input handling: outputTable ###
    outputTable=checkAndGetBool(outputTable)

    ##### Input handling: outputPlots ###
    outputPlots=checkAndGetBool(outputPlots)
    
    ##### Input handling: timescaling ###
    if timescaling in ['sec','s','seconds','se','second']:
        timeScalingDivisor=1000
    elif timescaling in ['min','mi','minutes','minute']:
        timeScalingDivisor=1000*60
    elif timescaling in ['hour','h','ho','hou','hours']:
        timeScalingDivisor=1000*60*60    
    elif timescaling in ['day','d','da','days']:
        timeScalingDivisor=1000*60*60*24
    elif timescaling in ['mon','mo','month','months']:
        timeScalingDivisor=1000*60*60*24*30.4366666666
    elif timescaling in ['year','yea','ye','y','years']:
        timeScalingDivisor=1000*60*60*24*30.4366666666*365
    else:
        printL("Warning: No valid timescaling provided (sec|min|hour|day|mon|year). Set to month.")
    
    ##### Input handling: outputTablename ###
    if outputTablename is None:
        printL("Warning: No valid outputTableName provided. As it is used for file naming, 'testtable' is used.")
        outputTablename="testtable"
        
    ##### Input handling: columnFillThreshold ###
    if columnFillThreshold>1:
        printL("Warning: columnFillThreshold was specified > 1 ! Set to 1" )
        columnFillThreshold=1
    if columnFillThreshold<=0:
        printL("Warning: columnFillThreshold was specified <= 0 ! Set to 0.1" )
        columnFillThreshold=0.1

        
        
    ############################ Code: #############################

    
    #### specify the columns of the returntable:
    resulttablecols=['tablename','datecol','valuecol','analyzed_fraction','exponent','r_squared'] 
    
    printL ('######## Starting ' + outputTablename + ' ###### fraction '+str(fractionToAnalyze)+'########')
    printL ('##########################################')
    
    #### specify which column types are regarded as numeric (and get analyzed):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    #### specify which chars to remove in the filenames:
    cleanlist=['(',')',' ',':','[',']','#','/']  
    

    #### initialize an empty data frame with the columns for returning the results:
    df_result = pd.DataFrame(columns=resulttablecols)
    
    #### Loop through all datetimecols:
    for datetimecol in data.columns: 
        df_temp=data.copy()

             
        ### identify date columns and append as converted column (datetime) and converted2 (numeric - for correlation)
        
        if any(df_temp[datetimecol].astype(str).str.len()<4):
            printL("####### The datetime column "+ datetimecol+": has less than 4 chars --> not used as datetime column.")
            continue
        try:
            df_temp['date_converted']=pd.to_datetime(df_temp[datetimecol])
            df_temp['date_converted2']=mdates.date2num(df_temp['date_converted'])
        except:
            if debug:
                raise
            else:
                printL("####### Datetime column "+ datetimecol+": conversion error!")
                continue
        if any(df_temp['date_converted'] < '1990-01-01'):
            printL("####### The datetime column "+ datetimecol+" had values before 2000-01-01 --> not used as date")
            continue
        if datetimecol!='date_converted':
            printL("####### The datetime column: "+ datetimecol + " is used as datetimecol!")

            
        ### filter columns where only 50% of the rows have values:
        df_temp= df_temp.loc[:, df_temp.isnull().mean() < columnFillThreshold]
        
        ### Only use the last fraction of the data, indexed / determined by the time column at hand:
        maxval=max(df_temp['date_converted2']) #use converted time columns to allow for easy multiplication
        minval=min(df_temp['date_converted2'])
        timepoint_to_cut=(maxval-minval)*(1-fractionToAnalyze)+minval
        df_temp=df_temp[(df_temp['date_converted2'] > timepoint_to_cut)]
 
        ###loop through all numeric cols:
        for numericcol in data.select_dtypes(include=numerics).columns:
            if numericcol==datetimecol or numericcol not in df_temp.columns:
                continue ###skip this column if it is the date col
            try:
                #### zero values will break the algorithm with log calculations. 
                #### Therefore, we move all data points slightly above 0.
                #### 'slightly" is defined as min_max_diff/100000

                min_max_diff=max(df_temp[numericcol])-min(df_temp[numericcol])
                min0=False
                if min(df_temp[numericcol])==0:
                       min0=True
                shiftamount=min_max_diff/100000
                #### Start computing the values:
                printL('##### Computing numeric col: '+ numericcol)
                printL('##### Date col: '+datetimecol)
                cols_to_keep=['date_converted','date_converted2',datetimecol,numericcol]
                df_temp_2=df_temp[cols_to_keep].copy()# this df is used for cleaning and afterwards splitted
                #remove all rows with nan or inf:
                df_temp_2=df_temp_2.replace([np.inf, -np.inf], np.nan)
                df_temp_2=df_temp_2.dropna(subset=[numericcol])
                df_temp_2=df_temp_2.sort_values(['date_converted'],ascending=True)

                #now get minimum val, and move all points if negative:
                minval=min(df_temp_2[numericcol])


                #df_temp_2 is used for the regular plot, df_temp_3 is used for log calculations/plots (values are moved here):
                df_temp_3=df_temp_2
                if minval<=0:
                    df_temp_3[numericcol]=df_temp_3[numericcol]+shiftamount 
                    df_temp_3[numericcol]=df_temp_3[numericcol]-minval
                    printL('! moved by '+str(minval) +' to correct for negative values')


                x=df_temp_3['date_converted2']
                y=df_temp_3[numericcol]
                datetime=df_temp_3['date_converted']#datetime

                #### fit a regression line and get the slope (= exponential factor):
                slope,intercept,r_s=powerfit(x,y)   ###TODO:sebastian:checkRMSE
                y_lin = slope*x + intercept
                
                slope=slope*timeScalingDivisor
                if r_s<r_s_threshold or slope<exp_threshold or is_nan(r_s) or is_nan(slope):
                    continue

                #append to output table:
                df_result=df_result.append(pd.Series([outputTablename,datetimecol,numericcol,fractionToAnalyze,slope,r_s],index=resulttablecols),ignore_index=True)
                if outputTable:
                    df_result.to_csv(str(pathlib.Path(outputPath+'/table/'+cleanfilename(outputTablename+"-"
                                +str(int(round(fractionToAnalyze*100,0)))+"perc.csv",cleanlist))))   
                ################################### Plotting #########################################
                    
                if outputPlots:

                    
                    ########### Plotparameters:
                    figsize_plot=(11,5) #inches
                    fontsize_plot=12
                    linestyle='-'#'--'
                    linewidth_plot=2
                    ############################ Plot 1: Logarithmized - Dev ############################
                    fig, ax = plt.subplots(figsize=figsize_plot)
                    plt.plot(datetime, y,'.', alpha=.3,color="#3e5463") #plotting the values

                    ##exp to all y values: 
                    ys_exp = [math.exp(x) for x in y_lin]

                    plt.plot(datetime,ys_exp,linestyle, linewidth=linewidth_plot,color='#F38d00') #plotting the line

                    #plotting additional information:
                    plt.annotate("ex="+str(round(slope,4)), xy=(0.95,0.95),xycoords='axes fraction',
                     fontsize=fontsize_plot)
                    plt.annotate("r_squared="+str(round(r_s,4)), xy=(0.95,0.90),xycoords='axes fraction',
                     fontsize=fontsize_plot)
                    plt.title(datetimecol+"~"+numericcol + " (fraction: last "+str(100*fractionToAnalyze)+"%)", fontsize=14)
                    plt.yscale('log')
                    if min0: #only set min y axis if 0 values are existing:
                        x1,x2,y1,y2 = plt.axis()
                        plt.axis((x1,x2,shiftamount/10,y2))
                        #plt.annotate("0 (no log)", xy=(-0.005,shiftamount),xycoords=('axes fraction','data'),fontsize=fontsize_plot,color='red',ha='right')

                    plt.xticks(rotation=90)
                    ax.spines['right'].set_visible(False)
                    ax.spines['top'].set_visible(False)
                       
                    plt.savefig(str(pathlib.Path(outputPath+'/plots/'+cleanfilename(outputTablename+'-'+datetimecol+'-'
                                +numericcol,cleanlist)+'-'+str(int(round(fractionToAnalyze*100,0)))+'perc-log.png')))
                    plt.close('all')
                    


                    
                ############################ Plot 2: Regular Plot - Dev ############################
                    fig, ax = plt.subplots(figsize=figsize_plot)

                    plt.plot(datetime, y,'.', alpha=.3,color="#3e5463") #plotting the values

                    plt.plot(datetime,ys_exp,linestyle, linewidth=linewidth_plot,color='#F38d00') #plotting the line

                    #plotting additional information:
                    plt.annotate("ex="+str(round(slope,4)), xy=(0.95,0.95),xycoords='axes fraction',
                     fontsize=fontsize_plot)
                    plt.annotate("r_squared="+str(round(r_s,4)), xy=(0.95,0.90),xycoords='axes fraction',
                     fontsize=fontsize_plot)
                    plt.title(datetimecol+"~"+numericcol + " (fraction: last "+str(100*fractionToAnalyze)+"%)", fontsize=14)
                    if min0: #only set min y axis if 0 values are existing:
                        x1,x2,y1,y2 = plt.axis()
                        plt.axis((x1,x2,shiftamount/10,y2))
                        #plt.annotate("0", xy=(-0.005,shiftamount),xycoords=('axes fraction','data'),fontsize=fontsize_plot,color='red',ha='right')

                    plt.xticks(rotation=90)
                    ax.spines['right'].set_visible(False)
                    ax.spines['top'].set_visible(False)

                    plt.savefig(str(pathlib.Path(outputPath+'/plots/'+cleanfilename(outputTablename+'-'+datetimecol+
                                '-'+numericcol,cleanlist)+'-'+str(int(round(fractionToAnalyze*100,0)))+'perc-nonlog.png')))
                    plt.close('all')

            except:
                if debug:
                    raise
                else:
                    printL("Unexpected error:" + str(sys.exc_info()[0]))
    if df_result.shape[0]>0: ##only append if there are results:
        ##finally create a combined score for easy sorting:

        #exponent_scaled = normalize(list(df_result['exponent']))

        #r squared is already scaled, but we want a higher score for lower r values:
        #r_prepared=1-r #a low r should lead to a higher score
        #it is much more important, that is is a power law (low r²), a high exponent is rather secondary --> weight
        #weight_factor_exponent=100
       
        #sort_score=[(weight_factor_exponent*r_prepared+x)/(weight_factor_exponent+1) for x in exponent_scaled]
        #df_result['sort_score']=sort_score
        df_result=df_result.sort_values(['exponent'],ascending=False)     

    return(df_result)
