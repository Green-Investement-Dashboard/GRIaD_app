# -*- coding: utf-8 -*-
"""
© GRID Team, 2021
"""


import plotly.graph_objects as go
import pandas
import json
import plotly
import numpy
from plotly.subplots import make_subplots
from agri_data import data_import
import os
from app import SAVE_MODE, DEMO_MODE

class BulletChart:
    """Cette classe génère une échelle à 3 couleurs pour un indicateur donné

      :param indic: le code indicateur au format Ex, Sx ou Gx (où x est un int)
      :type indic: str
      :param indic_name: le nom de l'indicateur utilisé pour le titre
      :type addr: str
    """
    def __init__ (self, indic, indic_name):
      self.data = data_import.ReadData('graph_data').read_json()
      self.value_range = data_import.ReadData('value_range').read_json()
      self.indic = indic
      self.indic_name = indic_name
      self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))

    def plot(self):
      """Les données sont importées depuis l'__init__

      :return: objet json contenant le plot
      :rtype: json
      """
      self.value = self.data.loc[self.indic, 'list_y'][-1]
      data = go.Indicator(mode = "gauge", 
                    gauge = {'shape': "bullet",
                             'steps': [
                                 {'range': [self.value_range.loc[self.indic, 'Bin'][0], self.value_range.loc[self.indic, 'Bin'][1]], 'color': "#e5f5e0"},
                                 {'range': [self.value_range.loc[self.indic, 'Bin'][1], self.value_range.loc[self.indic, 'Bin'][2]], 'color': "#a1d99b"},
                                 {'range': [self.value_range.loc[self.indic, 'Bin'][2], self.value_range.loc[self.indic, 'Bin'][3]], 'color': "#31a354"}
                                 ],
                             'axis': {'range': [self.value_range.loc[self.indic, 'Bin'][0], self.value_range.loc[self.indic, 'Bin'][-1]]},
                             'bar': {'color': "black"}
                             },
                    #title = {'text': f'<b>{self.indic_name}</b>'},
                    value = self.value, 
                    #delta = {'reference': 300},
                    domain = {'x': [0, 1], 'y': [0, 1]}
                    )
      
      layout = go.Layout(height=250, 
                   paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                         )

      fig = go.Figure(data, layout)
      #fig.write_html("html/gauge.html")
      self.plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


      if self.value < self.value_range.loc[self.indic, 'Bin'][1]:
        self.color = 'red'
      elif self.value > self.value_range.loc[self.indic, 'Bin'][1] and self.value <= self.value_range.loc[self.indic, 'Bin'][2]:
        self.color = 'yellow'
      else:
        self.color = 'red'

    def save (self):
      if SAVE_MODE:
        with open(os.path.normcase(f"{self.current}/json_files/BulletChart_{self.indic}.json"), "w") as outfile:
          outfile.write(self.plot_json)
          print(f'Saved BulletChart_{self.indic}.json')
        with open(os.path.normcase(f"{self.current}/json_files/BulletChart_para_{self.indic}.txt"), "w") as outfile:
          outfile.writelines(self.indic_name + '\n')
          outfile.writelines(self.color + '\n')
          outfile.writelines(str(self.value) + '\n')

    def open (self):
      with open(os.path.normcase(f"{self.current}/json_files/BulletChart_{self.indic}.json"), 'r') as openfile:
        plot_json = json.load(openfile)
        self.plot_json = json.dumps(plot_json)

      with open(os.path.normcase(f"{self.current}/json_files/BulletChart_para_{self.indic}.txt"), "r") as outfile:
        list_lines = outfile.readlines()
        self.indic_name = list_lines[0]
        self.color = list_lines [1]
        self.value = list_lines [2]

    def main(self):
      if DEMO_MODE:
        self.open()
        self.color = 'red'

      else:
        self.plot()

      self.save()
      return {'graph':self.plot_json, 'title': self.indic_name, 'color':self.color, 'value':self.value}



class PieChart:
  """Cette classe génère les diagrames camembert

      :param indic: le code indicateur au format Ex, Sx ou Gx (où x est un int)
      :type indic: str
      :param indic_name: le nom de l'indicateur utiliser pour le titre
      :type addr: str
    """
  def __init__ (self, indic, indic_name):
    self.data =  data_import.ReadData('graph_data').read_json()
    self.indic = indic
    self.indic_name = indic_name
    self.colors = ['#35978f', '#66c2a4', '#c7eae5', "#dfc27d"]
    self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))

  def plot(self):
    """Les données sont importées depuis l'__init__

        :return: objet json contenant le plot
        :rtype: json
    """
    data = go.Pie(labels=self.data.loc[self.indic, 'list_x'], values=self.data.loc[self.indic, 'list_y'], marker=dict(colors=self.colors))
    layout = go.Layout(height=600,
                     paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                     
                           )
    fig = go.Figure(data, layout)
    #fig.write_html("pie_ch.html")
    self.plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  def save (self):
    if SAVE_MODE:
      with open(os.path.normcase(f"{self.current}/json_files/PieChart_{self.indic}.json"), "w") as outfile:
        outfile.write(self.plot_json)
        print(f'Saved BulletChart_{self.indic}.json')

  def open (self):
    with open(os.path.normcase(f"{self.current}/json_files/PieChart_{self.indic}.json"), 'r') as openfile:
      self.plot_json = json.dumps(json.load(openfile))

  def main(self):
    if DEMO_MODE:
      self.open()

    else:
      self.plot()

    self.save()
    return self.plot_json

class FinancialChart:
  """Cette classe génère les diagrammes pour la partie finance

    :param *args: le code indicateur au format Ex, Sx ou Gx (où x est un int)
    :type indic: str
  """
  def __init__ (self, type_graph, *args):
    self.data =  data_import.ReadData('graph_data').read_json()
    self.type = type_graph
    self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))

    if isinstance(args, str):
      self.list_indic = [args]
    else:
      self.list_indic = list(args)

    self.color = '#3D3D34'

  def plot_bar(self):
    """Les données sont importées depuis l'__init__. Génère un graphique barre

        :return: list d'objet json
        :rtype: list[json]
    """
    self.list_graph = []

    for indic in self.list_indic:
      list_x = [pandas.to_datetime(date) for date in self.data.loc[indic, 'list_x']]
      data = go.Bar(x=self.data.loc[indic, 'list_x'], y=self.data.loc[indic, 'list_y'], marker_color=self.color)
      layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title=self.data.loc[indic, 'name'], font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0),
                         )
      fig = go.Figure(data=data, layout=layout)
      plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
      self.list_graph.append(plot_json)
      #fig.write_html(f"{indic}.html")

  def plot_sgl_line (self):
    """Les données sont importées depuis l'__init__. Génère un graphique ligne

        :return: list d'objet json
        :rtype: list[json]
    """
    self.list_graph = []

    for indic in self.list_indic:
      list_x = [pandas.to_datetime(date) for date in self.data.loc[indic, 'list_x']]
      data = go.Scatter(x=self.data.loc[indic, 'list_x'], y=self.data.loc[indic, 'list_y'])
      layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title=self.data.loc[indic, 'name'], font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                         )
      fig = go.Figure(data=data, layout=layout)
      plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
      self.list_graph.append(plot_json)
      #fig.write_html(f"{indic}_sgl.html")


  def plot_mltpl_line (self):
    """Les données sont importées depuis l'__init__. Génère un graphique ligne avec 2 axes y

        :return: list d'objet json
        :rtype: list[json]
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    secondary_axes = False
    for indic in self.list_indic:
      list_x = [pandas.to_datetime(date) for date in self.data.loc[indic, 'list_x']]
      fig.add_trace(go.Scatter(x=self.data.loc[indic, 'list_x'], y=self.data.loc[indic, 'list_y'],
                               name=self.data.loc[indic, 'name']),
                    secondary_y=secondary_axes
                    
                    )
      
      fig.update_layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                         )
      fig.update_yaxes(title_text=self.data.loc[indic, 'name'], secondary_y=secondary_axes)
      secondary_axes=True

    #fig.write_html(f"{indic}_mtpl.html")  
    self.list_graph = [json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)]

  def save (self):
    if SAVE_MODE:
      if self.type in ['plot_bar', 'plot_sgl_line']:
        for graph, indic in zip(self.list_graph, self.list_indic):
          with open(os.path.normcase(f"{self.current}/json_files/FinancialChart_{self.type}_{indic}.json"), "w") as outfile:
            outfile.write(graph)
            print(f'Saved FinancialChart_{self.type}_{indic}.json')
      else:
        indic = f'{self.list_indic[0]}_{self.list_indic[1]}'
        with open(os.path.normcase(f"{self.current}/json_files/FinancialChart_{self.type}_{indic}.json"), "w") as outfile:
            outfile.write(self.list_graph[0])
            print(f'Saved {self.current}/json_files/FinancialChart_{self.type}_{indic}.json')

  def open (self):
    self.list_graph = []
    if self.type in ['plot_bar', 'plot_sgl_line']:
      for indic in self.list_indic:
        with open(os.path.normcase(f"{self.current}/json_files/FinancialChart_{self.type}_{indic}.json"), "r") as openfile:
          plot_json = json.load(openfile)
          self.list_graph.append(json.dumps(plot_json))
    else:
      indic = f'{self.list_indic[0]}_{self.list_indic[1]}'
      with open(os.path.normcase(f"{self.current}/json_files/FinancialChart_{self.type}_{indic}.json"), "r") as openfile:
          plot_json = json.load(openfile)
          self.list_graph.append(json.dumps(plot_json))


  def main(self):
    if DEMO_MODE:
      self.open()

    else: 
      if self.type == 'plot_bar':
        self.plot_bar()

      elif self.type == 'plot_sgl_line':
        self.plot_sgl_line()

      elif self.type == 'plot_mltpl_line':
        self.plot_mltpl_line()
        
    self.save()
    return self.list_graph


class CaniculePlot:
  """Cette classe génère le graphique des canicules dans la page Environnement.
  Les données sont importées directement
  """
  def __init__ (self):
    self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
    self.file_name='data/full_data_heatwave.json'
    self.full_path = os.path.normcase(f'{self.current}/{self.file_name}')
    self.df = pandas.read_json(self.full_path, orient='table')
    self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))

    self.agri_data =  data_import.ReadData('data_agri').read_json()

    self.colors = ['#3D3D34', '#72B857', '#BA475C', "#4771BA"]

  def find_closest (self):
    """Sur la base de la localisation de la PME, recherche le point de donnée le plus proche.
    Ces données deviennent les variables self.lat et self.lon
    """
    temp_df = self.df.reset_index()
    temp_df['diff_lon'] = temp_df['lon'].sub(self.agri_data['Long'].iloc[-1]).abs()
    temp_df['diff_lat'] = temp_df['lat'].sub(self.agri_data['Lat'].iloc[-1]).abs()
    temp_df['global_diff'] = temp_df.apply(lambda x: numpy.sqrt(x['diff_lat']**2 + x['diff_lon']**2), axis=1 )

    self.lat = temp_df.loc[temp_df['global_diff'].idxmin(), 'lat']
    self.lon = temp_df.loc[temp_df['global_diff'].idxmin(), 'lon']
    print(self.lat, self.lon)
    

  def plot (self):
      """Plot un graphique ligne et stocke l'object json dans self.plot_json
      """
      data_extract = self.df.loc[(self.lat, self.lon, slice(None)), ['HWD_EU_climate']].reset_index()
      
      data = go.Scatter(x=data_extract['time'], y=data_extract['HWD_EU_climate'], line=dict(color=self.colors[0]))
      layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title='Nombre de jours de canicules', font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0)
                         )
      fig = go.Figure(data=data, layout=layout)
      self.plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
      
  def save (self):
      if SAVE_MODE:
        with open(os.path.normcase(f"{self.current}/json_files/CaniculePlot.json"), "w") as outfile:
          outfile.write(self.plot_json)
          print(f'Saved Canicule Plot.json')

  def open (self):
    with open(os.path.normcase(f"{self.current}/json_files/CaniculePlot.json"), 'r') as openfile:
      self.plot_json = json.dumps(json.load(openfile))


  def main(self):
      """Fonction principale de la classe

          :return: objet json
          :rtype: json
      """
      if DEMO_MODE:
        self.open()

      else:
        self.find_closest()
        #self.lat = 43.8 
        #self.lon = 3.9
        self.plot()

      self.save()
      return self.plot_json


class RadarChart:
  """Cette classe est utilisée pour représenter le score de plusieurs """

  def __init__ (self, *args):
    self.data =  data_import.ReadData('graph_data').read_json()
    self.val_rg = data_import.ReadData('value_range').read_json()
    self.indic = args
    self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
  
  def data_prep(self):
    """Preparation data pour format circulaire"""
    self.r = []
    self.theta = []
    for indic in self.indic:
      self.r.append(self.data.loc[indic[0], 'list_x'][-1])
      self.theta.append(self.indic[1])

  def range_bin (self):
    self.val_max = self.val_rg.loc[self.list_indic, 'Max'].max()
    self.val_min = self.val_rg.loc[self.list_indic, 'Max'].min()

    self.r_bin = [[],[],[]]
    self.r_theta = [[],[],[]]
    
    for a_bin in range(len(self.r_bin[0])):
      for indic in self.indic:
        self.r.append(self.val_rg.loc[indic[0], 'list_x'][-1])
        self.theta.append(self.indic[1])

  def plot(self):
    """Actual plot"""
    data = go.Scatterpolar(r=self.r,
      theta = self.theta,
      )

    list_indic = [indic[0] for indic in self.indic]
    val_max = self.val_rg.loc[list_indic, 'Max'].max()

    layout = go.Layout(polar=dict(radialaxis=dict(visible=True, range=[0, val_max])),
      show_legend=True)

    fig = go.Figure(data=data, layout=layout)
    fig.write_html(f"html/radar.html")  
    self.plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

  def save (self):
      if SAVE_MODE:
        with open(os.path.normcase(f"{self.current}/json_files/RadarChart_{self.indic}.json"), "w") as outfile:
          outfile.write(self.plot_json)
          print(f'Saved RadarChart_{self.indic}.json')

  def open (self):
    with open(os.path.normcase(f"{self.current}/json_files/RadarChart_{self.indic}.json"), 'r') as openfile:
      self.plot_json = json.dumps(json.load(openfile))

  def main(self):
    if DEMO_MODE:
      self.open()

    else:
      self.data_prep()
      self.plot()

    self.save()
    return self.plot_json


    
if __name__ == '__main__':
  #BulletChart('S1', 'Test').plot()
  #PieChart('G6', "Diversification d'activité").plot()
  #FinancialChart('F1', 'F2').plot_bar()
  #FinancialChart('F1', 'F2').plot_sgl_line()
  #FinancialChart('F1', 'F2').plot_mltpl_line()
  
  #PlotCanicule().find_closest()
  RadarChart(('E0', 'Indic E'), ('E9', 'Indic1'), ('S1', 'Indic 2'), ('S3', 'Indic 4')).plot()


