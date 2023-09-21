import pandas as pd
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

std_cols = ['DateTime','CV1_Position','CV2_Position','CV3_Position','CV4_Position',
            'ChangeoverInProgress','MachineStatus','ControlType',
            'Temperature','TemperatureSetPoint','TemperatureHighLimit','TemperatureLowLimit',
            'Viscosity','ViscositySetPoint','ViscosityHighLimit','ViscosityLowLimit',
            'ActualSetpoint','PID_OutputError','FlowMeter',
            'PT1','PT2']
alm_cols = ['DateTime', 'AlarmNumber']

change_over_vars = {
    'Temperature': ['Temperature','TemperatureSetPoint','TemperatureHighLimit','TemperatureLowLimit'],
    'Viscosity': ['Viscosity','ViscositySetPoint','ViscosityHighLimit','ViscosityLowLimit'],
    'Valves': ['CV1_Position','CV2_Position','CV3_Position','CV4_Position'],
    'Bool': ['ChangeoverInProgress'],
    'Flow': ['FlowMeter'],
    'Pressure': ['PT1','PT2']
    }

alarm_cats = {
    'Main1': [1,14],
    'Filter': [15,19],
    'Fuel Handling': [20,29],
    'Pumps': [30,49],
    'Flow Meter': [50,54],
    'Mixing Tank': [55,59],
    'Cooler': [60,69],
    'Others': [70,99],
    'TempControl Alarms': [100,199],
    'Main2': [200,255]
}

# Alfa Laval brand colors
ALcolors = ['rgba(17, 56, 127, 1)', #AL blue
            'rgba(0, 0, 0, 1)', #AL white
            'rgba(220, 146, 118, 1)', #AL earth
            'rgba(254, 205, 96, 1)', #AL sun
            'rgba(147, 199, 198, 1)', #AL water
            'rgba(0, 127, 200, 1)', #AL innovation
            ]

# Import data
def concat_files(AllFilesNames):
    print("concat_files started ---")
   # Create an empty list to store the dataframes
    ListDataframe = list()

    # For each file in the specified directory import the data and add it in the list
    for Filename in AllFilesNames:
        ListDataframe.append(pd.read_csv(Filename, sep=';', skiprows=3, decimal=',', encoding='unicode_escape'))

    # Concatenate the files in the list in unique dataframe
    DF_Data = pd.concat(ListDataframe, axis=0, ignore_index=True)

    # DateTime
    DF_Data['DateTime'] = pd.to_datetime(DF_Data['DateTime'], format="%Y-%m-%d %H:%M:%S")
    # ordering ascending
    DF_Data = DF_Data.sort_values(by='DateTime', ascending=True).reset_index(drop=True)

    #Remove duplicates
    DF_Data.drop_duplicates(keep=False, inplace=True)
    
    print("--- raw data imported:")
    print(DF_Data.shape)
    print(DF_Data.columns.tolist())

    return(DF_Data)

def Format_DF_SLogs(list_files):

    LogsStandard = concat_files(list_files)
    
    print("Formatting Standard Logs ---")

    # Format LogsStandard
    LogsStandard = LogsStandard[std_cols]

    # Columns as float
    LogsStandard.iloc[:,8:] = LogsStandard.iloc[:,8:].astype(float)

    # Create labels for CV positions
    LogsStandard[['CV1_Label','CV2_Label','CV3_Label','CV4_Label']] = LogsStandard[['CV1_Position','CV2_Position','CV3_Position','CV4_Position']]

    LogsStandard[['CV1_Label']] = LogsStandard[['CV1_Label']] .replace({ 
        0: "Both LS activated",
        1: "Fuel 1 Position",
        2: "No LS activated",
        3: "Other fuel Position"
    }).fillna('Unknown')

    LogsStandard[['CV2_Label']] = LogsStandard[['CV2_Label']] .replace({ 
        0: "Both LS activated",
        1: "Fuel 2 Position",
        2: "No LS activated",
        3: "Other Fuel Position"
    }).fillna('Unknown')

    LogsStandard[['CV3_Label']] = LogsStandard[['CV3_Label']] .replace({ 
        0: "Both LS activated",
        1: "Heater Position",
        2: "No LS activated",
        3: "Cooler Position"
    }).fillna('Unknown')

    LogsStandard[['CV4_Label']] = LogsStandard[['CV4_Label']] .replace({ 
        0: "Both LS activated",
        1: "Cooler Position",
        2: "No LS activated",
        3: "Bypass Position"
    }).fillna('Unknown')

    # Identify when Change Over Started and Finished
    # ChangeOverInProgress = O : no change
    # ChangeOverInProgress = 1 : started
    # ChangeOverInProgress = -1 : finished

    # Create column with value change
    LogsStandard['ChangeoverCMDchange'] = LogsStandard['ChangeoverInProgress'].diff()

    print("--- Standard Logs formatted")
    print(LogsStandard.shape)
    print(LogsStandard.columns.tolist())
    print(LogsStandard.dtypes)

    return(LogsStandard)

def Format_DF_ALogs(list_files):

    LogsAlarms = concat_files(list_files)
    print("Formatting Alarm Logs ---")

    LogsAlarms = LogsAlarms[['DateTime', 'AlarmNumber']]

    # Create Labels of the Alarms
    #LogsAlarms['Label'] = LogsAlarms['AlarmNumber'] 
    #LogsAlarms[['Label']] = LogsAlarms[['Label']] .replace({ 0: "PLC battery low / Not present" }).fillna('Unknown')
    #LogsAlarms['Alm_Code_Label'] = "A" + LogsAlarms['AlarmNumber'].astype(str) + "_" + LogsAlarms['Label'] 
    
    print("--- Alarm Logs formatted")
    print(LogsAlarms.shape)
    print(LogsAlarms.columns.tolist())
    print(LogsAlarms.dtypes)

    return(LogsAlarms)

def IdentifyCOs(logs):
    print("IdentifyCOs started ---")

    # memorize starting DateTimes
    COstart = logs[logs['ChangeoverCMDchange'] == 1]['DateTime'].tolist()

    # memorize finishing DateTimes
    COfinish = logs[(logs['ChangeoverCMDchange'] == -1)]['DateTime'].tolist()

    COs = []
    for i in range(len(COfinish)):
        duration = COfinish[i]-COstart[i]
        if duration > datetime.timedelta(minutes = 1):
            COs.append({'Start': COstart[i], 'Finish': COfinish[i], 'Duration': duration})

    print('In the logs imported there are ' + str(len(COs)) + ' changeovers')
    for CO in COs:
        print('- From ' + str(CO['Start']) + ' to ' + str(CO['Finish']) + '. Duration: ' + str(CO['Duration'])) 

    return COs

def ChangeOverToDF(CO, logs):
    print("ChangeOverToDF started ---")
    print(CO)

    delta = datetime.timedelta(minutes = 20)
    df = logs[(logs['DateTime'] >= CO['Start']-delta) & (logs['DateTime'] <= CO['Finish']+delta)]

    print(df.shape)
    return(df)

def import_data(dirname, file_list):
    print("--- import_data started ---")

    #Init variables
    LogsStandard = pd.DataFrame()
    COs = []
    LogsAlarms = pd.DataFrame()

    #Create paths joining folder and file names
    if dirname != None:
        DataFiles = [dirname + '/' + x for x in file_list if x.startswith('S')]
        AlarmFiles = [dirname + '/' + x for x in file_list if x.startswith('A')]
    else:
        print("dirname == None -> Stop")
        return None, None, None 

    # Check file names first
    if len(DataFiles + AlarmFiles) == 0:
        print("no .csv files starting with S* or A* --> Stop")
        return None, None, None 

    # LOGS STANDARD
    if DataFiles:
        print("Importing Standard Logs ---")

        LogsStandard = Format_DF_SLogs(DataFiles)
        COs = IdentifyCOs(LogsStandard)

    # ALARMS
    if AlarmFiles:
        print("Importing Alarm Logs ---")
        LogsAlarms = Format_DF_ALogs(AlarmFiles)
 
    return COs, LogsStandard, LogsAlarms

#----------------------------------------------------------- PLOTLY Functions
def plot_alarms(x,y,cat,labels=None):
    trace = go.Scatter(x=x, y=y.astype(str),
                       name=cat,
                       mode='markers', marker_symbol='x',
                       marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                       marker_line_width=1, marker_size=8,
                       legendgroup="Alarms",legendgrouptitle_text="Alarms")
    
    if isinstance(labels, pd.Series):
        trace.hovertext = labels
    return trace

def plot_events(x,y,labels):
    trace = go.Scatter(x=x, y=y.astype(int),
                       name='Event Number',
                       mode='markers',marker_symbol='star',
                       marker_line_color=ALcolors[5], marker_color=ALcolors[5],
                       marker_line_width=1, marker_size=8,
                       legendgroup="Events",legendgrouptitle_text="Events",
                       hovertext=labels)
    return trace

def line_trace(x,y,name,cat,color=None):
    if color is not None:
        trace = go.Scatter(x=x, y=y,
                           name = name,
                           line=dict(color = color), line_shape='spline',
                           legendgroup=cat, legendgrouptitle_text=cat)    
    else: #default plotly color assignment
        trace = go.Scatter(x=x, y=y,
                           name = name,
                           line_shape='spline',
                           legendgroup=cat, legendgrouptitle_text=cat)
    return trace

def square_line_trace(x,y,name,cat,color=None,labels=None):
    if color is not None:
        trace = go.Scatter(x=x, y=y,
                           name = name,
                           line=dict(color = color), line_shape='hv',
                           legendgroup=cat, legendgrouptitle_text=cat)
    else: #default plotly color assignment
        trace = go.Scatter(x=x, y=y,
                   name = name, line_shape='hv',
                   legendgroup=cat, legendgrouptitle_text=cat)

    if isinstance(labels, pd.Series):
        trace.hovertext = labels
    
    return trace

def square_disc_line_trace(x,y,name,color,cat):
    trace = go.Scatter(x=x, y=y,
                       name = name,
                       line=dict(color = color, dash='dot'), line_shape='hv',
                       legendgroup=cat, legendgrouptitle_text=cat)
    return trace

def filled_trace(x,y,name,color,cat):
    trace = go.Scatter(x=x,y=y,
                       name= name,
                       fill='tozeroy', mode='none', 
                       fillcolor = color,
                       line_shape='hv')
    if cat is not None:
        trace.legendgroup = cat
        trace.legendgrouptitle_text = cat
    
    return trace

def change_over_overlap(LogsStandard, LogsAlarms, LogsEvents=pd.DataFrame()):
    print("change_over_overlap started ---")

    # dates of Standard logs to filter Events and Alarms
    mindate = LogsStandard['DateTime'].min()
    maxdate = LogsStandard['DateTime'].max()

    if not LogsAlarms.empty:
        alm = LogsAlarms[(LogsAlarms['DateTime'] > mindate) & (LogsAlarms['DateTime'] <= maxdate)]
    else:
        alm = pd.DataFrame()

    if not LogsEvents.empty:
        eve = LogsEvents[(LogsEvents['DateTime'] > mindate) & (LogsEvents['DateTime'] <= maxdate)]
    else:
        eve = pd.DataFrame()

    print("fig init")
    fig = go.Figure()

    # Create axis objects
    fig.update_layout(
        xaxis=dict(domain=[0.1, 0.9]), #compress x axis 10% left an right

        yaxis=dict(title="Temperature"),

        yaxis2=dict(title="Viscosity",
            anchor="free", overlaying="y", side="left", position=0),

        yaxis3=dict(title="", #ChangeOver
            overlaying='y',side='left',
            showline=False, showticklabels=False),

        yaxis4=dict(title="", #CVs
            overlaying='y', side='left',
            showline=False, showticklabels=False),

        yaxis5=dict(title="Flow",
            anchor="x",overlaying="y",side="right"),

        yaxis6=dict(title="Pressure",
            anchor="free", overlaying="y", side="right", position=1),

        yaxis7=dict(title="", #Density
            overlaying='y', side='left',
            showline=False, showticklabels=False),

        yaxis8=dict(title="", #Events
            overlaying='y', side='left',
            showline=False, showticklabels=False),

        yaxis9=dict(title="", #Alarms
            overlaying='y', side='left',
            showline=False, showticklabels=False),

        legend=dict(orientation="v", x = 1.1)
    )

    # Iterate change_over_vars, to plot each category of variables
    for i, (category, variables) in enumerate(change_over_vars.items()):
        print(category)

        if category == 'Temperature':            

            for j, variable in enumerate(variables):
                print(variable)

                if ('Limit' in variable):
                    trace = square_disc_line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color=px.colors.sequential.OrRd[(j+2)],
                        cat=category)
                    
                    fig.add_trace(trace)
                    
                else:
                    if not (LogsStandard[variable] == 0).all():
                        if ('Target' in variable):
                            color=px.colors.sequential.OrRd[(j+2)]
                        else:
                            color=px.colors.sequential.OrRd[-(j+1)]

                        trace = line_trace(
                            x=LogsStandard['DateTime'],
                            y=LogsStandard[variable],
                            name=variable,
                            color=color,
                            cat=category)
                        
                        fig.add_trace(trace)
        
        if category == 'Viscosity':

            for j, variable in enumerate(variables):
                print(variable)

                if ('Limit' in variable):
                    trace = square_disc_line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color=px.colors.sequential.dense[(j+3)],
                        cat=category)
                    trace.yaxis="y2"
                else:
                    if ('Target' in variable):
                        color=px.colors.sequential.dense[(j+3)]
                    else:
                        color=px.colors.sequential.PuBu[-(j+1)]

                    trace = line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color=color,
                        cat=category)
                    trace.yaxis="y2"
                    
                fig.add_trace(trace)

        if category == 'Valves':

            for j, variable in enumerate(variables):
                print(variable)

                trace = square_line_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variable],
                    labels=LogsStandard[variable.split('_')[0]+'_Label'],
                    name=variable,
                    color=px.colors.qualitative.G10[j],
                    cat=category)
                trace.visible = 'legendonly'
                trace.yaxis="y3"
                
                fig.add_trace(trace)
        
        if category == 'Bool': #ChangeOverInProgress

            trace = filled_trace(
                x=LogsStandard['DateTime'],
                y=LogsStandard[variables[0]],
                name=variables[0],
                color='rgba(0, 128, 0, 0.1)', #green opacity 10%
                cat=None)
            trace.yaxis="y4"
                        
            fig.add_trace(trace)
        
        if category == 'Flow':
            
            for variable in variables:
                print(variable)

                if variable == 'FT_MassFlow':
                    flag=False
                    if not (LogsStandard[variable] == 0).all():
                        trace = line_trace(
                            x=LogsStandard['DateTime'],
                            y=LogsStandard[variable],
                            name=variable,
                            color=px.colors.qualitative.G10[j+1],
                            cat=category)
                        trace.visible = 'legendonly'
                        trace.yaxis="y5"

                        fig.add_trace(trace)

                    for j, fm in enumerate(['FM1_MassFlow','FM2_MassFlow','FM3_MassFlow','FM4_MassFlow']):
                        if not (LogsStandard[fm] == 0).all():
                            trace = line_trace(
                                x=LogsStandard['DateTime'],
                                y=LogsStandard[fm],
                                name=fm,
                                color=px.colors.qualitative.G10[j+2],
                                cat=category)
                            trace.visible = 'legendonly'
                            trace.yaxis="y5"
                            
                            fig.add_trace(trace)
                else:
                    flag=True
                            
                if variable == 'FT_VolumeFlow':
                    if flag:
                        trace = line_trace(
                                x=LogsStandard['DateTime'],
                                y=LogsStandard[variable],
                                name=variable,
                                color=px.colors.qualitative.G10[j+2],
                                cat=category)
                        trace.visible = 'legendonly'
                        trace.yaxis="y5"

                        fig.add_trace(trace)

        if category == 'Pressure':

            for j, variable in enumerate(variables):
                print(variable)

                trace = line_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variable],
                    name=variable,
                    color=px.colors.qualitative.Vivid[j],
                    cat=category)
                trace.visible = 'legendonly'
                trace.yaxis="y6"

                fig.add_trace(trace)

        if category == 'Density':
            
            trace = line_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variables[0]],
                    name=variables[0],
                    color=px.colors.qualitative.Vivid[j+1],
                    cat=category)
            trace.visible = 'legendonly'
            trace.yaxis="y7"

            fig.add_trace(trace)

    if (not eve.empty):
        print('events')

        trace = plot_events(
                    x=eve['DateTime'],
                    y=eve['EventNumber'],
                    labels=eve['Label'])
        trace.yaxis="y8"

        fig.add_trace(trace)

    if (not alm.empty):
        for cat, limits in alarm_cats.items():
            print(cat)

            filter_alm = alm[(alm['AlarmNumber'] >= limits[0]) & (alm['AlarmNumber'] <= limits[1])]
            if not filter_alm.empty:
                trace = plot_alarms(
                    x=filter_alm['DateTime'],
                    y=filter_alm['AlarmNumber'],
                    #labels=filter_alm['Label'],
                    cat=cat)
                trace.yaxis="y9"

                fig.add_trace(trace)
    
    print('fig config')

    # Update layout properties
    fig.update_layout(hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)', namelength = -1, font=dict(color='black')),  
        legend=dict(groupclick="toggleitem"), #avoid grouping all traces #orientation="v", x = 1.1, 
        title_text="ChangeOver FCM Basic" , title_x=0.5
    )

    print("fig done")
    return (fig)

def change_over_divided(LogsStandard, LogsAlarms, LogsEvents=pd.DataFrame()):
    print("change_over_divided started ---")

    # dates of Standard logs to filter Events and Alarms
    mindate = LogsStandard['DateTime'].min()
    maxdate = LogsStandard['DateTime'].max()

    if not LogsAlarms.empty:
        alm = LogsAlarms[(LogsAlarms['DateTime'] > mindate) & (LogsAlarms['DateTime'] <= maxdate)]
    else:
        alm = pd.DataFrame()

    if not LogsEvents.empty:
        eve = LogsEvents[(LogsEvents['DateTime'] > mindate) & (LogsEvents['DateTime'] <= maxdate)]
    else:
        eve = pd.DataFrame()

    print("fig init")

    # Change layout of plot based on if Alarms or Events where imported
    chart_type = ''
    if alm.empty and eve.empty:

        fig = make_subplots(
            rows=7, cols=1,
            specs=[[{"rowspan": 4, "colspan": 1, "secondary_y": True}], # 4 Rows for Visc and Temp Trends
                [None],
                [None],
                [None],
                [{"secondary_y": True}],  # Valves position & ChangeOverON
                [{"secondary_y": False}],  # FT Mass OR FT Volume
                [{"secondary_y": True}]],  # PT & Density
                shared_xaxes=True)

        chart_type = 'NO_AE'
        
    elif (alm.empty and (not eve.empty)) or ((not alm.empty) and eve.empty):

        fig = make_subplots(
            rows=8, cols=1,
            specs=[[{"rowspan": 4, "colspan": 1, "secondary_y": True}], # 4 Rows for Visc and Temp Trends
                [None],
                [None],
                [None],
                [{"secondary_y": True}],  # Valves position & ChangeOverON
                [{"secondary_y": False}],  # FT Mass OR FT Volume
                [{"secondary_y": True}],  # PT & Density
                [{"secondary_y": False}]], # Events OR Alarms
                shared_xaxes=True) 
        
        if alm.empty:
            chart_type = 'NO_A'
            fig.update_yaxes(title_text="Events", row=8)

        else:
            chart_type = 'NO_E'
            fig.update_yaxes(title_text="Alarms", row=8)

    elif (not alm.empty) and (not eve.empty):

        fig = make_subplots(
            rows=8, cols=1,
            specs=[[{"rowspan": 4, "colspan": 1, "secondary_y": True}], # 4 Rows for Visc and Temp Trends
                [None],
                [None],
                [None],
                [{"secondary_y": True}],  # Valves position & ChangeOverON
                [{"secondary_y": False}],  # FT Mass OR FT Volume
                [{"secondary_y": True}],  # PT & Density
                [{"secondary_y": True}]], # Events & Alarms
                shared_xaxes=True) 
        
        chart_type = 'AE'
        fig.update_yaxes(title_text="Events",
                        row=8, secondary_y=False)
        fig.update_yaxes(title_text="Alarms",
                        row=8, secondary_y=True)
    

    # Iterate change_over_vars, to plot each category of variables
    for i, (category, variables) in enumerate(change_over_vars.items()):
        print(category)

        if category == 'Temperature':
            plot_row = 1

            fig.update_yaxes(title_text="Temperature",
                            row=plot_row, secondary_y=False)
            
            for j, variable in enumerate(variables):
                print(variable)

                if ('Limit' in variable):
                    trace = square_disc_line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color=px.colors.sequential.OrRd[(j+2)],
                        cat=category)
                    fig.add_trace(trace, row=plot_row, col=1, secondary_y=False)
                    
                else:
                    if not (LogsStandard[variable] == 0).all():
                        if ('Target' in variable):
                            color=px.colors.sequential.OrRd[(j+2)]
                        else:
                            color=px.colors.sequential.OrRd[-(j+1)]

                        trace = line_trace(
                            x=LogsStandard['DateTime'],
                            y=LogsStandard[variable],
                            name=variable,
                            color=color,
                            cat=category)
                        fig.add_trace(trace, row=plot_row, col=1, secondary_y=False)
        
        if category == 'Viscosity':
            plot_row = 1

            fig.update_yaxes(title_text="Viscosity",
                            row=plot_row, secondary_y=True)
            
            for j, variable in enumerate(variables):
                print(variable)

                if ('Limit' in variable):
                    trace = square_disc_line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color=px.colors.sequential.dense[(j+3)],
                        cat=category)
                else:
                    if ('Target' in variable):
                        color=px.colors.sequential.dense[(j+3)]
                    else:
                        color=px.colors.sequential.PuBu[-(j+1)]

                    trace = line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color=color,
                        cat=category)
                    
                fig.add_trace(trace, row=plot_row, col=1, secondary_y=True)

        if category == 'Valves':
            plot_row = 5
            for j, variable in enumerate(variables):
                print(variable)

                trace = square_line_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variable],
                    labels=LogsStandard[variable.split('_')[0]+'_Label'],
                    name=variable,
                    color=px.colors.qualitative.G10[j],
                    cat=category)
                
                if (j > 0) and (j < 3):
                    trace.visible = 'legendonly'
                
                fig.add_trace(trace, row=plot_row, col=1, secondary_y=False)
        
        if category == 'Bool': #ChangeOverInProgress
            plot_row = 5 
            for variable in variables:
                print(variable)

                trace = filled_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variable],
                    name=variable,
                    color='rgba(0, 128, 0, 0.1)', #green opacity 10%
                    cat=None)
                    
                fig.add_trace(trace, row=plot_row, col=1, secondary_y=True)
        
        if category == 'Flow':
            plot_row = 6

            fig.update_yaxes(title_text="Flow", row=plot_row)
            
            for variable in variables:
                print(variable)

                if variable == 'FT_MassFlow':
                    flag=False
                    if not (LogsStandard[variable] == 0).all():
                        trace = line_trace(
                            x=LogsStandard['DateTime'],
                            y=LogsStandard[variable],
                            name=variable,
                            color=px.colors.qualitative.G10[j+1],
                            cat=category)
                        fig.add_trace(trace, row=plot_row, col=1)

                    for j, fm in enumerate(['FM1_MassFlow','FM2_MassFlow','FM3_MassFlow','FM4_MassFlow']):
                        if not (LogsStandard[fm] == 0).all():
                            trace = line_trace(
                                x=LogsStandard['DateTime'],
                                y=LogsStandard[fm],
                                name=fm,
                                color=px.colors.qualitative.G10[j+2],
                                cat=category)
                            fig.add_trace(trace, row=plot_row, col=1)
                else:
                    flag=True
                            
                if variable == 'FT_VolumeFlow': #Volumetric
                    if flag:
                        trace = line_trace(
                                x=LogsStandard['DateTime'],
                                y=LogsStandard[variable],
                                name=variable,
                                color=px.colors.qualitative.G10[j+2],
                                cat=category)
                        fig.add_trace(trace, row=plot_row, col=1)

        if category == 'Pressure':
            plot_row = 7

            fig.update_yaxes(title_text="Pressure",
                row=plot_row, secondary_y=False)

            for j, variable in enumerate(variables):
                print(variable)

                trace = line_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variable],
                    name=variable,
                    color=px.colors.qualitative.Vivid[j],
                    cat=category)
                
                fig.add_trace(trace, row=plot_row, col=1, secondary_y=False)

        if category == 'Density':
            plot_row = 7
        
            fig.update_yaxes(title_text="Density",
                row=plot_row, secondary_y=True)
        
            trace = line_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variables[0]],
                    name=variables[0],
                    color=px.colors.qualitative.Vivid[j+1],
                    cat=category)
            fig.add_trace(trace, row=plot_row, col=1, secondary_y=True)

    plot_row = 8
    if (not eve.empty):
        print('events')

        trace = plot_events(
                    x=eve['DateTime'],
                    y=eve['EventNumber'],
                    labels=eve['Label'])
        
        if chart_type == 'AE':
            fig.add_trace(trace, row=plot_row, col=1,secondary_y=False)
        elif chart_type == 'NO_A':
            fig.add_trace(trace, row=plot_row, col=1)

    if (not alm.empty):
        for cat, limits in alarm_cats.items():
            print(cat)

            filter_alm = alm[(alm['AlarmNumber'] >= limits[0]) & (alm['AlarmNumber'] <= limits[1])]
            if not filter_alm.empty:
                trace = plot_alarms(
                    x=filter_alm['DateTime'],
                    y=filter_alm['AlarmNumber'],
                    #labels=filter_alm['Label'],
                    cat=cat)
                
                if chart_type == 'AE':
                    fig.add_trace(trace, row=plot_row, col=1,secondary_y=True)
                elif chart_type == 'NO_E':
                    fig.add_trace(trace, row=plot_row, col=1)

    print('fig config')
                    
    # Update layout properties
    fig.update_layout(hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)', namelength = -1, font=dict(color='black')),  
        legend=dict(groupclick="toggleitem"), #avoid grouping all traces #orientation="v", x = 1.1, 
        title_text="ChangeOver FCM Basic" , title_x=0.5
    )
    
    print('fig done')
    return fig