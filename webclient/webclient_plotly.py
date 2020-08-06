from js import print_div
from RobotRaconteur.Client import *
import numpy as np
import time, traceback
from js import Plotly

periodvalue=100
x = np.linspace(0, 1, periodvalue)
y_A = np.zeros(periodvalue)
y_B = np.zeros(periodvalue)

async def client_matplotlib():

	try:
		m1k_obj=await RRN.AsyncConnectService('rr+ws://localhost:11111/?service=m1k',None,None,None,None)
		#set mode for each channel
		m1k_obj.async_setmode('A','SVMI',None)
		m1k_obj.async_setmode('B','HI_Z',None)
		#start waveform
		m1k_obj.async_wave('A', 'sine', 0, 5, periodvalue, -(periodvalue / 4), 0.5, None)

		#start streaming
		m1k_obj.async_StartStreaming(None)
		# samples_wire=await m1k_obj.samples.AsyncConnect(None)
		print_div("Running!")

		while True:
			try:
				await plot(m1k_obj)
			except RR.ValueNotSet:
				pass

	except:
		print_div(traceback.format_exc())
		m1k_obj.async_StopStreaming(None)
		raise

async def plot(m1k_obj):

	global x, y_A, y_B
	sample=await m1k_obj.samples.AsyncPeekInValue(None)
	# sample=samples_wire.InValue
	y_A=np.roll(y_A,1)
	y_A[0]=sample[0].A[0]
	y_B=np.roll(y_B,1)
	y_B[0]=sample[0].B[0]

	waveform_A={ 'y': y_A, 'x': x ,'xaxis': 'x2', 'yaxis': 'y2' ,'mode':'lines','name':'channel_A','type':'scatter','marker':{'size':10,'color':'#e31010'}}
	waveform_B={ 'y': y_B, 'x': x ,'xaxis': 'x1', 'yaxis': 'y1' ,'mode':'lines','name':'channel_B','type':'scatter','marker':{'size':10,'color':'#0000FF'}}

	layout = {
	'grid': {
    'rows': 2,
    'columns': 1,
    'pattern': 'independent',
    'roworder': 'bottom to top'
    },
  	'xaxis': {
    'autorange': True
  	},
  	'yaxis1': {
  	'range': [0, 5],
    'autorange': False
  	},
  	'yaxis2': {
  	'range': [0, 5],
    'autorange': False
  	},
  	'annotations': [
    {
    'xref': 'paper',
    'yref': 'paper',
    'x': 0,
    'xanchor': 'right',
    'y': 1,
    'yanchor': 'bottom',
    'text': 'Voltage (V)',
    'showarrow': False
    }, {
    'xref': 'paper',
    'yref': 'paper',
    'x': 1,
    'xanchor': 'left',
    'y': 0,
    'yanchor': 'top',
    'text': 'Y axis label',
    'showarrow': False}
    ]
    }
	Plotly.react('plot',[waveform_A, waveform_B],layout)


RR.WebLoop.run(client_matplotlib())