import pandas as pd
from pyswmm import Output
from swmm.toolkit.shared_enum import NodeAttribute, LinkAttribute
import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def read_out(nodes, links):
    nodes_dataframe = {}
    for name in nodes:
        nodes_dataframe[name] = pd.DataFrame(columns=['tm', 'value'])

    links_dataframe = {}
    for name in links:
        links_dataframe[name] = pd.DataFrame(columns=['tm', 'value'])

    files = os.listdir('swmm_out')
    fig = make_subplots(rows=2, cols=1, subplot_titles=('节点液位数据', '管道利用率数据'))

    for file in files:
        with Output('swmm_out/' + file) as out:
            for node_name in nodes:
                node_out_data = out.node_series(node_name, NodeAttribute.INVERT_DEPTH)
                for node_index in node_out_data:
                    node_data = pd.DataFrame({'tm':node_index, 'value':node_out_data[node_index]}, index=[0])
                    nodes_dataframe[node_name] = nodes_dataframe[node_name]._append(node_data, ignore_index=True)
            for link_name in links:
                link_out_data = out.link_series(link_name, LinkAttribute.CAPACITY)
                for link_index in link_out_data:
                    link_data = pd.DataFrame({'tm':link_index, 'value':link_out_data[link_index]}, index=[0])
                    links_dataframe[link_name] = links_dataframe[link_name]._append(link_data, ignore_index=True)

    for node_name in nodes:
        nodes_dataframe[node_name]['tm'] = pd.to_datetime(nodes_dataframe[node_name]['tm'])
        fig.add_trace(
            go.Scatter(x=nodes_dataframe[node_name]['tm'],
                       y=nodes_dataframe[node_name]['value'],
                       mode='lines+markers',
                       name=node_name,
                       visible='legendonly'
                       ),
            row=1, col=1
        )


    for link_name in links:
        links_dataframe[link_name]['tm'] = pd.to_datetime(links_dataframe[link_name]['tm'])
        fig.add_trace(
            go.Scatter(x=links_dataframe[link_name]['tm'],
                       y=links_dataframe[link_name]['value'],
                       mode='lines+markers',
                       name=link_name,
                       visible='legendonly'
                       ),
            row=2, col=1
        )

    # 更新第一个子图的X轴和Y轴标题
    fig.update_xaxes(title_text='Time', row=1, col=1)
    fig.update_yaxes(title_text='Depth', tickformat='%Y-%m-%d %H:%M', row=1, col=1)

    # 更新第二个子图的X轴和Y轴标题
    fig.update_xaxes(title_text='Time', row=2, col=1)
    fig.update_yaxes(title_text='Capacity', tickformat='%Y-%m-%d %H:%M', row=2, col=1)

    fig.update_layout(
        showlegend=True,
        title='Time Series',
    )
    fig.show()

