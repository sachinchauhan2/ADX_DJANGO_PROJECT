from django.shortcuts import redirect, render
from .forms import MyFileForm
from .models import MyFileUpload
from django.contrib import messages
from django.urls import path
import os
import pandas as pd
import time

from django.http import FileResponse
from django.http import HttpResponse
from django.conf import settings
# from django.utils.encoding import force_text, smart_str
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Create your views here.
def home(request):
    mydata=MyFileUpload.objects.all()    
    myform=MyFileForm()
    if mydata!='':
        context={'form':myform,'mydata':mydata}
        return render(request,'index.html',context)
    else:
        context={'form':myform}
        return render(request,"index.html",context)

def uploadfile(request):
    if request.method=="POST":
        myform=MyFileForm(request.POST,request.FILES)        
        if myform.is_valid():
            MyFileName = request.POST.get('file_name') 
            MyFile = request.FILES.get('file')
            exists=MyFileUpload.objects.filter(my_file=MyFile).exists()
            print("MyFile:" , MyFile)
            # df = pd.read_csv(MyFile)
            # df2 = pd.DataFrame(df)


            print("File type :",type(MyFile))


            if exists:
                messages.error(request,'The file %s is already exists...!!!'% MyFile)
            else:
                MyFileUpload.objects.create(file_name=MyFileName,my_file=MyFile).save()
                d = os.getcwd() # how we get the current dorectory
                # time.sleep(2)
                # print()
                file_directory = d+'\media\\'+str(MyFile) #saving the file in the media directory

                saveNAME = "C:\\Users\\sachi\\Downloads\\File-Upload-main\\File-Upload-main\\MyProject\\upload\\"
                # saveFILENAME = saveNAME+ str(MyFile)
                # df = pd.read_csv(saveFILENAME)
                # for i , row in df.iterrows():
                #     if i != 0:
                #         HmL= df['High'].iloc[i] -df['Low'].iloc[i]
                #         AHmC = df['High'].iloc[i] - df['Close'].iloc[i-1]
                #         ALmC = df['Low'].iloc[i] - df['Close'].iloc[i-1]
                #         df.at[i,'TR']=max(HmL,AHmC,ALmC)
                #     if i != 0:
                #         cH_pH = df['High'].iloc[i]-df['High'].iloc[i-1]
                #         pL_cL = df['Low'].iloc[i-1]-df['Low'].iloc[i]
                #         if(cH_pH > pL_cL):
                #             df.at[i,'+DM 1'] = (max(cH_pH,0))
                #         else:
                #             df.at[i,'+DM 1'] = 0
                #         if(pL_cL > cH_pH):
                #             df.at[i,'-DM 1'] = (max(pL_cL,0))
                #         else:
                #             df.at[i,'-DM 1'] = 0
                #     if i== 14:
                #             df.at[i,'TR14']= sum(df['TR'][:15].dropna())
                #             df.at[i,'+DM14']= sum(df['+DM 1'][:15].dropna())
                #             df.at[i,'-DM14']= sum(df['-DM 1'][:15].dropna())
                #     if i > 14:
                #             df.at[i,'TR14'] = df['TR14'].iloc[i-1] - (df['TR14'].iloc[i-1]/14) + df['TR'].iloc[i]
                #             df.at[i,'+DM14'] = df['+DM14'].iloc[i-1] - (df['+DM14'].iloc[i-1]/14) + df['+DM 1'].iloc[i]
                #             df.at[i,'-DM14'] = df['-DM14'].iloc[i-1] - (df['-DM14'].iloc[i-1]/14) + df['-DM 1'].iloc[i]
                    
                # df['+DI14']= (df['+DM14']/df['TR14'])*100
                # df['-D14'] = (df['-DM14']/df['TR14'])*100
                # df['DI 14 Diff'] = abs(df['+DI14'] - df['-D14'])
                # df['DI 14 Sum'] = df['+DI14'] + df['-D14']
                # df['DX'] = (df['DI 14 Diff']/df['DI 14 Sum'])*100
                # for i , row in df.iterrows():
                #     if i == 27:
                #         df.at[i,'ADX'] = round(sum(df['DX'][14:28].dropna())/14,2)
                #     if i > 27:
                #         df.at[i,'ADX'] = (((df['ADX'].iloc[i-1])*13)+df['DX'].iloc[i])/14              
                # df.to_csv(saveFILENAME)
                messages.success(request,"File uploaded successfully.")
        return redirect("home")

def deleteFile(request,id):
    mydata=MyFileUpload.objects.get(id=id)
    print("mydata ::::: =>",mydata)
    d = os.getcwd()
    print("get parth :",d) 
    mydata.delete()    
    os.remove(mydata.my_file.path)
    messages.success(request,'File deleted successfully.')  
    return redirect('home')

def viewFile(request,id):
    my_data =MyFileUpload.objects.get(id=id)

    file_path = os.path.join(settings.MEDIA_ROOT, my_data.my_file.path)
    df = pd.read_csv(file_path)
    for i , row in df.iterrows():
        if i != 0:
            HmL= df['High'].iloc[i] -df['Low'].iloc[i]
            AHmC = df['High'].iloc[i] - df['Close'].iloc[i-1]
            ALmC = df['Low'].iloc[i] - df['Close'].iloc[i-1]
            df.at[i,'TR']=max(HmL,AHmC,ALmC)
        if i != 0:
            cH_pH = df['High'].iloc[i]-df['High'].iloc[i-1]
            pL_cL = df['Low'].iloc[i-1]-df['Low'].iloc[i]
            if(cH_pH > pL_cL):
                df.at[i,'+DM 1'] = (max(cH_pH,0))
            else:
                df.at[i,'+DM 1'] = 0
            if(pL_cL > cH_pH):
                df.at[i,'-DM 1'] = (max(pL_cL,0))
            else:
                df.at[i,'-DM 1'] = 0
        if i== 14:
                df.at[i,'TR14']= sum(df['TR'][:15].dropna())
                df.at[i,'+DM14']= sum(df['+DM 1'][:15].dropna())
                df.at[i,'-DM14']= sum(df['-DM 1'][:15].dropna())
        if i > 14:
                df.at[i,'TR14'] = df['TR14'].iloc[i-1] - (df['TR14'].iloc[i-1]/14) + df['TR'].iloc[i]
                df.at[i,'+DM14'] = df['+DM14'].iloc[i-1] - (df['+DM14'].iloc[i-1]/14) + df['+DM 1'].iloc[i]
                df.at[i,'-DM14'] = df['-DM14'].iloc[i-1] - (df['-DM14'].iloc[i-1]/14) + df['-DM 1'].iloc[i]
        
    df['+DI14']= (df['+DM14']/df['TR14'])*100
    df['-D14'] = (df['-DM14']/df['TR14'])*100
    df['DI 14 Diff'] = abs(df['+DI14'] - df['-D14'])
    df['DI 14 Sum'] = df['+DI14'] + df['-D14']
    df['DX'] = (df['DI 14 Diff']/df['DI 14 Sum'])*100
    for i , row in df.iterrows():
        if i == 27:
            df.at[i,'ADX'] = round(sum(df['DX'][14:28].dropna())/14,2)
        if i > 27:
            df.at[i,'ADX'] = (((df['ADX'].iloc[i-1])*13)+df['DX'].iloc[i])/14              
         
    response = HttpResponse(content_type='text/application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={my_data.my_file}'

    df.to_excel(response,float_format='%.2f',index=False)
    return response


def adx_chart(request,id):
    # print("HELLO WORLD")
    my_data =MyFileUpload.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, my_data.my_file.path)
    df = pd.read_csv(file_path)
    df.columns = ['Datetime','Open','High','Low','Close']
    df = ADX_fuc(df)
    df['Datetime']  = pd.to_datetime(df['Datetime'])
    df['Datetime'] =df['Datetime'].astype(str)
    df.set_index('Datetime',inplace=True)
    #  add subplot properties when initializing fig variable
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.01, row_heights=[0.5,0.1])
    # import plotly.graph_objects as go
    fig =fig.add_trace(go.Candlestick(x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close']),row=1, col=1)
    # removing rangeslider
    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[23.20, 10], pattern="hour"),  # hide hours outside of 9.30am-4pm
    #         dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
    # removing rangeslider
    # removing all empty dates
    # build complete timeline from start date to end date
    dt_all = pd.date_range(start=df.index[0],end=df.index[-1])
    # retrieve the dates that ARE in the original datset
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
    # define dates with missing values
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    # hide dates with no values
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])# remove rangeslider
    fig.update_layout(xaxis_rangeslider_visible=False)

    # Plot ADX 
    fig.add_trace(go.Scatter(x=df.index, 
                        y=df['ADX'],name='ADX',
                        line=dict(color='blue', width=1),
                        ), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, 
                        y=df['+DI14'],
                        name="+DI14",
                        line=dict(color='green', width=1),
                        ), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, 
                        y=df['-DI14'],
                            name="-DI14",
                        line=dict(color='red', width=1),
                        ), row=2, col=1)
    # update layout by changing the plot size, hiding legends & rangeslider, and removing gaps between dates
    fig.update_layout(height=700, width=1400, 
                    showlegend=False, 
                    xaxis_rangeslider_visible=False,
                    xaxis_rangebreaks=[dict(values=dt_breaks)])
    
    # update y-axis label
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="ADX",showgrid=False, row=2, col=1)
    # removing white space
    fig.update_layout(margin=go.layout.Margin(
            l=10, #left margin
            r=10, #right margin
            b=10, #bottom margin
            t=10  #top margin
        ))
    html_page = fig.to_html()
    return HttpResponse(html_page)
    # return render(request,'chart.html', context=html_page)

    # return render(request, 'chart.html',html_page)

    # context['graph'] = df.to_html()

    # messages.success(request,'Working successfully.')  
    # return redirect("chart")
def ADX_fuc(df):
    for i , row in df.iterrows():
        if i != 0:
            HmL= df['High'].iloc[i] -df['Low'].iloc[i]
            AHmC = df['High'].iloc[i] - df['Close'].iloc[i-1]
            ALmC = df['Low'].iloc[i] - df['Close'].iloc[i-1]
            df.at[i,'TR']=max(HmL,AHmC,ALmC)
        if i != 0:
            cH_pH = df['High'].iloc[i]-df['High'].iloc[i-1]
            pL_cL = df['Low'].iloc[i-1]-df['Low'].iloc[i]
            if(cH_pH > pL_cL):
                df.at[i,'+DM 1'] = (max(cH_pH,0))
            else:
                df.at[i,'+DM 1'] = 0
            if(pL_cL > cH_pH):
                df.at[i,'-DM 1'] = (max(pL_cL,0))
            else:
                df.at[i,'-DM 1'] = 0
        if i== 14:
                df.at[i,'TR14']= sum(df['TR'][:15].dropna())
                df.at[i,'+DM14']= sum(df['+DM 1'][:15].dropna())
                df.at[i,'-DM14']= sum(df['-DM 1'][:15].dropna())
        if i > 14:
                df.at[i,'TR14'] = df['TR14'].iloc[i-1] - (df['TR14'].iloc[i-1]/14) + df['TR'].iloc[i]
                df.at[i,'+DM14'] = df['+DM14'].iloc[i-1] - (df['+DM14'].iloc[i-1]/14) + df['+DM 1'].iloc[i]
                df.at[i,'-DM14'] = df['-DM14'].iloc[i-1] - (df['-DM14'].iloc[i-1]/14) + df['-DM 1'].iloc[i]

    df['+DI14']= (df['+DM14']/df['TR14'])*100
    df['-DI14'] = (df['-DM14']/df['TR14'])*100
    df['DI 14 Diff'] = abs(df['+DI14'] - df['-DI14'])
    df['DI 14 Sum'] = df['+DI14'] + df['-DI14']
    df['DX'] = (df['DI 14 Diff']/df['DI 14 Sum'])*100
    
    for i , row in df.iterrows():
        if i == 27:
            df.at[i,'ADX'] = round(sum(df['DX'][14:28].dropna())/14,2)
        if i > 27:
            df.at[i,'ADX'] = (((df['ADX'].iloc[i-1])*13)+df['DX'].iloc[i])/14 
            
    return df
