from __future__ import division
import math
# import multiprocessing
import itertools
import time
from decimal import *
from django.forms.models import model_to_dict
from core.models import Factor,Radiators,Horizontal,Vertical,Fins

class MultiIters(object):
	counter=0
	basic={}
	core={}
	tapping={}
	lv={}
	hv={}
	cca={}
	cooling={}
	tank={}
	other={}
	check={}
	costing={}
	iters={}
	
	def assign_data(self,basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,iters):
		self.basic=basic
		self.core=core
		self.tapping=tapping
		self.lv=lv
		self.hv=hv
		self.cca=cca
		self.cooling=cooling
		self.tank=tank
		self.other=other
		self.check=check
		self.costing=costing
		self.iters=iters
		self.counter=0

	def run_thread(self):
		x=Factor.objects.all()
		watt_kg_table={}
		for k in x:
			h=model_to_dict(k)
			if (h['core'] in watt_kg_table):
				if (h['flux'] in watt_kg_table[h['core']]):
					watt_kg_table[h['core']][h['flux']][h['frequency']]=h['factor']
				else:
					watt_kg_table[h['core']][h['flux']]={}
					watt_kg_table[h['core']][h['flux']][h['frequency']]=h['factor']
			else:
				watt_kg_table[h['core']]={}
				watt_kg_table[h['core']][h['flux']]={}
				watt_kg_table[h['core']][h['flux']][h['frequency']]=h['factor']

		y=Radiators.objects.all()
		radiator_table={}
		for k in y:
			h=model_to_dict(k)
			if(h['pannel'] in radiator_table):
				radiator_table[h['pannel']][h['length']]={}
				radiator_table[h['pannel']][h['length']]['sarea_sec']=h['sarea_sec']
				radiator_table[h['pannel']][h['length']]['deg35']=h['deg35']
				radiator_table[h['pannel']][h['length']]['deg40']=h['deg40']
				radiator_table[h['pannel']][h['length']]['deg45']=h['deg45']
				radiator_table[h['pannel']][h['length']]['deg50']=h['deg50']
				radiator_table[h['pannel']][h['length']]['deg55']=h['deg55']
				radiator_table[h['pannel']][h['length']]['deg60']=h['deg60']
				radiator_table[h['pannel']][h['length']]['wt_sec']=h['wt_sec']
				radiator_table[h['pannel']][h['length']]['oil_sec']=h['oil_sec']
			else:
				radiator_table[h['pannel']]={}
				radiator_table[h['pannel']][h['length']]={}
				radiator_table[h['pannel']][h['length']]['sarea_sec']=h['sarea_sec']
				radiator_table[h['pannel']][h['length']]['deg35']=h['deg35']
				radiator_table[h['pannel']][h['length']]['deg40']=h['deg40']
				radiator_table[h['pannel']][h['length']]['deg45']=h['deg45']
				radiator_table[h['pannel']][h['length']]['deg50']=h['deg50']
				radiator_table[h['pannel']][h['length']]['deg55']=h['deg55']
				radiator_table[h['pannel']][h['length']]['deg60']=h['deg60']
				radiator_table[h['pannel']][h['length']]['wt_sec']=h['wt_sec']
				radiator_table[h['pannel']][h['length']]['oil_sec']=h['oil_sec']

		z=Vertical.objects.all()
		vertical_table={}
		for k in z:
			h=model_to_dict(k)
			vertical_table[h['vertdist']]=h['factor']

		w=Fins.objects.all()
		fins_table={}
		for k in w:
			h=model_to_dict(k)
			fins_table[h['nums']]=h['factor']

		u=Horizontal.objects.all()
		horizontal_table={}
		for k in u:
			h=model_to_dict(k)
			if(h['pannel'] in horizontal_table):
				horizontal_table[h['pannel']][h['horzdist']]=h['factor']
			else:
				horizontal_table[h['pannel']]={}
				horizontal_table[h['pannel']][h['horzdist']]=h['factor']

		threads=[]
		# m=multiprocessing.Manager()
		# q=m.list()
		q=[]
		cmain=self.iters['corewidth']['min']
		while(cmain<=self.iters['corewidth']['max']):
			# t2=multiprocessing.Process(target=thread_main,args=(cmain,self.basic,self.core,self.tapping,self.lv,self.hv,self.cca,self.cooling,self.tank,self.other,self.check,self.costing,self.iters,q,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table))
			# threads.append(t2)
			# t2.start()
			thread_main(cmain,self.basic,self.core,self.tapping,self.lv,self.hv,self.cca,self.cooling,self.tank,self.other,self.check,self.costing,self.iters,q,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table)
			cmain=cmain+self.iters['corewidth']['step']
		# for thread in threads:
		# 		thread.join()
		r=list(itertools.chain.from_iterable(q))
		r1=sorted(r,key=lambda x:x['capcosting'])
		if len(r)==0:
			returning=[]
		elif len(r)<25:
			returning=r1
		else:
			returning=r1[:25]

		datas={}
		# if not any(d['main'].get('lvwmain')==self.iters['lvwidth']['min'] for d in r1):
		# 	datas.append([0,'lvwidth min'])
		# else:
		# 	datas.append([1,'lvwidth min'])
		# if not any(d['main'].get('lvwmain')==self.iters['lvwidth']['max'] for d in r1):
		# 	datas.append([0,'lv width max'])
		# else:
		# 	datas.append([1,'lvwidth max'])
		# if not any(d['main'].get('hvwmain')==self.iters['hvwidth']['min'] for d in r1):
		# 	datas.append([0,'hv width min'])
		# else:
		# 	datas.append([1,'hvwidth min'])
		# if not any(d['main'].get('hvwmain')==self.iters['hvwidth']['max'] for d in r1):
		# 	datas.append([0,'hvwidth max'])
		# else:
		# 	datas.append([1,'hvwidth max'])
		# if not any(d['main'].get('cmain')==self.iters['corewidth']['min'] for d in r1):
		# 	datas.append([0,'corewidth min'])
		# else:
		# 	datas.append([1,'corewidth min'])
		# if not any(d['main'].get('cmain')==self.iters['corewidth']['max'] for d in r1):
		# 	datas.append([0,'corewidth max'])
		# else:
		# 	datas.append([1,'corewidth max'])
		# if not any(d['main'].get('fmain')==self.iters['flux']['min'] for d in r1):
		# 	datas.append([0,'flux min'])
		# else:
		# 	datas.append([1,'flux min'])
		# if not any(d['main'].get('fmain')==self.iters['flux']['max'] for d in r1):
		# 	datas.append([0,'flux max'])
		# else:
		# 	datas.append([1,'flux max'])
		# if not any(d['main'].get('lvhmain')==self.iters['lvhvgap']['min'] for d in r1):
		# 	datas.append([0,'lvhvgap min'])
		# else:
		# 	datas.append([1,'lvhvgap min'])
		# if not any(d['main'].get('lvhmain')==self.iters['lvhvgap']['max'] for d in r1):
		# 	datas.append([0,'lvhvgap max'])
		# else:
		# 	datas.append([1,'lvhvgap max'])
		# if not any(d['main'].get('lvtmain')==self.iters['lvturns']['min'] for d in r1):
		# 	datas.append([0,'lvturns min'])
		# else:
		# 	datas.append([1,'lvturns min'])
		# if not any(d['main'].get('lvtmain')==self.iters['lvturns']['max'] for d in r1):
		# 	datas.append([0,'lvturns max'])
		# else:
		# 	datas.append([1,'lvturns max'])
		# if(self.hv['condtype']!='round'):
		# 	if not any(d['main'].get('hvkmain')==self.iters['hvthk']['min'] for d in r1):
		# 		datas.append([0,'hvthk min'])
		# 	else:
		# 		datas.append([1,'hvthk min'])
		# 	if not any(d['main'].get('hvkmain')==self.iters['hvthk']['max'] for d in r1):
		# 		datas.append([0,'hvthk max'])
		# 	else:
		# 		datas.append([1,'hvthk max'])
		# if(self.lv['condtype']!='round'):
		# 	if not any(d['main'].get('lvkmain')==self.iters['lvthk']['min'] for d in r1):
		# 		datas.append([0,'lvthk min'])
		# 	else:
		# 		datas.append([1,'lvthk min'])
		# 	if not any(d['main'].get('lvkmain')==self.iters['lvthk']['max'] for d in r1):
		# 		datas.append([0,'lvthk max'])
		# 	else:
		# 		datas.append([1,'lvthk max'])
		# print datas
		self.counter=len(r)
		print self.counter
		return [returning,datas]

def myrounder(n):
	intn=int(n)
	if(n>intn+0.49999):
		return intn+1
	else:
		return intn

def myceil(n):
	intn=int(n)
	if(n<intn+0.00001):
		return intn
	else:
		return intn+1

def myfloor(n):
	intn=int(n)
	if(n>intn+0.99999):
		return intn+1
	else:
		return intn

def thread_main(cmain,basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,iters,q,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table):
	out=[]
	if(lv['condtype']=='round'):
		if(hv['condtype']=='round'):
			fmain=iters['flux']['min']
			while(fmain<=iters['flux']['max']):
				lvtmain=iters['lvturns']['min']
				while (lvtmain<=iters['lvturns']['max']):
					lvwmain=iters['lvwidth']['min']
					while (lvwmain<=iters['lvwidth']['max']):
						lvkmain=lvwmain
						hvwmain=iters['hvwidth']['min']
						while (hvwmain<=iters['hvwidth']['max']):
							hvkmain=hvwmain
							lvhmain=iters['lvhvgap']['min']
							while (lvhmain<=iters['lvhvgap']['max']):
								lvemain=iters['lvedge']['min']
								while(lvemain<=iters['lvedge']['max']):
									test={'cmain':cmain,'fmain':fmain,'lvtmain':lvtmain,'lvwmain':round(lvwmain,2),'lvkmain':lvkmain,'hvwmain':hvwmain,'hvkmain':hvkmain,'lvhmain':lvhmain,'lvemain':lvemain}
									y=design(basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test,out,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table)
									lvemain=round(lvemain+iters['lvedge']['step'],2)
								lvhmain=round((lvhmain+iters['lvhvgap']['step']),2)
							hvwmain=round((hvwmain+iters['hvwidth']['step']),2)
						lvwmain=round((lvwmain+iters['lvwidth']['step']),2)
					lvtmain=round((lvtmain+iters['lvturns']['step']),2)
				fmain=round((fmain+iters['flux']['step']),3)
		else:
			fmain=iters['flux']['min']
			while(fmain<=iters['flux']['max']):
				lvtmain=iters['lvturns']['min']
				while (lvtmain<=iters['lvturns']['max']):
					lvwmain=iters['lvwidth']['min']
					while (lvwmain<=iters['lvwidth']['max']):
						lvkmain=lvwmain
						hvwmain=iters['hvwidth']['min']
						while (hvwmain<=iters['hvwidth']['max']):
							hvkmain=iters['hvthk']['min']
							while (hvkmain<=iters['hvthk']['max']):
								lvhmain=iters['lvhvgap']['min']
								while (lvhmain<=iters['lvhvgap']['max']):
									lvemain=iters['lvedge']['min']
									while(lvemain<=iters['lvedge']['max']):
										test={'cmain':cmain,'fmain':fmain,'lvtmain':lvtmain,'lvwmain':round(lvwmain,2),'lvkmain':lvkmain,'hvwmain':hvwmain,'hvkmain':hvkmain,'lvhmain':lvhmain,'lvemain':lvemain}
										y=design(basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test,out,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table)
										lvemain=round(lvemain+iters['lvedge']['step'],2)
									lvhmain=round((lvhmain+iters['lvhvgap']['step']),2)
								hvkmain=round((hvkmain+iters['hvthk']['step']),2)
							hvwmain=round((hvwmain+iters['hvwidth']['step']),2)
						lvwmain=round((lvwmain+iters['lvwidth']['step']),2)
					lvtmain=round((lvtmain+iters['lvturns']['step']),2)
				fmain=round((fmain+iters['flux']['step']),3)
	else:
		if(hv['condtype']=='round'):
			fmain=iters['flux']['min']
			while(fmain<=iters['flux']['max']):
				lvtmain=iters['lvturns']['min']
				while (lvtmain<=iters['lvturns']['max']):
					lvwmain=iters['lvwidth']['min']
					while (lvwmain<=iters['lvwidth']['max']):
						lvkmain=iters['lvthk']['min']
						while (lvkmain<=iters['lvthk']['max']):
							hvwmain=iters['hvwidth']['min']
							while (hvwmain<=iters['hvwidth']['max']):
								hvkmain=hvwmain
								lvhmain=iters['lvhvgap']['min']
								while (lvhmain<=iters['lvhvgap']['max']):
									lvemain=iters['lvedge']['min']
									while(lvemain<=iters['lvedge']['max']):
										test={'cmain':cmain,'fmain':fmain,'lvtmain':lvtmain,'lvwmain':round(lvwmain,2),'lvkmain':lvkmain,'hvwmain':hvwmain,'hvkmain':hvkmain,'lvhmain':lvhmain,'lvemain':lvemain}
										y=design(basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test,out,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table)
										lvemain=round(lvemain+iters['lvedge']['step'],2)
									lvhmain=round((lvhmain+iters['lvhvgap']['step']),2)
								hvwmain=round((hvwmain+iters['hvwidth']['step']),2)
							lvkmain=round((lvkmain+iters['lvthk']['step']),2)
						lvwmain=round((lvwmain+iters['lvwidth']['step']),2)
					lvtmain=round((lvtmain+iters['lvturns']['step']),2)
				fmain=round((fmain+iters['flux']['step']),3)
		else:
			fmain=iters['flux']['min']
			while(fmain<=iters['flux']['max']):
				lvtmain=iters['lvturns']['min']
				while (lvtmain<=iters['lvturns']['max']):
					lvwmain=iters['lvwidth']['min']
					while (lvwmain<=iters['lvwidth']['max']):
						lvkmain=iters['lvthk']['min']
						while (lvkmain<=iters['lvthk']['max']):
							hvwmain=iters['hvwidth']['min']
							while (hvwmain<=iters['hvwidth']['max']):
								hvkmain=iters['hvthk']['min']
								while (hvkmain<=iters['hvthk']['max']):
									lvhmain=iters['lvhvgap']['min']
									while (lvhmain<=iters['lvhvgap']['max']):
										lvemain=iters['lvedge']['min']
										while(lvemain<=iters['lvedge']['max']):
											test={'cmain':cmain,'fmain':fmain,'lvtmain':lvtmain,'lvwmain':round(lvwmain,2),'lvkmain':lvkmain,'hvwmain':hvwmain,'hvkmain':hvkmain,'lvhmain':lvhmain,'lvemain':lvemain}
											y=design(basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test,out,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table)
											lvemain=round(lvemain+iters['lvedge']['step'],2)
										lvhmain=round((lvhmain+iters['lvhvgap']['step']),2)
									hvkmain=round((hvkmain+iters['hvthk']['step']),2)
								hvwmain=round((hvwmain+iters['hvwidth']['step']),2)
							lvkmain=round((lvkmain+iters['lvthk']['step']),2)
						lvwmain=round((lvwmain+iters['lvwidth']['step']),2)
					lvtmain=round((lvtmain+iters['lvturns']['step']),2)
				fmain=round((fmain+iters['flux']['step']),3)
	q.append(out)

def ceiling(a):
	if(a-int(a)>0.5):
		return int(a)+1
	else:
		return int(a)+0.5

def design(basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test,que,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table):
	output={}
	bchanneldata={}
	bchanneldata['75x40']=7.14
	bchanneldata['100x50']=9.56
	bchanneldata['125x65']=13.1
	bchanneldata['150x75']=16.8
	bchanneldata['200x75']=22.3
	bchanneldata['250x80']=30.6
	bchanneldata['300x90']=36.3

	hstifdata={}
	hstifdata['40x40x5']=3
	hstifdata['40x40x6']=3.5
	hstifdata['50x50x6']=4.5
	hstifdata['65x65x6']=5.8
	hstifdata['65x65x8']=7.7
	hstifdata['75x75x8']=8.9
	hstifdata['80x80x8']=9.6

	consdata={}
	consdata['160']={}
	consdata['200']={}
	consdata['220']={}
	consdata['250']={}
	consdata['280']={}
	consdata['320']={}
	consdata['350']={}
	consdata['380']={}
	consdata['420']={}
	consdata['450']={}
	consdata['480']={}
	consdata['500']={}
	consdata['550']={}
	consdata['580']={}
	consdata['600']={}

	consdata['160']['front']=2.13
	consdata['160']['curb']=1.5
	consdata['160']['side']=0.63
	consdata['200']['front']=2.57
	consdata['200']['curb']=1.58
	consdata['200']['side']=0.99
	consdata['220']['front']=2.94
	consdata['220']['curb']=1.75
	consdata['220']['side']=1.19
	consdata['250']['front']=3.55
	consdata['250']['curb']=2.01
	consdata['250']['side']=1.54
	consdata['280']['front']=4.21
	consdata['280']['curb']=2.93
	consdata['280']['side']=2.42
	consdata['320']['front']=5.2
	consdata['320']['curb']=3.44
	consdata['320']['side']=3.16
	consdata['350']['front']=6.27
	consdata['350']['curb']=4.17
	consdata['350']['side']=3.78
	consdata['380']['front']=7.17
	consdata['380']['curb']=4.64
	consdata['380']['side']=4.45
	consdata['420']['front']=8.43
	consdata['420']['curb']=5.21
	consdata['420']['side']=5.44
	consdata['450']['front']=9.43
	consdata['450']['curb']=5.68
	consdata['450']['side']=6.24
	consdata['480']['front']=10.49
	consdata['480']['curb']=6.15
	consdata['480']['side']=7.10
	consdata['500']['front']=11.23
	consdata['500']['curb']=6.47
	consdata['500']['side']=7.71
	consdata['550']['front']=13.18
	consdata['550']['curb']=7.3
	consdata['550']['side']=9.33
	consdata['580']['front']=18.31
	consdata['580']['curb']=7.94
	consdata['580']['side']=10.37
	consdata['600']['front']=19.4
	consdata['600']['curb']=8.3
	consdata['600']['side']=11.1

	corechart=[[],[0.7071],[0.8506,0.5257],[0.9056,0.7071,0.424],[0.9332,0.7949,0.6062,0.3589],[0.9495,0.8458,0.7071,0.5336,0.3138],[0.9559,0.878,0.7699,0.6378,0.4784,0.2802],[0.9671,0.9003,0.8127,0.7071,0.5826,0.4353,0.2543],[0.9723,0.9163,0.8432,0.756,0.6564,0.5375,0.4005,0.2335],[0.9763,0.9283,0.8661,0.7922,0.7071,0.6103,0.4998,0.3717,0.2164],[0.9792,0.9373,0.8832,0.8193,0.7463,0.664,0.5716,0.4672,0.3469,0.2017],[0.9818,0.9451,0.8977,0.8419,0.7784,0.7073,0.6282,0.5401,0.441,0.3272,0.1901],[0.9838,0.9512,0.9092,0.8598,0.8038,0.7414,0.6724,0.5963,0.512,0.4176,0.3096,0.1798],[0.9853,0.9558,0.918,0.8737,0.8237,0.7682,0.7071,0.6403,0.5671,0.4864,0.3964,0.2936,0.1704],[0.9866,0.9597,0.9253,0.8851,0.8399,0.79,0.7354,0.676,0.6114,0.5409,0.4635,0.3774,0.2793,0.162],[0.9878,0.9634,0.9322,0.8958,0.8549,0.8097,0.7604,0.707,0.6492,0.5866,0.5186,0.4441,0.3614,0.2674,0.155],[0.9888,0.9662,0.9374,0.9036,0.8656,0.8237,0.778,0.7285,0.685,0.6282,0.567,0.5,0.4283,0.3482,0.272,0.1492],[0.9897,0.9689,0.9422,0.911,0.8759,0.8372,0.7951,0.7496,0.7026,0.6618,0.6064,0.5468,0.4824,0.4124,0.335,0.2474,0.1431],[0.9904,0.9711,0.9464,0.9176,0.8853,0.8498,0.8112,0.7696,0.7249,0.6888,0.6385,0.5847,0.5271,0.465,0.3975,0.3229,0.2306,0.1382],[0.991,0.9729,0.9497,0.9226,0.8922,0.8588,0.8226,0.7836,0.7418,0.702,0.6706,0.6212,0.5686,0.5123,0.4516,0.3857,0.3131,0.2312,0.1334],[0.9915,0.9794,0.9525,0.927,0.8984,0.867,0.833,0.7964,0.7572,0.7154,0.6987,0.6531,0.6047,0.5532,0.4972,0.4391,0.375,0.3045,0.2248,0.1301],[0.9919,0.9756,0.9547,0.9303,0.9030,0.8731,0.8407,0.8059,0.7687,0.7291,0.7015,0.6844,0.6396,0.5920,0.5415,0.4875,0.4296,0.3667,0.2975,0.2195,0.127]]

	if(basic['altitude']>1000):
		d1=basic['altitude']-1000
		d2=myceil(d1/200)
		moilrise=other['oilrise']-(d2*0.5)
		mwindrise=other['windrise']-(d2*0.5)
	else:
		moilrise=other['oilrise']
		mwindrise=other['windrise']

	if(core['subtype']=='CRGO'):
		core_type_ef=0.97
		loop_wt_ef=7.571134
		displacement_ef=7.65
		bot_core_clamp_kf=1
	else:
		if((test['cmain']*10)%1422==0 or (test['cmain']*10)%1702==0):
			core_type_ef=0.86
		else:
			core_type_ef=0.85
		loop_wt_ef=7.18
		displacement_ef=7.18
		bot_core_clamp_kf=1.3

	if(lv['material']=='copper'):
		lv_mat_ef=2.1
		lv_wt_ef=8.9
	else:
		lv_mat_ef=3.46
		lv_wt_ef=2.7

	if(hv['material']=='copper'):
		hv_mat_ef=2.1
		hv_wt_ef=8.9
	else:
		hv_mat_ef=3.46
		hv_wt_ef=2.7

	if(basic['phases']=='3'):
		wt_pf=3
	else:
		wt_pf=1

	if(hv['coveringmat']=='enamel'):
		hv_cover_ef=3
		covered_wt_hv_ef1=1.2
	else:
		hv_cover_ef=4
		covered_wt_hv_ef1=0.9

	if(lv['coveringmat']=='enamel'):
		lv_cover_ef=3
		covered_wt_lv_ef1=1.2
	else:
		lv_cover_ef=4
		covered_wt_lv_ef1=0.9

	if(lv['condtype']=='foil'):
		lv['nolayers']=test['lvtmain']
		lv['transpos']=0
		lv['coveringthk']=0

	if(hv['condtype']=='foil'):
		hv['transpos']=0
		hv['coveringthk']=0
	elif(hv['condtype']=='round'):
		hv['transpos']=0
	elif(hv['radials']==1):
		hv['transpos']=0

	if(hv['connectiontype']=='Star' or hv['connectiontype']=='Zigzag'):
		hvphvolt=myrounder(basic['hvvoltage']/math.sqrt(3))
	elif(hv['connectiontype']=='Delta'):
		hvphvolt=myrounder(basic['hvvoltage'])
	elif(hv['connectiontype']=='Parallel' or hv['connectiontype']=='Series'):
		hvphvolt=myrounder(basic['hvvoltage'])

	if(lv['connectiontype']=='Star' or lv['connectiontype']=='Zigzag'):
		lvphvolt=myrounder(basic['lvvoltage']/math.sqrt(3))
	elif(lv['connectiontype']=='Delta'):
		lvphvolt=myrounder(basic['lvvoltage'])
	elif(lv['connectiontype']=='Parallel' or lv['connectiontype']=='Series'):
		lvphvolt=myrounder(basic['lvvoltage'])

	#line_hv
	if(hv['connectiontype']=='Series' or hv['connectiontype']=='Parallel'):
		line_hv=myrounder(((basic['rating']*1000)/(basic['hvvoltage']))*10000)/10000
	else:
		line_hv=myrounder(((basic['rating']*1000)/(math.sqrt(3)*basic['hvvoltage']))*10000)/10000

	#line_lv
	if(lv['connectiontype']=='Series' or lv['connectiontype']=='Parallel'):
		line_lv=myrounder(((basic['rating']*1000)/(basic['lvvoltage']))*10000)/10000
	else:
		line_lv=myrounder(((basic['rating']*1000)/(math.sqrt(3)*basic['lvvoltage']))*10000)/10000

	#get_hv_coils
	get_hv_coils=myfloor(hv['mcoils']+hv['tcoils'])

	#get_turn_layer
	get_turn_layer=myrounder((test['lvtmain']/lv['nolayers'])*10)/10

	#get_rated_hvturns
	get_rated_hvturns=myrounder(test['lvtmain']*hvphvolt/lvphvolt)

	maxhvt=0
	minhvt=0
	minhvol=0
	if(tapping['yn']=='yes'):
		tapper=tapping['min']
		while(tapper<=tapping['max']):
			hvphn=myrounder(hvphvolt*(1+tapper/100))
			nhvturns=myrounder(test['lvtmain']*hvphn/lvphvolt)
			if(maxhvt==0 or nhvturns>maxhvt):
				maxhvt=nhvturns
			if(minhvt==0 or nhvturns<minhvt):
				minhvt=nhvturns
			if(minhvol==0 or hvphn<minhvol):
				minhvol=hvphn
			tapper=tapper+tapping['step']



	#get_hvturns
	if(tapping['yn']=='yes'):
		get_hvturns=maxhvt
	else:
		get_hvturns=get_rated_hvturns

	#get_minhvturns
	if(tapping['yn']=='yes'):
		get_minhvturns=minhvt
	else:
		get_minhvturns=get_rated_hvturns

	#get_volt_turn
	if(lv['connectiontype']=='Delta' or lv['connectiontype']=='delta_delta' or lv['connectiontype']=='Series' or lv['connectiontype']=='Parallel'):
		get_volt_turn=myrounder((basic['lvvoltage']/test['lvtmain'])*1000)/1000
	else:
		get_volt_turn=myrounder((basic['lvvoltage']/(math.sqrt(3)*test['lvtmain']))*1000)/1000

	if(core['coretype']=='stacked' and core['num']=='Multi'):
		get_core_area=myrounder((get_volt_turn*1000000)/(4.44*basic['frequency']*test['fmain']))/100
		coredia=myrounder(10*10*math.sqrt((get_core_area*4)/(math.pi*(core['uarea'])*0.97)))/10
		coredats=[]
		twidth=0
		tarea=0
		for i in range(0,int(core['steps'])):
			sw=myrounder((corechart[core['steps']][i])*coredia/5)*5
			if(i==0):
				st=myrounder((myfloor(math.sqrt((coredia*coredia)-(sw*sw))/(core['platethk']*core['lamsperset']))*(core['platethk']*core['lamsperset']))*100)/100
				twidth=twidth+st
				sa=myrounder(sw*st*0.97*100)/10000
				tarea=tarea+sa
				coredats.append([sw,st,st,sa])
			else:
				st=math.sqrt((coredia*coredia)-(sw*sw))
				st1=myrounder((myfloor(((st-coredats[i-1][2])/2)/(core['platethk']*core['lamsperset']))*(core['platethk']*core['lamsperset']))*100)/100
				st=(st1*2)+(coredats[i-1][2])
				sa=myrounder(sw*st1*2*0.97*100)/10000
				twidth=twidth+(st1*2)
				tarea=tarea+sa
				coredats.append([sw,st1,st,sa])
		coredat=coredats
		twidth=myrounder(twidth*100)/100
		get_core_area=myrounder(tarea*10000)/10000
		act_flx_d=myrounder(((get_volt_turn*10000)/(4.44*basic['frequency']*get_core_area))*1000)/1000
		if(act_flx_d>check['maxfd']):
			print 'act_flx_d'
			return 0
		if(core['grade']=='AMTSA1' or core['grade']=='AMTHB1'):
			cgef='AMDT'
		else:
			cgef=core['grade']
		watt_kgfl1=myfloor((act_flx_d)*100)/100
		watt_kgfl2=myceil((act_flx_d)*100)/100
		watt_kg1=watt_kg_table[cgef][str(watt_kgfl1)][str(basic['frequency'])]
		watt_kg2=watt_kg_table[cgef][str(watt_kgfl2)][str(basic['frequency'])]
		if(watt_kg1==watt_kg2):
			watt_kg=myrounder(float(watt_kg1)*10000)/10000
		else:
			watt_kg=myrounder(((float(watt_kg1))+((float(watt_kg2)-float(watt_kg1))/(watt_kgfl2-watt_kgfl1))*((act_flx_d)-watt_kgfl1))*10000)/10000
	else:
		#get_stack_thk
		sthk=(get_volt_turn*1000000)/(4.44*basic['frequency']*test['fmain']*core_type_ef*test['cmain'])
		if(core['coretype']=='stacked'):
			get_stack_thk=myrounder(((myceil(sthk/(core['platethk']*core['lamsperset'])))*core['platethk']*core['lamsperset'])*100)/100
		else:
			sthkout=myceil(sthk/core['platethk'])
			bytwo=sthkout%2
			if(bytwo!=0):
				sthkout=sthkout-1
			get_stack_thk=myrounder((sthkout*core['platethk'])*100)/100
		act_flx_d=myrounder(((get_volt_turn*1000000)/(4.44*basic['frequency']*get_stack_thk*core_type_ef*test['cmain']))*1000)/1000
		if(act_flx_d>check['maxfd']):
			print 'act_flx_d'
			return 0
		coreratio=test['cmain']/get_stack_thk
		if(coreratio>check['maxlegdia'] or coreratio<check['minlegdia']):
			print 'coreratio'
			return 0
		#get_core_area
		get_core_area=myrounder((test['cmain']*get_stack_thk*core_type_ef*0.01)*1000)/1000
		if(get_core_area>check['maxcorearea'] or get_core_area<check['mincorearea']):
			print 'get_core_area'
			return 0

		#watt_kg
		if(core['grade']=='AMTSA1' or core['grade']=='AMTHB1'):
			cgef='AMDT'
		else:
			cgef=core['grade']
		watt_kg_fl1=myfloor(act_flx_d*100)/100
		watt_kg_fl2=myceil(act_flx_d*100)/100
		watt_kg1=watt_kg_table[cgef][str(watt_kg_fl1)][str(basic['frequency'])]
		watt_kg2=watt_kg_table[cgef][str(watt_kg_fl2)][str(basic['frequency'])]
		if(watt_kg1==watt_kg2):
			watt_kg=myrounder(float(watt_kg1)*10000)/10000
		else:
			watt_kg=myrounder((float(watt_kg1)+((float(watt_kg2)-float(watt_kg1))/(watt_kg_fl2-watt_kg_fl1))*(act_flx_d-watt_kg_fl1))*10000)/10000

	#lv_cond_area
	if(lv['condtype']=='round'):
		lv_cond_area=myrounder((math.pi*test['lvwmain']*test['lvwmain']/4)*1000)/1000
	elif(lv['condtype']=='foil'):
		lv_cond_area=myrounder((test['lvwmain']*test['lvkmain']*lv['radials'])*1000)/1000
	else:
		if(test['lvkmain']>2.99):
			lv_cond_area_ef=0.9
		else:
			lv_cond_area_ef=0.5
		lv_cond_area=myrounder((((test['lvwmain']*test['lvkmain'])-lv_cond_area_ef)*lv['flats']*lv['radials'])*1000)/1000
	if(lv_cond_area>check['maxcondlv'] or lv_cond_area<check['mincondlv']):
		print 'lv_cond_area'
		return 0

	#hv_cond_area
	if(hv['condtype']=='round'):
		hv_cond_area=myrounder((math.pi*test['hvwmain']*test['hvwmain']/4)*1000)/1000
	elif(hv['condtype']=='foil'):
		hv_cond_area=myrounder((test['hvwmain']*test['hvkmain']*hv['radials'])*1000)/1000
	else:
		if(test['hvkmain']>2.99):
			hv_cond_area_ef=0.9
		else:
			hv_cond_area_ef=0.5
		hv_cond_area=myrounder((((test['hvwmain']*test['hvkmain'])-hv_cond_area_ef)*hv['flats']*hv['radials'])*1000)/1000
	if(hv_cond_area>check['maxcondhv'] or hv_cond_area<check['mincondhv']):
		print 'hv_cond_area'
		return 0

	#phase_lv
	if(lv['connectiontype']=='Star' or lv['connectiontype']=='Zigzag'):
		phase_lv=myrounder(((basic['rating']*1000)/(math.sqrt(3)*basic['lvvoltage']))*10000)/10000
	elif(lv['connectiontype']=='Delta'):
		phase_lv=myrounder(((basic['rating']*1000)/(3*basic['lvvoltage']))*10000)/10000
	elif(lv['connectiontype']=='Series' or lv['connectiontype']=='Parallel'):
		phase_lv=myrounder(((basic['rating']*1000)/(basic['lvvoltage']))*10000)/10000

	#phase_hv
	if(hv['connectiontype']=='Star' or hv['connectiontype']=='Zigzag'):
		phase_hv=myrounder(((basic['rating']*1000)/(math.sqrt(3)*basic['hvvoltage']))*10000)/10000
	elif(hv['connectiontype']=='Delta'):
		phase_hv=myrounder(((basic['rating']*1000)/(3*basic['hvvoltage']))*10000)/10000
	elif(hv['connectiontype']=='Series' or hv['connectiontype']=='Parallel'):
		phase_hv=myrounder(((basic['rating']*1000)/(basic['hvvoltage']))*10000)/10000

	#lv_cd
	lv_cd=myrounder((phase_lv/lv_cond_area)*10000)/10000
	if(lv_cd<check['mincdlv'] or lv_cd>check['maxcdlv']):
		print 'lv_cd'
		return 0

	#hv_cd
	hv_cd=myrounder((phase_hv/hv_cond_area)*10000)/10000
	if(hv_cd<check['mincdhv'] or hv_cd>check['maxcdhv']):
		print 'hv_cd'
		return 0

	#lv_axial_elect
	lv_axial_elect=myrounder(((test['lvwmain']+lv['coveringthk'])*((test['lvtmain']/lv['nolayers']*lv['flats'])+lv['transpos']))*100)/100

	#lv_axial_phy
	if(lv['condtype']=='foil'):
		lvphyef=0
	else:
		lvphyef=1
	lv_axial_phy=myceil((test['lvwmain']+lv['coveringthk'])*((((test['lvtmain']/lv['nolayers'])+lvphyef)*lv['flats'])+lv['transpos']))

	#ccalvedge
	if(check['matchht']=='yes'):
		#get_hv_turn_layer
		if(hv['condtype']=='foil'):
			get_hv_turn_layer=1
			hvphyef=0
			hv_axial_elect=myrounder(((test['hvwmain']+hv['coveringthk'])*(get_hv_turn_layer*hv['flats']+hv['transpos']))*100)/100
		else:
			hvphyef=1
			if(hv['windtype']=='crossover'):
				if(tapping['yn']=='yes'):
					get_hv_turn_layer=myfloor(((lv_axial_elect-(hv['transpos']*((test['hvwmain'])+(hv['coveringthk'])))-(((hv['mcoils']))*hv['minsu'])-(((hv['tcoils'])-1)*hv['tinsu']))/((((test['hvwmain'])+(hv['coveringthk']))*hv['flats'])*(hv['mcoils']+hv['tcoils'])))-1)
					hv_axial_elect=myrounder(((((hv['mcoils'])+(hv['tcoils']))*(((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos']))))+((((hv['mcoils']))*hv['minsu'])+(((hv['tcoils'])-1)*hv['tinsu'])))*100)/100
					hv_single_coil_ht=myrounder((((((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos'])))))*100)/100
				else:
					get_hv_turn_layer=myfloor(((lv_axial_elect-(hv['transpos']*((test['hvwmain'])+(hv['coveringthk'])))-(((hv['mcoils'])-1)*hv['minsu']))/(((test['hvwmain'])+(hv['coveringthk']))*hv['flats']*hv['mcoils']))-1)
					hv_axial_elect=myrounder(((((hv['mcoils']))*(((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos']))))+((((hv['mcoils'])-1)*hv['minsu'])))*100)/100
					hv_single_coil_ht=myrounder((((((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos'])))))*100)/100
			else:
				get_hv_turn_layer=myfloor((lv_axial_elect-(hv['transpos']*(test['hvwmain']+hv['coveringthk'])))/((test['hvwmain']+hv['coveringthk'])*hv['flats']))
				hv_axial_elect=myrounder(((test['hvwmain']+hv['coveringthk'])*(get_hv_turn_layer*hv['flats']+hv['transpos']))*100)/100
		#hv_axial_phy
		hv_axial_phy=myceil(hv_axial_elect+(hvphyef*(((test['hvwmain'])+(hv['coveringthk']))*hv['flats'])))
		#hv_axial_pack
		hv_axial_pack=hv_axial_phy+(cca['hvedge']*2)
		#hv_axial_elect
		ccalvedge=(hv_axial_pack-lv_axial_phy)/2
		#lv_axial_pack
		if(ccalvedge<test['lvemain']):
			ccalvedge=test['lvemain']
			lv_axial_pack=lv_axial_phy+(ccalvedge*2)
			ccahvedge=(lv_axial_pack-hv_axial_phy)/2
			hv_axial_pack=hv_axial_phy+((ccahvedge)*2)
		else:
			ccahvedge=cca['hvedge']
			lv_axial_pack=lv_axial_phy+(ccalvedge*2)
	else:
		ccalvedge=test['lvemain']
		ccahvedge=cca['hvedge']
		#lv_axial_pack
		lv_axial_pack=lv_axial_phy+(ccalvedge*2)
		#get_hv_turn_layer
		if(hv['condtype']=='foil'):
			get_hv_turn_layer=1
			hvphyef=0
			#hv_axial_elect
			hv_axial_elect=myrounder(((test['hvwmain']+hv['coveringthk'])*(get_hv_turn_layer*hv['flats']+hv['transpos']))*100)/100
		else:
			hvphyef=1
			if(hv['windtype']=='crossover'):
				if(tapping['yn']=='yes'):
					get_hv_turn_layer=myfloor(((lv_axial_pack-((ccahvedge)*2)-(hv['transpos']*((test['hvwmain'])+(hv['coveringthk'])))-(((hv['mcoils']))*hv['minsu'])-(((hv['tcoils'])-1)*hv['tinsu']))/((((test['hvwmain'])+(hv['coveringthk']))*hv['flats'])*(hv['mcoils']+hv['tcoils'])))-1)
					hv_axial_elect=myrounder(((((hv['mcoils'])+(hv['tcoils']))*(((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos']))))+((((hv['mcoils']))*hv['minsu'])+(((hv['tcoils'])-1)*hv['tinsu'])))*100)/100
					hv_single_coil_ht=myrounder((((((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos'])))))*100)/100
				else:
					get_hv_turn_layer=myfloor(((lv_axial_pack-((ccahvedge)*2)-(hv['transpos']*((test['hvwmain'])+(hv['coveringthk'])))-(((hv['mcoils'])-1)*hv['minsu']))/(((test['hvwmain'])+(hv['coveringthk']))*hv['flats']*hv['mcoils']))-1)
					hv_axial_elect=myrounder(((((hv['mcoils']))*(((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos']))))+((((hv['mcoils'])-1)*hv['minsu'])))*100)/100
					hv_single_coil_ht=myrounder((((((test['hvwmain'])+(hv['coveringthk']))*((get_hv_turn_layer+1)*(hv['flats'])+(hv['transpos'])))))*100)/100
			else:
				get_hv_turn_layer=myfloor(((lv_axial_pack-(ccahvedge*2)-(hv['transpos']*(test['hvwmain']+hv['coveringthk'])))/((test['hvwmain']+hv['coveringthk'])*hv['flats']))-1)
				#hv_axial_elect
				hv_axial_elect=myrounder(((test['hvwmain']+hv['coveringthk'])*(get_hv_turn_layer*hv['flats']+hv['transpos']))*100)/100
		#hv_axial_phy
		hv_axial_phy=myceil(hv_axial_elect+(hvphyef*(((test['hvwmain'])+(hv['coveringthk']))*hv['flats'])))
		#hv_axial_pack
		hv_axial_pack=hv_axial_phy+(ccahvedge*2)
		

	#hvdaihen
	if(hv['condtype']=='round' and hv['connectiontype']=='Delta'):
		hvdaihen=((other['hvimpulse']*4.5*get_hv_turn_layer/get_minhvturns)-(7*math.sqrt(test['hvwmain'])))/50
	elif(hv['condtype']=='round' and (hv['connectiontype']=='Star'or hv['connectiontype']=='Zigzag')):
		hvdaihen=((other['hvimpulse']*3.15*get_hv_turn_layer/get_minhvturns)-(7*math.sqrt(test['hvwmain'])))/50
	elif(hv['condtype']=='rectangular' and hv['connectiontype']=='Delta'):
		hvdaihen=((other['hvimpulse']*4.5*get_hv_turn_layer/get_minhvturns))/50-(hv['coveringthk'])
	elif(hv['condtype']=='rectangular' and (hv['connectiontype']=='Star'or hv['connectiontype']=='Zigzag')):
		hvdaihen=((other['hvimpulse']*3.15*get_hv_turn_layer/get_minhvturns))/50-(hv['coveringthk'])

	#hvssel
	if(hv['coveringmat']=='dpc' and (hv['condtype']=='round' or hv['condtype']=='rectangular')):
		hvssel=(4*get_volt_turn*get_hv_turn_layer/6000)-hv['coveringthk']
	elif(hv['coveringmat']=='enamel' and hv['condtype']=='round'):
		if(hv['material']=='copper'):
			hvssel=(((4*get_volt_turn*get_hv_turn_layer)-1000)/6000)
		else:
			hvssel=(((4*get_volt_turn*get_hv_turn_layer)-500)/6000)
	elif(hv['coveringmat']=='enamel' and hv['condtype']=='rectangular'):
		hvssel=(((4*get_volt_turn*get_hv_turn_layer)-500)/6000)

	#lvdaihen
	if(lv['condtype']=='round' and lv['connectiontype']=='Delta'):
		lvdaihen=((other['lvimpulse']*4.5*get_turn_layer/test['lvtmain'])-(7*math.sqrt(test['lvwmain'])))/50
	elif(lv['condtype']=='round' and (lv['connectiontype']=='Star' or lv['connectiontype']=='Zigzag')):
		lvdaihen=((other['lvimpulse']*3.15*get_turn_layer/test['lvtmain'])-(7*math.sqrt(test['lvwmain'])))/50
	elif(lv['condtype']=='rectangular' and lv['connectiontype']=='Delta'):
		lvdaihen=((other['lvimpulse']*4.5*get_turn_layer/test['lvtmain']))/50-(lv['coveringthk'])
	elif(lv['condtype']=='rectangular' and (lv['connectiontype']=='Star' or lv['connectiontype']=='Zigzag')):
		lvdaihen=((other['lvimpulse']*3.15*get_turn_layer/test['lvtmain']))/50-(lv['coveringthk'])

	#lvssel
	if(lv['coveringmat']=='dpc' and (lv['condtype']=='round' or lv['condtype']=='rectangular')):
		lvssel=(4*get_volt_turn*get_turn_layer/6000)-lv['coveringthk']
	elif(lv['coveringmat']=='enamel' and lv['condtype']=='round'):
		if(lv['material']=='copper'):
			lvssel=(((4*get_volt_turn*get_turn_layer)-1000)/6000)
		else:
			lvssel=(((4*get_volt_turn*get_turn_layer)-500)/6000)
	elif(lv['coveringmat']=='enamel' and lv['condtype']=='rectangular'):
		lvssel=(((4*get_volt_turn*get_turn_layer)-500)/6000)

	#get_lv_insu
	if(lv['insulshow']==True):
		get_lv_insu=lv['layerinsu']
	else:
		if(other['lvimpulse']<95):
			get_lv_insu_out=lvdaihen if (lvdaihen<lvssel) else lvssel
		else:
			get_lv_insu_out=lvdaihen
		if(get_lv_insu_out<0.15):
			get_lv_insu=0.15
		else:
			get_lv_insu=myrounder(myceil(get_lv_insu_out/0.025)*0.025*1000)/1000

	#get_hv_insu
	if(hv['condtype']=='foil'):
		get_hv_insu=hv['layerinsu']
	else:
		if(other['hvimpulse']<=95):
			get_hv_insu_out=hvdaihen if (hvdaihen<hvssel) else hvssel
		else:
			get_hv_insu_out=hvdaihen
		if(get_hv_insu_out<0.15):
			get_hv_insu=0.15
		else:
			get_hv_insu=myrounder(myceil(get_hv_insu_out/0.025)*0.025*1000)/1000

	#get_hv_nolayers
	if(hv['condtype']=='foil'):
		get_hv_nolayers=get_hvturns
	else:
		get_hv_nolayers_out=(get_hvturns/get_hv_coils)/get_hv_turn_layer
		get_hv_nolayers_c=myceil(get_hv_nolayers_out)
		get_hv_nolayers_b=((get_hv_nolayers_c*get_hv_turn_layer)-(get_hvturns/get_hv_coils))/get_hv_nolayers_c
		if(hv['condtype']=='round'):
			if(test['hvwmain']<=1):
				if(get_hv_nolayers_b<4):
					get_hv_nolayers=get_hv_nolayers_c+1
				else:
					get_hv_nolayers=get_hv_nolayers_c
			elif(test['hvwmain']<=1.5):
				if(get_hv_nolayers_b<3):
					get_hv_nolayers=get_hv_nolayers_c+1
				else:
					get_hv_nolayers=get_hv_nolayers_c
			elif(test['hvwmain']<=2):
				if(get_hv_nolayers_b<2):
					get_hv_nolayers=get_hv_nolayers_c+1
				else:
					get_hv_nolayers=get_hv_nolayers_c
			else:
				if(get_hv_nolayers_b<1):
					get_hv_nolayers=get_hv_nolayers_c+1
				else:
					get_hv_nolayers=get_hv_nolayers_c
		else:
			get_hv_nolayers=get_hv_nolayers_c

	#rdlv
	if(lv['condtype']=='foil'):
		lvintturnthk=lv['nolayers']*lv['turninsu']
	else:
		lvintturnthk=0
	rdlv=((test['lvkmain']+lv['coveringthk'])*lv['radials']*lv['nolayers'])+(get_lv_insu*(lv['nolayers']-1))+(lv['fullthk']*lv['nofull'])+lvintturnthk

	#rdhv
	if(hv['condtype']=='foil'):
		hvintturnthk=get_hv_nolayers*hv['turninsu']
	else:
		hvintturnthk=0
	rdhv=((test['hvkmain']+hv['coveringthk'])*hv['radials']*get_hv_nolayers)+(get_hv_insu*(get_hv_nolayers-1-hv['nofull']))+((hv['fullthk']+0.25)*hv['nofull'])+hvintturnthk+0.5
	
	#lv_rd
	lv_rd=myceil(rdlv*2)/2
	hv_rd=myceil(rdhv*2)/2

	if(core['coretype']=='stacked' and core['num']=='Multi'):
		if(basic['corelvhv']=='lvstart'):
			lv_id=myceil(((coredia)+(((cca['corelvgap']))*2))*2)/2
			lv_od=lv_id+(lv_rd*2)
			lv_mean_dia=lv_id+lv_rd
			lv_lmt=myrounder(math.pi*lv_mean_dia*1000)/1000
			lvhv_mean_dia=lv_od+(test['lvhmain'])
			get_lv_hv_mlt=myrounder(math.pi*lvhv_mean_dia*1000)/1000
			hv_id=lv_od+(test['lvhmain'])*2
			hv_od=hv_id+hv_rd*2
			hv_mean_dia=hv_id+hv_rd
			hv_lmt=myrounder(math.pi*hv_mean_dia*1000)/1000
			lv_fnb_perimeter=0
			hv_fnb_perimeter=0
			lv_id_perimeter=myrounder(math.pi*lv_id*1000)/1000
			hv_id_perimeter=math.pi*hv_id
			hv_od_perimeter=myrounder(math.pi*hv_od*1000)/1000
			lv_od_perimeter=math.pi*lv_od
			lv_no_full_duct_runners_inside=lv_id_perimeter/30
			lv_no_full_duct_runners_outside=get_lv_hv_mlt/30
			hv_no_full_duct_runners_inside=hv_id_perimeter/30
			hv_no_full_duct_runners_outside=hv_od_perimeter/30
		else:
			hv_id=myceil(((coredia)+(((cca['corelvgap']))*2))*2)/2
			hv_od=hv_id+(hv_rd*2)
			hv_mean_dia=hv_id+hv_rd
			hv_lmt=myrounder(math.pi*hv_mean_dia*1000)/1000
			lvhv_mean_dia=hv_od+(test['lvhmain'])
			get_lv_hv_mlt=myrounder(math.pi*lvhv_mean_dia*1000)/1000
			lv_id=hv_od+(test['lvhmain'])*2
			lv_od=lv_id+lv_rd*2
			lv_mean_dia=lv_id+lv_rd
			lv_lmt=myrounder(math.pi*lv_mean_dia*1000)/1000
			lv_fnb_perimeter=0
			hv_fnb_perimeter=0
			lv_id_perimeter=myrounder(math.pi*lv_id*1000)/1000
			hv_id_perimeter=math.pi*hv_id
			hv_od_perimeter=myrounder(math.pi*hv_od*1000)/1000
			lv_od_perimeter=math.pi*lv_od
			lv_no_full_duct_runners_inside=lv_id_perimeter/30
			lv_no_full_duct_runners_outside=get_lv_hv_mlt/30
			hv_no_full_duct_runners_inside=hv_id_perimeter/30
			hv_no_full_duct_runners_outside=hv_od_perimeter/30
	else:
		#get_mandril_a
		if(core['coretype']=='stacked'):
			get_mandril_a=myrounder(get_stack_thk+1+cca['mandrila'])
		else:
			if(basic['rating']<=100):
				get_mandril_a=test['cmain']+7+cca['mandrila']
			else:
				get_mandril_a=test['cmain']+8+cca['mandrila']

		#get_mandril_b
		if(core['coretype']=='stacked'):
			get_mandril_b=myceil((test['cmain']+1+cca['mandrilb'])*2)/2
		else:
			if(core['subtype']=='CRGO'):
				if(basic['rating']<=63):
					get_mandril_b=myceil((get_stack_thk+8+cca['mandrilb'])*2)/2
				elif(basic['rating']<=100):
					get_mandril_b=myceil((get_stack_thk+9+cca['mandrilb'])*2)/2
				else:
					get_mandril_b=myceil((get_stack_thk+10+cca['mandrilb'])*2)/2
			else:
				get_mandril_b=myceil((get_stack_thk+4+cca['mandrilb'])*2)/2

		#hv_rd_nonlead
		hv_rd_nonlead=ceiling(rdhv*1.02)

		#lv_rd_nonlead
		lv_rd_nonlead=ceiling(rdlv*1.02)

		#hv_rd_lead
		if(tapping['yn']=="no"):
			hv_rd_lead_dat=ceiling((rdhv+((hv['fnbthk']+0.25)*hv['nofnb']))*1.05)
		else:
			hv_rd_lead_dat=ceiling(((rdhv+((hv['fnbthk']+0.25)*hv['nofnb']))*1.05)+1.5)
		if(hv['condtype']=='foil'):
			hv_rd_lead=(hv['busbart']/2)+hv_rd_lead_dat
		else:
			hv_rd_lead=hv_rd_lead_dat

		#lv_rd_lead
		if(basic['rating']<=40):
			lv_rd_lead_dat=ceiling(rdlv+((lv['fnbthk']+0.125)*lv['nofnb'])+1.2)
		else:
			lv_rd_lead_dat=ceiling((rdlv+((lv['fnbthk']+0.125)*lv['nofnb'])+1.2)*1.02)
		if(lv['condtype']=='foil'):
			lv_rd_lead=(lv['busbart']/2)+lv_rd_lead_dat
		else:
			lv_rd_lead=lv_rd_lead_dat

		if(lv['condtype']=='foil'):
			lvfoilef=lv['busbart']
		else:
			lvfoilef=0
		if(hv['condtype']=='foil'):
			hvfoilef=hv['busbart']
		else:
			hvfoilef=0

		if(basic['corelvhv']=='lvstart'):
			#get_lv_id_b
			get_lv_id_b=myceil((get_mandril_b+(cca['corelvgap']*2))*2)/2

			#get_lv_id_a
			get_lv_id_a=myceil((get_mandril_a+(cca['corelvgap']*2))*2)/2

			#get_lv_od_b
			get_lv_od_b=(get_lv_id_b)+(lv_rd_nonlead*2)

			#get_lv_od_a
			get_lv_od_a=(get_lv_id_a)+(lv_rd_lead*2)

			#get_hv_id_b
			get_hv_id_b=get_lv_od_b+(test['lvhmain']*2)

			#get_hv_id_a
			get_hv_id_a=get_lv_od_a+(test['lvhmain']*2)

			#get_hv_od_b
			get_hv_od_b=(get_hv_id_b)+(hv_rd_nonlead*2)

			#get_hv_od_a
			get_hv_od_a=((get_hv_id_a)+(hv_rd_lead*2))

			#lv_lmt
			lv_lmt=myrounder(((2*(get_mandril_a+get_mandril_b-(4*lv_cover_ef))+2*math.pi*(lv_cover_ef+cca['corelvgap']+(lv_rd*0.5))+2*(lv['nofnb']*(lv['fnbthk']+0.125)))+(lvfoilef*2))*1000)/1000

			#hv_lmt
			hv_lmt=myrounder(((2*(get_mandril_a+get_mandril_b-(4*lv_cover_ef))+2*math.pi*(lv_cover_ef+cca['corelvgap']+lv_rd+test['lvhmain']+(hv_rd*0.5))+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25)))+(lvfoilef*4)+(hvfoilef*2))*1000)/1000
			#get_lv_hv_mlt
			get_lv_hv_mlt=myrounder(((2*(get_mandril_a+get_mandril_b-(4*lv_cover_ef))+2*math.pi*(lv_cover_ef+cca['corelvgap']+lv_rd+test['lvhmain']*0.5)+4*(lv['nofnb']*(lv['fnbthk']+0.125)))+(lvfoilef*4))*1000)/1000

			#lv_fnb_perimeter
			lv_fnb_perimeter=get_mandril_b+math.pi*0.5*(lv_cover_ef+cca['corelvgap']+(lv_rd*0.5))

			#lv_id_perimeter
			lv_id_perimeter=myrounder((2*(get_mandril_a+get_mandril_b-(4*lv_cover_ef))+2*math.pi*(lv_cover_ef+cca['corelvgap']))*1000)/1000

			#hv_fnb_perimeter
			hv_fnb_perimeter=get_mandril_b+math.pi*0.5*(lv_cover_ef+cca['corelvgap']+lv_rd+test['lvhmain']+(hv_rd*0.5))

			#hv_od_perimeter
			hv_od_perimeter=myrounder(((2*(get_mandril_a+get_mandril_b-(4*lv_cover_ef))+2*math.pi*(lv_cover_ef+cca['corelvgap']+lv_rd+test['lvhmain']+(hv_rd))+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25)))+(lvfoilef*4)+(hvfoilef*4))*1000)/1000

			#lv_od_perimeter
			lv_od_perimeter=myrounder(((2*(get_mandril_a+get_mandril_b-(4*lv_cover_ef))+2*math.pi*(lv_cover_ef+cca['corelvgap']+lv_rd)+2*(lv['nofnb']*(lv['fnbthk']+0.125)))+(lvfoilef*4))*1000)/1000

			#hv_id_perimeter
			hv_id_perimeter=myrounder(((2*(get_mandril_a+get_mandril_b-(4*lv_cover_ef))+2*math.pi*(lv_cover_ef+cca['corelvgap']+lv_rd+test['lvhmain'])+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25)))+(lvfoilef*2))*1000)/1000
			lv_no_full_duct_runners_inside=lv_id_perimeter/30
			lv_no_full_duct_runners_outside=get_lv_hv_mlt/30
			hv_no_full_duct_runners_inside=hv_id_perimeter/30
			hv_no_full_duct_runners_outside=hv_od_perimeter/30
		else:
			#get_hv_id_a
			get_hv_id_a=get_mandril_a+(cca['corelvgap']*2)

			#get_hv_od_a
			get_hv_od_a=(get_hv_id_a)+(hv_rd_lead*2)

			#get_hv_id_b
			get_hv_id_b=get_mandril_b+(cca['corelvgap']*2)

			#get_hv_od_b
			get_hv_od_b=(get_hv_id_b)+(hv_rd_nonlead*2)

			#get_lv_id_b
			get_lv_id_b=myceil((get_hv_od_b+(test['lvhmain']*2))*2)/2

			#get_lv_id_a
			get_lv_id_a=myceil((get_hv_od_a+(test['lvhmain']*2))*2)/2

			#get_lv_od_b
			get_lv_od_b=(get_lv_id_b)+(lv_rd_nonlead*2)

			#get_lv_od_a
			get_lv_od_a=(get_lv_id_a)+(lv_rd_lead*2)

			#lv_lmt
			hv_lmt=myrounder(((2*(get_mandril_a+get_mandril_b-(4*hv_cover_ef))+2*math.pi*(hv_cover_ef+cca['corelvgap']+(hv_rd*0.5))+2*(hv['nofnb']*(hv['fnbthk']+0.125)))+(hvfoilef*2))*1000)/1000

			#lv_lmt
			lv_lmt=myrounder(((2*(get_mandril_a+get_mandril_b-(4*hv_cover_ef))+2*math.pi*(hv_cover_ef+cca['corelvgap']+hv_rd+test['lvhmain']+(lv_rd*0.5))+4*(hv['nofnb']*(hv['fnbthk']+0.125))+2*(lv['nofnb']*(lv['fnbthk']+0.25)))+(hvfoilef*4)+(lvfoilef*2))*1000)/1000

			#get_lv_hv_mlt
			get_lv_hv_mlt=myrounder(((2*(get_mandril_a+get_mandril_b-(4*hv_cover_ef))+2*math.pi*(hv_cover_ef+cca['corelvgap']+hv_rd+test['lvhmain']*0.5)+4*(hv['nofnb']*(hv['fnbthk']+0.125)))+(hvfoilef*4))*1000)/1000

			#lv_fnb_perimeter
			hv_fnb_perimeter=get_mandril_b+math.pi*0.5*(hv_cover_ef+cca['corelvgap']+(hv_rd*0.5))

			#hv_fnb_perimeter
			lv_fnb_perimeter=get_mandril_b+math.pi*0.5*(hv_cover_ef+cca['corelvgap']+hv_rd+test['lvhmain']+(lv_rd*0.5))

			#lv_id_perimeter
			lv_id_perimeter=myrounder(((2*(get_mandril_a+get_mandril_b-(4*hv_cover_ef))+2*math.pi*(hv_cover_ef+cca['corelvgap']))+(lvfoilef*2))*1000)/1000

			#hv_od_perimeter
			hv_od_perimeter=myrounder(((2*(get_mandril_a+get_mandril_b-(4*hv_cover_ef))+2*math.pi*(hv_cover_ef+cca['corelvgap']+lv_rd+test['lvhmain']+(hv_rd))+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25)))+(hvfoilef*4))*1000)/1000

			#lv_od_perimeter
			lv_od_perimeter=myrounder(((2*(get_mandril_a+get_mandril_b-(4*hv_cover_ef))+2*math.pi*(hv_cover_ef+cca['corelvgap']+lv_rd)+2*(lv['nofnb']*(lv['fnbthk']+0.125)))+(lv['busbart']*4)+(hvfoilef*4))*1000)/1000

			#hv_id_perimeter
			hv_id_perimeter=myrounder((2*(get_mandril_a+get_mandril_b-(4*hv_cover_ef))+2*math.pi*(hv_cover_ef+cca['corelvgap']+lv_rd+test['lvhmain'])+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25)))*1000)/1000
			lv_no_full_duct_runners_inside=lv_id_perimeter/30
			lv_no_full_duct_runners_outside=lv_od_perimeter/30
			hv_no_full_duct_runners_inside=hv_id_perimeter/30
			hv_no_full_duct_runners_outside=get_lv_hv_mlt/30

	#lv_resi_ph
	lv_resi_ph=myrounder((lv_mat_ef*lv_lmt*test['lvtmain']/(100000*lv_cond_area))*1000000)/1000000

	#hv_resi_ph
	hv_resi_ph=myrounder((hv_mat_ef*hv_lmt*get_rated_hvturns/(100000*hv_cond_area))*1000000)/1000000

	#bfactor_eddy
	bfactor_eddy=phase_lv*test['lvtmain']*1.78/(1000*(lv_axial_elect+hv_axial_elect)*0.5)

	#lv_cond_wt
	lv_cond_wt=myrounder((lv_lmt*test['lvtmain']*lv_wt_ef*lv_cond_area*wt_pf/1000000)*100)/100

	#hv_cond_wt
	hv_cond_wt=myrounder((hv_lmt*get_hvturns*hv_wt_ef*hv_cond_area*wt_pf/1000000)*100)/100

	#lv_eddy
	if(lv['material']=='copper'):
		lv_eddy_ef=9
	else:
		lv_eddy_ef=19
	if(lv['condtype']=='round'):
		lv_eddy_ef1=0.4
	else:
		lv_eddy_ef1=1
	lv_eddy=myrounder((lv_eddy_ef1*lv_eddy_ef*basic['frequency']*basic['frequency']*bfactor_eddy*bfactor_eddy*test['lvkmain']*test['lvkmain']*lv_cond_wt/1000)*10)/10

	#hv_eddy
	if(hv['material']=='copper'):
		hv_eddy_ef=9
	else:
		hv_eddy_ef=19
	if(hv['condtype']=='round'):
		hv_eddy_ef1=0.4
	else:
		hv_eddy_ef1=1
	hv_eddy=myrounder((hv_eddy_ef1*hv_eddy_ef*basic['frequency']*basic['frequency']*bfactor_eddy*bfactor_eddy*test['hvkmain']*test['hvkmain']*hv_cond_wt/1000)*10)/10

	#lv_inner_duct_cooling_area
	lv_no_full_duct_runners=lv_lmt/30
	lv_no_fnb_duct_runners=lv_fnb_perimeter/30
	if(lv['fullthk']<3):
		lv_full_duct_area=(lv_lmt-(10*lv_no_full_duct_runners))*lv_axial_phy*2/1000000*lv['nofull']*0.5
	elif(lv['fullthk']<4):
		if(lv_axial_phy<=350):
			lv_full_duct_area=(lv_lmt-(10*lv_no_full_duct_runners))*lv_axial_phy*2/1000000*lv['nofull']
		else:
			lv_full_duct_area=(lv_lmt-(10*lv_no_full_duct_runners))*lv_axial_phy*2/1000000*lv['nofull']*0.75
	else:
		lv_full_duct_area=(lv_lmt-(10*lv_no_full_duct_runners))*lv_axial_phy*2/1000000*lv['nofull']
	if(lv['fnbthk']<3):
		lv_fnb_duct_area=(lv_fnb_perimeter-(10*lv_no_fnb_duct_runners))*lv_axial_phy*4/1000000*lv['nofnb']
	elif(lv['fnbthk']<4):
		if(lv_axial_phy<=350):
			lv_fnb_duct_area=(lv_fnb_perimeter-(10*lv_no_fnb_duct_runners))*lv_axial_phy*4/1000000*lv['nofnb']
		else:
			lv_fnb_duct_area=(lv_fnb_perimeter-(10*lv_no_fnb_duct_runners))*lv_axial_phy*4/1000000*lv['nofnb']*0.75
	else:
		lv_fnb_duct_area=(lv_fnb_perimeter-(10*lv_no_fnb_duct_runners))*lv_axial_phy*4/1000000*lv['nofnb']
	lv_inner_duct_cooling_area=lv_full_duct_area+lv_fnb_duct_area

	#lv_outer_duct_cooling_area
	lv_full_duct_area_inside=(lv_id_perimeter-10*lv_no_full_duct_runners_inside)*lv_axial_phy/1000000
	lv_outer_duct_cooling_area=0
	if(basic['corelvhv']=='lvstart'):
		if(hv['windtype']=='crossover'):
			lv_full_duct_area_outside=(lv_od_perimeter-18*hv['bpercircle'])*lv_axial_phy/1000000
		else:
			lv_full_duct_area_outside=(lv_od_perimeter-10*lv_no_full_duct_runners_outside)*lv_axial_phy/1000000
		if(cca['corelvgap']<=2):
			lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+(0*lv_full_duct_area_inside)
		elif(cca['corelvgap']<=3):
			lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+(0.25*lv_full_duct_area_inside)
		elif(cca['corelvgap']<=4):
			lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+(0.5*lv_full_duct_area_inside)
		elif(cca['corelvgap']<=5):
			lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+(0.75*lv_full_duct_area_inside)
		else:
			lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+lv_full_duct_area_inside
		if(test['lvhmain']>3.5):
			lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+lv_full_duct_area_outside
	else:
		lv_full_duct_area_outside=(lv_od_perimeter)*lv_axial_phy/1000000
		if(test['lvhmain']>=8):
			lv_outer_duct_cooling_area=lv_full_duct_area_inside+(lv_full_duct_area_outside*0.7)
		else:
			lv_outer_duct_cooling_area=(lv_full_duct_area_outside*0.7)

	#lv_total_duct_cooling_area
	if(basic['phases']=='3'):
		lv_total_duct_cooling_area_ef=3
	else:
		if(core['structure']=='Core'):
			lv_total_duct_cooling_area_ef=2
		else:
			lv_total_duct_cooling_area_ef=1
	lv_total_duct_cooling_area=(lv_inner_duct_cooling_area+lv_outer_duct_cooling_area)*lv_total_duct_cooling_area_ef

	#hv_inner_duct_cooling_area
	hv_no_full_duct_runners=hv_lmt/30
	hv_no_fnb_duct_runners=hv_fnb_perimeter/30
	if(hv['windtype']=='crossover'):
		if(tapping['yn']=='yes'):
			hvcoolingareafactor=hv_axial_phy-(((hv['mcoils']))*(hv['minsu']))-(((hv['tcoils'])-1)*(hv['tinsu']))
		else:
			hvcoolingareafactor=hv_axial_phy-(((hv['mcoils'])-1)*(hv['minsu']))
		hvheightfactor=hv_single_coil_ht
		hvcrossradialsurfacearea=((math.pi*((hv_od*hv_od)-((hv_od-hv_rd)*(hv_od-hv_rd)))/4)-(hv['bpercircle']*35*hv_rd))*((hv['mcoils'])+(hv['tcoils']))*2/1000000
	else:
		hvheightfactor=hv_axial_phy
		hvcoolingareafactor=hv_axial_phy
		hvcrossradialsurfacearea=0
	if(hv['fullthk']<3):
		hv_full_duct_area=(hv_lmt-(10*hv_no_full_duct_runners))*hvcoolingareafactor*2/1000000*hv['nofull']*0.5
	elif(hv['fullthk']<4):
		if(hvheightfactor<=350):
			hv_full_duct_area=(hv_lmt-(10*hv_no_full_duct_runners))*hvcoolingareafactor*2/1000000*hv['nofull']
		else:
			hv_full_duct_area=(hv_lmt-(10*hv_no_full_duct_runners))*hvcoolingareafactor*2/1000000*hv['nofull']*0.75
	else:
		hv_full_duct_area=(hv_lmt-(10*hv_no_full_duct_runners))*hvcoolingareafactor*2/1000000*hv['nofull']
	if(hv['fnbthk']<3):
		hv_fnb_duct_area=(hv_fnb_perimeter-(10*hv_no_fnb_duct_runners))*hvcoolingareafactor*4/1000000*hv['nofnb']*0.5
	elif(hv['fnbthk']<4):
		if(hvheightfactor<=350):
			hv_fnb_duct_area=(hv_fnb_perimeter-(10*hv_no_fnb_duct_runners))*hvcoolingareafactor*4/1000000*hv['nofnb']
		else:
			hv_fnb_duct_area=(hv_fnb_perimeter-(10*hv_no_fnb_duct_runners))*hvcoolingareafactor*4/1000000*hv['nofnb']*0.75
	else:
		hv_fnb_duct_area=(hv_fnb_perimeter-(10*hv_no_fnb_duct_runners))*hvcoolingareafactor*4/1000000*hv['nofnb']
	hv_inner_duct_cooling_area=hv_full_duct_area+hv_fnb_duct_area

	#hv_outer_duct_cooling_area
	hv_outer_duct_cooling_area=0
	if(hv['windtype']=='crossover'):
		hv_full_duct_area_inside=(hv_id_perimeter-18*hv['bpercircle'])*hvcoolingareafactor/1000000
	else:
		hv_full_duct_area_inside=(hv_id_perimeter-10*hv_no_full_duct_runners_inside)*hvcoolingareafactor/1000000
	hv_outer_duct_cooling_area=0
	if(basic['corelvhv']=='lvstart'):
		hv_full_duct_area_outside=(hv_od_perimeter)*hvcoolingareafactor/1000000
		if(test['lvhmain']>=8):
			hv_outer_duct_cooling_area=hv_full_duct_area_inside+(hv_full_duct_area_outside*0.7)
		else:
			hv_outer_duct_cooling_area=(hv_full_duct_area_outside*0.7)
	else:
		hv_full_duct_area_outside=(hv_od_perimeter-10*hv_no_full_duct_runners_outside)*hvcoolingareafactor/1000000
		if(cca['corelvgap']<=2):
			hv_outer_duct_cooling_area=hv_outer_duct_cooling_area+(0*hv_full_duct_area_inside)
		elif(cca['corelvgap']<=3):
			hv_outer_duct_cooling_area=hv_outer_duct_cooling_area+(0.25*hv_full_duct_area_inside)
		elif(cca['corelvgap']<=4):
			hv_outer_duct_cooling_area=hv_outer_duct_cooling_area+(0.5*hv_full_duct_area_inside)
		elif(cca['corelvgap']<=5):
			hv_outer_duct_cooling_area=hv_outer_duct_cooling_area+(0.75*hv_full_duct_area_inside)
		else:
			hv_outer_duct_cooling_area=hv_outer_duct_cooling_area+hv_full_duct_area_inside
		if(test['lvhmain']>3.5):
			hv_outer_duct_cooling_area=hv_outer_duct_cooling_area+hv_full_duct_area_outside

	#hv_total_duct_cooling_area
	if(basic['phases']=='3'):
		hv_total_duct_cooling_area_ef=3
	else:
		if(core['structure']=='Core'):
			hv_total_duct_cooling_area_ef=2
		else:
			hv_total_duct_cooling_area_ef=1
	hv_total_duct_cooling_area=(hv_inner_duct_cooling_area+hv_outer_duct_cooling_area+hvcrossradialsurfacearea)*hv_total_duct_cooling_area_ef

	#lv_l2r_loss
	if(basic['phases']=='3'):
		l2r_loss_pf=3
	else:
		l2r_loss_pf=1
	lv_l2r_loss=myrounder(l2r_loss_pf*phase_lv*phase_lv*lv_resi_ph*2)/2

	#hv_l2r_loss
	hv_l2r_loss=myrounder(l2r_loss_pf*phase_hv*phase_hv*hv_resi_ph*2)/2

	#get_window_height
	if(hv_axial_pack>=lv_axial_pack):
		gwhdat=hv_axial_pack
	else:
		gwhdat=lv_axial_pack
	if(core['coretype']=='stacked'):
		get_window_height=myceil(gwhdat+cca['coilyokegap']+cca['coilyokegap2'])
	else:
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			get_window_height=myceil(gwhdat+cca['coilyokegap']+cca['coilyokegap2']+8)
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			get_window_height1=gwhdat+cca['coilyokegap']+cca['coilyokegap2']+8
			get_window_height=get_window_height2=out1+get_stack_thk+2
			if(get_window_height2>get_window_height1):
				get_window_height_big=get_window_height2
				get_window_height_small=get_window_height1
			else:
				get_window_height_big=get_window_height1
				get_window_height_small=get_window_height2
		if(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			get_window_height=myceil(gwhdat+cca['coilyokegap']+cca['coilyokegap2']+13)
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			get_window_height1=gwhdat+cca['coilyokegap']+cca['coilyokegap2']+13
			get_window_height=get_window_height2=out1+(get_stack_thk*1.3)+2
			if(get_window_height2>get_window_height1):
				get_window_height_big=get_window_height2
				get_window_height_small=get_window_height1
			else:
				get_window_height_big=get_window_height1
				get_window_height_small=get_window_height2
	if(get_window_height>check['maxleglnth'] or get_window_height<check['minleglnth']):
		print 'get_window_height'
		return 0

	#total_weight
	if(core['coretype']=='stacked'):
		if(core['num']=='Multi'):
			get_leg_center=hv_od+(cca['hvhvgap'])
			along_mlt=myrounder(((3*get_window_height)+4*(get_leg_center-coredat[0][0]))*100)/100
			across_mlt=myrounder((6*coredat[0][0])*100)/100
			along_wt=myrounder((along_mlt*7.65*get_core_area*1.007*0.0001)*100)/100
			across_wt=myrounder((across_mlt*7.65*get_core_area*1.007*0.0001)*100)/100
			total_weight=myrounder((across_wt+along_wt)*100)/100

		else:
			#get_leg_center
			get_leg_center=myceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']+1+test['cmain']+cca['mandrilb'])
			if(get_leg_center>check['maxlegcenter'] or get_leg_center<check['minlegcenter']):
				print 'get_leg_center'
				return 0
			#along_mlt
			along_mlt=myceil(3*get_window_height)+4*(get_leg_center-test['cmain'])
			#across_mlt
			across_mlt=6*test['cmain']
			#along_wt
			along_wt=myrounder((along_mlt*7.65*get_core_area/10000)*100)/100
			#across_wt
			across_wt=myrounder((across_mlt*7.65*get_core_area/10000)*100)/100
			total_weight=myrounder((along_wt+across_wt)*100)/100
	else:
		#get_small_loop_ww
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			get_small_loop_ww=myceil(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead+cca['hvend']+(cca['mandrilb']*0.5))
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			get_small_loop_ww=myceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']+cca['mandrilb'])
		if(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			get_small_loop_ww=myceil(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead+cca['hvend']+2+(cca['mandrilb']*0.5))
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			get_small_loop_ww=myceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']+4+cca['mandrilb'])
		#get_big_loop_ww
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			get_big_loop_ww=myceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']+cca['mandrilb'])
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			if(basic['rating']<=63):
				get_big_loop_ww_ef=8
			elif(basic['rating']<=100):
				get_big_loop_ww_ef=9
			else:
				get_big_loop_ww_ef=10
			get_big_loop_ww=myceil((get_small_loop_ww*2)+(get_stack_thk*2)+get_big_loop_ww_ef)
		if(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			get_big_loop_ww=myceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']+4+cca['mandrilb'])
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			get_big_loop_ww=myceil((get_small_loop_ww*2)+(get_stack_thk*2)+6)
		if(get_big_loop_ww>check['maxlegcenter'] or get_big_loop_ww<check['minlegcenter']):
			print 'get_big_loop_ww'
			return 0
		#big_loop_mlt
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			big_loop_mlt=myrounder((2*(get_window_height+5.6)+(2*get_big_loop_ww)+(1.7*get_stack_thk))*100)/100
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			big_loop_mlt=myrounder((2*(get_window_height2+5.6)+(2*get_big_loop_ww)+(1.7*get_stack_thk))*100)/100
		if(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			if(basic['rating']<315):
				big_loop_mlt_ef=15
			else:
				big_loop_mlt_ef=25
			big_loop_mlt=myrounder(((2*get_window_height)+(2*get_big_loop_ww)-52+(2*math.pi*(6.5+get_stack_thk*0.25*1.1))+big_loop_mlt_ef)*100)/100
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			if(basic['rating']<315):
				big_loop_mlt_ef=15
			else:
				big_loop_mlt_ef=25
			big_loop_mlt=myrounder(((2*get_window_height2)+(2*get_big_loop_ww)-52+(2*math.pi*(6.5+get_stack_thk*0.25*1.1))+big_loop_mlt_ef)*100)/100
		#small_loop_mlt
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			small_loop_mlt=myrounder((2*(get_window_height+5.6)+(2*get_small_loop_ww)+(1.7*get_stack_thk))*100)/100
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			small_loop_mlt=myrounder((2*(get_window_height1+5.6)+(2*get_small_loop_ww)+(1.7*get_stack_thk))*100)/100
		if(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			if(basic['rating']<315):
				small_loop_mlt_ef=15
			else:
				small_loop_mlt_ef=25
			small_loop_mlt=myrounder((2*(get_window_height)+(2*get_small_loop_ww)-52+(2*math.pi*(6.5+get_stack_thk*0.25*1.1))+small_loop_mlt_ef)*100)/100
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			if(basic['rating']<315):
				small_loop_mlt_ef=15
			else:
				small_loop_mlt_ef=25
			small_loop_mlt=myrounder(((2*get_window_height1)+(2*get_small_loop_ww)-52+(2*math.pi*(6.5+get_stack_thk*0.25*1.1))+small_loop_mlt_ef)*100)/100
		big_loop_wt=myrounder(((big_loop_mlt*loop_wt_ef*get_core_area)/10000)*100)/100
		small_loop_wt=myrounder(((small_loop_mlt*loop_wt_ef*get_core_area)/10000)*100)/100
		total_weight=myrounder((big_loop_wt+small_loop_wt)*100)/100

	if(basic['corelvhv']=='lvstart'):
		if(core['coretype']=='stacked'):
			if(core['num']=='Multi'):
				tank_length=myceil((2*get_leg_center+hv_od+2*tank['hvlength'])/5)*5
				tank_breadth=myceil((hv_od+(tank['hvwidth'])+(tank['lvwidth']))/5)*5
			else:
				tank_length=myceil((2*get_leg_center+get_hv_od_b+2*tank['hvlength'])/5)*5
				tank_breadth=myceil((get_hv_od_a+tank['hvwidth']+tank['lvwidth'])/5)*5
		else:
			if(core['structure']=='Shell'):
				tank_length=myceil(((get_big_loop_ww+get_small_loop_ww)*2+(get_stack_thk*4)+22+(2*tank['hvlength']))/5)*5
				tank_breadth=myceil((get_hv_od_a+tank['hvwidth']+tank['lvwidth'])/5)*5
			else:
				tank_length=myceil(((3*get_hv_od_b)+(2*cca['hvhvgap'])+(2*tank['hvlength']))/5)*5
				tank_breadth=myceil((get_hv_od_a+tank['hvwidth']+tank['lvwidth'])/5)*5
	else:
		if(core['coretype']=='stacked'):
			if(core['num']=='Multi'):
				tank_length=myceil((2*get_leg_center+lv_od+2*tank['hvlength'])/5)*5
				tank_breadth=myceil((lv_od+(tank['hvwidth'])+(tank['lvwidth']))/5)*5
			else:
				tank_length=myceil((2*get_leg_center+get_lv_od_b+2*tank['hvlength'])/5)*5
				tank_breadth=myceil((get_lv_od_a+tank['hvwidth']+tank['lvwidth'])/5)*5
		else:
			if(core['structure']=='Shell'):
				tank_length=myceil(((get_big_loop_ww+get_small_loop_ww)*2+(get_stack_thk*4)+22+(2*tank['hvlength']))/5)*5
				tank_breadth=myceil((get_lv_od_a+tank['hvwidth']+tank['lvwidth'])/5)*5
			else:
				tank_length=myceil(((3*get_lv_od_b)+(2*cca['hvhvgap'])+(2*tank['hvlength']))/5)*5
				tank_breadth=myceil((get_lv_od_a+tank['hvwidth']+tank['lvwidth'])/5)*5
	#tank_breadth			
	if(tank_breadth>check['maxtankwidth'] or tank_breadth<check['mintankwidth']):
		print 'tank_breadth'
		return 0

	#tank_length
	if(tank_length>check['maxtanklength'] or tank_length<check['mintanklength']):
		print 'tank_length'
		return 0

	#covered_wt_lv
	if(lv['condtype']=='round'):
		lvcoveredthk=test['lvkmain']+lv['coveringthk']
		covered_wt_lv=myrounder((((((lvcoveredthk*lvcoveredthk)-(test['lvkmain']*test['lvkmain']))*covered_wt_lv_ef1/((test['lvkmain']*test['lvkmain'])*lv_wt_ef))*(lv_cond_wt))+lv_cond_wt)*100)/100
	else:
		lvcoverwith=test['lvwmain']+lv['coveringthk']
		lvcoverthk=test['lvkmain']+lv['coveringthk']
		if(lvcoverthk>2.99):
			covered_wt_lv_ef=0.9
		else:
			covered_wt_lv_ef=0.5
		lvcoverarea=((lvcoverthk*lvcoverwith)-covered_wt_lv_ef)*lv['flats']*lv['radials']
		covered_wt_lv=myrounder(((((lvcoverarea-lv_cond_area)*covered_wt_lv_ef1/(lv_cond_area*lv_wt_ef))*(lv_cond_wt))+lv_cond_wt)*100)/100

	#covered_wt_hv
	if(hv['condtype']=='round'):
		hvcoveredthk=test['hvkmain']+hv['coveringthk']
		covered_wt_hv=myrounder((((((hvcoveredthk*hvcoveredthk)-(test['hvkmain']*test['hvkmain']))*covered_wt_hv_ef1/((test['hvkmain']*test['hvkmain'])*hv_wt_ef))*(hv_cond_wt))+hv_cond_wt)*100)/100
	else:
		hvcoverwith=test['hvwmain']+hv['coveringthk']
		hvcoverthk=test['hvkmain']+hv['coveringthk']
		if(hvcoverthk>2.99):
			covered_wt_hv_ef=0.9
		else:
			covered_wt_hv_ef=0.5
		hvcoverarea=((hvcoverthk*hvcoverwith)-covered_wt_hv_ef)*hv['flats']*hv['radials']
		covered_wt_hv=myrounder(((((hvcoverarea-hv_cond_area)*covered_wt_hv_ef1/(hv_cond_area*hv_wt_ef))*(hv_cond_wt))+hv_cond_wt)*100)/100


	#displacement
	if(core['coretype']=='stacked'):
		d2=cca['channelthk'].split('x')
		if(core['num']=='Multi'):
			clamprod=twidth+80
		else:
			clamprod=get_stack_thk+80
		tierodlength=get_window_height+20+(float(d2[0])*2)+60+clamprod
		channelwt=myrounder(((tank_length-20)*4*(bchanneldata[cca['channelthk']])/1000)*100)/100
		tierod=myrounder((((math.pi)/4)*cca['tierods']*cca['tierods']*7.85*8*tierodlength/1000000)*1000)/1000
		displacement=myrounder(((total_weight/displacement_ef)+(covered_wt_lv/lv_wt_ef)+(covered_wt_hv/hv_wt_ef)+(cca['insuwt']/1.1)+((channelwt+tierod)/7.85))*1000)/1000
	else:
		#tierod
		if(core['structure']=='Shell'):
			tieroddata=get_window_height
		else:
			tieroddata=get_window_heightsmall
		tierodlength=tieroddata+20+(cca['clampthk']*2)+60
		tierod=myrounder((((math.pi)/4)*cca['tierods']*cca['tierods']*7.85*8*tierodlength/1000000)*1000)/1000
		if(basic['corelvhv']=='lvstart'):
			if(core['structure']=='Shell'):
				tcclength=myrounder((2*(get_big_loop_ww+get_small_loop_ww))+(4*get_stack_thk)+34)
				tccwidth=myrounder(get_hv_od_a+get_stack_thk+15)
				bcclength=myrounder((2*(get_big_loop_ww+get_small_loop_ww))+(4*get_stack_thk)+34)
				bccwidth=myrounder(get_hv_od_a+(bot_core_clamp_kf*get_stack_thk)+15)
			else:
				tcclength=myrounder(get_big_loop_ww+(get_stack_thk)+22)
				tccwidth=myrounder(get_hv_od_a+(2*get_stack_thk)+15)
				bcclength=myrounder(get_big_loop_ww+(get_stack_thk)+22)
				bccwidth=myrounder(get_hv_od_a+(2*bot_core_clamp_kf*get_stack_thk)+15)
		else:
			if(core['structure']=='Shell'):
				tcclength=myrounder((2*(get_big_loop_ww+get_small_loop_ww))+(4*get_stack_thk)+34)
				tccwidth=myrounder(get_lv_od_a+get_stack_thk+15)
				bcclength=myrounder((2*(get_big_loop_ww+get_small_loop_ww))+(4*get_stack_thk)+34)
				bccwidth=myrounder(get_lv_od_a+(bot_core_clamp_kf*get_stack_thk)+15)
			else:
				tcclength=myrounder(get_big_loop_ww+(get_stack_thk)+22)
				tccwidth=myrounder(get_lv_od_a+(2*get_stack_thk)+15)
				bcclength=myrounder(get_big_loop_ww+(get_stack_thk)+22)
				bccwidth=myrounder(get_lv_od_a+(2*bot_core_clamp_kf*get_stack_thk)+15)
		#top_core_clamp
		top_core_clamp=myrounder(((tcclength*tccwidth*cca['clampthk']*7.85)/1000000)*1000)/1000
		#bot_core_clamp
		bot_core_clamp=myrounder(((bcclength*bccwidth*cca['clampthk']*7.85)/1000000)*1000)/1000
		displacement=myrounder(((total_weight/displacement_ef)+(covered_wt_lv/lv_wt_ef)+(covered_wt_hv/hv_wt_ef)+(cca['insuwt']/1.1)+((top_core_clamp+bot_core_clamp+tierod)/7.85))*1000)/1000

	#lv_bushing
	if(basic['rating']<=400):
		lv_bushing_ef=1
	else:
		lv_bushing_ef=0.5
	lv_bushing=myrounder((math.pow(line_lv,1.25)*0.045*lv_bushing_ef)*10)/10

	#hv_bushing
	hv_bushing=myrounder((math.pow(line_hv,1.25)*0.045)*10)/10

	#lvbusbarl
	if(lv['condtype']=='foil'):
		if(core['coretype']=='stacked'):
			if(core['num']=='Multi'):
				lvbusbarl=myrounder((lv_axial_pack+get_window_height)*3+(hv_od*2)+(2*cca['hvhvgap'])+50+((5+(1*coredat[0][0])+300))*3)
			else:
				lvbusbarl=myrounder((lv_axial_pack+get_window_height)*3+(get_hv_od_b*2)+(2*cca['hvhvgap'])+50+((5+(1*test['cmain'])+300))*3)
		else:
			if(core['structure']=='Shell'):
				lvbusbarl_ef2=0.5
				lvbusbarl_data=get_window_height
			else:
				lvbusbarl_ef2=1
				lvbusbarl_data=get_window_height_small
			lvbusbarl=myrounder((lv_axial_pack+lvbusbarl_data)*3+(get_hv_od_b*2)+(2*cca['hvhvgap'])+50+(((cca['clampthk'])+5+(get_stack_thk*lvbusbarl_ef2)+300))*3)
	else:
		if(core['coretype']=='stacked'):
			if(core['num']=='Multi'):
				lvbusbarl=myrounder((hv_od*2)+(2*cca['hvhvgap'])+50+(cca['coilyokegap']*3)+((5+(1*coredat[0][0])+300))*3)
			else:
				lvbusbarl=myrounder((get_hv_od_b*2)+(2*cca['hvhvgap'])+50+(cca['coilyokegap']*3)+((5+(1*test['cmain'])+300))*3)
		else:
			if(core['structure']=='Shell'):
				lvbusbarl_ef2=0.5
				lvbusbarl_data=get_window_height
			else:
				lvbusbarl_ef2=1
				lvbusbarl_data=get_window_height_small
			lvbusbarl=myrounder((get_hv_od_b*2)+(2*cca['hvhvgap'])+50+(cca['coilyokegap']*3)+(((cca['clampthk'])+5+(get_stack_thk*lvbusbarl_ef2)+300))*3)
	#hvbusbarl
	if(hv['condtype']=='foil'):
		if(core['coretype']=='stacked'):
			if(core['num']=='Multi'):
				hvbusbarl=myrounder((hv_axial_pack+get_window_height)*3+(hv_od*2)+(2*cca['hvhvgap'])+50+((5+(1*coredat[0][0])+300))*3)
			else:
				hvbusbarl=myrounder((hv_axial_pack+get_window_height)*3+(get_hv_od_b*2)+(2*cca['hvhvgap'])+50+((5+(1*test['cmain'])+300))*3)
		else:
			if(core['structure']=='Shell'):
				hvbusbarl_ef2=0.5
			else:
				hvbusbarl_ef2=1
			hvbusbarl=myrounder((hv_axial_pack+hvbusbarl_data)*3+(get_hv_od_b*2)+(2*cca['hvhvgap'])+50+(((cca['clampthk'])+5+(get_stack_thk*hvbusbarl_ef2)+300))*3)
	else:
		hvbusbarl=0

	#lead_wire_loss_lv
	if(basic['rating']>250):
		if(lv['busshow']==True):
			lead_wire_loss_lv=myrounder((phase_lv*phase_lv*(lv_mat_ef*lvbusbarl/(100000*lv['busbarw']*lv['busbart'])))*100)/100
		else:
			lead_wire_loss_lv=myrounder((phase_lv*phase_lv*(lv_mat_ef*lvbusbarl/(100000*lv_cond_area)))*100)/100
	else:
		lead_wire_loss_lv=myrounder((0.02*lv_l2r_loss)*100)/100

	#lead_wire_loss_hv
	if(hv['condtype']=='foil'):
		if(lv['busshow']==True):
			lead_wire_loss_hv=myrounder((phase_hv*phase_hv*(hv_mat_ef*hvbusbarl/(100000*hv['busbarw']*hv['busbart'])))*100)/100
		else:
			lead_wire_loss_hv=myrounder((phase_hv*phase_hv*(hv_mat_ef*hvbusbarl/(100000*hv_cond_area)))*100)/100
	else:
		lead_wire_loss_hv=myrounder((0.005*hv_l2r_loss)*10)/10

	#lv_misc_loss
	lv_misc_loss=myrounder(((lv_l2r_loss+lv_bushing+lead_wire_loss_lv+lv_eddy)*1.5/100)*10)/10

	#hv_misc_loss
	hv_misc_loss=myrounder(((hv_l2r_loss+hv_bushing+lead_wire_loss_hv+hv_eddy)*1.5/100)*10)/10

	#lv_stray_loss
	lv_stray_loss=myrounder((lv_eddy+lv_bushing+lead_wire_loss_lv+lv_misc_loss)*10)/10

	#hv_stray_loss
	hv_stray_loss=myrounder((hv_eddy+hv_bushing+lead_wire_loss_hv+hv_misc_loss)*10)/10

	#total_stray_loss
	total_stray_loss=myrounder((lv_stray_loss+hv_stray_loss)*100)/100

	#cal_bf
	if(core['coretype']=='stacked'):
		if(core['factor']==0):
			cal_bf=myrounder((1+across_wt/total_weight)*core['steplapfactor']*1000)/1000
		else:
			cal_bf=float(core['factor'])*float(core['steplapfactor'])
	else:
		cal_bf=core['factor']

	#no_load_losses
	no_load_losses=myrounder((total_weight*cal_bf*watt_kg)*100)/100
	if(other['noload1']):
		cal_no=other['noload1']*(100-other['noload2'])/100
		if(cal_no<no_load_losses):
			print 'no_load_losses'
			return 0

	#load_losses
	if(other['stray']==0):
		load_losses=lv_l2r_loss+hv_l2r_loss+lv_stray_loss+hv_stray_loss
	else:
		load_losses=lv_l2r_loss+hv_l2r_loss+other['stray']
	if(other['fullload1']):
		cal_ll=other['fullload1']*(100-other['fullload2'])/100
		if(cal_ll<load_losses):
			print 'load_losses'
			return 0

	#percentage_r
	percentage_r=myrounder((load_losses*1000/(basic['rating']*10000))*1000)/1000
	if(percentage_r>check['percentr']):
		print 'percentage_r'
		return 0

	#percentage_x_delta
	percentage_x_delta=(lv_lmt*lv_rd/(3*lv_axial_elect))+(hv_lmt*hv_rd/(3*hv_axial_elect))+(get_lv_hv_mlt*test['lvhmain']/(0.5*(lv_axial_elect+hv_axial_elect)))

	#percentage_x_k
	percentage_x_k=1-((lv_rd+test['lvhmain']+hv_rd)/(math.pi*0.5*(lv_axial_elect+hv_axial_elect)))


	if(hv['windtype']=='crossover'):
		percentage_x=myrounder(((1.24*(basic['rating'])*(lv_od+hv_id)*0.5*((lv_rd+hv_rd)/3+(test['lvhmain']))*percentage_x_k*1.04*((basic['frequency'])/50))/(3*get_volt_turn*get_volt_turn*0.5*(lv_axial_elect+hv_axial_elect)))*100)/1000
	else:
		percentage_x=myrounder((8*math.pi*math.pi*basic['frequency']*phase_lv*test['lvtmain']*test['lvtmain']*percentage_x_k*percentage_x_delta*0.00000001/lvphvolt)*100)/100
	#percentage_x

	#percentage_z
	percentage_z=myrounder((math.sqrt((percentage_x*percentage_x)+(percentage_r*percentage_r)))*1000)/1000
	if(percentage_z<check['minimpedance'] or percentage_z>check['maximpedance']):
		print 'percentage_z'
		# return 0

	#efficiency
	efficiency=myrounder((1-((no_load_losses+(load_losses*(check['maxloadfactor']/100)*(check['maxloadfactor']/100)))/((basic['rating']*check['maxloadfactor']*check['maxpf']*10)+(no_load_losses+(load_losses*(check['maxloadfactor']/100)*(check['maxloadfactor']/100))))))*100*100)/100

	if(efficiency<check['maxefficiency']):
		print 'efficiency'
		return 0

	minefficiency=myrounder((1-((no_load_losses+(load_losses*(check['minloadfactor']/100)*(check['minloadfactor']/100)))/((basic['rating']*check['minloadfactor']*check['minpf']*10)+(no_load_losses+(load_losses*(check['minloadfactor']/100)*(check['minloadfactor']/100))))))*100*100)/100
	if(minefficiency<check['minefficiency']):
		print 'minefficiency'
		return 0

	ampturns=myrounder(((math.fabs(((test['lvtmain']*phase_lv/lv_axial_elect)-(get_hvturns*phase_hv/hv_axial_elect))/(test['lvtmain']*phase_lv/lv_axial_elect)))*100)*100)/100
	if(ampturns>check['maxampturns'] or ampturns<check['minampturns']):
		print 'ampturns'
		return 0

	if(other['staryn']=='yes'):
		#totloss1
		totloss1=myrounder((no_load_losses+(load_losses*other['loss1']*other['loss1']/10000))*100)/100
		cal_totloss1=other['nloss1']*(100-other['ploss1'])/100
		if(totloss1>cal_totloss1):
			print 'totloss1'
			return 0

		#totloss1
		totloss2=myrounder((no_load_losses+(load_losses*other['loss2']*other['loss2']/10000))*100)/100
		cal_totloss2=other['nloss2']*(100-other['ploss2'])/100
		if(totloss2>cal_totloss2):
			print 'totloss2'
			return 0

	#noiselvl
	if(core['coretype']=='stacked'):
		noiselvldata=get_window_height
	else:
		if(core['structure']=='Shell'):
			noiselvldata=get_window_height
		else:
			noiselvldata=get_window_height_big
	noiselvl=myrounder((39.2+(10*(math.log10(noiselvldata/100)))+(20*(math.log10((1.35*act_flx_d*2)-2.51))))*100)/100
	if(noiselvl>check['maxnoise'] or noiselvl<check['minnoise']):
		print 'noiselvl'
		return 0

	if(tapping['yn']=='yes'):
		tappingef=myrounder((1-(tapping['min']/100))*100)/100
	else:
		tappingef=1
	if(lv['material']=='copper'):
		maxtemplvef=235
		maxtemplvef2=106000
	else:
		maxtemplvef2=45700
		maxtemplvef=225
	maxtemplv=myrounder((((mwindrise)+(other['ambienttemp']))+(2*((mwindrise)+(other['ambienttemp'])+maxtemplvef))/((maxtemplvef2/(lv_cd*100/(percentage_z*tappingef))*(lv_cd*100/(percentage_z*tappingef))*(other['thermalab']))-1))*100)/100
	if(maxtemplv>check['maxlvtemp']):
		print 'maxtemplv'
		return 0
	if(hv['material']=='copper'):
		maxtemphvef=235
		maxtemphvef2=106000
	else:
		maxtemphvef2=45700
		maxtemphvef=225
	maxtemphv=myrounder((((mwindrise)+(other['ambienttemp']))+(2*((mwindrise)+(other['ambienttemp'])+maxtemphvef))/((maxtemphvef2/((hv_cd/tappingef)*100/(percentage_z*tappingef))*((hv_cd/tappingef)*100/(percentage_z*tappingef))*(other['thermalab']))-1))*100)/100
	if(maxtemphv>check['maxhvtemp']):
		print 'maxtemphv'
		return 0

	#lvcost
	lvcost=myrounder((costing['lv']*covered_wt_lv*1.02)*100)/100

	#hvcost
	hvcost=myrounder((costing['hv']*covered_wt_hv*1.01)*100)/100

	#corecost
	corecost=myrounder((costing['core']*total_weight*1.01)*100)/100

	#negativetaploss
	if(tapping['yn']=='yes'):
		if(hv['connectiontype']=='Star' or hv['connectiontype']=='Zigzag'):
			ntp_out=(basic['rating']*1000)/(math.sqrt(3)*minhvol)
		elif(hv['connectiontype']=='Delta'):
			ntp_out=(basic['rating']*1000)/(3*minhvol)
		elif(hv['connectiontype']=='Series' or hv['connectiontype']=='Parallel'):
			ntp_out=(basic['rating']*1000)/(minhvol)
		ntp_out1=hv_mat_ef*hv_lmt*minhvt/(100000*hv_cond_area)
		if(basic['phases']=='3'):
			ntp_loss_pf=3
		else:
			ntp_loss_pf=1
		negativetaploss=myceil(ntp_loss_pf*ntp_out*ntp_out*ntp_out1-hv_l2r_loss)
	else:
		negativetaploss=0

	#lv_watt_dissipation
	lv_watt_dissipation=myrounder(((lv_l2r_loss+lv_eddy)*0.01/lv_total_duct_cooling_area)*1000)/1000

	#hv_watt_dissipation
	hv_watt_dissipation=myrounder(((hv_l2r_loss+hv_eddy)*0.01/hv_total_duct_cooling_area)*1000)/1000

	#lv_gradient
	if(basic['corelvhv']=='lvstart'):
		lv_gradient=myceil(((0.0016*lv_axial_phy)+1.78)*math.pow(lv_watt_dissipation,0.8)*1.15)
	else:
		lv_gradient=myceil(((0.0016*lv_axial_phy)+1.78)*math.pow(lv_watt_dissipation,0.8)*1)
	if(lv_gradient>check['maxlvgradient'] or lv_gradient<check['minlvgradient']):
		print 'lv_gradient'
		return 0

	#hv_gradient
	if(basic['corelvhv']=='lvstart'):
		hv_gradient=myceil(((0.0016*hv_axial_phy)+1.78)*math.pow(hv_watt_dissipation,0.8)*1)
	else:
		hv_gradient=myceil(((0.0016*hv_axial_phy)+1.78)*math.pow(hv_watt_dissipation,0.8)*1.15)
	if(hv_gradient>check['maxhvgradient'] or hv_gradient<check['minhvgradient']):
		print 'hv_gradient'
		return 0
	#topoilrise
	ccal=(mwindrise-(moilrise)*0.8)
	if(ccal>lv_gradient and ccal>hv_gradient):
		topoilrise=moilrise
	else:
		if(lv_gradient>hv_gradient):
			topoilrise=(mwindrise-lv_gradient)/0.8
		else:
			topoilrise=(mwindrise-hv_gradient)/0.8
	#meanoilrise
	meanoilrise=topoilrise*0.8

	#tank_height
	if(core['coretype']=='stacked'):
		if(core['num']=='Multi'):
			if(tank['type']=='sealed'):
				tank_height=myrounder(get_window_height+(coredat[0][0]*2)+tank['ccabot']+10+tank['oillvl'])
			else:
				tank_height=myceil((get_window_height+(coredat[0][0]*2)+tank['ccabot']+tank['ccatop'])/5)*5
		else:
			if(tank['type']=='sealed'):
				tank_height=myrounder(get_window_height+(test['cmain']*2)+tank['ccabot']+10+tank['oillvl'])
			else:
				tank_height=myceil((get_window_height+(test['cmain']*2)+tank['ccabot']+tank['ccatop'])/5)*5
	else:
		if(core['structure']=='Shell'):
			tank_height_data=get_window_height
		else:
			tank_height_data=get_window_height_big
		if(core['subtype']=='CRGO'):
			tank_height_ef=0
		else:
			tank_height_ef=0.3
		if(tank['type']=='sealed'):
			tank_height=myrounder(tank['ccabot']+(cca['clampthk']*2)+10+tank_height_data+((1+tank_height_ef)*get_stack_thk)+tank['oillvl'])
		else:
			tank_height=myceil((tank['ccabot']+(cca['clampthk']*2)+10+tank_height_data+((1+tank_height_ef)*get_stack_thk)+tank['ccatop'])/5)*5

	#oil_main_tank
	oil_main_tank=myrounder(((tank_length*tank_breadth*tank_height)/1000000)*100)/100

	#tank_height_m
	if(tank['type']=='sealed'):
		if(tank['tanklvl']=='yes'):
			tank_height_m=myceil((tank_height+tank['airlvl'])/5)*5
		else:
			tank_height_m=myceil((tank_height+((oil_main_tank-displacement)*tank['airlvl']*10000/(tank_length*tank_breadth)))/5)*5
	else:
		tank_height_m=myceil((tank_height)/5)*5

	if(cooling['type']=='Corrugation'):
		if('L' in cooling['corrgside']):
			tdef1=2-int(cooling['corrgside'][cooling['corrgside'].index('L')-1:cooling['corrgside'].index('L')])
		else:
			tdef1=2
		if('W' in cooling['corrgside']):
			tdef2=2-int(cooling['corrgside'][cooling['corrgside'].index('W')-1:cooling['corrgside'].index('W')])
		else:
			tdef2=2
	else:
		tdef1=2
		tdef2=2

	#tank_diss_upto_oil
	if(cooling['oildiss']):
		tank_diss_upto_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*tank_height*cooling['oildiss']/1000000
	else:
		tank_diss_upto_oil=((tank_length*tdef1)+(tank_breadth*tdef2))*tank_height*meanoilrise*11/1000000


	#tank_diss_above_oil
	if(cooling['airdiss']==0):
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*meanoilrise*5.5/1000000
	else:
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*cooling['airdiss']/1000000

	#coolingreq
	if(cooling['cals']=='cal'):
		if((no_load_losses+load_losses+negativetaploss)>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(no_load_losses+load_losses+negativetaploss-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0
	else:
		if((other['noload1']+other['fullload1']+negativetaploss)>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(other['noload1']+other['fullload1']+negativetaploss-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0
	htcorrection=0
	#oilincoolingw
	if(coolingreq==0):
		oilincooling=0
	else:
		if(cooling['type']=='Tube'):
			if(coolingreq==0):
				tubelength=0
			else:
				tubelength=myrounder((coolingreq/(0.119*11*meanoilrise))*100)/100
			oilincooling=myrounder(tubelength*0.95*100)/100
		elif(cooling['type']=='PressedRadiator'):
			#radbot
			if(cooling['auto']==True):
				if(core['subtype']=="CRGO"):
					radbot_cf=0
				else:
					radbot_cf=0.3
				if(core['structure']=='Shell'):
					radbot_data=get_window_height
					radbot_sf=1
				else:
					radbot_sf=2
					radbot_data=get_window_heightsmall
				if(core['coretype']=='stacked'):
					if(core['num']=='Multi'):
						radbot_v1=(tank['ccabot']+coredat[0][0])
					else:
						radbot_v1=(tank['ccabot']+test['cmain'])
				else:
					radbot_v1=(tank['ccabot']+(get_stack_thk*0.5*(radbot_sf+radbot_cf))+cca['clampthk']+5)
				if(radbot_v1<=65):
					radbot=65
				else:
					radbot=radbot_v1
			else:
				radbot=cooling['radbottank']
			#radiatorht
			radiatorht=(tank_height-radbot-95)
			#radiatorhtf
			radiatorhtf=int(myfloor(radiatorht/50)*50)
			if(cooling['radwidth']==226):
				if(radiatorhtf<400):
					radiatorhtf=400
					htcorrection=(radiatorhtf-radiatorht)
			elif(cooling['radwidth']==300):
				if(radiatorhtf<400):
					radiatorhtf=400
					htcorrection=(radiatorhtf-radiatorht)
			elif(cooling['radwidth']==380):
				if(radiatorhtf<500):
					radiatorhtf=500
					htcorrection=(radiatorhtf-radiatorht)
			elif(cooling['radwidth']==520):
				if(radiatorhtf<500):
					radiatorhtf=500
					htcorrection=(radiatorhtf-radiatorht)
			#radiator_oil
			radiator_oil=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['oil_sec'])
			#radiator_wt
			radiator_wt=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['wt_sec'])
			#radiator_area
			radiator_area=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['sarea_sec'])
			#sfr
			if(topoilrise<=35):
				sfr_f0=35
				sfr_f1=40
			elif(topoilrise<=40):
				sfr_f0=35
				sfr_f1=40
			elif(topoilrise<=45):
				sfr_f0=40
				sfr_f1=45
			elif(topoilrise<=50):
				sfr_f0=45
				sfr_f1=50
			elif(topoilrise<=55):
				sfr_f0=50
				sfr_f1=55
			elif(topoilrise<=60):
				sfr_f0=55
				sfr_f1=60
			else:
				sfr_f0=55
				sfr_f1=60
			sfr_valf0=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f0)])
			sfr_valf1=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f1)])
			sfr=sfr_valf1-((sfr_valf1-sfr_valf0)/(sfr_f1-sfr_f0))*(sfr_f1-topoilrise)
			#vfr
			if(core['coretype']=='wound'):
				if(core['subtype']=="CRGO"):
					vfr_cf=0
				else:
					vfr_cf=0.3
				if(core['structure']=='Shell'):
					vfr_data=get_window_height
					vfr_sf=1
				else:
					vfr_sf=2
					vfr_data=get_window_heightsmall
				vfr_vval=(radbot+(radiatorht+htcorrection-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(get_stack_thk*0.5*(vfr_sf+vfr_cf))+(vfr_data*0.5)+(cca['clampthk']+5))
			else:
				if(core['num']=='Multi'):
					vfr_vval=(radbot+(radiatorht+htcorrection-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(coredat[0][0])+(get_window_height*0.5))
				else:
					vfr_vval=(radbot+(radiatorht+htcorrection-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(test['cmain'])+(get_window_height*0.5))
			vfr_vval1=int(myfloor(vfr_vval/100)*100)
			vfr_vval2=int(myceil(vfr_vval/100)*100)
			if(vfr_vval1==vfr_vval2):
				vfr=float(vertical_table[str(int(vfr_vval))])
			else:
				if(vfr_vval<0):
					vfr=0.8
				else:
					vfr=float(vertical_table[str(vfr_vval2)])-((float(vertical_table[str(vfr_vval2)])-float(vertical_table[str(vfr_vval1)]))/(vfr_vval2-vfr_vval1))*(vfr_vval2-vfr_vval)
			vfr=int(vfr*100)/100
			#radhoriz
			if(cooling['auto']):
				if(cooling['norads']==1):
					radhoriz=1
				elif(cooling['norads']<=3):
					radhoriz=(tank_length-130)/(cooling['norads']-1)
				else:
					if(cooling['norads']%2==0):
						radhoriz=(tank_length-130)/(cooling['norads']/2-1)
					else:
						radhoriz=(((tank_length-130)/myceil(cooling['norads']*0.5-1))+((tank_length-130)/myfloor(cooling['norads']*0.5-1)))*0.5
			else:
				radhoriz=cooling['radhoriz']

			#hfr
			hfr_i=0
			hfr_j=0
			hfr_l=0
			hfr_m=0
			hfr_k=0
			if(cooling['norads']==1):
					hfr=1
			else:
				for key,value in horizontal_table[str(cooling['radwidth'])].iteritems():
					if(radhoriz>=Decimal(key)):
						hfr_i=Decimal(value)
						hfr_l=Decimal(key)
					elif(radhoriz<Decimal(key)):
						if(hfr_k==0):
							hfr_j=Decimal(value)
							hfr_m=Decimal(key)
							hfr_k=1
				if(hfr_j==0):
					hfr=1
				else:
					hfr=float(hfr_j)-((float(hfr_j)-float(hfr_i))/(float(hfr_m)-float(hfr_l)))*(float(hfr_m)-float(radhoriz))
			hfr=int(hfr*1000)/1000
			#no_elements
			if(coolingreq==0):
				no_elements=0
			else:
				ele_out=myrounder(coolingreq/(sfr*vfr*hfr*cooling['norads'])*100)/100
				if(ele_out<=2):
					no_elements=myrounder((ele_out/float(fins_table['2']))*100)/100
				elif(ele_out>=32):
					no_elements=myrounder((ele_out/float(fins_table['32']))*100)/100
				else:
					ele_c=int(myceil(ele_out))
					ele_f=int(myfloor(ele_out))
					if(ele_c==ele_f):
						no_elements=myrounder((ele_out/float(fins_table[str(ele_c)]))*100)/100
					else:
						no_elements=myrounder((ele_out/(int((float(fins_table[str(ele_c)])-(((float(fins_table[str(ele_c)])-float(fins_table[str(ele_f)]))/(ele_c-ele_f))*(ele_c-ele_out)))*100)/100))*100)/100
			#actual_elements
			actual_elements=myceil(no_elements)
			oilincooling=myrounder(actual_elements*cooling['norads']*radiator_oil*100)/100
		else:
			#corrgheight
			if(cooling['auto']):
				corrgheight=myfloor((tank_height-165)/50)*50
			else:
				corrgheight=cooling['corrght']
			#corrgarea
			if(coolingreq==0):
				corrgarea=0
			else:
				corrgfinnol=((2-tdef1)*myceil((tank_length-100)/cooling['corrgfindist']))
				corrgfingapl=corrgfinnol-(2-tdef1)
				corrgfinnow=(2-tdef2)*myceil((tank_breadth-100)/cooling['corrgfindist'])
				corrgfingapw=corrgfinnow-(2-tdef2)
				if(cooling['auto']==True):
					corrgfins=corrgfinnol+corrgfinnow
					corrggaps=corrgfingapl+corrgfingapw
				else:
					corrgfins=cooling['corrgfinsno']
					corrggaps=cooling['corrgfinsno']-(4-int(tdef1)-int(tdef2))
				gap_surf_area=corrggaps*cooling['corrgfindist']*corrgheight/1000000
				corrgarea=myrounder(((coolingreq/(topoilrise*cooling['corrgwms']))-gap_surf_area)*1000)/1000
			#corrgwm2
			corrgwm2=myrounder((coolingreq/(topoilrise*float(cooling['corrgwms'])))*100)/100
			#corrgdepth
			if(cooling['auto']==True):
				corrgdepth=myceil((corrgarea*1000000/(2*corrgfins*corrgheight))/5)*5
			else:
				corrgdepth=cooling['corrgdepth']
			oilincooling=(8*corrgheight*corrgdepth*corrgfins/1000000)

	#tank_height
	if(tank['type']=='sealed'):
		tank_height=myrounder(tank_height+htcorrection)
	else:
		tank_height=myceil((tank_height+htcorrection)/5)*5
	#oil_main_tank
	oil_main_tank=myrounder(((tank_length*tank_breadth*tank_height)/1000000)*100)/100

	#tank_diss_upto_oil
	if(cooling['oildiss']):
		tank_diss_upto_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*tank_height*cooling['oildiss']/1000000
	else:
		tank_diss_upto_oil=((tank_length*tdef1)+(tank_breadth*tdef2))*tank_height*meanoilrise*11/1000000

	#conservatoroil
	if(tank['type']=='conservator'):
		conservatoroil=myrounder(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket'])*3)/100*100)/100
	else:
		conservatoroil=0

	#totoil
	totoil=myrounder(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket']+conservatoroil)*1.03)*100)/100

	#tank_height_m
	if(tank['type']=='sealed'):
		if(tank['tanklvl']=='yes'):
			tank_height_m=myceil((tank_height+tank['airlvl'])/5)*5
		else:
			tank_height_m=myceil((tank_height+((totoil)*tank['airlvl']*10000/(tank_length*tank_breadth)))/5)*5
	else:
		tank_height_m=myceil((tank_height)/5)*5

	if(tank_height_m>check['maxtankheight'] or tank_height_m<check['mintankheight']):
		print 'tank_height'
		return 0

	#tank_diss_above_oil
	if(cooling['airdiss']==0):
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*meanoilrise*5.5/1000000
	else:
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*cooling['airdiss']/1000000

	#coolingreq
	if(cooling['cals']=='cal'):
		if((no_load_losses+load_losses+negativetaploss)>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(no_load_losses+load_losses+negativetaploss-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0
	else:
		if((other['noload1']+other['fullload1']+negativetaploss)>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(other['noload1']+other['fullload1']+negativetaploss-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0

	#oilincooling
	if(coolingreq==0):
		oilincooling=0
	else:
		if(cooling['type']=='Tube'):
			#tubelength
			if(coolingreq==0):
				tubelength=0
			else:
				tubelength=myrounder((coolingreq/(0.119*11*meanoilrise))*100)/100
			oilincooling=myrounder(tubelength*0.95*100)/100
		elif(cooling['type']=='PressedRadiator'):
			#radbot
			if(cooling['auto']==True):
				if(core['subtype']=="CRGO"):
					radbot_cf=0
				else:
					radbot_cf=0.3
				if(core['structure']=='Shell'):
					radbot_data=get_window_height
					radbot_sf=1
				else:
					radbot_sf=2
					radbot_data=get_window_heightsmall
				if(core['coretype']=='stacked'):
					if(core['num']=='Multi'):
						radbot_v1=(tank['ccabot']+coredat[0][0])
					else:
						radbot_v1=(tank['ccabot']+test['cmain'])
				else:
					radbot_v1=(tank['ccabot']+(get_stack_thk*0.5*(radbot_sf+radbot_cf))+cca['clampthk']+5)
				if(radbot_v1<=65):
					radbot=65
				else:
					radbot=radbot_v1
			else:
				radbot=cooling['radbottank']
			#radiatorht
			radiatorht=(tank_height-radbot-95)
			#radiatorhtf
			radiatorhtf=int(myfloor(radiatorht/50)*50)
			#radiator_oil
			radiator_oil=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['oil_sec'])
			#radiator_wt
			radiator_wt=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['wt_sec'])
			#radiator_area
			radiator_area=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['sarea_sec'])
			#sfr
			if(topoilrise<=35):
				sfr_f0=35
				sfr_f1=40
			elif(topoilrise<=40):
				sfr_f0=35
				sfr_f1=40
			elif(topoilrise<=45):
				sfr_f0=40
				sfr_f1=45
			elif(topoilrise<=50):
				sfr_f0=45
				sfr_f1=50
			elif(topoilrise<=55):
				sfr_f0=50
				sfr_f1=55
			elif(topoilrise<=60):
				sfr_f0=55
				sfr_f1=60
			else:
				sfr_f0=55
				sfr_f1=60
			sfr_valf0=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f0)])
			sfr_valf1=float(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f1)])
			sfr=sfr_valf1-((sfr_valf1-sfr_valf0)/(sfr_f1-sfr_f0))*(sfr_f1-topoilrise)
			#vfr
			if(core['coretype']=='wound'):
				if(core['subtype']=="CRGO"):
					vfr_cf=0
				else:
					vfr_cf=0.3
				if(core['structure']=='Shell'):
					vfr_data=get_window_height
					vfr_sf=1
				else:
					vfr_sf=2
					vfr_data=get_window_heightsmall
				vfr_vval=(radbot+(radiatorht-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(get_stack_thk*0.5*(vfr_sf+vfr_cf))+(vfr_data*0.5)+(cca['clampthk']+5))
			else:
				if(core['num']=='Multi'):
					vfr_vval=(radbot+(radiatorht-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(coredat[0][0])+(get_window_height*0.5))
				else:
					vfr_vval=(radbot+(radiatorht-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(test['cmain'])+(get_window_height*0.5))
			vfr_vval1=int(myfloor(vfr_vval/100)*100)
			vfr_vval2=int(myceil(vfr_vval/100)*100)
			if(vfr_vval1==vfr_vval2):
				vfr=float(vertical_table[str(int(vfr_vval))])
			else:
				if(vfr_vval<0):
					vfr=0.8
				else:
					vfr=float(vertical_table[str(vfr_vval2)])-((float(vertical_table[str(vfr_vval2)])-float(vertical_table[str(vfr_vval1)]))/(vfr_vval2-vfr_vval1))*(vfr_vval2-vfr_vval)
			vfr=int(vfr*100)/100
			#radhoriz
			if(cooling['auto']):
				if(cooling['norads']==1):
					radhoriz=1
				elif(cooling['norads']<=3):
					radhoriz=(tank_length-130)/(cooling['norads']-1)
				else:
					if(cooling['norads']%2==0):
						radhoriz=(tank_length-130)/(cooling['norads']/2-1)
					else:
						radhoriz=(((tank_length-130)/myceil((cooling['norads']*0.5)-1))+((tank_length-130)/myfloor((cooling['norads']*0.5)-1)))*0.5
			else:
				radhoriz=cooling['radhoriz']
			#hfr
			hfr_i=0
			hfr_j=0
			hfr_l=0
			hfr_m=0
			hfr_k=0
			if(cooling['norads']==1):
					hfr=1
			else:
				for key,value in horizontal_table[str(cooling['radwidth'])].iteritems():
					if(radhoriz>=Decimal(key)):
						hfr_i=Decimal(value)
						hfr_l=Decimal(key)
					elif(radhoriz<Decimal(key)):
						if(hfr_k==0):
							hfr_j=Decimal(value)
							hfr_m=Decimal(key)
							hfr_k=1
				if(hfr_j==0):
					hfr=1
				else:
					hfr=float(hfr_j)-((float(hfr_j)-float(hfr_i))/(float(hfr_m)-float(hfr_l)))*(float(hfr_m)-float(radhoriz))
			hfr=int(hfr*1000)/1000
			#no_elements
			if(coolingreq==0):
				no_elements=0
			else:
				ele_out=myrounder(coolingreq/(sfr*vfr*hfr*cooling['norads'])*100)/100
				if(ele_out<=2):
					no_elements=myrounder((ele_out/float(fins_table['2']))*100)/100
				elif(ele_out>=32):
					no_elements=myrounder((ele_out/float(fins_table['32']))*100)/100
				else:
					ele_c=int(myceil(ele_out))
					ele_f=int(myfloor(ele_out))
					if(ele_c==ele_f):
						no_elements=myrounder((ele_out/float(fins_table[str(ele_c)]))*100)/100
					else:
						no_elements=myrounder((ele_out/(int((float(fins_table[str(ele_c)])-(((float(fins_table[str(ele_c)])-float(fins_table[str(ele_f)]))/(ele_c-ele_f))*(ele_c-ele_out)))*100)/100))*100)/100
			#actual_elements
			actual_elements=myceil(no_elements)
			oilincooling=myrounder(actual_elements*cooling['norads']*radiator_oil*100)/100
		else:
			#corrgheight
			if(cooling['auto']):
				corrgheight=myfloor((tank_height-165)/50)*50
			else:
				corrgheight=cooling['corrght']
			#corrgarea
			if(coolingreq==0):
				corrgarea=0
			else:
				corrgfinnol=((2-tdef1)*myceil((tank_length-100)/cooling['corrgfindist']))
				corrgfingapl=corrgfinnol-(2-tdef1)
				corrgfinnow=(2-tdef2)*myceil((tank_breadth-100)/cooling['corrgfindist'])
				corrgfingapw=corrgfinnow-(2-tdef2)
				if(cooling['auto']==True):
					corrgfins=corrgfinnol+corrgfinnow
					corrggaps=corrgfingapl+corrgfingapw
				else:
					corrgfins=cooling['corrgfinsno']
					corrggaps=cooling['corrgfinsno']-(4-int(tdef1)-int(tdef2))
				gap_surf_area=corrggaps*cooling['corrgfindist']*corrgheight/1000000
				corrgarea=myrounder(((coolingreq/(topoilrise*cooling['corrgwms']))-gap_surf_area)*1000)/1000
			#corrgwm2
			corrgwm2=myrounder((coolingreq/(topoilrise*cooling['corrgwms']))*100)/100
			#corrgdepth
			if(cooling['auto']==True):
				corrgdepth=myceil((corrgarea*1000000/(2*corrgfins*corrgheight))/5)*5
			else:
				corrgdepth=cooling['corrgdepth']
			oilincooling=(8*corrgheight*corrgdepth*corrgfins/1000000)

	#conservatoroil
	if(tank['type']=='conservator'):
		conservatoroil=myrounder(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket'])*3)/100*100)/100
	else:
		conservatoroil=0

	#totoil
	totoil=myrounder(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket']+conservatoroil)*1.03)*100)/100

	#coolingnos
	if(coolingreq==0):
		coolingnos=0
	else:
		if(cooling['type']=='Tube'):
			coolingnos=tubelength
		elif(cooling['type']=='PressedRadiator'):
			coolingnos=actual_elements*cooling['norads']
		else:
			coolingnos=corrgfins

	#oilcost
	oilcost=myrounder(totoil*costing['oil'])

	#coolingqty
	if(coolingreq==0):
		coolingqty=0
	else:
		if(cooling['type']=="Tube"):
			coolingqty=myrounder((tubelength*1.44)*100)/100
		elif(cooling['type']=="PressedRadiator"):
			coolingqty=actual_elements*cooling['norads']*radiator_wt
		else:
			coolingqty=myrounder(((corrgheight*corrgdepth*corrgfins*2*cooling['corrgthk']*7.85/1000000)+(corrggaps*cooling['corrgfindist']*corrgheight*cooling['corrgthk']*7.85/1000000))*100)/100

	coolingqtyfin=myrounder((coolingqty*1.05)*100)/100

	#coolingtot
	coolingtot=myrounder((coolingqtyfin*costing['cooling'])*100)/100

	#lvflatqty
	if(lv['busshow']==True):
		lvflatqty=myrounder(((lvbusbarl)*lv['busbart']*lv['busbarw']*lv_wt_ef/1000000)*100)/100
	else:
		lvflatqty=myrounder(((lvbusbarl)*lv_cond_area*lv_wt_ef/1000000)*100)/100

	#hvflatqty
	if(hv['condtype']=='foil'):
		hvflatqty=myrounder(((hvbusbarl)*hv['busbart']*hv['busbarw']*hv_wt_ef/1000000)*100)/100
	else:
		hvflatqty=0

	#sidesheetwt
	if(cooling['type']=='Corrugation'):
		sidesheetwt=myrounder((((tdef1*tank_length+tdef2*tank_breadth)*tank_height_m)+((tank_height_m-corrgheight)*(((2-tdef1)*tank_length)+((2-tdef2)*tank_breadth))))*tank['sidesheet']*7.85/10000)/100
	else:
		sidesheetwt=myrounder(2*(tank_length+tank_breadth)*tank_height_m*tank['sidesheet']*7.85/10000)/100
	# sidesheetwt=myrounder((2*(tank_length+tank_breadth)*tank_height_m*tank['sidesheet']*7.85/1000000)*100)/100

	#bchannelwt
	bdata=tank['bchannel'].split('x')
	if(tank_breadth<=400):
		bchannelwt=myrounder((460*2*(bchanneldata[tank['bchannel']])/1000)*100)/100
	else:
		bchannelwt=myrounder(((tank_breadth+150)*2*(bchanneldata[tank['bchannel']])/10))/100

	#vstifnerwt
	vdata=tank['vstifner'].split('x')
	vstifnerwt=myrounder((int(vdata[0])*int(vdata[1])*tank_height_m*2*tank['vstifno']*7.85/1000000)*100)/100

	#hstifnerwt
	hdata=tank['hstifner'].split('x')
	hstifnerwt=myrounder(((((tank_length+tank_breadth+(float(hdata[0])*4))*2*hstifdata[tank['hstifner']])*tank['hstifno'])/1000)*100)/100

	#conswt
	if(tank['type']=='conservator'):
		consvol=myrounder(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket'])/10)*100)/100
		conslen=myceil(consvol*4*1000000/(tank['consdia']*tank['consdia']*math.pi*5))*5
		conswt=myrounder(((math.pi*tank['consdia']*tank['consthk']*conslen*7.85/1000000)+(consdata[str(tank['consdia'])]['front']+consdata[str(tank['consdia'])]['curb']+consdata[str(tank['consdia'])]['side']))*100)/100
	else:
		conslen=0
		conswt=0

	#liftinglugwt
	if(basic['rating']<100):
		liftinglugwt=0.5*tank['lftlug']
	elif(basic['rating']<500):
		liftinglugwt=1.875*tank['lftlug']
	else:
		liftinglugwt=5*tank['lftlug']

	#get_curb
	get_curb_cdata=tank['curb'].split('x')
	get_curb=myrounder(((((tank_length+(tank['sidesheet']*2)+(int(get_curb_cdata[0])*2))*2)+(tank_breadth+(tank['sidesheet']*2)))*int(get_curb_cdata[0])*int(get_curb_cdata[1])*7.85/1000000)*100)/100

	#topcoverwt
	topcoverwt_cdata=tank['curb'].split('x')
	topcoverwt=myrounder(((tank_length+(tank['sidesheet']*2)+(int(topcoverwt_cdata[0])*2)+50)*(tank_breadth+(tank['sidesheet']*2)+(int(topcoverwt_cdata[0])*2)+50)*tank['topcover']*7.85/1000000)*100)/100

	#botcoverwt
	botcoverwt=myrounder(((tank_length+25)*(tank_breadth+25)*tank['botcover']*7.85/1000000)*100)/100

	#ventpipewt
	ventpipewt=myrounder((math.pi*55*tank['ventpipe']*5*7.85/1000000)*100)/100

	#tottankwt
	tottankwt=myrounder((tank['misc']+ventpipewt+(tank['pullinglug']*0.157)+(tank['topcvrlft']*0.157)+liftinglugwt+hstifnerwt+bchannelwt+get_curb+vstifnerwt+conswt+botcoverwt+sidesheetwt+topcoverwt)*1000)/1000
	#steelqty
	if(core['coretype']=='stacked'):
		steelqty=myrounder(((tottankwt+channelwt)*1.05)*100)/100
	else:
		steelqty=myrounder(((tottankwt+top_core_clamp+bot_core_clamp)*1.05)*100)/100

	#steelcost
	steelcost=myrounder((costing['ms']*steelqty)*100)/100

	#lvflatcost
	lvflatcost=myrounder((costing['lv']*lvflatqty)*100)/100

	#hvflatcost
	hvflatcost=myrounder((costing['hv']*hvflatqty)*100)/100

	#totfinalcost
	totfinalcost=myrounder((costing['othermat']+(cca['insuwt']*costing['insu'])+coolingtot+steelcost+oilcost+lvflatcost+hvflatcost+hvcost+lvcost+corecost)*100)/100

	#nllcap
	if(costing['capitalyn']=='yes'):
		nllcap=myrounder((no_load_losses*costing['nllcap'])*100)/100
	else:
		nllcap=0

	#llcap
	if(costing['capitalyn']=='yes'):
		llcap=myrounder((load_losses*costing['llcap'])*100)/100
	else:
		llcap=0

	#capcost
	capcost=myrounder((totfinalcost+nllcap+llcap)*100)/100

	output['main']=test
	if(core['coretype']=='stacked' and core['num']=='Multi'):
		output['get_stack_thk']=coredat[0][0]
	else:
		output['get_stack_thk']=get_stack_thk
	output['no_load_losses']=no_load_losses
	output['load_losses']=load_losses
	output['percentage_z']=percentage_z
	output['costing']=totfinalcost
	output['capcosting']=capcost
	que.append(output)
