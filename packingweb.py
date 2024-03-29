import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from numpy import array, exp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy.optimize import fsolve
import plotly.figure_factory as ff
from PIL import Image

st.set_page_config(layout="wide")
image = Image.open('bare.png')
newsize = (400, 200)
image = image.resize(newsize)
st.image(image, use_column_width=False)
st.write("""
# Packing Density Prediction of Polydispersed Particle

this app using compressible linear model to predict adjustable (upto) 4 components of particle distributions

:barely_sunny:
Generated by Sorathep R. Additive and Green Solution/ Research and Innovation Center / SCG .
""")
col0 = st.sidebar
col1, col2,col3, col4,col5 = st.columns((1,1,1,1,2))


# Collects user input features into dataframe
forfit1 = r'PSD_unfit1.csv'
forfit1 = pd.read_csv(forfit1)

forfit2 = r'PSD_unfit2.csv'
forfit2 = pd.read_csv(forfit2)

forfit3 = r'PSD_unfit3.csv'
forfit3 = pd.read_csv(forfit3)

forfit4 = r'PSD_unfit4.csv'
forfit4 = pd.read_csv(forfit4)

col0.markdown("""
[Example CSV input file (Do not change header name!!!)](https://drive.google.com/file/d/13L_ZqgZREcllhrjM0MHTd_UNV0clk3l1/view?usp=sharing)
""")


uploaded_file1 = col0.file_uploader("Upload your input PSD 1 - CSV file", type=["csv"])
if uploaded_file1 is not None:
    forfit1 = pd.read_csv(uploaded_file1)
    
uploaded_file2 = col0.file_uploader("Upload your input PSD 2 - CSV file", type=["csv"])
if uploaded_file2 is not None:
    forfit2 = pd.read_csv(uploaded_file2)
       
uploaded_file3 = col0.file_uploader("Upload your input PSD 3 - CSV file", type=["csv"])   
if uploaded_file3 is not None:
    forfit3 = pd.read_csv(uploaded_file3)
    
uploaded_file4 = col0.file_uploader("Upload your input PSD 4 - CSV file", type=["csv"])    
if uploaded_file4 is not None:
    forfit4 = pd.read_csv(uploaded_file4)
    
def user_input_features():
    
    M1 = col1.number_input('Mass fraction of PSD1', min_value =0.00 , max_value = 1.00, value = 0.1, step= 0.01)
    if M1 == 0:
        M1 = 0.00000000001
    else:
        M1 = M1   
    D1 = col1.number_input('Input **specific gravity** (0-1) of PSD1',value = 2.75)
    Beta1 = col1.number_input('Input **residual value ** of PSD1',value = 0.65)
    
    M2 = col2.number_input(' Mass fraction of PSD2', min_value =0.00 , max_value = 1.00, value = 0.1, step= 0.01)
    if M2 == 0:
        M2 = 0.00000000001
    else :
        M2 = M2
    D2 = col2.number_input('Input **specific gravity** (0-1) of PSD2',value = 2.75)
    Beta2 = col2.number_input('Input **residual value ** of PSD2',value = 0.65)
    
    M3 = col3.number_input('Mass fraction of PSD3', min_value =0.00 , max_value = 1.00, value = 0.1, step= 0.01)
    if M3 == 0:
        M3 = 0.00000000001
    else :
        M3 = M3
    D3 = col3.number_input('Input **specific gravity** (0-1) of PSD3',value = 2.75)
    Beta3 = col3.number_input('Input **residual value ** of PSD3',value = 0.65)
    
    M4 = col4.number_input('Mass fraction of PSD4', min_value =0.00 , max_value = 1.00, value = 0.1, step= 0.01)
    if M4 == 0:
        M4 = 0.00000000001
    else :
        M4 = M4
    D4 = col4.number_input('Input **specific gravity** (0-1) of PSD4',value = 2.75)
    Beta4 = col4.number_input('Input **residual value ** of PSD4',value = 0.65)
   
    
    data = {'PSD1': [M1,D1,Beta1],
             'PSD2': [M2,D2,Beta2],
             'PSD3': [M3,D3,Beta3],
             'PSD4': [M4,D4,Beta4],}
    features = pd.DataFrame(data)
    return features




features = user_input_features()

M1 = features.iloc[0,0]
D1 = features.iloc[1,0]
Beta1 = features.iloc[2,0]

M2 = features.iloc[0,1]
D2 = features.iloc[1,1]
Beta2 = features.iloc[2,1]

M3 = features.iloc[0,2]
D3 = features.iloc[1,2]
Beta3 = features.iloc[2,2]

M4 = features.iloc[0,3]
D4 = features.iloc[1,3]
Beta4 = features.iloc[2,3]

space = 40

xData1 = forfit1['Size'].to_numpy()
yData1 = forfit1['Acc from small'].to_numpy()

xData2 = forfit2['Size'].to_numpy()
yData2 = forfit2['Acc from small'].to_numpy()

xData3 = forfit3['Size'].to_numpy()
yData3 = forfit3['Acc from small'].to_numpy()

xData4 = forfit4['Size'].to_numpy()
yData4 = forfit4['Acc from small'].to_numpy()

def func(xData, x0, n):
    return 100-(100*(np.exp(-(xData/x0)**n)))
#11111######################################################################################################
popt1, pcov1 = curve_fit(func, xData1, yData1,p0=[10,1], maxfev=5000)
modelPredictions1 = func(xData1,popt1[[0]],popt1[[1]]) 
absError1 = modelPredictions1 - yData1

SE1 = np.square(absError1) # squared errors
MSE1 = np.mean(SE1) # mean squared errors
RMSE1 = np.sqrt(MSE1) # Root Mean Squared Error, RMSE
Rsquared1 = 1.0 - (np.var(absError1) / np.var(yData1))


#22222######################################################################################################
popt2, pcov2 = curve_fit(func, xData2, yData2,p0=[10,1],maxfev=5000)
modelPredictions2 = func(xData2,popt2[[0]],popt2[[1]]) 
absError2 = modelPredictions2 - yData2

SE2 = np.square(absError2) # squared errors
MSE2 = np.mean(SE2) # mean squared errors
RMSE2 = np.sqrt(MSE2) # Root Mean Squared Error, RMSE
Rsquared2 = 1.0 - (np.var(absError2) / np.var(yData2))

#3333######################################################################################################
popt3, pcov3 = curve_fit(func, xData3, yData3,p0=[10,1],maxfev=5000)
modelPredictions3 = func(xData3,popt3[[0]],popt3[[1]]) 
absError3 = modelPredictions3 - yData3

SE3 = np.square(absError3) # squared errors
MSE3 = np.mean(SE3) # mean squared errors
RMSE3 = np.sqrt(MSE3) # Root Mean Squared Error, RMSE
Rsquared3 = 1.0 - (np.var(absError3) / np.var(yData3))

#######################################################################################################
popt4, pcov4 = curve_fit(func, xData4, yData4,p0=[10,1],maxfev=5000)
modelPredictions4 = func(xData4,popt4[[0]],popt4[[1]]) 
absError4 = modelPredictions4 - yData4

SE4 = np.square(absError4) # squared errors
MSE4 = np.mean(SE4) # mean squared errors
RMSE4 = np.sqrt(MSE4) # Root Mean Squared Error, RMSE
Rsquared4 = 1.0 - (np.var(absError4) / np.var(yData4))

lower_size = 0.1
upper_size1 = forfit1['Size'].max()
upper_size2 = forfit2['Size'].max()
upper_size3 = forfit3['Size'].max()
upper_size4 = forfit4['Size'].max()

Max_array= (upper_size1,upper_size2,upper_size3,upper_size4)
upper_size = np.max(Max_array)
X_new = np.logspace(np.log10(lower_size), np.log10(upper_size), num=space, endpoint=True, base=10.0, dtype=None, axis=0)
New_PSD1 = func(X_new,popt1[[0]],popt1[[1]])
New_PSD2 = func(X_new,popt2[[0]],popt2[[1]])
New_PSD3 = func(X_new,popt3[[0]],popt3[[1]])
New_PSD4 = func(X_new,popt4[[0]],popt4[[1]])
Formix1 = pd.DataFrame(zip(X_new, New_PSD1), columns=['Size','%ACC.'])
Formix2 = pd.DataFrame(zip(X_new, New_PSD2), columns=['Size','%ACC.'])
Formix3 = pd.DataFrame(zip(X_new, New_PSD3), columns=['Size','%ACC.'])
Formix4 = pd.DataFrame(zip(X_new, New_PSD4), columns=['Size','%ACC.'])

col1.caption(":exclamation: **Reccomendation**  \n residual value: cement=0.65, silicafume=0.72, limestone=0.48,sand= 0.6 ")
  
if col1.button('Show Fitted PSD1'):
   
    fig = px.line(Formix1, x="Size", y="%ACC.",log_x=True)
    fig.update_layout(height=250, width = 300, margin=dict(r=0, l=0, t=0, b=0))
    col2.write(fig)
    col2.caption('Rsquared for PSD1 (Rosin Rammler fit) : {0:3f}'.format(Rsquared1))
    col2.caption('x0 : {0:3f}'.format(popt1[0]))
    col2.caption('n : {0:3f}'.format(popt1[1]))
if col1.button('Show Fitted PSD2'):
    
    fig = px.line(Formix2, x="Size", y="%ACC.",log_x=True)
    fig.update_layout(height=250, width = 300, margin=dict(r=0, l=0, t=0, b=0))
    col2.write(fig)
    col2.caption('Rsquared for PSD2 (Rosin Rammler fit) : {0:3f}'.format(Rsquared2))
    col2.caption('x0 : {0:3f}'.format(popt2[0]))
    col2.caption('n : {0:3f}'.format(popt2[1]))

if col1.button('Show Fitted PSD3'):
    
    fig = px.line(Formix3, x="Size", y="%ACC.",log_x=True)
    fig.update_layout(height=250, width = 300, margin=dict(r=0, l=0, t=0, b=0))
    col2.write(fig)
    col2.caption('Rsquared for PSD3 (Rosin Rammler fit) : {0:3f}'.format(Rsquared3))
    col2.caption('x0 : {0:3f}'.format(popt3[0]))
    col2.caption('n : {0:3f}'.format(popt3[1]))

if col1.button('Show Fitted PSD4'):
    
    fig = px.line(Formix4, x="Size", y="%ACC.",log_x=True)
    fig.update_layout(height=250, width = 300, margin=dict(r=0, l=0, t=0, b=0))
    col2.write(fig)
    col2.caption('Rsquared for PSD4 (Rosin Rammler fit) : {0:3f}'.format(Rsquared4))
    col2.caption('x0 : {0:3f}'.format(popt4[0]))
    col2.caption('n : {0:3f}'.format(popt4[1]))    
st.write('---') 


V1 = M1/D1
V2 = M2/D2
V3 = M3/D3
V4 = M4/D4

sum_v = sum([V1,V2,V3,V4])
V1_f = V1/sum_v
V2_f = V2/sum_v
V3_f = V3/sum_v
V4_f = V4/sum_v

Formix = pd.DataFrame(zip(X_new, New_PSD1,New_PSD2,New_PSD3,New_PSD4), columns=['Size','ACC1','ACC2','ACC3','ACC4'])

long = len(Formix)

dfm = pd.DataFrame()
dfi = pd.DataFrame()

for i in range (0,long, 1):

    Mix = Formix.iloc[i,1]*V1_f + Formix.iloc[i,2]*V2_f + Formix.iloc[i,3]*V3_f + Formix.iloc[i,4]*V4_f
    temporary_df = pd.DataFrame([Mix], columns=['Mix'])
   
    dfm = dfm.append(temporary_df, ignore_index=True)
    
    
Mix = pd.concat([Formix, dfm], axis=1)
plotx = Mix['Size']
plotym = Mix['Mix']
ploty1 = Mix['ACC1']
ploty2 = Mix['ACC2']
ploty3 = Mix['ACC3']
ploty4 = Mix['ACC4']

figmix = go.Figure()
    
figmix.add_trace(go.Scatter(x=plotx, y=plotym,
                    mode='lines',
                    name='Mix'))
figmix.add_trace(go.Scatter(x=plotx, y=ploty1,
                    mode='lines',
                    name='PSD1'))
figmix.add_trace(go.Scatter(x=plotx, y=ploty2,
                    mode='lines',
                    name='PSD2'))
figmix.add_trace(go.Scatter(x=plotx, y=ploty3,
                    mode='lines',
                    name='PSD3'))
figmix.add_trace(go.Scatter(x=plotx, y=ploty4,
                    mode='lines',
                    name='PSD4'))
figmix.update_xaxes(title_text="Size (micron)", type="log")
figmix.update_yaxes(title_text="Cumulative Percent")
figmix.update_layout(height=300, width =450, margin=dict(r=0, l=0, t=0, b=0))
col5.write(figmix)


PSDmix = Mix[['Size','Mix']]
data =  PSDmix.rename({'Mix':'Acc from small'}, axis=1)

long = len(data)
df = pd.DataFrame()

for i in range (long-1,-1, -1):
    #temporary = pd.DataFrame([i], columns=['i'])
    #df = df.append(temporary, ignore_index=True)
    Size = data.iloc[[i],[0]]  #.to_string(header=None, index=None)
    first = data.iloc[[i],[1]]
    second = data.iloc[[i-1],[1]]
    #print(first.values)
    dif = first.values - second.values
    dif = dif[0]/100
    Size = Size.values[0]
    temporary = pd.DataFrame(zip(Size, dif), columns=['Size','Fraction'])
    df = df.append(temporary, ignore_index=True)
    
df2 = pd.merge(df,data, how='left', on='Size', sort=False)
df2[df2 <0] = data.iloc[[0],[1]] 
last_row = len(df2)-1
df2.iloc[last_row][1] = df2.iloc[last_row][2]/100

dfi = pd.DataFrame()
long = len(df2)

for i in range (1,long+1, 1):
    temporary_df = pd.DataFrame([i], columns=['i'])
    dfi = dfi.append(temporary_df, ignore_index=True)

                  
df3 = pd.concat([dfi, df2], axis=1)
dfb = pd.DataFrame()

for i in range (0,long, 1):
    sumweight = df3.iloc[i,2]*V1_f + df3.iloc[i,2]*V2_f + df3.iloc[i,2]*V3_f + df3.iloc[i,2]*V4_f
    Beta = (df3.iloc[i,2]*V1_f*Beta1 + df3.iloc[i,2]*V2_f*Beta2 + df3.iloc[i,2]*V3_f*Beta3 + df3.iloc[i,2]*V4_f*Beta4)/sumweight
    temporary_df = pd.DataFrame([Beta], columns=['Beta'])
    dfb = dfb.append(temporary_df, ignore_index=True)
    
df4 = pd.concat([df3, dfb], axis=1)
df4 = df4.dropna(axis=0)
df4.to_csv('PSD.csv', index=False)

def pack1():
    data =  r'PSD.csv'
    data = pd.read_csv(data)
    long= len(data)
    

    df = pd.DataFrame()
    df2 = pd.DataFrame()

    for i in range (1,long+1, 1):
        for j in range(1,i,1):
            temporary_df = pd.DataFrame([i], columns=['i'])
            df = df.append(temporary_df, ignore_index=True)
            temporary_df2 = pd.DataFrame([j], columns=['j'])
            df2 = df2.append(temporary_df2, ignore_index=True)
                    
    result = pd.concat([df, df2], axis=1)

    alli = pd.merge(data, result, on="i", sort= False)
    alli = alli.rename({'Size':'Size_i'}, axis=1)
    alli = alli.rename({'Fraction':'Fraction_i'}, axis=1)

    alli_noj = alli[['i','Size_i','Fraction_i']]

    alli_noj = alli[['i','Size_i','Fraction_i']]

    data_forj = data
    allj = data_forj.rename({'i':'j'}, axis=1)
    allj = pd.merge(result,allj, how='left', on='j', sort=False)
    allj = allj.rename({'Size':'Size_j'}, axis=1)
    allj = allj.rename({'Fraction':'Fraction_j'}, axis=1)

    concat_wall = pd.concat([alli_noj, allj], axis=1)

    concat_wall['Size_ratioij'] = concat_wall['Size_i']/concat_wall['Size_j']
    concat_wall['Wall'] = (1-concat_wall['Size_ratioij'])**1.3
    concat_wall['Wall_term'] = concat_wall['Wall']*concat_wall['Fraction_j']
    concat_wall = concat_wall.iloc[: , 1:]
    

    summary_wall = concat_wall.groupby(['i'])['Wall_term'].agg('sum')
    summary_wall = pd.DataFrame(summary_wall)
    summary_wall = summary_wall.rename({'Wall_term':'Sum wall term in class i'}, axis=1)

    df3 = pd.DataFrame()
    df4 = pd.DataFrame()

    for i in range(1,long+1,1):
        for j in range(i+1,long+1,1):
            temporary_df = pd.DataFrame([i], columns=['i'])
            df3 = df3.append(temporary_df, ignore_index=True)
            temporary_df2 = pd.DataFrame([j], columns=['j'])
            df4 = df4.append(temporary_df2, ignore_index=True)
                    
    result2 = pd.concat([df3, df4], axis=1)



    alli2 = pd.merge(result2, data, how='left', on="i", sort= False)
    alli2 = alli2.rename({'Size':'Size_i'}, axis=1)
    alli2 = alli2.rename({'Fraction':'Fraction_i'}, axis=1)
    pd.set_option('display.max_rows', df.shape[0]+1)

    alli_noj2 = alli2[['i','Size_i','Fraction_i']]

    data_forj = data
    allj2 = data_forj.rename({'i':'j'}, axis=1)
    allj2 = pd.merge(result2,allj2, how='left', on='j', sort=False)
    allj2 = allj2.rename({'Size':'Size_j'}, axis=1)
    allj2 = allj2.rename({'Fraction':'Fraction_j'}, axis=1)

    concat_loose = pd.concat([alli_noj2, allj2], axis=1)

    concat_loose['Size_ratioij'] = concat_loose['Size_i']/concat_loose['Size_j']
    concat_loose['Loose'] = 0.7*(1-(1/concat_loose['Size_ratioij']))+0.3*(1-(1/concat_loose['Size_ratioij']))**12
    concat_loose['Loose_term'] = concat_loose['Loose']*concat_loose['Fraction_j']
    concat_loose = concat_loose.iloc[: , 1:]

    summary_loose = concat_loose.groupby(['i'])['Loose_term'].agg('sum')
    summary_loose = pd.DataFrame(summary_loose)
    summary_loose = summary_loose.rename({'Loose_term':'Sum loose term in class i'}, axis=1)


    ready_for_pack = pd.concat([summary_wall, summary_loose], axis=1)
    #ready_for_pack.to_csv('ready_for_pack.csv', index=False)


    beta = data['Beta']

    Pack = beta/(1-((1-beta)*ready_for_pack['Sum wall term in class i'])-ready_for_pack['Sum loose term in class i'])
    ready_for_pack['Packing'] = Pack
    ready_for_pack = ready_for_pack[(ready_for_pack.iloc[:,0] != 0) & (ready_for_pack.iloc[:,1] != 0)]
    #ready_for_pack.to_csv('ready_for_pack.csv', index=False)

    Final_Packing = ready_for_pack['Packing'].min()
    return Final_Packing
Final_Packing = pack1()

def compact():
    
    data = r'PSD.csv'
    data = pd.read_csv(data)
    
    y = data['Fraction']
    B = data['Beta']
    True_packing_initial = 0.5
    V = Final_Packing

    def Compact_(True_packing_initial):
        compact_class = (y/B) / ((1/True_packing_initial) - (1/V))
        Sum = (compact_class.sum()) - K
        return Sum
    K = 4
    True_Packing4 = fsolve(Compact_,(True_packing_initial))
    K = 4.1
    True_Packing41 = fsolve(Compact_,(True_packing_initial))
    K = 4.5
    True_Packing45 = fsolve(Compact_,(True_packing_initial))
    K = 4.75
    True_Packing475 = fsolve(Compact_,(True_packing_initial))
    K = 6.7
    True_Packing67 = fsolve(Compact_,(True_packing_initial))
    K = 8
    True_Packing8 = fsolve(Compact_,(True_packing_initial))
    K = 10
    True_Packing10 = fsolve(Compact_,(True_packing_initial))
    K = 12
    True_Packing12 = fsolve(Compact_,(True_packing_initial)) 
    K = 14
    True_Packing14 = fsolve(Compact_,(True_packing_initial))  
    
    True_Packing = {'K4': [True_Packing4],
                    'K41': [True_Packing41],
                    'K45': [True_Packing45],
                    'K475': [True_Packing475],
                     'K67': [True_Packing67],
                     'K8': [True_Packing8],
                     'K10': [True_Packing10],
                     'K12': [True_Packing12],
                     'K14': [True_Packing14],}
    True_Packing = pd.DataFrame(True_Packing)
    return True_Packing
True_Packing = compact()
True_Packing_noindex = Final_Packing
True_Packing4 = True_Packing.iloc[0,0]
True_Packing41 = True_Packing.iloc[0,1]
True_Packing45 = True_Packing.iloc[0,2]
True_Packing475 = True_Packing.iloc[0,3]
True_Packing67 = True_Packing.iloc[0,4]
True_Packing8 = True_Packing.iloc[0,5]
True_Packing10 = True_Packing.iloc[0,6]
True_Packing12 = True_Packing.iloc[0,7]
True_Packing14 = True_Packing.iloc[0,8]

col5.write(':sun_small_cloud: Results:')
col5.write('packing density when  \nK=4 = {0:3f}'.format(True_Packing4[0]))
col5.write('K=4.1 = {0:3f}'.format(True_Packing41[0]))
col5.write('K=4.5 = {0:3f}'.format(True_Packing45[0]))
col5.write('K=4.75 = {0:3f}'.format(True_Packing475[0]))
col5.write('K=6.7 = {0:3f}'.format(True_Packing67[0]))
col5.write('K=8 = {0:3f}'.format(True_Packing8[0]))
col5.write('K=10 = {0:3f}'.format(True_Packing10[0]))
col5.write('K=12 = {0:3f}'.format(True_Packing12[0]))
col5.write('K=14 = {0:3f}'.format(True_Packing14[0]))
col5.write('no compaction index = {0:3f}'.format(Final_Packing))

col5.caption(':exclamation: **Reccomendation**   \n Dry pouring K = 4.1  \n Dry sticking with a rod K=4.5  \n Dry vibration K=4.75  \n Dry vibration + 10 Kpa compression K=9  \n Wet smooth thick past K=6.7  '
                )

def prep():
    
    V1 = M1/D1
    V2 = M2/D2
    V3 = M3/D3
    V4 = M4/D4

    sum_v = sum([V1,V2,V3,V4])
    V1_f = V1/sum_v
    V2_f = V2/sum_v
    V3_f = V3/sum_v
    V4_f = V4/sum_v
    
    Formix = pd.DataFrame(zip(X_new, New_PSD1,New_PSD2,New_PSD3,New_PSD4), columns=['Size','ACC1','ACC2','ACC3','ACC4'])

    long = len(Formix)

    dfm = pd.DataFrame()
    dfi = pd.DataFrame()

    for i in range (0,long, 1):

        Mix = Formix.iloc[i,1]*V1_f + Formix.iloc[i,2]*V2_f + Formix.iloc[i,3]*V3_f + Formix.iloc[i,4]*V4_f
        temporary_df = pd.DataFrame([Mix], columns=['Mix'])
   
        dfm = dfm.append(temporary_df, ignore_index=True)
    
    
    Mix = pd.concat([Formix, dfm], axis=1)

    PSDmix = Mix[['Size','Mix']]
    data =  PSDmix.rename({'Mix':'Acc from small'}, axis=1)

    long = len(data)
    df = pd.DataFrame()

    for i in range (long-1,-1, -1):
    #temporary = pd.DataFrame([i], columns=['i'])
    #df = df.append(temporary, ignore_index=True)
        Size = data.iloc[[i],[0]]  #.to_string(header=None, index=None)
        first = data.iloc[[i],[1]]
        second = data.iloc[[i-1],[1]]
    #print(first.values)
        dif = first.values - second.values
        dif = dif[0]/100
        Size = Size.values[0]
        temporary = pd.DataFrame(zip(Size, dif), columns=['Size','Fraction'])
        df = df.append(temporary, ignore_index=True)
    
    df2 = pd.merge(df,data, how='left', on='Size', sort=False)
    df2[df2 <0] = data.iloc[[0],[1]] 
    last_row = len(df2)-1
    df2.iloc[last_row][1] = df2.iloc[last_row][2]/100

    dfi = pd.DataFrame()
    long = len(df2)

    for i in range (1,long+1, 1):
        temporary_df = pd.DataFrame([i], columns=['i'])
        dfi = dfi.append(temporary_df, ignore_index=True)

                  
    df3 = pd.concat([dfi, df2], axis=1)
    dfb = pd.DataFrame()

    for i in range (0,long, 1):
        sumweight = df3.iloc[i,2]*V1_f + df3.iloc[i,2]*V2_f + df3.iloc[i,2]*V3_f + df3.iloc[i,2]*V4_f
        Beta = (df3.iloc[i,2]*V1_f*Beta1 + df3.iloc[i,2]*V2_f*Beta2 + df3.iloc[i,2]*V3_f*Beta3 + df3.iloc[i,2]*V4_f*Beta4)/sumweight
        temporary_df = pd.DataFrame([Beta], columns=['Beta'])
        dfb = dfb.append(temporary_df, ignore_index=True)
    
    df4 = pd.concat([df3, dfb], axis=1)
    df4 = df4.dropna(axis=0)
    #df4 = df4.to_csv('PSD.csv', index=False)
    return df4

def pack2():
    # data =  prep()
    # data
    #data = pd.read_csv(data)
    long= len(data)
    

    df = pd.DataFrame()
    df2 = pd.DataFrame()

    for i in range (1,long+1, 1):
        for j in range(1,i,1):
            temporary_df = pd.DataFrame([i], columns=['i'])
            df = df.append(temporary_df, ignore_index=True)
            temporary_df2 = pd.DataFrame([j], columns=['j'])
            df2 = df2.append(temporary_df2, ignore_index=True)
                    
    result = pd.concat([df, df2], axis=1)

    alli = pd.merge(data, result, on="i", sort= False)
    alli = alli.rename({'Size':'Size_i'}, axis=1)
    alli = alli.rename({'Fraction':'Fraction_i'}, axis=1)

    alli_noj = alli[['i','Size_i','Fraction_i']]

    alli_noj = alli[['i','Size_i','Fraction_i']]

    data_forj = data
    allj = data_forj.rename({'i':'j'}, axis=1)
    allj = pd.merge(result,allj, how='left', on='j', sort=False)
    allj = allj.rename({'Size':'Size_j'}, axis=1)
    allj = allj.rename({'Fraction':'Fraction_j'}, axis=1)

    concat_wall = pd.concat([alli_noj, allj], axis=1)

    concat_wall['Size_ratioij'] = concat_wall['Size_i']/concat_wall['Size_j']
    concat_wall['Wall'] = (1-concat_wall['Size_ratioij'])**1.3
    concat_wall['Wall_term'] = concat_wall['Wall']*concat_wall['Fraction_j']
    concat_wall = concat_wall.iloc[: , 1:]
    

    summary_wall = concat_wall.groupby(['i'])['Wall_term'].agg('sum')
    summary_wall = pd.DataFrame(summary_wall)
    summary_wall = summary_wall.rename({'Wall_term':'Sum wall term in class i'}, axis=1)

    df3 = pd.DataFrame()
    df4 = pd.DataFrame()

    for i in range(1,long+1,1):
        for j in range(i+1,long+1,1):
            temporary_df = pd.DataFrame([i], columns=['i'])
            df3 = df3.append(temporary_df, ignore_index=True)
            temporary_df2 = pd.DataFrame([j], columns=['j'])
            df4 = df4.append(temporary_df2, ignore_index=True)
                    
    result2 = pd.concat([df3, df4], axis=1)



    alli2 = pd.merge(result2, data, how='left', on="i", sort= False)
    alli2 = alli2.rename({'Size':'Size_i'}, axis=1)
    alli2 = alli2.rename({'Fraction':'Fraction_i'}, axis=1)
    pd.set_option('display.max_rows', df.shape[0]+1)

    alli_noj2 = alli2[['i','Size_i','Fraction_i']]

    data_forj = data
    allj2 = data_forj.rename({'i':'j'}, axis=1)
    allj2 = pd.merge(result2,allj2, how='left', on='j', sort=False)
    allj2 = allj2.rename({'Size':'Size_j'}, axis=1)
    allj2 = allj2.rename({'Fraction':'Fraction_j'}, axis=1)

    concat_loose = pd.concat([alli_noj2, allj2], axis=1)

    concat_loose['Size_ratioij'] = concat_loose['Size_i']/concat_loose['Size_j']
    concat_loose['Loose'] = 0.7*(1-(1/concat_loose['Size_ratioij']))+0.3*(1-(1/concat_loose['Size_ratioij']))**12
    concat_loose['Loose_term'] = concat_loose['Loose']*concat_loose['Fraction_j']
    concat_loose = concat_loose.iloc[: , 1:]

    summary_loose = concat_loose.groupby(['i'])['Loose_term'].agg('sum')
    summary_loose = pd.DataFrame(summary_loose)
    summary_loose = summary_loose.rename({'Loose_term':'Sum loose term in class i'}, axis=1)


    ready_for_pack = pd.concat([summary_wall, summary_loose], axis=1)



    beta = data['Beta']

    Pack = beta/(1-((1-beta)*ready_for_pack['Sum wall term in class i'])-ready_for_pack['Sum loose term in class i'])
    ready_for_pack['Packing'] = Pack
    ready_for_pack = ready_for_pack[(ready_for_pack.iloc[:,0] != 0) & (ready_for_pack.iloc[:,1] != 0)]

    Final_Packing = ready_for_pack['Packing'].min()
    return Final_Packing

col6, col7 = st.columns((1,1))

if st.button('Generate all combination of contour plot'):
    dfm1= pd.DataFrame()
    dfm2= pd.DataFrame()
    dfm3= pd.DataFrame()
    dfm4= pd.DataFrame()
    dfp= pd.DataFrame()
    for M1 in range(10,100,20):
        M1 = M1/100
        for M2 in range(10,100,20):
            M2 = M2/100
            for M3 in range(10,100,20):
                M3 = M3/100
                for M4 in range(10,100,20):                 
                    
                    M4 = M4/100
                    
                    # D1 = features.iloc[1,0]
                    # Beta1 = features.iloc[2,0]
                    # D2 = features.iloc[1,1]
                    # Beta2 = features.iloc[2,1]
                    # D3 = features.iloc[1,2]
                    # Beta3 = features.iloc[2,2]
                    # D4 = features.iloc[1,3]
                    # Beta4 = features.iloc[2,3]
                    data = prep()
                    long= len(data)
                    
                    Final_Packing = pack2()
                    temporary_df = pd.DataFrame([M1], columns=['M1'])
                    dfm1 = dfm1.append(temporary_df, ignore_index=True)
                    temporary_df = pd.DataFrame([M2], columns=['M2'])
                    dfm2 = dfm2.append(temporary_df, ignore_index=True)
                    temporary_df = pd.DataFrame([M3], columns=['M3'])
                    dfm3 = dfm3.append(temporary_df, ignore_index=True)
                    temporary_df = pd.DataFrame([M4], columns=['M4'])
                    dfm4 = dfm4.append(temporary_df, ignore_index=True)
                    temporary_df = pd.DataFrame([Final_Packing], columns=['Final_Packing'])
                    dfp = dfp.append(temporary_df, ignore_index=True)
                    
    result2 = pd.concat([dfm1, dfm2,dfm3,dfm4,dfp], axis=1)
    

    
    
########################################################### M1=0.1
    M110 = result2.loc[result2['M1'] == 0.1]
    M110no = M110.drop(['M1','Final_Packing'], axis=1)
    dfnew = pd.DataFrame()
    dfnew2 = pd.DataFrame()
    dfnew3 = pd.DataFrame()
    dfnew4 = pd.DataFrame()
    long = len(M110no)

    for i in range (0,long, 1):
        total = M110no.iloc[i,0] + M110no.iloc[i,1] + M110no.iloc[i,2] 
        temporary_df = pd.DataFrame(M110no.iloc[i,0]/[total], columns=['newM2'])
        dfnew2 = dfnew2.append(temporary_df, ignore_index=True)
        temporary_df1 = pd.DataFrame(M110no.iloc[i,1]/[total], columns=['newM3'])
        dfnew3 = dfnew3.append(temporary_df1, ignore_index=True)
        temporary_df2 = pd.DataFrame(M110no.iloc[i,2]/[total], columns=['newM4'])
        dfnew4 = dfnew4.append(temporary_df2, ignore_index=True)

    dfnewm = pd.concat([dfnew2, dfnew3,dfnew4, ], axis=1)


    Al = dfnewm[['newM2']]
    Cu = dfnewm[['newM3']]
    Y = dfnewm[['newM4']]
# synthetic data for mixing enthalpy
# See https://pycalphad.org/docs/latest/examples/TernaryExamples.html
    enthalpy = M110[['Final_Packing']]
    dd = pd.concat([Al, Cu,Y,enthalpy ], axis=1)
    fig = px.scatter_ternary(dd, a="newM2", b="newM3", c="newM4",color="Final_Packing",size="Final_Packing", size_max=15)

    col6.write('ternary plot when PSD1 has mass ratio 0.1')
    col6.write(fig)
    
    
########################################################### M1=0.3
    M130 = result2.loc[result2['M1'] == 0.3]
    M130no = M130.drop(['M1','Final_Packing'], axis=1)
    dfnew = pd.DataFrame()
    dfnew2 = pd.DataFrame()
    dfnew3 = pd.DataFrame()
    dfnew4 = pd.DataFrame()
    long = len(M130no)

    for i in range (0,long, 1):
        total = M130no.iloc[i,0] + M130no.iloc[i,1] + M130no.iloc[i,2] 
        temporary_df = pd.DataFrame(M130no.iloc[i,0]/[total], columns=['newM2'])
        dfnew2 = dfnew2.append(temporary_df, ignore_index=True)
        temporary_df1 = pd.DataFrame(M130no.iloc[i,1]/[total], columns=['newM3'])
        dfnew3 = dfnew3.append(temporary_df1, ignore_index=True)
        temporary_df2 = pd.DataFrame(M130no.iloc[i,2]/[total], columns=['newM4'])
        dfnew4 = dfnew4.append(temporary_df2, ignore_index=True)

    dfnewm = pd.concat([dfnew2, dfnew3,dfnew4, ], axis=1)


    Al = dfnewm[['newM2']]
    Cu = dfnewm[['newM3']]
    Y = dfnewm[['newM4']]
# synthetic data for mixing enthalpy
# See https://pycalphad.org/docs/latest/examples/TernaryExamples.html
    enthalpy = M130[['Final_Packing']]
    enthalpy = enthalpy.reset_index()
    dd = pd.concat([Al, Cu,Y,enthalpy ], axis=1)
    fig30 = px.scatter_ternary(dd, a="newM2", b="newM3", c="newM4",color="Final_Packing",size="Final_Packing", size_max=15)

    col6.write('ternary plot when PSD1 has mass ratio 0.3')
    col6.write(fig30)
    
########################################################### M1=0.5
    M150 = result2.loc[result2['M1'] == 0.5]
    M150no = M150.drop(['M1','Final_Packing'], axis=1)
    dfnew = pd.DataFrame()
    dfnew2 = pd.DataFrame()
    dfnew3 = pd.DataFrame()
    dfnew4 = pd.DataFrame()
    long = len(M150no)

    for i in range (0,long, 1):
        total = M150no.iloc[i,0] + M150no.iloc[i,1] + M150no.iloc[i,2] 
        temporary_df = pd.DataFrame(M150no.iloc[i,0]/[total], columns=['newM2'])
        dfnew2 = dfnew2.append(temporary_df, ignore_index=True)
        temporary_df1 = pd.DataFrame(M150no.iloc[i,1]/[total], columns=['newM3'])
        dfnew3 = dfnew3.append(temporary_df1, ignore_index=True)
        temporary_df2 = pd.DataFrame(M150no.iloc[i,2]/[total], columns=['newM4'])
        dfnew4 = dfnew4.append(temporary_df2, ignore_index=True)

    dfnewm = pd.concat([dfnew2, dfnew3,dfnew4, ], axis=1)


    Al = dfnewm[['newM2']]
    Cu = dfnewm[['newM3']]
    Y = dfnewm[['newM4']]
# synthetic data for mixing enthalpy
# See https://pycalphad.org/docs/latest/examples/TernaryExamples.html
    enthalpy = M150[['Final_Packing']]
    enthalpy = enthalpy.reset_index()
    dd = pd.concat([Al, Cu,Y,enthalpy ], axis=1)
    fig50 = px.scatter_ternary(dd, a="newM2", b="newM3", c="newM4",color="Final_Packing",size="Final_Packing", size_max=15)

    col6.write('ternary plot when PSD1 has mass ratio 0.5')
    col6.write(fig50)
    
########################################################### M1=0.7
    M170 = result2.loc[result2['M1'] == 0.7]
    M170no = M170.drop(['M1','Final_Packing'], axis=1)
    dfnew = pd.DataFrame()
    dfnew2 = pd.DataFrame()
    dfnew3 = pd.DataFrame()
    dfnew4 = pd.DataFrame()
    long = len(M170no)

    for i in range (0,long, 1):
        total = M170no.iloc[i,0] + M170no.iloc[i,1] + M170no.iloc[i,2] 
        temporary_df = pd.DataFrame(M170no.iloc[i,0]/[total], columns=['newM2'])
        dfnew2 = dfnew2.append(temporary_df, ignore_index=True)
        temporary_df1 = pd.DataFrame(M170no.iloc[i,1]/[total], columns=['newM3'])
        dfnew3 = dfnew3.append(temporary_df1, ignore_index=True)
        temporary_df2 = pd.DataFrame(M170no.iloc[i,2]/[total], columns=['newM4'])
        dfnew4 = dfnew4.append(temporary_df2, ignore_index=True)

    dfnewm = pd.concat([dfnew2, dfnew3,dfnew4, ], axis=1)


    Al = dfnewm[['newM2']]
    Cu = dfnewm[['newM3']]
    Y = dfnewm[['newM4']]
# synthetic data for mixing enthalpy
# See https://pycalphad.org/docs/latest/examples/TernaryExamples.html
    enthalpy = M170[['Final_Packing']]
    enthalpy = enthalpy.reset_index()
    dd = pd.concat([Al, Cu,Y,enthalpy ], axis=1)
    fig70 = px.scatter_ternary(dd, a="newM2", b="newM3", c="newM4",color="Final_Packing",size="Final_Packing", size_max=15)

    col6.write('ternary plot when PSD1 has mass ratio 0.7')
    col6.write(fig70)
########################################################### M1=0.9
    M190 = result2.loc[result2['M1'] == 0.9]
    M190no = M190.drop(['M1','Final_Packing'], axis=1)
    dfnew = pd.DataFrame()
    dfnew2 = pd.DataFrame()
    dfnew3 = pd.DataFrame()
    dfnew4 = pd.DataFrame()
    long = len(M190no)

    for i in range (0,long, 1):
        total = M190no.iloc[i,0] + M190no.iloc[i,1] + M190no.iloc[i,2] 
        temporary_df = pd.DataFrame(M190no.iloc[i,0]/[total], columns=['newM2'])
        dfnew2 = dfnew2.append(temporary_df, ignore_index=True)
        temporary_df1 = pd.DataFrame(M190no.iloc[i,1]/[total], columns=['newM3'])
        dfnew3 = dfnew3.append(temporary_df1, ignore_index=True)
        temporary_df2 = pd.DataFrame(M190no.iloc[i,2]/[total], columns=['newM4'])
        dfnew4 = dfnew4.append(temporary_df2, ignore_index=True)

    dfnewm = pd.concat([dfnew2, dfnew3,dfnew4, ], axis=1)


    Al = dfnewm[['newM2']]
    Cu = dfnewm[['newM3']]
    Y = dfnewm[['newM4']]
# synthetic data for mixing enthalpy
# See https://pycalphad.org/docs/latest/examples/TernaryExamples.html
    enthalpy = M190[['Final_Packing']]
    enthalpy = enthalpy.reset_index()
    dd = pd.concat([Al, Cu,Y,enthalpy ], axis=1)
    fig90 = px.scatter_ternary(dd, a="newM2", b="newM3", c="newM4",color="Final_Packing",size="Final_Packing", size_max=15)

    col6.write('ternary plot when PSD1 has mass ratio 0.9')
    col6.write(fig90)

  
#     fig = ff.create_ternary_contour(np.array([results[['M1', Y, Cu]), enthalpy,
#                               pole_labels=['Al', 'Y', 'Cu'],
#                                  interp_mode='cartesian')
                    
