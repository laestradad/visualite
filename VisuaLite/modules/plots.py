import pandas as pd
from PIL import Image
import datetime
import os
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from modules import data_analysis as fcm

from modules.logging_cfg import setup_logger
logger = setup_logger()
logger.info("plots.py imported")

# Get the path to the current script
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
# Alfa Laval Logo path
AL_LOGO = os.path.join(SCRIPT_PATH, '..', 'resources', 'ALlogo.png')

# Custom dark style for matplotlib
custom_dark_style = {
    'axes.facecolor': '#24242424',  # Custom background color / DEFAULT '#1e1e1e'
    'axes.edgecolor': '#ffffff',  # Color of axes edges / DEFAULT '#ffffff'
    'axes.labelcolor': '#ffffff',  # Color of axes labels / DEFAULT 
    'text.color': '#ffffff',  # Color of text / DEFAULT '#ffffff'
    'xtick.color': '#ffffff',  # Color of x-axis ticks / DEFAULT '#ffffff'
    'ytick.color': '#ffffff',  # Color of y-axis ticks / DEFAULT '#ffffff'
    'figure.facecolor': '#1e1e1e',  # Figure background color / DEFAULT '#1e1e1e'
    'figure.edgecolor': '#1e1e1e',  # Figure edge color / DEFAULT '#1e1e1e'
    'axes.grid': False,  # Show grid / DEFAULT True
    'grid.color': '#333333',  # Color of grid lines / DEFAULT '#333333'
}

# Alfa Laval brand colors
ALcolors = ['rgba(17, 56, 127, 1)', #AL blue
            'rgba(0, 0, 0, 1)', #AL white
            'rgba(220, 146, 118, 1)', #AL earth
            'rgba(254, 205, 96, 1)', #AL sun
            'rgba(147, 199, 198, 1)', #AL water
            'rgba(0, 127, 200, 1)', #AL innovation
            ]

#----------------------------------------------------------- DECORATORS (to wrap functions and log errors if any)
def custom_callback(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("--- Callback failed ---")
            logger.error(e, exc_info=True)
    return wrapper

#----------------------------------------------------------- PLOTLY Functions
def plot_alarms(x,y,labels,cat):
    trace = go.Scatter(x=x, y=y.astype(str),
                       name=cat,
                       mode='markers', marker_symbol='x',
                       marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                       marker_line_width=1, marker_size=8,
                       legendgroup="Alarms",legendgrouptitle_text="Alarms",
                       hovertext=labels)
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

@custom_callback # wrapper to catch errors
def change_over_overlap(LogsStandard, LogsAlarms, LogsEvents, mch_info):
    logger.debug("change_over_overlap started ---")

    # Change over variables and classification
    change_over_vars = fcm.DATA['change_over_vars']

    # Alarms classification
    alarm_cats = fcm.DATA['alarm_cats']

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

    logger.debug("fig init")
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
        logger.debug(category)

        if category == 'Temperature':            

            for j, variable in enumerate(variables):
                logger.debug(variable)

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
                logger.debug(variable)

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
                logger.debug(variable)

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
        
        if category == 'Bool':
            for variable in variables:
                logger.debug(variable)
                if (variable == 'ChangeoverInProgress') or (variable == 'ChangeOverInProgress'):
                    trace = filled_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color='rgba(0, 128, 0, 0.1)', #green opacity 10%
                        cat=None)

                elif (variable == 'ControlType') or (variable == 'CurrentControl'):
                    trace = square_line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        labels=LogsStandard['CC_Label'],
                        name=variable,
                        color=px.colors.qualitative.G10[6],
                        cat=category)
                    trace.visible = 'legendonly'

                trace.yaxis="y4"           
                fig.add_trace(trace)
        
        if category == 'Flow':
            
            for variable in variables:
                logger.debug(variable)

                if fcm.MT == "FCM Oil 2b":

                    trace = line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variables[0]],
                        name=variables[0],
                        color=px.colors.qualitative.G10[j+1],
                        cat=category)
                    trace.yaxis="y5"
                    trace.visible = 'legendonly'
                    fig.add_trace(trace)

                elif fcm.MT == "FCM One | 1.5":

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
                logger.debug(variable)

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

    if fcm.MT == "FCM Oil 2b":

        trace = square_line_trace(
            x=LogsStandard['DateTime'],
            y=LogsStandard['MachineStatus'],
            labels=LogsStandard['STS_Label'],
            name='MachineStatus',
            color=ALcolors[5],
            cat='Events')
        trace.yaxis="y8"
        trace.visible = 'legendonly'

        fig.add_trace(trace)

    elif fcm.MT == "FCM One | 1.5":
        if (not eve.empty):
            logger.debug('events')

            trace = plot_events(
                        x=eve['DateTime'],
                        y=eve['EventNumber'],
                        labels=eve['Label'])
            trace.yaxis="y8"

            fig.add_trace(trace)

    if (not alm.empty):
        for cat, limits in alarm_cats.items():
            logger.debug(cat)

            filter_alm = alm[(alm['AlarmNumber'] >= limits[0]) & (alm['AlarmNumber'] <= limits[1])]
            if not filter_alm.empty:
                trace = plot_alarms(
                    x=filter_alm['DateTime'],
                    y=filter_alm['AlarmNumber'],
                    labels=filter_alm['Label'],
                    cat=cat)
                trace.yaxis="y9"

                fig.add_trace(trace)
    
    logger.debug('fig config')

    # Update layout properties
    fig.update_layout(hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)', namelength = -1, font=dict(color='black')),  
        legend=dict(groupclick="toggleitem"), #avoid grouping all traces #orientation="v", x = 1.1, 
        title_text=(mch_info[0] + " | " + mch_info[1] + " | " + mch_info[2]) , title_x=0.5
    )

    # Add image
    alLogo = Image.open(AL_LOGO)
    fig.add_layout_image(
        dict(
            source=alLogo,
            xref="paper", yref="paper",
            x=0, y=1.025,
            sizex=0.14, sizey=0.14,
            xanchor="left", yanchor="bottom"
        )
    )

    logger.debug("fig done")
    return (fig)

@custom_callback # wrapper to catch errors
def change_over_divided(LogsStandard, LogsAlarms, LogsEvents, mch_info):
    logger.debug("change_over_divided started ---")

    # Change over variables and classification
    change_over_vars = fcm.DATA['change_over_vars']

    # Alarms classification
    alarm_cats = fcm.DATA['alarm_cats']

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

    logger.debug("fig init")

    # Change layout of plot based on if Alarms or Events where imported
    chart_type = ''
    if (fcm.MT == "FCM One | 1.5") and (alm.empty and eve.empty):

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
        
    elif ((fcm.MT == "FCM One | 1.5") and ((alm.empty and (not eve.empty)) or ((not alm.empty) and eve.empty))) or ((fcm.MT == "FCM Oil 2b") and (alm.empty)):
            
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

    elif ((fcm.MT == "FCM One | 1.5") and (not alm.empty) and (not eve.empty)) or ((fcm.MT == "FCM Oil 2b") and (not alm.empty)):

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
    
    logger.debug(f"{chart_type=}")

    # Iterate change_over_vars, to plot each category of variables
    for i, (category, variables) in enumerate(change_over_vars.items()):
        logger.debug(category)

        if category == 'Temperature':
            plot_row = 1

            fig.update_yaxes(title_text="Temperature",
                            row=plot_row, secondary_y=False)
            
            for j, variable in enumerate(variables):
                logger.debug(variable)

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
                logger.debug(variable)

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
                logger.debug(variable)

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
                logger.debug(variable)

                if (variable == 'ChangeoverInProgress') or (variable == 'ChangeOverInProgress'):

                    trace = filled_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        name=variable,
                        color='rgba(0, 128, 0, 0.1)', #green opacity 10%
                        cat=None)

                elif (variable == 'ControlType') or (variable == 'CurrentControl'):
                    trace = square_line_trace(
                        x=LogsStandard['DateTime'],
                        y=LogsStandard[variable],
                        labels=LogsStandard['CC_Label'],
                        name=variable,
                        color=px.colors.qualitative.G10[6],
                        cat=category)
                    
                fig.add_trace(trace, row=plot_row, col=1, secondary_y=True)
        
        if category == 'Flow':
            plot_row = 6

            fig.update_yaxes(title_text="Flow", row=plot_row)
            
            if fcm.MT == "FCM Oil 2b":

                trace = line_trace(
                    x=LogsStandard['DateTime'],
                    y=LogsStandard[variables[0]],
                    name=variables[0],
                    color=px.colors.qualitative.G10[j+1],
                    cat=category)
                fig.add_trace(trace, row=plot_row, col=1)

            elif fcm.MT == "FCM One | 1.5":
                for variable in variables:
                    logger.debug(variable)

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
                logger.debug(variable)

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
        logger.debug('events')

        trace = plot_events(
                    x=eve['DateTime'],
                    y=eve['EventNumber'],
                    labels=eve['Label'])
        
        if chart_type == 'AE':
            fig.add_trace(trace, row=plot_row, col=1,secondary_y=False)
        elif chart_type == 'NO_A':
            fig.add_trace(trace, row=plot_row, col=1)

    # For FCM Basic, no Event logs but Event Number
    if fcm.MT == "FCM Oil 2b":
        trace = square_line_trace(
            x=LogsStandard['DateTime'],
            y=LogsStandard['MachineStatus'],
            labels=LogsStandard['STS_Label'],
            name='MachineStatus',
            color=ALcolors[5],
            cat='Events')

        if chart_type == 'NO_A':
            fig.add_trace(trace, row=plot_row, col=1)
        else:
            fig.add_trace(trace, row=plot_row, col=1,secondary_y=False)

    if (not alm.empty):
        for cat, limits in alarm_cats.items():
            logger.debug(cat)

            filter_alm = alm[(alm['AlarmNumber'] >= limits[0]) & (alm['AlarmNumber'] <= limits[1])]
            if not filter_alm.empty:
                trace = plot_alarms(
                    x=filter_alm['DateTime'],
                    y=filter_alm['AlarmNumber'],
                    labels=filter_alm['Label'],
                    cat=cat)
                
                if fcm.MT == "FCM Oil 2b":
                    fig.add_trace(trace, row=plot_row, col=1,secondary_y=True)

                elif fcm.MT == "FCM One | 1.5":
                    if chart_type == 'AE':
                        fig.add_trace(trace, row=plot_row, col=1,secondary_y=True)
                    elif chart_type == 'NO_E':
                        fig.add_trace(trace, row=plot_row, col=1)

    logger.debug('fig config')
                    
    # Update layout properties
    fig.update_layout(hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)', namelength = -1, font=dict(color='black')),  
        legend=dict(groupclick="toggleitem"), #avoid grouping all traces #orientation="v", x = 1.1, 
        title_text=(mch_info[0] + " | " + mch_info[1] + " | " + mch_info[2]) , title_x=0.5
    )

    # Add image
    alLogo = Image.open(AL_LOGO)
    fig.add_layout_image(
        dict(
            source=alLogo,
            xref="paper", yref="paper",
            x=0, y=1.025,
            sizex=0.14, sizey=0.14,
            xanchor="left", yanchor="bottom"
        )
    )

    logger.debug('fig done')
    return fig

@custom_callback # wrapper to catch errors
def custom_plot_divided(dfs, dfa, dfe, cols, date1, date2, tittle): # n rows, one for each unit
    logger.debug("custom_plot1 started ---")


    # Columns with its respective unit
    units = fcm.DATA['units']

    # Alarms classification
    alarm_cats = fcm.DATA['alarm_cats']

    logger.debug("date limits:")
    logger.debug(f"{date1=},{date2=}")
    
    # filter dataframes for date interval selected
    if not dfs.empty:
        dfs = dfs[(dfs['DateTime'] >= date1) & (dfs['DateTime'] <= date2)]
    else:
        dfs = pd.DataFrame()
        logger.debug("Standard Logs empty in date range selected")

    if not dfa.empty:
        dfa = dfa[(dfa['DateTime'] >= date1) & (dfa['DateTime'] <= date2)]
    else:
        dfa = pd.DataFrame()
        logger.debug("Alarm Logs empty in date range selected")

    if not dfe.empty:
        dfe = dfe[(dfe['DateTime'] >= date1) & (dfe['DateTime'] <= date2)]
    else:
        dfe = pd.DataFrame()
        logger.debug("Event Logs empty in date range selected")

    #returns an empty plot if no data to plot
    if dfs.empty and dfa.empty and dfe.empty:
        fig = go.Figure()
        fig.update_layout(title_text=tittle)
        logger.debug("--- no data to plot")
        return fig

    # From column list, get a dictionary with cols classified by unit type
    cols2 = fcm.classify_cols(cols)
    logger.debug("selected units and columns:")
    logger.debug(cols2)

    logger.debug("fig init")
    fig = make_subplots(rows=len(cols2), cols=1, shared_xaxes=True, vertical_spacing=0.02)

    # Iterate classified cols and create traces
    for i, (unit, cols) in enumerate(cols2.items()):
        logger.debug(f"{i=}, {unit=}, {cols=}")

        fig.update_yaxes(title_text=unit,row=i+1)

        for col in cols:
            logger.debug(f"{col=}")

            if col == 'AlarmNumber':
                for cat, limits in alarm_cats.items():
                    logger.debug(cat)

                    filter_alm = dfa[(dfa['AlarmNumber'] >= limits[0]) & (dfa['AlarmNumber'] <= limits[1])]
                    if not filter_alm.empty:
                        trace = plot_alarms(
                            x=filter_alm['DateTime'],
                            y=filter_alm['AlarmNumber'],
                            labels=filter_alm['Label'],
                            cat=cat)
                        fig.add_trace(trace, row=i+1, col=1)

            elif col == 'EventNumber':
                if not dfe.empty:
                    trace = plot_events(
                        x=dfe['DateTime'],
                        y=dfe['EventNumber'],
                        labels=dfe['Label'])
                    
                    fig.add_trace(trace, row=i+1, col=1)

            elif col == 'MachineStatus':
                trace = square_line_trace(
                    x=dfs['DateTime'],
                    y=dfs['MachineStatus'],
                    labels=dfs['STS_Label'],
                    name='MachineStatus',
                    color=ALcolors[5],
                    cat='Events')
                    
                fig.add_trace(trace, row=i+1, col=1)

            elif 'CV' in col:
                trace = square_line_trace(
                    x=dfs['DateTime'],
                    y=dfs[col],
                    labels=dfs[col.split('_')[0]+'_Label'],
                    name=col,
                    cat=unit)
                fig.add_trace(trace, row=i+1, col=1)

            elif (col == 'ControlType') or (col == 'CurrentControl'):
                trace = square_line_trace(
                    x=dfs['DateTime'],
                    y=dfs[col],
                    labels=dfs['CC_Label'],
                    name=col,
                    cat=unit)
                fig.add_trace(trace, row=i+1, col=1)

            else:
                if not dfs.empty:
                    # If unit is a bool, int or valve_pos(int), create a square line trace instead of spline
                    if unit in ['bool', 'int', 'valve_pos']:
                        trace = square_line_trace(
                            x=dfs['DateTime'],
                            y=dfs[col],
                            name=col,
                            cat=unit)
                    else:
                        trace = line_trace(
                            x=dfs['DateTime'],
                            y=dfs[col],
                            name=col,
                            cat=unit)

                    fig.add_trace(trace, row=i+1, col=1)

    logger.debug("fig config")

    # Update layout properties
    fig.update_layout(hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)', namelength = -1, font=dict(color='black')),  
        legend=dict(groupclick="toggleitem"), #avoid grouping all traces
        title_text=tittle , title_x=0.5
    )

    # Add image
    alLogo = Image.open(AL_LOGO)
    fig.add_layout_image(
        dict(
            source=alLogo,
            xref="paper", yref="paper",
            x=0, y=1.025,
            sizex=0.14, sizey=0.14,
            xanchor="left", yanchor="bottom"
        )
    )
    
    logger.debug("fig done")
    return fig

@custom_callback # wrapper to catch errors
def custom_LPGplot_divided(dfs, dfa, cols, date1, date2, tittle): # n rows, one for each unit
    logger.debug("custom_plot1 started ---")
    logger.debug("date limits:")
    logger.debug(f"{date1=},{date2=}")
    
    # filter dataframes for date interval selected
    if not dfs.empty:
        dfs = dfs[(dfs['Timestamp'] >= date1) & (dfs['Timestamp'] <= date2)]
    else:
        dfs = pd.DataFrame()
        logger.debug("Standard Logs empty in date range selected")

    if not dfa.empty:
        dfa = dfa[(dfa['Timestamp'] >= date1) & (dfa['Timestamp'] <= date2)]
    else:
        dfa = pd.DataFrame()
        logger.debug("Alarm Logs empty in date range selected")

    #returns an empty plot if no data to plot
    if dfs.empty and dfa.empty:
        fig = go.Figure()
        fig.update_layout(title_text=tittle)
        logger.debug("--- no data to plot")
        return fig

    # From column list, get a dictionary with cols classified by unit type
    cols2 = fcm.classify_cols(cols)
    logger.debug("selected units and columns:")
    logger.debug(cols2)

    logger.debug("fig init")
    fig = make_subplots(rows=len(cols2), cols=1, shared_xaxes=True, vertical_spacing=0.02)

    # Iterate classified cols and create traces
    for i, (unit, cols) in enumerate(cols2.items()):
        logger.debug(f"{i=}, {unit=}, {cols=}")

        fig.update_yaxes(title_text=unit,row=i+1)

        for col in cols:
            logger.debug(f"{col=}")

            if col == 'Alarms':
                # Pivot the DataFrame
                pivot_df = dfa.pivot(index='Timestamp', columns='Name', values='Change')
                # Reset index to have Timestamp as a column
                pivot_df = pivot_df.reset_index()

                # Iterate over the columns of the pivot DataFrame
                for column in pivot_df.columns[1:]:
                    # Create a DataFrame for each column without NaN values
                    df_col = pivot_df[['Timestamp', column]].dropna()
                    # Create a trace for the current column
                    trace = go.Scatter(x=df_col['Timestamp'], y=df_col[column], line_shape='hv', name=column)
                    # Append the trace to the list of traces
                    fig.add_trace(trace, row=i+1, col=1)

            else:
                if not dfs.empty:
                    # If unit is a bool, int or valve_pos(int), create a square line trace instead of spline
                    if unit in ['Bool', 'Step']:
                        trace = square_line_trace(
                            x=dfs['Timestamp'],
                            y=dfs[col],
                            name=col,
                            cat=unit)
                    else:
                        trace = line_trace(
                            x=dfs['Timestamp'],
                            y=dfs[col],
                            name=col,
                            cat=unit)

                    fig.add_trace(trace, row=i+1, col=1)

    logger.debug("fig config")

    # Update layout properties
    fig.update_layout(hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)', namelength = -1, font=dict(color='black')),  
        legend=dict(groupclick="toggleitem"), #avoid grouping all traces
        title_text=tittle , title_x=0.5
    )

    # Add image
    alLogo = Image.open(AL_LOGO)
    fig.add_layout_image(
        dict(
            source=alLogo,
            xref="paper", yref="paper",
            x=0, y=1.025,
            sizex=0.14, sizey=0.14,
            xanchor="left", yanchor="bottom"
        )
    )
    
    logger.debug("fig done")
    return fig
