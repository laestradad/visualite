import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import datetime
import os
import json


from modules import data_analysis as fcm

from modules.logging_cfg import setup_logger
logger = setup_logger()
logger.info("plots.py imported")

# Get the path to the current script
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
# Alfa Laval Logo path
AL_LOGO = os.path.join(SCRIPT_PATH, '..', 'resources', 'ALlogo.png')
# Construct the path to the file.txt in the resources directory
UNITS = os.path.join(SCRIPT_PATH, '..', 'resources', 'units.txt')

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

greens = ['rgba(0, 128, 0, 0.1)', #green opacity 10%
          'rgba(196, 180, 84, 1)', #vegas gold
          'rgba(64, 224, 208, 1)', #turquoise
          'rgba(69, 75, 27, 1)', #army green
          'rgba(147, 197, 114, 1)', #pistachio
          'rgba(8, 143, 143, 1)', #citrine
        ]

blues = ['rgba(0, 71, 171, 1)', #cobalt blue
        'rgba(70, 130, 180, 1)' #steel blue
        ]

reds = ['rgba(255, 87, 51, 1)', #cherry
        'rgba(250, 160, 160, 1)', #pastel red
        ]

purples = ['rgba(191, 64, 191, 1)', #bright purple
           'rgba(93, 63, 211, 1)', #iris
           'rgba(127, 0, 255, 1)', #violet
           'rgba(149, 53, 83, 1)', #red purple
           'rgba(218, 112, 214, 1)' #mulberry
           ]

comp1 = ['rgba(29, 157, 228, 1)', #blue*
           'rgba(228, 100, 29, 1)', #orange*
           'rgba(63, 166, 121, 1)', #green*
           ]

ALcolors = ['rgba(17, 56, 127, 1)', #AL blue
            'rgba(0, 0, 0, 1)', #AL white
            'rgba(220, 146, 118, 1)', #AL earth
            'rgba(254, 205, 96, 1)', #AL sun
            'rgba(147, 199, 198, 1)', #AL water
            'rgba(0, 127, 200, 1)', #AL innovation
            ]

#----------------------------------------------------------- DECORATORS
def custom_callback(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("--- Callback failed ---")
            logger.error(e, exc_info=True)
    return wrapper

#----------------------------------------------------------- IMPORT UNITS FOR FCM ONE LOG FILES
with open(UNITS, 'r') as file:
    units = json.load(file)

# plotly
@custom_callback # wrapper to catch errors
def Plot_ChangeOver_simple(df, mch_info, LogsAlarms, LogsEvents):
    logger.debug("Plot_ChangeOver_simple started ---")

    mindate = df['DateTime'].min()
    maxdate = df['DateTime'].max()
    logger.debug(f"{mindate=}, {maxdate=}")

    if not LogsAlarms.empty:
        alm = LogsAlarms[(LogsAlarms['DateTime'] > mindate) & (LogsAlarms['DateTime'] <= maxdate)]
    else:
        logger.debug("LogsAlarms is empty")
        alm = pd.DataFrame()
    
    if not LogsEvents.empty:
        eve = LogsEvents[(LogsEvents['DateTime'] > mindate) & (LogsEvents['DateTime'] <= maxdate)]
    else:
        logger.debug("LogsEvents is empty")
        eve = pd.DataFrame()

    logger.debug("fig init")
    fig = go.Figure()

    # --------------------------------------------------- Valves
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['ChangeOverInProgress'].astype(bool),
        name="Change Over InProgress",
        fill='tozeroy', mode='none', fillcolor = greens[0],    
        yaxis="y4"
    ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV1_Position'],
        name="CV1 Position",
        line=dict(color = greens[1]), 
        legendgroup="Valves",legendgrouptitle_text="Valves",
        line_shape='hv',
        hovertext=df['CV1_Label'], 
        visible='legendonly',
        yaxis="y3"
    ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV2_Position'],
        name="CV2 Position",
        line=dict(color = greens[2]),
        legendgroup="Valves",legendgrouptitle_text="Valves",
        line_shape='hv',
        hovertext=df['CV2_Label'], 
        visible='legendonly',
        yaxis="y3"
    ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV3_Position'],
        name="CV3 Position",
        line=dict(color = greens[3]),    
        legendgroup="Valves",legendgrouptitle_text="Valves",
        line_shape='hv',
        hovertext=df['CV3_Label'], 
        visible='legendonly',
        yaxis="y3"
    ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV4_Position'],
        name="CV4 Position",
        line=dict(color = greens[4]), 
        legendgroup="Valves",legendgrouptitle_text="Valves",
        line_shape='hv',
        hovertext=df['CV4_Label'], 
        visible='legendonly',
        yaxis="y3"
    ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV5_Position'],
        name="CV5 Position",
        line=dict(color = greens[5]),
        legendgroup="Valves",legendgrouptitle_text="Valves",
        line_shape='hv',
        hovertext=df['CV5_Label'], 
        visible='legendonly',
        yaxis="y3"
    ))
       
    # --------------------------------------------------- Flow

    if not (df['FT_MassFlow'] == 0).all():
        # -------------------------------------------- Mass Flows
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['FT_MassFlow'],
            name='FT_MassFlow',
            line=dict(color = purples[0]),
            legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly',
                yaxis="y7"))
        
        if not (df['FM1_MassFlow'] == 0).all():
            fig.add_trace(go.Scatter(
                x=df['DateTime'],
                y=df['FM1_MassFlow'],
                name='FM1 MassFlow',
                line=dict(color = purples[1]),
                legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly',
                yaxis="y7"))

        if not (df['FM2_MassFlow'] == 0).all():
            fig.add_trace(go.Scatter(
                x=df['DateTime'],
                y=df['FM2_MassFlow'],
                name='FM2 MassFlow',
                line=dict(color = purples[2]),
                legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly',
                yaxis="y7"))
            
        if not (df['FM3_MassFlow'] == 0).all():
            fig.add_trace(go.Scatter(
                x=df['DateTime'],
                y=df['FM3_MassFlow'],
                name='FM3 MassFlow',
                line=dict(color = purples[3]),
                legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly',
                yaxis="y7"))

        if not (df['FM4_MassFlow'] == 0).all():
            fig.add_trace(go.Scatter(
                x=df['DateTime'],
                y=df['FM4_MassFlow'],
                name='FM4 MassFlow',
                line=dict(color = purples[4]),
                legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly',
                yaxis="y7"))
    
    else:
        # -------------------------------------------- Volume Flow
        fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['FT_VolumeFlow'],
        name='FT_VolumeFlow',
        line=dict(color = comp1[2]),
        legendgroup="Flow",legendgrouptitle_text="Flow", 
        visible='legendonly',
        yaxis="y7"))
    
    # --------------------------------------------------- Density
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['Density'],
        name='Density',
        line=dict(color = ALcolors[3]),
        legendgroup="Density",legendgrouptitle_text="Density", 
        visible='legendonly', yaxis="y9"))  
    
    # --------------------------------------------------- Pressures
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['PT1'],
        name='PT1',
        line=dict(color = purples[3]),
        legendgroup="Pressure",legendgrouptitle_text="Pressure", 
        visible='legendonly',
        yaxis="y8"))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['PT2'],
        name='PT2',
        line=dict(color = purples[4]),
        legendgroup="Pressure",legendgrouptitle_text="Pressure", 
        visible='legendonly',
        yaxis="y8"))
    
    # ---------------------------------------------------Temperature
    if (df['TT1'] != 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['TT1'],
            name='TT1 - Act Temp',
            line=dict(color = reds[0]),
            legendgroup="Temperature",legendgrouptitle_text="Temperature",
        ))

    if (df['TT2'] != 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['TT2'],
            name='TT2 - Act Temp',
            line=dict(color = reds[0]),
            legendgroup="Temperature",legendgrouptitle_text="Temperature",
        ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TargetTemperature'],
        name='Target Temperature',
        line=dict(color = reds[1]),
        legendgroup="Temperature",legendgrouptitle_text="Temperature",
    ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TemperatureLowLimit'],
        name='Temp Low Limit',
        line=dict(color = reds[1], dash='dot'),
        legendgroup="Temperature",legendgrouptitle_text="Temperature",
    ))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TemperatureHighLimit'],
        name='Temperature High Limit',
        line=dict(color = reds[1], dash='dot'),
        legendgroup="Temperature",legendgrouptitle_text="Temperature",
    ))

    # --------------------------------------------------- Viscosity
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['VT'],
        name='Viscosity',
        line=dict(color = blues[0]),
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity",
        yaxis="y2"))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TargetViscosity'],
        name='Target Viscosity',
        line=dict(color = blues[1]),
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity",
        yaxis="y2"))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['ViscosityLowLimit'],
        name='Viscosity Low Limit',
        line=dict(color = blues[1], dash='dot'),
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity",
        yaxis="y2"))

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['ViscosityHighLimit'],
        name='Viscosity High Limit',
        line=dict(color = blues[1], dash='dot'),
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity",
        yaxis="y2"))
    
    # --------------------------------------------------- Events
    if not eve.empty:
        fig.add_trace(go.Scatter(x=eve['DateTime'], y=eve['EventNumber'].astype(int),
                                name='Event Number',
                                mode='markers',marker_symbol='star',
                                marker_line_color=ALcolors[5], marker_color=ALcolors[5],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Events",legendgrouptitle_text="Events",
                                hovertext=eve['Label'], yaxis="y5"))
        
    # --------------------------------------------------- Alarms
    p_alm = alm[(alm['AlarmNumber'] < 199)] # System Alarms A0xx to A1xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='System Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6"))
        
    p_alm = alm[(alm['AlarmNumber'] > 199) & (alm['AlarmNumber'] <= 299)] # ChangeOver Alarms A2xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='ChangeOver Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6"))    
        
    p_alm = alm[(alm['AlarmNumber'] > 299) & (alm['AlarmNumber'] <= 399)] # Blending Alarms A3xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Blending Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6"))  
        
    p_alm = alm[(alm['AlarmNumber'] > 499) & (alm['AlarmNumber'] <= 599)] # Pumps Alarms A5xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Pressure Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6"))  
        
    p_alm = alm[(alm['AlarmNumber'] > 599) & (alm['AlarmNumber'] <= 699)] # Filter Alarms A6xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Filter Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6"))
        
    p_alm = alm[(alm['AlarmNumber'] > 799) & (alm['AlarmNumber'] <= 899)] # Mixing Tank Alarms A8xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Mixing Tank',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6"))
        
    p_alm = alm[(alm['AlarmNumber'] > 899) & (alm['AlarmNumber'] <= 999)] # TempControl Alarms A9xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='TempControl Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6")) 
        
    p_alm = alm[(alm['AlarmNumber'] > 999) & (alm['AlarmNumber'] <= 1099)] # ViscMeas Alarms A9xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='ViscMeas Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label'], yaxis="y6"))  
        
    # Create axis objects
    fig.update_layout(
        xaxis=dict(domain=[0.1, 0.9]), #compress x axis 10% left an right

        yaxis=dict(
            title="Temperature"),
        yaxis2=dict(
            title="Viscosity",
            anchor="free",
            overlaying="y",
            side="left",
            position=0
            ),
        yaxis3=dict(
            title="", #ChangeOver
            overlaying='y',
            side='left',
            showline=False,
            showticklabels=False
            ),
        yaxis4=dict(
            title="", #CVs
            overlaying='y',
            side='left',
            showline=False,
            showticklabels=False
            ),
        yaxis5=dict(
            title="", #Events
            overlaying='y',
            side='left',
            showline=False,
            showticklabels=False
            ),
        yaxis6=dict(
            title="", #Alarms
            overlaying='y',
            side='left',
            showline=False,
            showticklabels=False
            ),
        yaxis7=dict(
            title="Flow",
            anchor="x",
            overlaying="y",
            side="right"
            ),
        yaxis8=dict(
            title="Pressure",
            anchor="free",
            overlaying="y",
            side="right",
            position=1
            ),
        yaxis9=dict(
            title="", #Density
            overlaying='y',
            side='left',
            showline=False,
            showticklabels=False
            ),

        legend=dict(orientation="v", x = 1.1)
    )

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
def Plot_ChangeOver(df, mch_info, LogsAlarms, LogsEvents):
    logger.debug("Plot_ChangeOver started ---")

    mindate = df['DateTime'].min()
    maxdate = df['DateTime'].max()
    logger.debug(f"{mindate=}, {maxdate=}")
    
    if not LogsAlarms.empty:
        alm = LogsAlarms[(LogsAlarms['DateTime'] > mindate) & (LogsAlarms['DateTime'] <= maxdate)]
    else:
        logger.debug("LogsAlarms is empty")
        alm = pd.DataFrame()
    
    if not LogsEvents.empty:
        eve = LogsEvents[(LogsEvents['DateTime'] > mindate) & (LogsEvents['DateTime'] <= maxdate)]
    else:
        logger.debug("LogsEvents is empty")
        eve = pd.DataFrame()

    logger.debug("fig init")

    fig = make_subplots(
        rows=8, cols=1,
        specs=[[{"rowspan": 4, "colspan": 1, "secondary_y": True}], # 4 Rows for Visc and Temp Trends
            [None],
            [None],
            [None],
            [{"secondary_y": True}],  # Valves position & ChangeOverON
            [{"secondary_y": True}],  # FT Mass & FT Volume
            [{"secondary_y": True}],  # PT & Density
            [{"secondary_y": True}]], # Events & Alarms
            shared_xaxes=True) #,print_grid=True)

    # --------------------------------------------------------------------------------------------- R1-4 C1
    plot_row= 1
    plot_col= 1

    fig.update_yaxes(title_text="Temperature", 
                    title_font_color= reds[0],
                    color= reds[0],row=plot_row, secondary_y=False)
    fig.update_yaxes(title_text="Viscosity", 
                    title_font_color= blues[0],
                    color= blues[0], row=plot_row, secondary_y=True)

    # ---------------------------------------------------Temperature
    if (df['TT1'] != 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['TT1'],
            name='TT1 - Act Temp',
            line=dict(color = reds[0]),
            legendgroup="Temperature",legendgrouptitle_text="Temperature",
        ), row=plot_row, col=plot_col, secondary_y=False)

    if (df['TT2'] != 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['TT2'],
            name='TT2 - Act Temp',
            line=dict(color = reds[0]),
            legendgroup="Temperature",legendgrouptitle_text="Temperature",
        ), row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TargetTemperature'],
        name='Target Temperature',
        line=dict(color = reds[1]),line_shape='hv',
        legendgroup="Temperature",legendgrouptitle_text="Temperature",
    ), row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TemperatureLowLimit'],
        name='Temp Low Limit',
        line=dict(color = reds[1], dash='dot'),line_shape='hv',
        legendgroup="Temperature",legendgrouptitle_text="Temperature",
    ), row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TemperatureHighLimit'],
        name='Temperature High Limit',
        line=dict(color = reds[1], dash='dot'),line_shape='hv',
        legendgroup="Temperature",legendgrouptitle_text="Temperature",
    ), row=plot_row, col=plot_col, secondary_y=False)

    # --------------------------------------------------- Viscosity

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['VT'],
        name='Viscosity',
        line=dict(color = blues[0]),
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity"),
        row=plot_row, col=plot_col, secondary_y=True)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['TargetViscosity'],
        name='Target Viscosity',
        line=dict(color = blues[1]),line_shape='hv',
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity"),
        row=plot_row, col=plot_col, secondary_y=True)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['ViscosityLowLimit'],
        name='Viscosity Low Limit',
        line=dict(color = blues[1], dash='dot'),line_shape='hv',
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity"),
        row=plot_row, col=plot_col, secondary_y=True)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['ViscosityHighLimit'],
        name='Viscosity High Limit',
        line=dict(color = blues[1], dash='dot'),line_shape='hv',
        legendgroup="Viscosity",legendgrouptitle_text="Viscosity"),
        row=plot_row, col=plot_col, secondary_y=True)

    # --------------------------------------------------------------------------------------------- R5 C1
    plot_row= 5
    plot_col= 1

    fig.update_yaxes(visible = False,
                    title_text="True/False",
                    row=plot_row, secondary_y=True)
    fig.update_yaxes(title_text="Valve Position",
                    row=plot_row, secondary_y=False)
    # --------------------------------------------------- Bools
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['ChangeOverInProgress'].astype(bool),
        name="Change Over InProgress",
        fill='tozeroy', mode='none', fillcolor = greens[0],    
        line_shape='hv'
    ), row=plot_row, col=plot_col, secondary_y=True)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV1_Position'],
        name="CV1 Position",
        line=dict(color = ALcolors[0]), 
        legendgroup="Valves",legendgrouptitle_text="Valves", line_shape='hv',
        hovertext=df['CV1_Label']), row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV2_Position'],
        name="CV2 Position",
        line=dict(color = ALcolors[2]),
        legendgroup="Valves",legendgrouptitle_text="Valves", line_shape='hv',
        hovertext=df['CV2_Label'], visible='legendonly'), row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV3_Position'],
        name="CV3 Position",
        line=dict(color = ALcolors[3]),    
        legendgroup="Valves",legendgrouptitle_text="Valves", line_shape='hv',
        hovertext=df['CV3_Label'], visible='legendonly'), row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV4_Position'],
        name="CV4 Position",
        line=dict(color = ALcolors[4]), 
        legendgroup="Valves",legendgrouptitle_text="Valves", line_shape='hv',
        hovertext=df['CV4_Label']), row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['CV5_Position'],
        name="CV5 Position",
        line=dict(color = ALcolors[5]),
        legendgroup="Valves",legendgrouptitle_text="Valves", line_shape='hv',
        hovertext=df['CV5_Label']), row=plot_row, col=plot_col, secondary_y=False)

    # --------------------------------------------------------------------------------------------- R6 C1
    plot_row= 6
    plot_col= 1

    fig.update_yaxes(title_text="Mass Flow",
                    row=plot_row, secondary_y=False)
    fig.update_yaxes(title_text="Volume Flow",
                    row=plot_row, secondary_y=True)
    # --------------------------------------------------- Flow Meter
    
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['FT_MassFlow'],
        name='FT_MassFlow',
        line=dict(color = purples[0]),
        legendgroup="FT",legendgrouptitle_text="Flow"),
        row=plot_row, col=plot_col, secondary_y=False)
        
    if not (df['FM1_MassFlow'] == 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['FM1_MassFlow'],
            name='FM1 MassFlow',
            line=dict(color = purples[1]),
            legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly'),
            row=plot_row, col=plot_col, secondary_y=False)

    if not (df['FM2_MassFlow'] == 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['FM2_MassFlow'],
            name='FM2 MassFlow',
            line=dict(color = purples[2]),
            legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly'),
            row=plot_row, col=plot_col, secondary_y=False)
        
    if not (df['FM3_MassFlow'] == 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['FM3_MassFlow'],
            name='FM3 MassFlow',
            line=dict(color = purples[3]),
            legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly'),
            row=plot_row, col=plot_col, secondary_y=False)

    if not (df['FM4_MassFlow'] == 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['FM4_MassFlow'],
            name='FM4 MassFlow',
            line=dict(color = purples[4]),
            legendgroup="FT",legendgrouptitle_text="Flow", visible='legendonly'),
            row=plot_row, col=plot_col, secondary_y=False)

    # --------------------------------------------------- Volume Flow
    if not (df['FT_VolumeFlow'] == 0).all():
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['FT_VolumeFlow'],
            name='FT_VolumeFlow',
            line=dict(color = comp1[2]),
            legendgroup="FT",legendgrouptitle_text="Flow"),
            row=plot_row, col=plot_col, secondary_y=True)
            
    # --------------------------------------------------------------------------------------------- R7 C1
    plot_row= 7
    plot_col= 1

    fig.update_yaxes(title_text="Pressure",
                    row=plot_row, secondary_y=False)
    fig.update_yaxes(title_text="Density",
                    row=plot_row, secondary_y=True)
    # --------------------------------------------------- Pressures
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['PT1'],
        name='PT1',
        line=dict(color = comp1[0]),
        legendgroup="PT",legendgrouptitle_text="Pressure"),
        row=plot_row, col=plot_col, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['PT2'],
        name='PT2',
        line=dict(color = comp1[1]),
        legendgroup="PT",legendgrouptitle_text="Pressure"),
        row=plot_row, col=plot_col, secondary_y=False)
    
        # --------------------------------------------------- Density
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['Density'],
        name='Density',
        line=dict(color = ALcolors[3]),
        legendgroup="Density",legendgrouptitle_text="Density", visible='legendonly'),
        row=plot_row, col=plot_col, secondary_y=True)

    # --------------------------------------------------------------------------------------------- R8 C1
    plot_row= 8
    plot_col= 1

    fig.update_yaxes(title_text="Events",
                    row=plot_row, secondary_y=False)
    fig.update_yaxes(title_text="Alarms",
                    row=plot_row, secondary_y=True)
    # --------------------------------------------------- Events
    if not eve.empty:
        fig.add_trace(go.Scatter(x=eve['DateTime'], y=eve['EventNumber'].astype(int),
                                name='Event Number',
                                mode='markers',marker_symbol='star',
                                marker_line_color=ALcolors[5], marker_color=ALcolors[5],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Events",legendgrouptitle_text="Events",
                                hovertext=eve['Label']),
                        row=plot_row, col=plot_col,secondary_y=False)
    else:
        fig.add_trace(go.Scatter(x=df['DateTime'], y=[0] * len(df),
                                name='dummy',
                                line=dict(color = ALcolors[3]),
                                visible='legendonly'),
                                row=plot_row, col=plot_col, secondary_y=True)

    # --------------------------------------------------- Alarms
    p_alm = alm[(alm['AlarmNumber'] < 199)] # System Alarms A0xx to A1xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='System Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True)     
        

    p_alm = alm[(alm['AlarmNumber'] > 199) & (alm['AlarmNumber'] <= 299)] # ChangeOver Alarms A2xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='ChangeOver Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True)     
        
    p_alm = alm[(alm['AlarmNumber'] > 299) & (alm['AlarmNumber'] <= 399)] # Blending Alarms A3xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Blending Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True) 
    
    p_alm = alm[(alm['AlarmNumber'] > 399) & (alm['AlarmNumber'] <= 499)] # Pumps Alarms A4xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Pressure Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True)   
        
    p_alm = alm[(alm['AlarmNumber'] > 499) & (alm['AlarmNumber'] <= 599)] # Pumps Alarms A5xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Pressure Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True)    
        
    p_alm = alm[(alm['AlarmNumber'] > 599) & (alm['AlarmNumber'] <= 699)] # Filter Alarms A6xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Filter Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True) 
        
    p_alm = alm[(alm['AlarmNumber'] > 799) & (alm['AlarmNumber'] <= 899)] # Mixing Tank Alarms A8xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='Mixing Tank',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True) 
        
    p_alm = alm[(alm['AlarmNumber'] > 899) & (alm['AlarmNumber'] <= 999)] # TempControl Alarms A9xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='TempControl Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True) 
        
    p_alm = alm[(alm['AlarmNumber'] > 999) & (alm['AlarmNumber'] <= 1099)] # ViscMeas Alarms A9xx
    if not p_alm.empty:
        fig.add_trace(go.Scatter(x=p_alm['DateTime'], y=p_alm['AlarmNumber'].astype(str),
                                name='ViscMeas Alarms',
                                mode='markers', marker_symbol='x',
                                marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                                marker_line_width=1, marker_size=8,
                                legendgroup="Alarms",legendgrouptitle_text="Alarms",
                                hovertext=p_alm['Label']),
                        row=plot_row, col=plot_col,secondary_y=True) 

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
        ))

    logger.debug("fig done")

    return(fig)


@custom_callback # wrapper to catch errors
def custom_plot1 (dfs, dfa, dfe, cols, date1, date2, tittle): # n rows, one for each unit
    logger.debug("custom_plot1 started ---")
    
    dfs = dfs[(dfs['DateTime'] >= date1) & (dfs['DateTime'] <= date2)]
    dfa = dfa[(dfa['DateTime'] >= date1) & (dfa['DateTime'] <= date2)]
    dfe = dfe[(dfe['DateTime'] >= date1) & (dfe['DateTime'] <= date2)]

    cols2 = fcm.classify_cols(cols)

    logger.debug("fig init")
    fig = make_subplots(rows=len(cols2), cols=1, shared_xaxes=True, vertical_spacing=0.02)

    for i, (unit, cols) in enumerate(cols2.items()):
        logger.debug(f"{i=}, {unit=}, {cols=}")

        fig.update_yaxes(title_text=unit,row=i+1)

        for col in cols:
            if col == 'AlarmNumber':
                trace = go.Scatter(x=dfa['DateTime'], y=dfa['AlarmNumber'].astype(str),
                        name=col,
                        mode='markers', marker_symbol='x',
                        marker_line_color=ALcolors[2], marker_color=ALcolors[3],
                        marker_line_width=1, marker_size=8,
                        legendgroup=unit,legendgrouptitle_text=unit,
                        hovertext=dfa['Label'])
                 
            elif col == 'EventNumber':
                trace = go.Scatter(x=dfe['DateTime'], y=dfe['EventNumber'].astype(str),
                        name='Event Number',
                        mode='markers',marker_symbol='star',
                        marker_line_color=ALcolors[5], marker_color=ALcolors[5],
                        marker_line_width=1, marker_size=8,
                        legendgroup="Events",legendgrouptitle_text="Events",
                        hovertext=dfe['Label'])
            else:
                trace = go.Scatter(
                    x=dfs['DateTime'],
                    y=dfs[col],
                    name=col,
                    legendgroup=unit,legendgrouptitle_text=unit,
                )
                
            fig.add_trace(trace, row=i+1, col=1)

    # Update layout properties
    fig.update_layout(hovermode="x unified", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)', namelength = -1, font=dict(color='black')),  
        legend=dict(groupclick="toggleitem"), #avoid grouping all traces #orientation="v", x = 1.1, 
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

# NEW PLOTLY
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

def line_trace(x,y,name,color,cat):
    trace = go.Scatter(x=x, y=y,
                       name = name,
                       line=dict(color = color), line_shape='spline',
                       legendgroup=cat, legendgrouptitle_text=cat)
    return trace

def square_line_trace(x,y,name,color,cat,labels):
    trace = go.Scatter(x=x, y=y,
                       name = name,
                       line=dict(color = color), line_shape='hv',
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

def new_change_over_overlap(LogsStandard,LogsAlarms,LogsEvents,mch_info):
    mindate = LogsStandard['DateTime'].min()
    maxdate = LogsStandard['DateTime'].max()
    print(mindate,maxdate)

    if LogsAlarms is not None:
        alm = LogsAlarms[(LogsAlarms['DateTime'] > mindate) & (LogsAlarms['DateTime'] <= maxdate)]
    else:
        alm = pd.DataFrame()

    if not LogsEvents.empty:
        eve = LogsEvents[(LogsEvents['DateTime'] > mindate) & (LogsEvents['DateTime'] <= maxdate)]
    else:
        eve = pd.DataFrame()

    change_over_vars = {
        'Temperature': ['TT1','TT2','TargetTemperature','TemperatureLowLimit', 'TemperatureHighLimit'],
        'Viscosity': ['VT','TargetViscosity','ViscosityLowLimit','ViscosityHighLimit'],
        'Valves': ['CV1_Position', 'CV2_Position', 'CV3_Position', 'CV4_Position', 'CV5_Position'],
        'Bool': ['ChangeOverInProgress'],
        'Flow': ['FT_MassFlow','FT_VolumeFlow'],
        'Pressure': ['PT1','PT2'],
        'Density': ['Density']
        }

    alarm_cats = {
        'System Alarms': [0,199],
        'ChangeOver Alarms': [200,299],
        'Blending Alarms': [300,399],
        'Pressure Alarms': [400,599],
        'Filter Alarms': [500,699],
        'Mixing Tank': [800,899],
        'TempControl Alarms': [900,999],
        'ViscMeas Alarms': [1000,1099]
    }

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

    for i, (category, variables) in enumerate(change_over_vars.items()):

        if category == 'Temperature':            

            for j, variable in enumerate(variables):
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
        trace = plot_events(
                    x=eve['DateTime'],
                    y=eve['EventNumber'],
                    labels=eve['Label'])
        trace.yaxis="y8"

        fig.add_trace(trace)

    if (not alm.empty):
        for cat, limits in alarm_cats.items():
            filter_alm = alm[(alm['AlarmNumber'] >= limits[0]) & (alm['AlarmNumber'] <= limits[1])]
            if not filter_alm.empty:
                trace = plot_alarms(
                    x=filter_alm['DateTime'],
                    y=filter_alm['AlarmNumber'],
                    labels=filter_alm['Label'],
                    cat=cat)
                trace.yaxis="y9"

                fig.add_trace(trace)

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

    return (fig)

def new_change_over(LogsStandard,LogsAlarms,LogsEvents,mch_info):
    mindate = LogsStandard['DateTime'].min()
    maxdate = LogsStandard['DateTime'].max()
    print(mindate,maxdate)

    if LogsAlarms is not None:
        alm = LogsAlarms[(LogsAlarms['DateTime'] > mindate) & (LogsAlarms['DateTime'] <= maxdate)]
    else:
        alm = pd.DataFrame()

    if not LogsEvents.empty:
        eve = LogsEvents[(LogsEvents['DateTime'] > mindate) & (LogsEvents['DateTime'] <= maxdate)]
    else:
        eve = pd.DataFrame()

    change_over_vars = {
        'Temperature': ['TT1','TT2','TargetTemperature','TemperatureLowLimit', 'TemperatureHighLimit'],
        'Viscosity': ['VT','TargetViscosity','ViscosityLowLimit','ViscosityHighLimit'],
        'Valves': ['CV1_Position', 'CV2_Position', 'CV3_Position', 'CV4_Position', 'CV5_Position'],
        'Bool': ['ChangeOverInProgress'],
        'Flow': ['FT_MassFlow','FT_VolumeFlow'],
        'Pressure': ['PT1','PT2'],
        'Density': ['Density']
        }

    alarm_cats = {
        'System Alarms': [0,199],
        'ChangeOver Alarms': [200,299],
        'Blending Alarms': [300,399],
        'Pressure Alarms': [400,599],
        'Filter Alarms': [500,699],
        'Mixing Tank': [800,899],
        'TempControl Alarms': [900,999],
        'ViscMeas Alarms': [1000,1099]
    }

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
            fig.update_yaxes(title_text="Alarms", row=8)

        else:
            chart_type = 'NO_E'
            fig.update_yaxes(title_text="Events", row=8)

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

    for i, (category, variables) in enumerate(change_over_vars.items()):

        if category == 'Temperature':
            plot_row = 1

            fig.update_yaxes(title_text="Temperature",
                            row=plot_row, secondary_y=False)
            
            for j, variable in enumerate(variables):
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
            filter_alm = alm[(alm['AlarmNumber'] >= limits[0]) & (alm['AlarmNumber'] <= limits[1])]
            if not filter_alm.empty:
                trace = plot_alarms(
                    x=filter_alm['DateTime'],
                    y=filter_alm['AlarmNumber'],
                    labels=filter_alm['Label'],
                    cat=cat)
                
                if chart_type == 'AE':
                    fig.add_trace(trace, row=plot_row, col=1,secondary_y=True)
                elif chart_type == 'NO_E':
                    fig.add_trace(trace, row=plot_row, col=1)

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
    return fig

# matplotlib plots
@custom_callback # wrapper to catch errors
def create_aux_plot(LogsStandard, LogsAlarms, LogsEvents):
    logger.debug("create_aux_plot started ---")


    plt.style.use(custom_dark_style)
    #plt.style.use('default')
    #plt.style.use('dark_background')

    # Create a two-row plot
    logger.debug("fig init")
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 6), gridspec_kw={'height_ratios': [1, 5]})

    # ---------------------------------------------------------------------------- Row 1: Line plots
    axes[0].set_title('Date range of Log files')
    axes[0].plot(LogsStandard['DateTime'], [3] * len(LogsStandard), color='#FFCC00', linewidth=8, label='LogsStandard')

    axes[0].plot(LogsAlarms['DateTime'], [2] * len(LogsAlarms), color='#ec6066ff', linewidth=8, label='LogsAlarms')
    axes[0].plot(LogsEvents['DateTime'], [1] * len(LogsEvents), color='#6699ccff', linewidth=8, label='LogsEvents')

    axes[0].grid(axis='both', linestyle='--', linewidth=0.5, alpha=0.7)  # Add auxiliary x-axis grid

    #Get min and max date for each dataframe
    mindateS = LogsStandard['DateTime'].min()
    maxdateS = LogsStandard['DateTime'].max()

    mindateA = LogsAlarms['DateTime'].min()
    maxdateA = LogsAlarms['DateTime'].max()

    mindateE = LogsEvents['DateTime'].min()
    maxdateE = LogsEvents['DateTime'].max()

    # Filter datetime values to get unique dates ignoring time
    dates = [mindateS, mindateA, mindateE, maxdateS, maxdateA, maxdateE]
    ticks = list(set(dt.date() for dt in dates))
    ticks.sort()

    # Create a new list to store filtered dates
    filtered_dates = [ticks[0]]
    # Iterate through the sorted date list and delete dates near less than x days
    for i in range(1, len(ticks)):
        if (ticks[i] - filtered_dates[-1]).days >= 2:
            filtered_dates.append(ticks[i])
    # Format the unique dates as "01/01/23" strings
    xtick_labels = [date.strftime('%m/%d/%y') for date in filtered_dates]

    axes[0].set_xticks(filtered_dates)
    axes[0].set_xticklabels(xtick_labels, rotation=45)
    axes[0].set_yticks([1, 2, 3])
    axes[0].set_yticklabels(['Events Logs', 'Alarms Logs', 'Standard Logs'])

    # ----------------------------------------------------------------------------- Row 2: Multiple y-axes
    ax1 = axes[1]
    ax1.set_title('Main variables trend')
    ax1.grid(axis='both', linestyle='--', linewidth=0.5, alpha=0.7)  # Add auxiliary x-axis grid

    # Data
    x = LogsStandard['DateTime']
    # Plot Volumetric or Mass
    if not (LogsStandard['FT_VolumeFlow'] == 0).all():
        y1 = LogsStandard['FT_VolumeFlow']
    else:
        y1 = LogsStandard['FT_MassFlow']
    y2 = LogsStandard['TT2']
    y3 = LogsStandard['VT']

    #y1
    ax1.plot(x, y1, color='#6699ccff', label='FT')
    ax1.set_ylabel('Flow', color='#6699ccff')
    ax1.tick_params(axis='y', labelcolor='#6699ccff')

    #y2
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='#ec6066ff', label='TT2')
    ax2.set_ylabel('TT2', color='#ec6066ff')
    ax2.tick_params(axis='y', labelcolor='#ec6066ff')

    #y3
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 50))
    ax3.plot(x, y3, color='#FFCC00', label='VT')
    ax3.set_ylabel('Viscosity', color='#FFCC00')
    ax3.tick_params(axis='y', labelcolor='#FFCC00')

    # Set fewer ticks on the x-axis
    min_date = LogsStandard['DateTime'].min()
    max_date = LogsStandard['DateTime'].max()
    num_ticks = 10  # Choose the number of ticks you prefer
    x_ticks = pd.date_range(start=min_date, end=max_date, freq='D')
    x_ticks = x_ticks[::len(x_ticks) // num_ticks]  # Select every Nth tick

    # Set custom tick positions and labels on the x-axis
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_ticks.strftime('%m/%d/%y'), rotation=45)  # Format and rotate tick labels

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)  # Adjust vertical spacing between rows

    logger.debug("fig done")
    return fig

@custom_callback # wrapper to catch errors
def change_over_preview(df):
    logger.debug("change_over_preview started ---")

    plt.style.use(custom_dark_style)

    logger.debug("fig init")
    # Create a two-row plot
    fig, ax1 = plt.subplots()

    ax1.set_title('Change Over Preview')
    ax1.grid(axis='both', linestyle='--', linewidth=0.5, alpha=0.7)  # Add auxiliary x-axis grid

    # Data
    x = df['DateTime']
    y1 = df['TT2']
    y2 = df['VT']

    #y1
    ax1.plot(x, y1, color='#ec6066ff', label='TT2')
    ax1.set_ylabel('Temperature', color='#ec6066ff')
    ax1.tick_params(axis='y', labelcolor='#ec6066ff')

    #y2
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='#6699ccff', label='VT')
    ax2.set_ylabel('Viscosity', color='#6699ccff')
    ax2.tick_params(axis='y', labelcolor='#6699ccff')

    # Set fewer ticks on the x-axis
    min_date = df['DateTime'].min()
    max_date = df['DateTime'].max()
    # Calculate the time interval between dates
    num_dates = 5
    date_delta = (max_date - min_date) / (num_dates - 1)
    # Generate the equally spaced dates
    x_ticks = [min_date + i * date_delta for i in range(num_dates)]

    # Set custom tick positions and labels on the x-axis
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels((date.strftime('%d/%m %H:%M') for date in x_ticks), rotation=45)  # Format and rotate tick labels

    # Adjust layout
    plt.tight_layout()

    logger.debug("fig done")
    return fig

