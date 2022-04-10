#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
© GRID Team, 2021
"""
import pandas
import os
import json
import plotly.graph_objects as go
import plotly
import tqdm
import numpy
from agri_data import data_import
from app import SAVE_MODE, DEMO_MODE

class CaniculePlot:
    """Cette classe génère une heat map des canicules sur la base des données de Copernicus.

    Les données ont été pré-traitées et stockées dans le même répertoire.
    """
    def __init__ (self):
         self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
         self.file_name='data/full_data_heatwave.json'
         self.full_path = os.path.normcase(f'{self.current}/{self.file_name}')
         
    def read_json (self):
         self.df = pandas.read_json(self.full_path, orient='table')
         
         print(self.df)
         
    def plot_at_date (self):
        """Crée un carte pour un date données

        :return: objet json
        :rtype: json
        """
        date = pandas.to_datetime('2035-01-01')
        self.df = self.df.loc[(slice(None), slice(None), date),:]
        self.df = self.df.reset_index()
        data = go.Densitymapbox(lat=self.df['lat'], lon=self.df['lon'], 
                                         z=self.df['HWD_EU_climate'], radius=10)
    
        layout = go.Layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=4),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650
                           )
        fig=go.Figure(data=data, layout=layout)
        #fig.write_html("cannicule.html")
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json
    
    def plot_cursor (self):
        """Crée un carte pour différentes dates avec un slider temporel
        (dates définies dans la variable `list_date`)

        :return: objet json
        :rtype: json
        """
        #self.df = self.df.reset_index()
        data_slider = []
        fig = go.Figure()
        list_date = ["2021-01-01", "2031-01-01", "2041-01-01", "2051-01-01", "2061-01-01", "2081-01-01"]
        list_date = [pandas.to_datetime(k) for k in list_date]
        
        for date in tqdm.tqdm(list_date):
            temp_df = self.df.loc[(slice(None), slice(None), date),:].reset_index()
            temp_df['int_days'] = temp_df.apply(lambda x: int(x['HWD_EU_climate']), axis=1)
            temp_df['year'] = temp_df.apply(lambda x: x['time'].strftime('%Y'), axis=1)
            fig.add_trace(go.Densitymapbox(lat=temp_df['lat'], lon=temp_df['lon'], 
                                           z=temp_df['HWD_EU_climate'], radius=10,
                                           colorbar= {'title':'Nb de jours'},
                                           zmin=0, zmax=temp_df['HWD_EU_climate'].max(),
                                           customdata = temp_df[['int_days', 'year']],
                                           hovertemplate = '<b>%{customdata[0]}</b> jours<br>' + "%{customdata[1]} <extra></extra>"
                                           )
                          )
        fig.add_trace(go.Scattermapbox(lat=[43.58], lon=[4.04], marker = {'size': 30, 'color':["#0D9580"]},
                                       hovertemplate = "<b>Exploitation</b> <extra></extra>")) #Agri location
        steps = []
        for i, date in zip(range(len(fig.data)-1), list_date): #Creation of slider by looping in dates
            step = dict(method='update',
                        args=[{"visible": [False] * (len(fig.data)-1) + [True]}, #Add True at the end to show location
                              {"title": f"Carte des canicules {date.strftime('%Y')}"}],
                        label=f"Year: {date.strftime('%Y')}",
                        )
            step["args"][0]["visible"][i] = True
            steps.append(step)
            
        sliders = [dict(active=0, pad={"t": 1}, steps=steps)]  
            
    
        fig.update_layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=6),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650, sliders=sliders
                           )
        #fig=go.Figure(data=data_slider, layout=layout)
        #fig.write_html("cannicule.html") #utilisé en phase de test
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json


    def main(self):
        """Fonction lançant le tout

        :return: objet json
        :rtype: json
        """
        self.read_json()
        plot_json = self.plot_cursor()
        return plot_json


class FirePlot:
    """Cette classe génère une carte avec un scatter plot des risques incendies sur la base des données de Copernicus.

      Les données ont été pré-traitées et stockées dans le même répertoire.
    """
    def __init__ (self):
         self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
         self.file_name='data/full_data_fire.json'
         self.full_path = os.path.normcase(f'{self.current}/{self.file_name}')
         
         self.agri_data =  data_import.ReadData('data_agri').read_json()
         self.lat = self.agri_data['Lat'].iloc[-1] #Agri Lat
         self.lon = self.agri_data['Long'].iloc[-1] #Agri Lon
         
         
    def read_json (self):
         """Lecture du fichier .json et tri de l'index
         """
         self.df = pandas.read_json(self.full_path, orient='table')
         self.df = self.df.set_index(['lat','lon', 'time'])
         self.df = self.df.sort_index()
         
         print(self.df)
        
     
    def color_scale(self, zmax):
        """Cette fonction accomplit 2 choses en parallèle: création d'une echelle de couleurs pour correpondre au Fire Index européen et
        trouve les valeurs centrales de chacun des intervalles utilisés pour afficher l'echelle de couleur annotée

        :return: liste de l'echelle de couleurs normée (i.e. valeurs entre 0 et 1) et liste du centre des intervalles
        :rtype: list
        """
        colorscale=[[0.00, '#fee5d9'],
                     [5.20, '#fcbba1'],
                     [11.2, '#fc9272'],
                     [21.3, '#fb6a4a'],
                     [38.0, '#ef3b2c'],
                     [50.0, "#cb181d"],
                     [zmax, "#99000d"],
                     ]

        Delta = colorscale[-1][0] - colorscale[0][0]
        colorscheme = []
        tick_val = []
        current_val = colorscale[0][0]
        
        for k in range(len(colorscale)-1):
            #First determine the range for a color
            delta = colorscale[k+1][0] - colorscale[k][0]
            step = delta/Delta
            for a_val in numpy.linspace(current_val, current_val+step, num=10, endpoint=False):
                colorscheme.append([a_val, colorscale[k][1]])
            a_val = 0.99*(colorscale[k+1][0]/colorscale[-1][0])
            colorscheme.append([a_val, colorscale[k][1]])
            current_val = colorscale[k+1][0]/colorscale[-1][0]
            
            #Define the middle of the range
            tick_val.append(colorscale[k][0])
            tick_val.append((colorscale[k+1][0] - colorscale[k][0])/2.0+colorscale[k][0] )

            
        colorscheme.append([1.0, colorscale[k][1]]) #Append last value
        tick_val.append(int(colorscale[k+1][0])) #Append last value

        return colorscheme, tick_val
         
    def plot_at_date (self):
        """Crée un carte pour une date donnée

        :return: objet json
        :rtype: json
        """
        date = pandas.to_datetime('2097-11-01')
        self.df = self.df.loc[(slice(None), slice(None), date),:]
        self.df = self.df.reset_index()
        data = go.Densitymapbox(lat=self.df['lat'], lon=self.df['lon'], 
                                         z=self.df['fwi-mean-jjas'], radius=10)
    
        layout = go.Layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=43.58, lon=4.04),pitch=0, zoom=4),
                           paper_bgcolor='rgba(61,61,51,0.3)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650
                           )
        fig=go.Figure(data=data, layout=layout)
        #fig.write_html("fire.html") #utilisé en phase de test
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return plot_json
    
    def plot_cursor (self):
        """Crée un carte pour différentes dates avec un slider temporel
        (dates définies dans la variable `list_date`)

        :return: objet json
        :rtype: json
        """
        fig = go.Figure()
        
        list_date = ["2021-11-01", "2031-11-01", "2041-11-01", "2051-11-01", "2061-11-01", "2081-11-01"]
        list_date = [pandas.to_datetime(k) for k in list_date]
        partial_df = self.df.loc[(slice(None), slice(None), list_date),:]
        
        zmax = partial_df['fwi-mean-jjas'].max()
        colorscheme, tick_val = self.color_scale(zmax)
        
        for date in tqdm.tqdm(list_date):
            temp_df = partial_df.loc[(slice(None), slice(None), date),:].reset_index()
            temp_df['int_days'] = temp_df.apply(lambda x: round(x['fwi-mean-jjas'],2), axis=1)
            temp_df['year'] = temp_df.apply(lambda x: x['time'].strftime('%Y'), axis=1)
            
            fig.add_trace(go.Scattermapbox(lat=temp_df['lat'], lon=temp_df['lon'], 
                                           marker = dict(color=temp_df['fwi-mean-jjas'],
                                                         size=20,
                                                         colorscale = colorscheme,
                                                         colorbar= {'title':'Probabilité de feu',
                                                                    'tickvals':tick_val,
                                                                    'ticktext':[0, "<b>Très bas</b>", 5.2, "<b>Bas</b>", 11.2, "<b>Modéré</b>", 21.3, "<b>Haut</b>", 38.0, "<b>Très haut</b>", 50.0, "<b>Extrême</b>"],
                                                                    'ticks':"outside"
                                                                    },
                                                         cmin=0, cmax=zmax, opacity=1
                                                         ),
                                           customdata = temp_df[['int_days', 'year']],
                                           hovertemplate = '<b>%{customdata[0]}</b> index feu<br>' + "%{customdata[1]} <extra></extra>"
                                           )
                          )
            
        fig.add_trace(go.Scattermapbox(lat=[self.lat], 
                                       lon=[self.lon],
                                       marker = {'size': 30, 'color':["#0D9580"]},
                                       hovertemplate = "<b>Exploitation</b> <extra></extra>")) #Add point for agri
            
        steps = []
        for i, date in zip(range(len(fig.data)-1), list_date):
            step = dict(method='update',
                        args=[{"visible": [False] * (len(fig.data)-1) + [True]}, #Keep the last one true b/c agri location
                              {"title": f"Carte des canicules {date.strftime('%Y')}"}],
                        label=f"Year: {date.strftime('%Y')}",
                        )
            step["args"][0]["visible"][i] = True #Turn on the one selected by slider
            steps.append(step)
            
        sliders = [dict(active=0, pad={"t": 1}, steps=steps)]  
            
        fig.update_layout(mapbox_style="open-street-map",
                           mapbox=dict(bearing=0,center=dict(lat=self.lat, lon=self.lon),pitch=0, zoom=6),
                           paper_bgcolor='#F8FCF7', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                           height=650, sliders=sliders, showlegend=False
                           )
        
        #fig.write_html("fire.html") #utilisé en phase de test
        self.plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    def save (self):
      if SAVE_MODE:
        with open(os.path.normcase(f"{self.current}/json_files/FireMap.json"), "w") as outfile:
          outfile.write(self.plot_json)
          print(f'Saved FireMap.json')

    def open (self):
      with open(os.path.normcase(f"{self.current}/json_files/FireMap.json"), 'r') as openfile:
        self.plot_json = json.dumps(json.load(openfile))
    
    def main(self):
      """Fonction lançant le tout

      :return: objet json
      :rtype: json
      """
      if DEMO_MODE:
        self.open()

      else:
        self.read_json()
        self.plot_cursor()

      self.save()

      return self.plot_json
        
         
         
         
if __name__ == '__main__':
    canicule = FirePlot().main()
    