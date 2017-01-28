from __future__ import division
import math
import multiprocessing
import itertools
import time
from decimal import *
from django.forms.models import model_to_dict
from core.models import Factor,Radiators,Horizontal,Vertical,Fins

class Iters(object):
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
				watt_kg_table[h['core']]={};
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
		m=multiprocessing.Manager()
		q=m.list()
		cmain=self.iters['corewidth']['min']
		while(cmain<=self.iters['corewidth']['max']):
			t2=multiprocessing.Process(target=thread_main,args=(cmain,self.basic,self.core,self.tapping,self.lv,self.hv,self.cca,self.cooling,self.tank,self.other,self.check,self.costing,self.iters,q,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table))
			threads.append(t2)
			t2.start()
			cmain=cmain+self.iters['corewidth']['step']
		for thread in threads:
				thread.join()
		r=list(itertools.chain.from_iterable(q))
		r1=sorted(r,key=lambda x:x['capcosting'])
		if len(r)==0:
			returning=[]
		elif len(r)<20:
			returning=r1
		else:
			returning=[r1[0],r1[1],r1[2],r1[3],r1[4],r1[5],r1[6],r1[7],r1[8],r1[9],r1[10],r1[11],r1[12],r1[13],r1[14],r1[15],r1[16],r1[17],r1[18],r1[19]]
		self.counter=len(r)
		print self.counter
		return returning

def thread_main(cmain,basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,iters,q,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table):
	out=[]
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
						lvhmain=iters['lvhvgap']['min']
						while (lvhmain<=iters['lvhvgap']['max']):
							test={'cmain':cmain,'fmain':fmain,'lvtmain':lvtmain,'lvwmain':round(lvwmain,1),'lvkmain':lvkmain,'hvwmain':hvwmain,'lvhmain':lvhmain}
							y=design(basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test,out,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table)
							lvhmain=round((lvhmain+iters['lvhvgap']['step']),2)
						hvwmain=round((hvwmain+iters['hvwidth']['step']),2)
					lvkmain=round((lvkmain+iters['lvthk']['step']),2)
				lvwmain=round((lvwmain+iters['lvwidth']['step']),2)
			lvtmain=round((lvtmain+iters['lvturns']['step']),2)
		fmain=round((fmain+iters['flux']['step']),2)
	q.append(out)

def ceiling(a):
	if(a-int(a)<0.1):
		return int(a)
	elif(a-int(a)>0.5):
		return int(a)+1
	else:
		return int(a)+0.5

def design(basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test,que,watt_kg_table,radiator_table,vertical_table,horizontal_table,fins_table):
	output={}
	bchanneldata={}
	bchanneldata['75x40']=7.14
	bchanneldata['100x50']=9.56
	bchanneldata['125x65']=13.7
	bchanneldata['150x75']=17.7

	hstifdata={};
	hstifdata['40x40x5']=3
	hstifdata['40x40x6']=3.5
	hstifdata['50x50x5']=4.5
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

	if(hv['condtype']=='round'):
		test['hvkmain']=test['hvwmain']
		hv['radials']=hv['flats']=1;
		hv['transpos']=0;

	if(lv['radials']==1):
		lv['transpos']=0
	if(hv['radials']==1):
		hv['transpos']=0

	if(hv['connectiontype']=='star' or hv['connectiontype']=='zigzag'):
		hv['phvolt']=(basic['hvvoltage']/math.sqrt(3))
	elif(hv['connectiontype']=='delta'):
		hv['phvolt']=basic['hvvoltage']
	elif(hv['connectiontype']=='parallel' or hv['connectiontype']=='series'):
		hv['phvolt']=basic['hvvoltage']
	
	if(lv['connectiontype']=='star' or lv['connectiontype']=='zigzag'):
		lv['phvolt']=(basic['lvvoltage']/math.sqrt(3));
	elif(lv['connectiontype']=='delta'):
		lv['phvolt']=basic['lvvoltage']
	elif(lv['connectiontype']=='parallel' or lv['connectiontype']=='series'):
		lv['phvolt']=basic['lvvoltage']

	if(core['subtype']=='CRGO'):
		get_stack_thk_ef=0.97
		tank_height_ef=0
		displacement_ef=7.65
		loop_wt_ef=7.571134
		get_core_area_ef=0.97
		bot_core_clamp_kf=1
	else:
		get_stack_thk_ef=0.86
		tank_height_ef=0.3
		displacement_ef=7.18
		loop_wt_ef=7.18
		get_core_area_ef=0.86
		bot_core_clamp_kf=1.3

	if(lv['condtype']=='foil'):
		lv['nolayers']=test['lvtmain']

	if(lv['coveringmat']=='enamel'):
		lv_lmt_ef=3
		covered_wt_lv_ef1=1.2
	else:
		lv_lmt_ef=4
		covered_wt_lv_ef1=0.9

	if(hv['coveringmat']=='enamel'):
		hv_lmt_ef=3
		covered_wt_hv_ef1=1.2
	else:
		hv_lmt_ef=4
		covered_wt_hv_ef1=0.9

	if(lv['condtype']=='round'):
		lv_eddy_ef1=0.4
	else:
		lv_eddy_ef1=1

	if(hv['condtype']=='round'):
		hv_eddy_ef1=0.4
	else:
		hv_eddy_ef1=1

	if(lv['material']=='copper'):
		displacement_ef1=8.9
		covered_wt_lv_ef2=8.9
		lv_cond_wt_ef=8.9
		lv_resi_ph_ef=2.1
		lv_eddy_ef=9
		lvflatqty_ef=8.9
		maxtemplv_ef=235
		maxtemplv_ef2=106000
	else:
		displacement_ef1=2.7
		covered_wt_lv_ef2=2.7
		lv_cond_wt_ef=2.7
		lv_resi_ph_ef=3.46
		lv_eddy_ef=19
		lvflatqty_ef=2.7
		maxtemplv_ef2=45700
		maxtemplv_ef=225

	if(hv['material']=='copper'):
		displacement_ef2=8.9
		covered_wt_hv_ef2=8.9
		hv_cond_wt_ef=8.9
		hv_resi_ph_ef=2.1
		hv_eddy_ef=9
		maxtemphv_ef=235
		maxtemphv_ef2=106000
	else:
		displacement_ef2=2.7
		covered_wt_hv_ef2=2.7
		hv_cond_wt_ef=2.7
		hv_resi_ph_ef=3.46
		hv_eddy_ef=19
		maxtemphv_ef2=45700
		maxtemphv_ef=225

	if(basic['phases']=='3'):
		lv_cond_wt_pf=3
		hv_cond_wt_pf=3
		l2r_loss_pf=3
	else:
		lv_cond_wt_pf=1
		hv_cond_wt_pf=1
		l2r_loss_pf=1

	if(basic['rating']<315):
		loop_mlt_ef=15
	else:
		loop_mlt_ef=20

	if(cooling['type']=='Corrugation'):
		if('L' in cooling['corrgside']):
			tdef1=2-int(cooling['corrgside'][cooling['corrgside'].index('L')-1:1])
		else:
			tdef1=2
		if('W' in cooling['corrgside']):
			tdef2=2-int(cooling['corrgside'][cooling['corrgside'].index('W')-1:1])
		else:
			tdef2=2
	else:
		tdef1=2
		tdef2=2

	tapping_lst=range(tapping['min'],tapping['max'],(tapping['step']))
	maxtap_err=0
	maxhvt=0
	minhvt=0
	for tapper in tapping_lst:
		hvphn=round(hv['phvolt']*(1+tapper/100))
		nhvturns=round(lvtmain*hvphn/lv['phvolt'])
		if(maxhvt==0 or nhvturns>maxhvt):
			maxhvt=nhvturns
		if(minhvt==0 or nhvturns<minhvt):
			minhvt=nhvturns
		turerr=round((nhvturns/lvtmain),4)
		volrr=round((hvphn/lv['phvolt']),4)
		taperr=round(((volrr-turerr)*100/volrr),4)
		if(math.fabs(taperr)>math.fabs(maxtap_err)):
			maxtap_err=taperr

	#get_rated_hvturns
	get_rated_hvturns=round(test['lvtmain']*hv['phvolt']/lv['phvolt'])
	output['get_rated_hvturns']=get_hvturns

	#get_hvturns
	if(tapping['yn']=='yes'):
		get_hvturns=maxhvt
	else:
		get_hvturns=get_rated_hvturns
	output['get_hvturns']=get_hvturns

	#get_minhvturns
	if(tapping['yn']=='yes'):
		get_minhvturns=minhvt
	else:
		get_minhvturns=get_rated_hvturns
	output['get_minhvturns']=get_minhvturns

	#get_hv_coils
	get_hv_coils=hv['mcoils']+hv['tcoils']
	output['get_hv_coils']=get_hv_coils

	#lv_axial_elect
	lv_axial_elect=round(((test['lvwmain']+lv['coveringthk'])*((test['lvtmain']/lv['nolayers']*lv['flats'])+lv['transpos'])),2)
	output['lv_axial_elect']=lv_axial_elect

	#lv_axial_phy
	lv_axial_phy=math.ceil((test['lvwmain']+lv['coveringthk'])*((((test['lvtmain']/lv['nolayers'])+1)*lv['flats'])+lv['transpos']))
	output['lv_axial_phy']=lv_axial_phy

	#lv_axial_pack
	lv_axial_pack=lv_axial_phy+(cca['lvedge']*2)
	output['lv_axial_pack']=lv_axial_pack

	#get_hv_turn_layer
	if(hv['condtype']=='round'):
		get_hv_turn_layer=math.floor(((lv_axial_pack-(cca['hvedge']*2))/(test['hvwmain']+hv['coveringthk']))-1)
	output['get_hv_turn_layer']=get_hv_turn_layer

	#get_volt_turn
	if(lv['connectiontype']=='delta' or lv['connectiontype']=='delta_delta' or lv['connectiontype']=='series' or lv['connectiontype']=='parallel'):
		get_volt_turn=round((basic['lvvoltage']/test['lvtmain']),3)
	else:
		get_volt_turn=round((basic['lvvoltage']/(math.sqrt(3)*test['lvtmain'])),3)
	output['get_volt_turn']=get_volt_turn

	#get_turn_layer
	get_turn_layer=round((test['lvtmain']/lv['nolayers']),1)
	output['get_turn_layer']=get_turn_layer

	#hvdaihen
	if(hv['condtype']=='round' and hv['connectiontype']=='delta'):
		hvdaihen=((other['hvimpulse']*4.5*get_hv_turn_layer/get_hvturns)-(7*math.sqrt(test['hvwmain'])))/50
	elif(hv['condtype']=='round' and (hv['connectiontype']=='star'or hv['connectiontype']=='zigzag')):
		hvdaihen=((other['hvimpulse']*3.15*get_hv_turn_layer/get_hvturns)-(7*math.sqrt(test['hvwmain'])))/50
	elif(hv['condtype']=='rectangular' and hv['connectiontype']=='delta'):
		hvdaihen=((other['hvimpulse']*4.5*get_hv_turn_layer/get_hvturns)-(hv['coveringthk']))/50
	elif(hv['condtype']=='rectangular' and (hv['connectiontype']=='star'or hv['connectiontype']=='zigzag')):
		hvdaihen=((other['hvimpulse']*3.15*get_hv_turn_layer/get_hvturns)-(hv['coveringthk']))/50
	output['hvdaihen']=hvdaihen

	#hvssel
	if(hv['coveringmat']=='dpc' and (hv['condtype']=='round' or hv['condtype']=='rectangular')):
		hvssel=(4*get_volt_turn*get_hv_turn_layer/6000)-hv['coveringthk']
	elif(hv['coveringmat']=='enamel' and hv['condtype']=='round'):
		hvssel=(((4*get_volt_turn*get_hv_turn_layer)-1500)/6000)
	elif(hv['coveringmat']=='enamel' and hv['condtype']=='rectangular'):
		hvssel=(((4*get_volt_turn*get_hv_turn_layer)-500)/6000)
	output['hvssel']=hvssel

	#lvdaihen
	if(lv['condtype']=='round' and lv['connectiontype']=='delta'):
		lvdaihen=((other['lvimpulse']*4.5*get_turn_layer/test['lvtmain'])-(7*math.sqrt(test['lvwmain'])))/50
	elif(lv['condtype']=='round' and (lv['connectiontype']=='star' or lv['connectiontype']=='zigzag')):
		lvdaihen=((other['lvimpulse']*3.15*get_turn_layer/test['lvtmain'])-(7*math.sqrt(test['lvwmain'])))/50
	elif(lv['condtype']=='rectangular' and lv['connectiontype']=='delta'):
		lvdaihen=((other['lvimpulse']*4.5*get_turn_layer/test['lvtmain'])-(lv['coveringthk']))/50
	elif(lv['condtype']=='rectangular' and (lv['connectiontype']=='star' or lv['connectiontype']=='zigzag')):
		lvdaihen=((other['lvimpulse']*3.15*get_turn_layer/test['lvtmain'])-(lv['coveringthk']))/50
	output['lvdaihen']=lvdaihen

	#lvssel
	if(lv['coveringmat']=='dpc' and (lv['condtype']=='round' or lv['condtype']=='rectangular')):
		lvssel=(4*get_volt_turn*get_turn_layer/6000)-lv['coveringthk']
	elif(lv['coveringmat']=='enamel' and lv['condtype']=='round'):
		lvssel=(((4*get_volt_turn*get_turn_layer)-1500)/6000)
	elif(lv['coveringmat']=='enamel' and lv['condtype']=='rectangular'):
		lvssel=(((4*get_volt_turn*get_turn_layer)-500)/6000)
	output['lvssel']=lvssel

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
			get_lv_insu=round(math.ceil(get_lv_insu_out/0.025)*0.025,3)
	output['get_lv_insu']=get_lv_insu

	#get_hv_insu
	if(other['hvimpulse']<=95):
		get_hv_insu_out=hvdaihen if (hvdaihen<hvssel) else hvssel
	else:
		get_hv_insu_out=hvdaihen
	if(get_hv_insu_out<0.15):
		get_hv_insu=0.15
	else:
		get_hv_insu=round(math.ceil(get_hv_insu_out/0.025)*0.025,3)
	output['get_hv_insu']=get_hv_insu

	#get_mandril_a
	if(basic['rating']<=100):
		get_mandril_a=test['cmain']+7+cca['mandrila']
	else:
		get_mandril_a=test['cmain']+8+cca['mandrila']
	output['get_mandril_a']=get_mandril_a

	#get_stack_thk
	get_stack_thk=(get_volt_turn*1000000)/(4.44*basic['frequency']*test['fmain']*get_stack_thk_ef*test['cmain'])
	get_stack_thk_out=math.ceil(get_stack_thk/core['platethk'])
	get_stack_thk_bytwo=get_stack_thk_out%2;
	if(get_stack_thk_bytwo!=0):
		get_stack_thk_out=get_stack_thk_out-1;
	get_stack_thk=round((get_stack_thk_out*core['platethk']),2)
	act_flx_d=(get_volt_turn*1000000)/(4.44*basic['frequency']*get_stack_thk*get_stack_thk_ef*test['cmain'])
	fl1=math.floor(act_flx_d*100)/100
	fl2=math.ceil(act_flx_d*100)/100
	watt_kg1=float(watt_kg_table[core['grade']][str(fl1)][str(basic['frequency'])])
	watt_kg2=float(watt_kg_table[core['grade']][str(fl2)][str(basic['frequency'])])
	watt_kg=round((watt_kg1+((watt_kg2-watt_kg1)/(fl2-fl1))*(act_flx_d-fl1)),4)
	#watt_kg=float(watt_kg_table[core['grade']][str(test['fmain'])][str(basic['frequency'])])
	output['watt_kg']=watt_kg
	output['get_stack_thk']=get_stack_thk
	legdia=get_stack_thk/test['cmain']
	if(legdia<check['minlegdia'] or legdia>check['maxlegdia']):
		# print 'legdiafail'
		return 0

	#get_mandril_b
	if(core['subtype']=='CRGO'):
		if(basic['rating']<=63):
			get_mandril_b=math.ceil((get_stack_thk+8+cca['mandrilb'])*2)/2
		elif(basic['rating']<=100):
			get_mandril_b=math.ceil((get_stack_thk+9+cca['mandrilb'])*2)/2
		else:
			get_mandril_b=math.ceil((get_stack_thk+10+cca['mandrilb'])*2)/2
	else:
		get_mandril_b=math.ceil((get_stack_thk+4+cca['mandrilb'])*2)/2
	output['get_mandril_b']=get_mandril_b

	#get_hv_nolayers
	get_hv_nolayers=(get_hvturns/get_hv_coils)/(get_hv_turn_layer);
	get_hv_nolayers_c=math.ceil(get_hv_nolayers);
	get_hv_nolayers_b=((get_hv_nolayers_c*get_hv_turn_layer)-(get_hvturns/get_hv_coils))/get_hv_nolayers_c
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
	elif(test['hvwmain']>1.5):
		if(get_hv_nolayers_b<2):
			get_hv_nolayers=get_hv_nolayers_c+1
		else:
			get_hv_nolayers=get_hv_nolayers_c
	output['get_hv_nolayers']=get_hv_nolayers

	#rdlv
	rdlv=((test['lvkmain']+lv['coveringthk'])*lv['radials']*lv['nolayers'])+(get_lv_insu*(lv['nolayers']-1))+(lv['fullthk']*lv['nofull'])
	output['rdlv']=rdlv
	
	#lv_rd
	lv_rd=ceiling(rdlv)
	output['lv_rd']=lv_rd

	#rdhv
	rdhv=((test['hvkmain']+hv['coveringthk'])*hv['radials']*get_hv_nolayers)+(get_hv_insu*(get_hv_nolayers-1-hv['nofull']))+((hv['fullthk']+0.25)*hv['nofull'])
	output['rdhv']=rdhv

	#hv_rd
	hv_rd=ceiling(rdhv)
	output['hv_rd']=hv_rd

	#lv_lmt
	lv_lmt=round((2*(get_mandril_a+get_mandril_b-(4*lv_lmt_ef))+2*math.pi*(lv_lmt_ef+cca['corelvgap']+(lv_rd*0.5))+2*(lv['nofnb']*(lv['fnbthk']+0.125))),3)
	output['lv_lmt']=lv_lmt

	#hv_lmt
	hv_lmt=round((2*(get_mandril_a+get_mandril_b-(4*hv_lmt_ef))+2*math.pi*(hv_lmt_ef+cca['corelvgap']+lv_rd+test['lvhmain']+(hv_rd*0.5))+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25))),3)
	output['hv_lmt']=hv_lmt

	#hv_rd_nonlead
	hv_rd_nonlead=ceiling(rdhv*1.02)
	output['hv_rd_nonlead']=hv_rd_nonlead

	#lv_rd_nonlead
	lv_rd_nonlead=ceiling(rdlv*1.02)
	output['lv_rd_nonlead']=lv_rd_nonlead

	#get_small_loop_ww
	if(core['subtype']=='CRGO' and core['structure']=='Shell'):
		get_small_loop_ww=math.ceil(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead+cca['hvend'])
	elif(core['subtype']=='CRGO' and core['structure']=='Core'):
		get_small_loop_ww=math.ceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap'])
	if(core['subtype']=='Amorphous' and core['structure']=='Shell'):
		get_small_loop_ww=math.ceil(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead+cca['hvend']+2)
	elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
		get_small_loop_ww=math.ceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']+4)
	output['get_small_loop_ww']=get_small_loop_ww

	#get_big_loop_ww
	if(core['subtype']=='CRGO' and core['structure']=='Shell'):
		get_big_loop_ww=math.ceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap'])
	elif(core['subtype']=='CRGO' and core['structure']=='Core'):
		if(basic['rating']<=63):
			get_big_loop_ww_ef=8
		elif(basic['rating']<=100):
			get_big_loop_ww_ef=9
		else:
			get_big_loop_ww_ef=10
		get_big_loop_ww=math.ceil((get_small_loop_ww*2)+(get_stack_thk*2)+get_big_loop_ww_ef)
	elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
		get_big_loop_ww=math.ceil(2*(cca['corelvgap']+lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']+4)
	elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
		get_big_loop_ww=math.ceil((get_small_loop_ww*2)+(get_stack_thk*2)+6)
	output['get_big_loop_ww']=get_big_loop_ww
	if(get_big_loop_ww<check['minlegcenter'] or get_big_loop_ww>check['maxlegcenter']):
		# print 'bigwindowww'
		return 0

	#hv_rd_lead
	if(tapping['yn']=="no"):
		hv_rd_lead=ceiling((rdhv+((hv['fnbthk']+0.25)*hv['nofnb']))*1.05)
	else:
		hv_rd_lead=ceiling(((rdhv+((hv['fnbthk']+0.25)*hv['nofnb']))*1.05)+1.5)
	output['hv_rd_lead']=hv_rd_lead

	#lv_rd_lead
	if(basic['rating']<=40):
		lv_rd_lead=ceiling(rdlv+((lv['fnbthk']+0.125)*lv['nofnb'])+1.2)
	else:
		lv_rd_lead=ceiling((rdlv+((lv['fnbthk']+0.125)*lv['nofnb'])+1.2)*1.02)
	output['lv_rd_lead']=lv_rd_lead

	#get_lv_id_b
	get_lv_id_b=get_mandril_b+(cca['corelvgap']*2)
	output['get_lv_id_b']=get_lv_id_b

	#get_lv_id_a
	get_lv_id_a=get_mandril_a+(cca['corelvgap']*2)
	output['get_lv_id_a']=get_lv_id_a

	#get_lv_od_b
	get_lv_od_b=(get_lv_id_b)+(lv_rd_nonlead*2)
	output['get_lv_od_b']=get_lv_od_b

	#get_lv_od_a
	get_lv_od_a=(get_lv_id_a)+(lv_rd_lead*2);
	output['get_lv_od_a']=get_lv_od_a

	#get_hv_id_b
	get_hv_id_b=get_lv_od_b+(test['lvhmain']*2)
	output['get_hv_id_b']=get_hv_id_b

	#get_hv_id_a
	get_hv_id_a=get_lv_od_a+(test['lvhmain']*2)
	output['get_hv_id_a']=get_hv_id_a

	#get_hv_od_b
	get_hv_od_b=(get_hv_id_b)+(hv_rd_nonlead*2)
	output['get_hv_od_b']=get_hv_od_b

	#get_hv_od_a
	get_hv_od_a=(get_hv_id_a)+(hv_rd_lead*2)
	output['get_hv_od_a']=get_hv_od_a

	#tank_length
	if(core['structure']=='Shell'):
		tank_length=math.ceil(((get_big_loop_ww+get_small_loop_ww)*2+(get_stack_thk*4)+22+(2*tank['hvlength']))/5)*5
	else:
		tank_length=math.ceil(((3*get_hv_od_b)+(2*cca['hvhvgap'])+(2*tank['hvlength']))/5)*5
	output['tank_length']=tank_length
	if(tank_length<check['mintanklength'] or tank_length>check['maxtanklength']):
		# print 'tanklen'
		return 0

	#tank_breadth
	tank_breadth=math.ceil((get_hv_od_a+tank['hvwidth']+tank['lvwidth'])/5)*5
	output['tank_breadth']=tank_breadth
	if(tank_breadth<check['mintankwidth'] or tank_breadth>check['maxtankwidth']):
		# print 'tank wd'
		return 0

	#hv_axial_elect
	hv_axial_elect=(test['hvwmain']+hv['coveringthk'])*get_hv_turn_layer
	output['hv_axial_elect']=hv_axial_elect

	#hv_axial_phy
	hv_axial_phy=math.ceil(hv_axial_elect+test['hvwmain']+hv['coveringthk'])
	output['hv_axial_phy']=hv_axial_phy

	#hv_axial_pack
	hv_axial_pack=hv_axial_phy+(cca['hvedge']*2)
	output['hv_axial_pack']=hv_axial_pack

	#get_window_height
	if(core['subtype']=='CRGO' and core['structure']=='Shell'):
		get_window_height=math.ceil(hv_axial_pack+cca['coilyokegap']+cca['coilyokegap2']+8)
	elif(core['subtype']=='CRGO' and core['structure']=='Core'):
		get_window_height1=math.ceil(hv_axial_pack+cca['coilyokegap']+cca['coilyokegap2']+8)
		get_window_height2=math.ceil(get_window_height1+get_stack_thk+2)
		if(get_window_height1>get_window_height2):
			get_window_heightbig=get_window_height1
			get_window_heightsmall=get_window_height2
		else:
			get_window_heightbig=get_window_height2
			get_window_heightsmall=get_window_height1
	elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
		get_window_height=math.ceil(hv_axial_pack+cca['coilyokegap']+cca['coilyokegap2']+13)
	elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
		get_window_height1=math.ceil(hv_axial_pack+cca['coilyokegap']+cca['coilyokegap2']+13)
		get_window_height2=math.ceil(get_window_height1+(get_stack_thk*1.3)+2)
		if(get_window_height1>get_window_height2):
			get_window_heightbig=get_window_height1
			get_window_heightsmall=get_window_height2
		else:
			get_window_heightbig=get_window_height2
			get_window_heightsmall=get_window_height1
	if(core['structure']=='Shell'):
		if(get_window_height<check['minleglnth'] or get_window_height>check['maxleglnth']):
			output['get_window_height']=get_window_height
			# print'wind ht'
			return 0
	else:
		if(get_window_heightbig<check['minleglnth'] or get_window_heightbig>check['maxleglnth']):
			output['get_window_heightbig']=get_window_heightbig
			output['get_window_heightsmall']=get_window_heightsmall
			# print 'wind ht'
			return 0

	#noiselvl
	if(core['structure']=='Shell'):
		noiselvldata=get_window_height
	else:
		noiselvldata=get_window_heightbig
	noiselvl=round((39.2+(10*(math.log10(noiselvldata/100)))+(20*(math.log10((1.35*act_flx_d*2)-2.51)))),2)
	if(noiselvl<check['minnoise'] or noiselvl>check['maxnoise']):
		# print 'noise'
		return 0

	#tank_height
	if(core['structure']=='Shell'):
		tank_height_data=get_window_height
	else:
		tank_height_data=get_window_heightbig
	if(tank['type']=='sealed'):
		tank_height=round(tank['ccabot']+(cca['clampthk']*2)+10+tank_height_data+((1+tank_height_ef)*get_stack_thk)+tank['oillvl'])
	else:
		tank_height=round(tank['ccabot']+(cca['clampthk']*2)+10+tank_height_data+((1+tank_height_ef)*get_stack_thk)+tank['ccatop'])
	output['tank_height']=tank_height

	#big_loop_mlt
	if(core['subtype']=='CRGO' and core['structure']=='Shell'):
		big_loop_mlt=round((2*(get_window_height+5.6)+(2*get_big_loop_ww)+(1.7*get_stack_thk)),2)
	elif(core['subtype']=='CRGO' and core['structure']=='Core'):
		big_loop_mlt=round((2*(get_window_height2+5.6)+(2*get_big_loop_ww)+(1.7*get_stack_thk)),2)
	elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
		big_loop_mlt=round((2*(get_window_height)+(2*get_big_loop_ww)-(52)+(2*math.pi*(6.5+get_stack_thk*0.25*1.1))+loop_mlt_ef),2)
	elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
		big_loop_mlt=round((2*(get_window_height2)+(2*get_big_loop_ww)-(52)+(2*math.pi*(6.5+get_stack_thk*0.25*1.1))+loop_mlt_ef),2)
	output['big_loop_mlt']=big_loop_mlt

	#small_loop_mlt
	if(core['subtype']=='CRGO' and core['structure']=='Shell'):
		small_loop_mlt=round((2*(get_window_height+5.6)+(2*get_small_loop_ww)+(1.7*get_stack_thk)),2)
	elif(core['subtype']=='CRGO' and core['structure']=='Core'):
		small_loop_mlt=round((2*(get_window_height1+5.6)+(2*get_small_loop_ww)+(1.7*get_stack_thk)),2)
	elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
		small_loop_mlt=round((2*(get_window_height)+(2*get_small_loop_ww)-(52)+(2*pi*(6.5+get_stack_thk*0.25*1.1))+loop_mlt_ef),2)
	elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
		small_loop_mlt=round((2*(get_window_height1)+(2*get_small_loop_ww)-(52)+(2*math.pi*(6.5+get_stack_thk*0.25*1.1))+loop_mlt_ef),2)
	output['small_loop_mlt']=small_loop_mlt

	#get_core_area
	get_core_area=round((test['cmain']*get_stack_thk*get_core_area_ef*0.01),3)
	output['get_core_area']=get_core_area
	if(get_core_area<check['mincorearea'] or get_core_area>check['maxcorearea']):
		# print 'core area'
		return 0

	#loop_wt
	big_loop_wt=round(((big_loop_mlt*loop_wt_ef*get_core_area)/10000),2)
	small_loop_wt=round(((small_loop_mlt*loop_wt_ef*get_core_area)/10000),2)
	output['big_loop_wt']=big_loop_wt
	output['small_loop_wt']=small_loop_wt

	#hv_cond_area
	if(hv['condtype']=='round'):
		hv_cond_area=round((math.pi*test['hvwmain']*test['hvwmain']/4),3)
	elif(hv['condtype']=='foil'):
		hv_cond_area=round((test['hvwmain']*test['hvkmain']*hv['radials']),3)
	else:
		if(test['hvkmain']>2.99):
			hv_cond_area_ef=0.9
		else:
			hv_cond_area_ef=0.5
		hv_cond_area=round((((test['hvwmain']*test['hvkmain'])-hv_cond_area_ef)*hv['flats']*hv['radials']),3)
	output['hv_cond_area']=hv_cond_area
	if(hv_cond_area<check['mincondhv'] or hv_cond_area>check['maxcondhv']):
		# print 'hv cond'
		return 0

	#lv_cond_area
	if(lv['condtype']=='round'):
		lv_cond_area=round((math.pi*test['lvwmain']*test['lvwmain']/4),3)
	elif(lv['condtype']=='foil'):
		lv_cond_area=round((test['lvwmain']*test['lvkmain']*lv['radials']),3)
	else:
		if(test['lvkmain']>2.99):
			lv_cond_area_ef=0.9
		else:
			lv_cond_area_ef=0.5
		lv_cond_area=round((((test['lvwmain']*test['lvkmain'])-lv_cond_area_ef)*lv['flats']*lv['radials']),3)
	output['lv_cond_area']=lv_cond_area
	if(lv_cond_area<check['mincondlv'] or lv_cond_area>check['maxcondlv']):
		# print 'lv cond'
		return 0

	#lv_cond_wt
	lv_cond_wt=round((lv_lmt*test['lvtmain']*lv_cond_wt_ef*lv_cond_area*lv_cond_wt_pf/1000000),2)
	output['lv_cond_wt']=lv_cond_wt

	#hv_cond_wt
	hv_cond_wt=round(((hv_lmt*get_hvturns*hv_cond_wt_ef*hv_cond_area*hv_cond_wt_pf)/1000000),2)
	output['hv_cond_wt']=hv_cond_wt

	#total_weight
	total_weight=big_loop_wt+small_loop_wt
	output['total_weight']=total_weight

	#top_core_clamp
	if(core['structure']=='Shell'):
		tcclength=round((2*(get_big_loop_ww+get_small_loop_ww))+(4*get_stack_thk)+34)
		tccwidth=round(get_hv_od_a+get_stack_thk+15)
	else:
		tcclength=round(get_big_loop_ww+(get_stack_thk)+22)
		tccwidth=round(get_hv_od_a+(2*get_stack_thk)+15)
	top_core_clamp=round(((tcclength*tccwidth*cca['clampthk']*7.85)/1000000),3)
	output['top_core_clamp']=top_core_clamp

	#bot_core_clamp
	if(core['structure']=='Shell'):
		bcclength=round((2*(get_big_loop_ww+get_small_loop_ww))+(4*get_stack_thk)+34)
		bccwidth=round(get_hv_od_a+(bot_core_clamp_kf*get_stack_thk)+15)
	else:
		bcclength=round(get_big_loop_ww+(get_stack_thk)+22)
		bccwidth=round(get_hv_od_a+(2*bot_core_clamp_kf*get_stack_thk)+15)
	bot_core_clamp=round(((bcclength*bccwidth*cca['clampthk']*7.85)/1000000),3)
	output['bot_core_clamp']=bot_core_clamp

	#tierod
	if(core['structure']=='Shell'):
		tieroddata=get_window_height
	else:
		tieroddata=get_window_heightsmall
	tierodlength=tieroddata+20+(cca['clampthk']*2)+60;
	tierod=round((((math.pi)/4)*cca['tierods']*cca['tierods']*7.85*8*tierodlength/1000000),3)
	output['tierod']=tierod

	#covered_wt_lv
	if(lv['condtype']=='round'):
		lvcoveredthk=test['lvkmain']+lv['coveringthk']
		covered_wt_lv=round((((((lvcoveredthk*lvcoveredthk)-(test['lvkmain']*test['lvkmain']))*covered_wt_lv_ef1/((test['lvkmain']*test['lvkmain'])*covered_wt_lv_ef2))*(lv_cond_wt))+lv_cond_wt),2)
	else:
		lvcoverwith=test['lvwmain']+lv['coveringthk']
		lvcoverthk=test['lvkmain']+lv['coveringthk']
		if(lvcoverthk>2.99):
			covered_wt_lv_ef=0.9
		else:
			covered_wt_lv_ef=0.5
		lvcoverarea=((lvcoverthk*lvcoverwith)-covered_wt_lv_ef)*lv['flats']*lv['radials']
		covered_wt_lv=round(((((lvcoverarea-lv_cond_area)*covered_wt_lv_ef1/(lv_cond_area*covered_wt_lv_ef2))*(lv_cond_wt))+lv_cond_wt),2)
	output['covered_wt_lv']=covered_wt_lv

	#covered_wt_hv
	if(hv['condtype']=='round'):
		hvcoveredthk=test['hvkmain']+hv['coveringthk']
		covered_wt_hv=round((((((hvcoveredthk*hvcoveredthk)-(test['hvkmain']*test['hvkmain']))*covered_wt_hv_ef1/((test['hvkmain']*test['hvkmain'])*covered_wt_hv_ef2))*(hv_cond_wt))+hv_cond_wt),2)
	else:
		hvcoverwith=test['hvwmain']+hv['coveringthk']
		hvcoverthk=test['hvkmain']+hv['coveringthk']
		if(hvcoverthk>2.99):
			covered_wt_hv_ef=0.9
		else:
			covered_wt_hv_ef=0.5
		hvcoverarea=((hvcoverthk*hvcoverwith)-covered_wt_hv_ef)*hv['flats']*hv['radials']
		covered_wt_hv=round(((((hvcoverarea-hv_cond_area)*covered_wt_hv_ef1/(hv_cond_area*covered_wt_hv_ef2))*(hv_cond_wt))+hv_cond_wt),2)
	output['covered_wt_hv']=covered_wt_hv

	#phase_hv
	if(hv['connectiontype']=='star' or hv['connectiontype']=='zigzag'):
		phase_hv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['hvvoltage'])),4)
	elif(hv['connectiontype']=='delta'):
		phase_hv=round(((basic['rating']*1000)/(3*basic['hvvoltage'])),4)
	elif(hv['connectiontype']=='series' or hv['connectiontype']=='parallel'):
		phase_hv=round(((basic['rating']*1000)/(basic['hvvoltage'])),4)
	output['phase_hv']=phase_hv

	#phase_lv
	if(lv['connectiontype']=='star' or lv['connectiontype']=='zigzag'):
		phase_lv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['lvvoltage'])),4)
	elif(lv['connectiontype']=='delta'):
		phase_lv=round(((basic['rating']*1000)/(3*basic['lvvoltage'])),4)
	elif(lv['connectiontype']=='series' or lv['connectiontype']=='parallel'):
		phase_lv=round(((basic['rating']*1000)/(basic['lvvoltage'])),4)
	output['phase_lv']=phase_lv

	ampturns=round(((math.fabs(((test['lvtmain']*phase_lv/lv_axial_elect)-(get_hvturns*phase_hv/hv_axial_elect))/(test['lvtmain']*phase_lv/lv_axial_elect)))*100),2)
	if(ampturns<check['minampturns'] or ampturns>check['maxampturns']):
		# print 'amp turns'
		return 0

	#line_hv
	if(hv['connectiontype']=='series' or hv['connectiontype']=='parallel'):
		line_hv=round(((basic['rating']*1000)/(basic['hvvoltage'])),4)
	else:
		line_hv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['hvvoltage'])),4)
	output['line_hv']=line_hv

	#line_lv
	if(lv['connectiontype']=='series' or lv['connectiontype']=='parallel'):
		line_lv=round(((basic['rating']*1000)/(basic['lvvoltage'])),4)
	else:
		line_lv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['lvvoltage'])),4)
	output['line_lv']=line_lv

	#get_lv_hv_mlt
	get_lv_hv_mlt=round((2*(get_mandril_a+get_mandril_b-(4*hv_lmt_ef))+2*math.pi*(hv_lmt_ef+cca['corelvgap']+lv_rd+test['lvhmain']*0.5)+4*(lv['nofnb']*(lv['fnbthk']+0.125))),3)
	output['get_lv_hv_mlt']=get_lv_hv_mlt

	#lv_fnb_perimeter
	lv_fnb_perimeter=get_mandril_b+math.pi*0.5*(lv_lmt_ef+cca['corelvgap']+(lv_rd*0.5))
	output['lv_fnb_perimeter']=lv_fnb_perimeter

	#lv_id_perimeter
	lv_id_perimeter=round((2*(get_mandril_a+get_mandril_b-(4*lv_lmt_ef))+2*math.pi*(lv_lmt_ef+cca['corelvgap'])),3)
	output['lv_id_perimeter']=lv_id_perimeter

	#hv_od_perimeter
	hv_od_perimeter=round((2*(get_mandril_a+get_mandril_b-(4*hv_lmt_ef))+2*math.pi*(hv_lmt_ef+cca['corelvgap']+lv_rd+test['lvhmain']+(hv_rd))+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25))),3)
	output['hv_od_perimeter']=hv_od_perimeter

	#lv_od_perimeter
	lv_od_perimeter=round((2*(get_mandril_a+get_mandril_b-(4*lv_lmt_ef))+2*math.pi*(lv_lmt_ef+cca['corelvgap']+(lv_rd))+2*(lv['nofnb']*(lv['fnbthk']+0.125))),3)
	output['lv_od_perimeter']=lv_od_perimeter

	#hv_id_perimeter
	hv_id_perimeter=round((2*(get_mandril_a+get_mandril_b-(4*hv_lmt_ef))+2*math.pi*(hv_lmt_ef+cca['corelvgap']+lv_rd+test['lvhmain'])+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25))),3)
	output['hv_id_perimeter']=hv_id_perimeter

	#lv_inner_duct_cooling_area
	lv_no_full_duct_runners=lv_lmt/30
	lv_no_fnb_duct_runners=lv_fnb_perimeter/30
	lv_full_duct_area=(lv_lmt-(10*lv_no_full_duct_runners))*lv_axial_phy*2/1000000*lv['nofull']
	lv_fnb_duct_area=(lv_fnb_perimeter-(10*lv_no_fnb_duct_runners))*lv_axial_phy*4/1000000*lv['nofnb']
	lv_inner_duct_cooling_area=lv_full_duct_area+lv_fnb_duct_area
	output['lv_inner_duct_cooling_area']=lv_inner_duct_cooling_area

	#lv_outer_duct_cooling_area
	lv_no_full_duct_runners_inside=lv_id_perimeter/30
	lv_no_full_duct_runners_outside=lv_od_perimeter/30
	lv_full_duct_area_inside=(lv_id_perimeter-10*lv_no_full_duct_runners_inside)*lv_axial_phy/1000000
	lv_full_duct_area_outside=(lv_od_perimeter-10*lv_no_full_duct_runners_outside)*lv_axial_phy/1000000
	lv_outer_duct_cooling_area=0;
	if(lv['coreduct']==True):
		lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+lv_full_duct_area_inside
	if(lv['lvhvod']==True):
		lv_outer_duct_cooling_area=lv_outer_duct_cooling_area+lv_full_duct_area_outside
	output['lv_outer_duct_cooling_area']=lv_outer_duct_cooling_area

	#lv_total_duct_cooling_area
	if(basic['phases']=='3'):
		lv_total_duct_cooling_area_ef=3
	else:
		if(core['structure']=='Core'):
			lv_total_duct_cooling_area_ef=2
		else:
			lv_total_duct_cooling_area_ef=1
	lv_total_duct_cooling_area=(lv_inner_duct_cooling_area+lv_outer_duct_cooling_area)*lv_total_duct_cooling_area_ef
	output['lv_total_duct_cooling_area']=lv_total_duct_cooling_area

	#hv_fnb_perimeter
	hv_fnb_perimeter=get_mandril_b+math.pi*0.5*(hv_lmt_ef+cca['corelvgap']+lv_rd+test['lvhmain']+(hv_rd*0.5))
	output['hv_fnb_perimeter']=hv_fnb_perimeter

	#hv_inner_duct_cooling_area
	hv_no_full_duct_runners=hv_lmt/30
	hv_no_fnb_duct_runners=hv_fnb_perimeter/30
	hv_full_duct_area=(hv_lmt-(10*hv_no_full_duct_runners))*hv_axial_phy*2/1000000*hv['nofull']
	hv_fnb_duct_area=(hv_fnb_perimeter-(10*hv_no_fnb_duct_runners))*hv_axial_phy*4/1000000*hv['nofnb']
	hv_inner_duct_cooling_area=hv_full_duct_area+hv_fnb_duct_area
	output['hv_inner_duct_cooling_area']=hv_inner_duct_cooling_area

	#hv_outer_duct_cooling_area
	hv_no_full_duct_runners_inside=hv_id_perimeter/30
	hv_no_full_duct_runners_outside=hv_od_perimeter/30
	hv_full_duct_area_inside=(hv_id_perimeter-10*hv_no_full_duct_runners_inside)*hv_axial_phy/1000000
	hv_full_duct_area_outside=(hv_od_perimeter-10*hv_no_full_duct_runners_outside)*hv_axial_phy/1000000
	if(hv['lvhvid']==True):
		hv_outer_duct_cooling_area=hv_full_duct_area_inside+hv_full_duct_area_outside
	else:
		rhv_outer_duct_cooling_area=hv_full_duct_area_outside
	output['hv_outer_duct_cooling_area']=hv_outer_duct_cooling_area

	#hv_total_duct_cooling_area
	if(basic['phases']=='3'):
		hv_total_duct_cooling_area_ef=3
	else:
		if(core['structure']=='Core'):
			hv_total_duct_cooling_area_ef=2
		else:
			hv_total_duct_cooling_area_ef=1
	hv_total_duct_cooling_area=(hv_inner_duct_cooling_area+hv_outer_duct_cooling_area)*hv_total_duct_cooling_area_ef
	output['hv_total_duct_cooling_area']=hv_total_duct_cooling_area

	#lv_resi_ph
	lv_resi_ph=round((lv_resi_ph_ef*lv_lmt*test['lvtmain']/(100000*lv_cond_area)),6)
	output['lv_resi_ph']=lv_resi_ph

	#hv_resi_ph
	hv_resi_ph=round((hv_resi_ph_ef*hv_lmt*get_hvturns/(100000*hv_cond_area)),6)
	output['hv_resi_ph']=hv_resi_ph

	#lv_cd
	lv_cd=round((phase_lv/lv_cond_area),4)
	output['lv_cd']=lv_cd
	if(lv_cd<check['mincdlv'] or lv_cd>check['maxcdlv']):
		# print 'lvcd'
		return 0

	#hv_cd
	hv_cd=round((phase_hv/hv_cond_area),4)
	output['hv_cd']=hv_cd
	if(hv_cd<check['mincdhv'] or hv_cd>check['maxcdhv']):
		# print 'hvcd'
		return 0

	#lv_l2r_loss
	lv_l2r_loss=round(l2r_loss_pf*phase_lv*phase_lv*lv_resi_ph*2)/2
	output['lv_l2r_loss']=lv_l2r_loss

	#hv_l2r_loss
	hv_l2r_loss=round(l2r_loss_pf*phase_hv*phase_hv*hv_resi_ph*2)/2
	output['hv_l2r_loss']=hv_l2r_loss

	#bfactor_eddy
	bfactor_eddy=phase_lv*test['lvtmain']*1.78/(1000*(lv_axial_elect+hv_axial_elect)*0.5)
	output['bfactor_eddy']=bfactor_eddy

	#lv_eddy
	lv_eddy=round((lv_eddy_ef1*lv_eddy_ef*basic['frequency']*basic['frequency']*bfactor_eddy*bfactor_eddy*test['lvkmain']*test['lvkmain']*lv_cond_wt/1000),1)
	output['lv_eddy']=lv_eddy

	#hv_eddy
	hv_eddy=round((hv_eddy_ef1*hv_eddy_ef*basic['frequency']*basic['frequency']*bfactor_eddy*bfactor_eddy*test['hvkmain']*test['hvkmain']*hv_cond_wt/1000),1)
	output['hv_eddy']=hv_eddy

	#lv_bushing
	if(basic['rating']<=400):
		lv_bushing_ef=1
	else:
		lv_bushing_ef=0.5
	lv_bushing=round((math.pow(line_lv,1.25)*0.045*lv_bushing_ef),1)
	output['lv_bushing']=lv_bushing

	#lead_wire_loss_lv
	lead_wire_loss_lv=round((0.02*lv_l2r_loss),2)
	output['lead_wire_loss_lv']=lead_wire_loss_lv

	#lv_misc_loss
	lv_misc_loss=round(((lv_l2r_loss+lv_bushing+lead_wire_loss_lv+lv_eddy)*1.5/100),1)
	output['lv_misc_loss']=lv_misc_loss

	#hv_bushing
	hv_bushing=round((math.pow(line_hv,1.25)*0.045),1)
	output['hv_bushing']=hv_bushing

	#lead_wire_loss_hv
	lead_wire_loss_hv=round((0.005*hv_l2r_loss),1)
	output['lead_wire_loss_hv']=lead_wire_loss_hv

	#hv_misc_loss
	hv_misc_loss=round(((hv_l2r_loss+hv_bushing+lead_wire_loss_hv+hv_eddy)*1.5/100),1)
	output['hv_misc_loss']=hv_misc_loss

	#lv_stray_loss
	lv_stray_loss=round((lv_eddy+lv_bushing+lead_wire_loss_lv+lv_misc_loss),1)
	output['lv_stray_loss']=lv_stray_loss

	#hv_stray_loss
	hv_stray_loss=round((hv_eddy+hv_bushing+lead_wire_loss_hv+hv_misc_loss),1)
	output['hv_stray_loss']=hv_stray_loss

	#total_stray_loss
	total_stray_loss=round((lv_stray_loss+hv_stray_loss),2)
	output['total_stray_loss']=total_stray_loss

	#lv_watt_dissipation
	lv_watt_dissipation=round(((lv_l2r_loss+lv_eddy)*0.01/lv_total_duct_cooling_area),3)
	output['lv_watt_dissipation']=lv_watt_dissipation

	#hv_watt_dissipation
	hv_watt_dissipation=round(((hv_l2r_loss+hv_eddy)*0.01/hv_total_duct_cooling_area),3)
	output['hv_watt_dissipation']=hv_watt_dissipation

	#lv_gradient
	lv_gradient=math.ceil(((0.0016*lv_axial_phy)+1.78)*math.pow(lv_watt_dissipation,0.8)*1.15*2)/2
	output['lv_gradient']=lv_gradient
	if(lv_gradient<check['minlvgradient'] or lv_gradient>check['maxlvgradient']):
		# print 'lv grad'
		return 0

	#hv_gradient
	hv_gradient=math.ceil(((0.0016*hv_axial_phy)+1.78)*math.pow(hv_watt_dissipation,0.8)*1.15*2)/2
	output['hv_gradient']=hv_gradient
	if(hv_gradient<check['minhvgradient'] or hv_gradient>check['maxhvgradient']):
		# print 'hv grad'
		return 0

	#no_load_losses
	no_load_losses=round((total_weight*core['factor']*watt_kg),2)
	cal_no_load_losses=other['noload1']*(100-other['noload2'])/100
	if(cal_no_load_losses<=no_load_losses):
		no_load_check=False
		# print no_load_losses
		# print cal_no_load_losses
		# print 'nll'
		return 0
	else:
		no_load_check=True

	#load_losses
	if(other['stray']==0):
		load_losses=lv_l2r_loss+hv_l2r_loss+lv_stray_loss+hv_stray_loss
	else:
		load_losses=lv_l2r_loss+hv_l2r_loss+other['stray']
	cal_load_losses=other['fullload1']*(100-other['fullload2'])/100
	if(cal_load_losses<=load_losses):
		load_check=False
		# print 'll'
		return 0
	else:
		load_check=True

	#efficiency
	efficiency=round((1-((no_load_losses+(load_losses*(check['maxloadfactor']/100)*(check['maxloadfactor']/100)))/((basic['rating']*check['maxloadfactor']*check['maxpf']*10)+(no_load_losses+(load_losses*(check['maxloadfactor']/100)*(check['maxloadfactor']/100)))))),2)
	if(efficiency<check['minefficiency'] or efficiency>check['maxefficiency']):
		# print 'eff'
		return 0


	#percentage_r
	percentage_r=round((load_losses*1000/(basic['rating']*10000)),3)
	output['percentage_r']=percentage_r

	#percentage_x_delta
	percentage_x_delta=(lv_lmt*lv_rd/(3*lv_axial_elect))+(hv_lmt*hv_rd/(3*hv_axial_elect))+(get_lv_hv_mlt*test['lvhmain']/(0.5*(lv_axial_elect+hv_axial_elect)))

	#percentage_x_k
	percentage_x_k=1-((lv_rd+test['lvhmain']+hv_rd)/(math.pi*0.5*(lv_axial_elect+hv_axial_elect)))

	#percentage_x
	percentage_x=round((8*math.pi*math.pi*basic['frequency']*phase_lv*test['lvtmain']*test['lvtmain']*percentage_x_k*percentage_x_delta*0.00000001/lv['phvolt']),2)
	output['percentage_x']=percentage_x

	#percentage_z
	percentage_z=round((math.sqrt((percentage_x*percentage_x)+(percentage_r*percentage_r))),3)
	if(percentage_z<check['minimpedance'] or percentage_z>check['maximpedance']):
		# print 'imp fail'
		return 0

	#lvcost
	lvcost=round((costing['lv']*covered_wt_lv*1.02),2)
	output['lvcost']=lvcost

	#hvcost
	hvcost=round((costing['hv']*covered_wt_hv*1.01),2)
	output['hvcost']=hvcost

	#corecost
	corecost=round((costing['core']*total_weight*1.01),2)
	output['corecost']=corecost

	#lvqty
	lvqty=round((covered_wt_lv*1.02),2)
	output['lvqty']=lvqty

	#hvqty
	hvqty=round((covered_wt_hv*1.01),2)
	output['hvqty']=hvqty

	#coreqty
	coreqty=round((total_weight*1.01),2)
	output['coreqty']=coreqty

	#displacement
	displacement=round(((total_weight/displacement_ef)+(covered_wt_lv/displacement_ef1)+(covered_wt_hv/displacement_ef2)+(cca['insuwt']/1.1)+((top_core_clamp+bot_core_clamp+tierod)/7.85)),3)
	output['displacement']=displacement

	#oil_main_tank
	oil_main_tank=round(((tank_length*tank_breadth*tank_height)/1000000),2)
	output['oil_main_tank']=oil_main_tank

	#topoilrise
	ccal=(other['windrise']-(other['oilrise'])*0.8)
	if(ccal>lv_gradient and ccal>hv_gradient):
		topoilrise=other['oilrise']
	else:
		if(lv_gradient>hv_gradient):
			topoilrise=(other['windrise']-lv_gradient)/0.8
		else:
			topoilrise=(other['windrise']-hv_gradient)/0.8
	output['topoilrise']=topoilrise

	#meanoilrise
	meanoilrise=topoilrise*0.8
	output['meanoilrise']=meanoilrise

	#tank_diss_upto_oil
	if(cooling['oildiss']==0):
		tank_diss_upto_oil=((tank_length*tdef1)+(tank_breadth*tdef2))*tank_height*meanoilrise*11/1000000
	else:
		return ((tdef1*tank_length)+(tdef2*tank_breadth))*tank_height*cooling['oildiss']/1000000
	output['tank_diss_upto_oil']=tank_diss_upto_oil

	#tank_height_m
	if(tank['type']=='sealed'):
		if(tank['tanklvl']=='yes'):
			tank_height_m=math.ceil((tank_height+tank['airlvl'])/5)*5
		else:
			tank_height_m=math.ceil((tank_height+((oil_main_tank-displacement)*tank['airlvl']*10000/(tank_length*tank_breadth)))/5)*5
	else:
		tank_height_m=math.ceil((tank_height)/5)*5
	output['tank_height_m']=tank_height_m

	#tank_diss_above_oil
	if(cooling['airdiss']==0):
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*meanoilrise*5.5/1000000
	else:
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*cooling['airdiss']/1000000
	output['tank_diss_above_oil']=tank_diss_above_oil

	#coolingreq
	if(cooling['cals']=='cal'):
		if((no_load_losses+load_losses)>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(no_load_losses+load_losses-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0
	else:
		if((other['noload1']+other['fullload1'])>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(other['noload1']+other['fullload1']-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0
	output['coolingreq']=coolingreq

	#oilincooling
	if(coolingreq==0):
		oilincooling=0
	else:
		if(cooling['type']=='Tube'):
			if(coolingreq==0):
				tubelength=0
			else:
				tubelength=round((coolingreq/(0.119*11*meanoilrise)),2)
			oilincooling=round(tubelength*0.95*100)/100
		elif(cooling['type']=='PressedRadiator'):
			#radbot
			if(cooling['auto']=='true'):
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
				radbot_v1=(tank['ccabot']+(get_stack_thk*0.5*(radbot_sf+radbot_cf))+cca['clampthk']+5)
				if(radbot_v1<=65):
					radbot=65
				else:
					radbot=radbot_v1
			else:
				radbot=cooling['radbottank']
			#radiatorht
			radiatorht=(tank_height-radbot-75)
			#radiatorhtf
			radiatorhtf=int(math.floor(radiatorht/100)*100)
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
			sfr_valf0=int(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f0)])
			sfr_valf1=int(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f1)])
			sfr=sfr_valf1-((sfr_valf1-sfr_valf0)/(sfr_f1-sfr_f0))*(sfr_f1-topoilrise)
			#vfr
			if(core['coretype']=='wound'):
				if(core['subtype']=="CRGO"):
					vfr_cf=0
				else:
					vfr_cf=0.3;
				if(core['structure']=='Shell'):
					vfr_data=get_window_height
					vfr_sf=1
				else:
					vfr_sf=2
					vfr_data=get_window_heightsmall
			vfr_vval=(radbot+(radiatorht-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(get_stack_thk*0.5*(vfr_sf+vfr_cf))+(vfr_data*0.5)+(cca['clampthk']+5))
			vfr_vval1=int(math.floor(vfr_vval/100)*100)
			vfr_vval2=int(math.ceil(vfr_vval/100)*100)
			if(vfr_vval<0):
				vfr=0.8
			else:
				vfr=float(vertical_table[str(vfr_vval2)])-((float(vertical_table[str(vfr_vval2)])-float(vertical_table[str(vfr_vval1)]))/(vfr_vval2-vfr_vval1))*(vfr_vval2-vfr_vval)
			#radhoriz
			if(cooling['auto']):
				if(cooling['norads']<=3):
					radhoriz=(tank_length-130)/cooling['norads']
				else:
					if(cooling['norads']%2==0):
						radhoriz=(tank_length-130)/cooling['norads']*2
					else:
						radhoriz=(((tank_length-130)/math.ceil(cooling['norads']*0.5))+((tank_length-130)/math.floor(cooling['norads']*0.5)))*0.5
			else:
				radhoriz=cooling['radhoriz']
			#hfr
			hfr_i=0
			hfr_j=0
			hfr_l=0
			hfr_m=0
			hfr_k=0
			for key,value in horizontal_table[str(cooling['radwidth'])].iteritems():
				if(radhoriz>=Decimal(key)):
					hfr_i=Decimal(value)
					hfr_l=Decimal(key)
				elif(radhoriz<Decimal(key)):
					if(hfr_k==0):
						hfr_j=Decimal(value)
						hfr_m=Decimal(key)
						hfr_k=1
			hfr=float(hfr_j)-((float(hfr_j)-float(hfr_i))/(float(hfr_m)-float(hfr_l)))*(float(hfr_m)-float(radhoriz))
			#no_elements
			if(coolingreq==0):
				no_elements=0
			else:
				no_elements=coolingreq/(sfr*vfr*hfr*cooling['norads'])
			#actual_elements
			ace=int(math.ceil(no_elements))
			if(ace<=2):
				actual_elements=math.ceil(no_elements/float(fins_table['2']))
			else:
				actual_elements=math.ceil(no_elements/float(fins_table[str(ace)]))
			oilincooling=round(actual_elements*cooling['norads']*radiator_oil*100)/100
		else:
			#corrgheight
			if(cooling['auto']):
				corrgheight=math.floor((tank_height-100)/50)*50
			else:
				corrgheight=cooling['corrght']
			#corrgarea
			if(coolingreq==0):
				corrgarea=0
			else:
				corrgfinnol=((2-tdef1)*math.ceil((tank_length-100)/cooling['corrgfindist']))
				corrgfingapl=corrgfinnol-(2-tdef1)
				corrgfinnow=(2-tdef2)*math.ceil((tank_breadth-100)/cooling['corrgfindist'])
				corrgfingapw=corrgfinnow-(2-tdef2)
				if(cooling['auto']=='true'):
					corrgfins=corrgfinnol+corrgfinnow
					corrggaps=corrgfingapl+corrgfingapw
				else:
					corrgfins=cooling['corrgfinsno']
					corrggaps=cooling['corrgfinsno']-(4-int(tdef1)-int(tdef2))
				gap_surf_area=corrggaps*cooling['corrgfindist']*corrgheight/1000000
				corrgarea=round(((coolingreq/(topoilrise*cooling['corrgwms']))-gap_surf_area),3)
			#corrgwm2
			corrgwm2=round((coolingreq/(topoilrise*float(cooling['corrgwms']))),2)
			#corrgdepth
			if(cooling['auto']=='true'):
				corrgdepth=math.ceil((corrgarea*1000000/(2*corrgfins*corrgheight))/5)*5
			else:
				corrgdepth=cooling['corrgdepth']
			oilincooling=(8*corrgheight*corrgdepth*corrgfins/1000000)
	output['oilincooling']=oilincooling

	#conservatoroil
	if(tank['type']=='conservator'):
		conservatoroil=round(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket'])*3)/100,2)
	else:
		conservatoroil=0
	output['conservatoroil']=conservatoroil

	#totoil
	totoil=round(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket']+conservatoroil)*1.03),2)
	output['totoil']=totoil

	#tank_height_m
	if(tank['type']=='sealed'):
		if(tank['tanklvl']=='yes'):
			tank_height_m=math.ceil((tank_height+tank['airlvl'])/5)*5
		else:
			tank_height_m=math.ceil((tank_height+((totoil)*tank['airlvl']*10000/(tank_length*tank_breadth)))/5)*5
	else:
		tank_height_m=math.ceil((tank_height)/5)*5
	output['tank_height_m']=tank_height_m
	if(tank_height_m<check['mintankheight'] or tank_height_m>check['maxtankheight']):
		# print 'tank ht'
		return 0

	#tank_diss_above_oil
	if(cooling['airdiss']==0):
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*meanoilrise*5.5/1000000
	else:
		tank_diss_above_oil=((tdef1*tank_length)+(tdef2*tank_breadth))*(tank_height_m-tank_height)*cooling['airdiss']/1000000
	output['tank_diss_above_oil']=tank_diss_above_oil

	#coolingreq
	if(cooling['cals']=='cal'):
		if((no_load_losses+load_losses)>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(no_load_losses+load_losses-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0
	else:
		if((other['noload1']+other['fullload1'])>(tank_diss_upto_oil+tank_diss_above_oil)):
			coolingreq=(other['noload1']+other['fullload1']-(tank_diss_upto_oil+tank_diss_above_oil))*(1+(cooling['extra']/100))
		else:
			coolingreq=0
	output['coolingreq']=coolingreq

	#oilincooling
	if(coolingreq==0):
		oilincooling=0
	else:
		if(cooling['type']=='Tube'):
			#tubelength
			if(coolingreq==0):
				tubelength=0
			else:
				tubelength=round((coolingreq/(0.119*11*meanoilrise)),2)
			oilincooling=round(tubelength*0.95*100)/100
		elif(cooling['type']=='PressedRadiator'):
			#radbot
			if(cooling['auto']=='true'):
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
				radbot_v1=(tank['ccabot']+(get_stack_thk*0.5*(radbot_sf+radbot_cf))+cca['clampthk']+5)
				if(radbot_v1<=65):
					radbot=65
				else:
					radbot=radbot_v1
			else:
				radbot=cooling['radbottank']
			#radiatorht
			radiatorht=(tank_height-radbot-75)
			#radiatorhtf
			radiatorhtf=int(math.floor(radiatorht/100)*100)
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
			sfr_valf0=int(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f0)])
			sfr_valf1=int(radiator_table[str(cooling['radwidth'])][str(radiatorhtf)]['deg'+str(sfr_f1)])
			sfr=sfr_valf1-((sfr_valf1-sfr_valf0)/(sfr_f1-sfr_f0))*(sfr_f1-topoilrise)
			#vfr
			if(core['coretype']=='wound'):
				if(core['subtype']=="CRGO"):
					vfr_cf=0
				else:
					vfr_cf=0.3;
				if(core['structure']=='Shell'):
					vfr_data=get_window_height
					vfr_sf=1
				else:
					vfr_sf=2
					vfr_data=get_window_heightsmall
			vfr_vval=(radbot+(radiatorht-radiatorhtf)+(radiatorhtf*0.5))-(tank['ccabot']+(get_stack_thk*0.5*(vfr_sf+vfr_cf))+(vfr_data*0.5)+(cca['clampthk']+5))
			vfr_vval1=int(math.floor(vfr_vval/100)*100)
			vfr_vval2=int(math.ceil(vfr_vval/100)*100)
			vfr=float(vertical_table[str(vfr_vval2)])-((float(vertical_table[str(vfr_vval2)])-float(vertical_table[str(vfr_vval1)]))/(vfr_vval2-vfr_vval1))*(vfr_vval2-vfr_vval)
			#radhoriz
			if(cooling['auto']):
				if(cooling['norads']<=3):
					radhoriz=(tank_length-130)/cooling['norads']
				else:
					if(cooling['norads']%2==0):
						radhoriz=(tank_length-130)/cooling['norads']*2
					else:
						radhoriz=(((tank_length-130)/math.ceil(cooling['norads']*0.5))+((tank_length-130)/math.floor(cooling['norads']*0.5)))*0.5
			else:
				radhoriz=cooling['radhoriz']
			#hfr
			hfr_i=0
			hfr_j=0
			hfr_l=0
			hfr_m=0
			hfr_k=0
			for key,value in horizontal_table[str(cooling['radwidth'])].iteritems():
				if(radhoriz>=Decimal(key)):
					hfr_i=Decimal(value)
					hfr_l=Decimal(key)
				elif(radhoriz<Decimal(key)):
					if(hfr_k==0):
						hfr_j=Decimal(value)
						hfr_m=Decimal(key)
						hfr_k=1
			hfr=float(hfr_j)-((float(hfr_j)-float(hfr_i))/(float(hfr_m)-float(hfr_l)))*(float(hfr_m)-float(radhoriz))
			#no_elements
			if(coolingreq==0):
				no_elements=0
			else:
				no_elements=coolingreq/(sfr*vfr*hfr*cooling['norads'])
			output['no_elements']=no_elements
			#actual_elements
			ace=int(math.ceil(no_elements))
			if(ace<=2):
				actual_elements=math.ceil(no_elements/float(fins_table['2']))
			else:
				actual_elements=math.ceil(no_elements/float(fins_table[str(ace)]))
			oilincooling=round(actual_elements*cooling['norads']*radiator_oil*100)/100
		else:
			#corrgheight
			if(cooling['auto']):
				corrgheight=math.floor((tank_height-100)/50)*50
			else:
				corrgheight=cooling['corrght']
			#corrgarea
			if(coolingreq==0):
				corrgarea=0
			else:
				corrgfinnol=((2-tdef1)*math.ceil((tank_length-100)/cooling['corrgfindist']))
				corrgfingapl=corrgfinnol-(2-tdef1)
				corrgfinnow=(2-tdef2)*math.ceil((tank_breadth-100)/cooling['corrgfindist'])
				corrgfingapw=corrgfinnow-(2-tdef2)
				if(cooling['auto']=='true'):
					corrgfins=corrgfinnol+corrgfinnow
					corrggaps=corrgfingapl+corrgfingapw
				else:
					corrgfins=cooling['corrgfinsno']
					corrggaps=cooling['corrgfinsno']-(4-int(tdef1)-int(tdef2))
				gap_surf_area=corrggaps*cooling['corrgfindist']*corrgheight/1000000
				corrgarea=round(((coolingreq/(topoilrise*cooling['corrgwms']))-gap_surf_area),3)
			#corrgwm2
			corrgwm2=round((coolingreq/(topoilrise*cooling['corrgwms'])),2)
			#corrgdepth
			if(cooling['auto']=='true'):
				corrgdepth=math.ceil((corrgarea*1000000/(2*corrgfins*corrgheight))/5)*5
			else:
				corrgdepth=cooling['corrgdepth']
			oilincooling=(8*corrgheight*corrgdepth*corrgfins/1000000)
	output['oilincooling']=oilincooling

	#conservatoroil
	if(tank['type']=='conservator'):
		conservatoroil=round(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket'])*3)/100,2)
	else:
		conservatoroil=0
	output['conservatoroil']=conservatoroil

	#totoil
	totoil=round(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket']+conservatoroil)*1.03),2)
	output['totoil']=totoil

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
	output['coolingnos']=coolingnos

	#oilcost
	oilcost=round(totoil*costing['oil'])
	output['oilcost']=oilcost

	#coolingqty
	if(coolingreq==0):
		coolingqty=0
	else:
		if(cooling['type']=="Tube"):
			coolingqty=round((tubelength*1.44),2)
		elif(cooling['type']=="PressedRadiator"):
			coolingqty=actual_elements*cooling['norads']*radiator_wt
		else:
			coolingqty=round(((corrgheight*corrgdepth*corrgfins*2*cooling['corrgthk']*7.85/1000000)+(corrggaps*cooling['corrgfindist']*corrgheight*cooling['corrgthk']*7.85/1000000)),2)
	output['coolingqty']=coolingqty

	#coolingtot
	coolingtot=round((coolingqty*1.05),2)*costing['cooling']
	output['coolingtot']=coolingtot

	#totloss1
	totloss1=round((no_load_losses+(load_losses*other['loss1']*other['loss1']/10000)),2)
	caltotloss1=(other['nloss1'])*(1-(other['ploss1'])/100)
	if(totloss1>caltotloss1):
		return 0
	output['totloss1']=totloss1

	#totloss1
	totloss2=round((no_load_losses+(load_losses*other['loss2']*other['loss2']/10000)),2)
	caltotloss2=(other['nloss2'])*(1-(other['ploss2'])/100)
	if(totloss2>caltotloss2):
		return 0
	output['totloss2']=totloss2

	#get_curb
	get_curb_cdata=tank['curb'].split('x')
	get_curb=round(((((tank_length+(tank['sidesheet']*2)+(int(get_curb_cdata[0])*2))*2)+(tank_breadth+(tank['sidesheet']*2)))*int(get_curb_cdata[0])*int(get_curb_cdata[1])*7.85/1000000),2)
	output['get_curb']=get_curb

	#topcoverwt
	topcoverwt_cdata=tank['curb'].split('x')
	topcoverwt=round(((tank_length+(tank['sidesheet']*2)+(int(topcoverwt_cdata[0])*2)+50)*(tank_breadth+(tank['sidesheet']*2)+(int(topcoverwt_cdata[0])*2)+50)*tank['topcover']*7.85/1000000),2)
	output['topcoverwt']=topcoverwt

	#botcoverwt
	botcoverwt=round(((tank_length+25)*(tank_breadth+25)*tank['botcover']*7.85/1000000),2)
	output['botcoverwt']=botcoverwt

	#sidesheetwt
	sidesheetwt=round((2*(tank_length+tank_breadth)*tank_height_m*tank['sidesheet']*7.85/1000000),2)
	output['sidesheetwt']=sidesheetwt

	#bchannelwt
	bdata=tank['bchannel'].split('x')
	if(tank_breadth<=400):
		bchannelwt=round((460*2*(bchanneldata[tank['bchannel']])/1000),2)
	else:
		bchannelwt=round(((tank_breadth+150)*2*(bchanneldata[tank['bchannel']])/1000),2)
	output['bchannelwt']=bchannelwt

	#vstifnerwt
	vdata=tank['vstifner'].split('x')
	vstifnerwt=round((int(vdata[0])*int(vdata[1])*tank_height_m*2*tank['vstifno']*7.85/1000000),2)
	output['vstifnerwt']=vstifnerwt

	#hstifnerwt
	hdata=tank['hstifner'].split('x')
	hstifnerwt=round((((tank_length+tank_breadth+(int(hdata[0])*4))*2*hstifdata[tank['hstifner']])*tank['hstifno']/1000),2)
	output['hstifnerwt']=hstifnerwt

	#conswt
	if(tank['type']=='conservator'):
		consvol=round(((oil_main_tank-displacement+oilincooling+tank['lvpocket']+tank['hvpocket'])/10),2)
		conslen=math.ceil(consvol*4*1000000/(tank['consdia']*tank['consdia']*math.pi*5))*5
		conswt=round(((matth.pi*tank['consdia']*tank['consthk']*conslen*7.85/1000000)+(consdata[tank['consdia']]['front']+consdata[tank['consdia']]['curb']+consdata[tank['consdia']]['side'])),2)
	else:
		conslen=0
		conswt=0
	output['conswt']=conswt

	#liftinglugwt
	if(basic['rating']<100):
		liftinglugwt=0.5*tank['lftlug']
	elif(basic['rating']<500):
		liftinglugwt=1.875*tank['lftlug']
	else:
		liftinglugwt=5*tank['lftlug']
	output['liftinglugwt']=liftinglugwt

	#ventpipewt
	ventpipewt=round((math.pi*55*tank['ventpipe']*5*7.85/1000000),2)
	output['ventpipewt']=ventpipewt

	#tottankwt
	tottankwt=round((tank['misc']+ventpipewt+(tank['pullinglug']*0.157)+(tank['topcvrlft']*0.157)+liftinglugwt+hstifnerwt+bchannelwt+get_curb+vstifnerwt+conswt+botcoverwt+sidesheetwt+topcoverwt),3)
	output['tottankwt']=tottankwt

	#steelqty
	steelqty=round(((tottankwt+top_core_clamp+bot_core_clamp)*1.05),2)
	output['steelqty']=steelqty

	#steelcost
	steelcost=round((costing['ms']*steelqty),2)
	output['steelcost']=steelcost

	#lvbusbarl
	if(core['structure']=='Shell'):
		lvbusbarl_ef2=0.5
		lvbusbarl_data=get_window_height
	else:
		lvbusbarl_ef2=1
		lvbusbarl_data=get_window_heightsmall
	if(core['subtype']=='CRGO'):
		lvbusbarl_ef=0
	else:
		lvbusbarl_ef=0.3
	lvbusbarl=round((get_hv_od_b*2)+(2*cca['hvhvgap'])+50+cca['coilyokegap']+(tank_height_m-100-(tank['ccabot']+(cca['clampthk'])+5+lvbusbarl_data+((1+lvbusbarl_ef)*get_stack_thk*lvbusbarl_ef2)))*3)
	output['lvbusbarl']=lvbusbarl

	#lvflatqty
	lvflatqty=round(((lvbusbarl)*lv_cond_area*lvflatqty_ef/1000000),2)
	output['lvflatqty']=lvflatqty

	#lvflatcost
	lvflatcost=round((costing['lv']*lvflatqty),2)
	output['lvflatcost']=lvflatcost

	#totfinalwt
	totfinalwt=math.ceil(total_weight+covered_wt_lv+covered_wt_hv+totoil+tottankwt)
	output['totfinalwt']=totfinalwt

	#maxtemplv
	maxtemplv=(other['windrise']+other['ambienttemp'])+(2*(other['windrise']+other['ambienttemp']+maxtemplv_ef))/((maxtemplv_ef2/(lv_cd*100/percentage_z)*(lv_cd*100/percentage_z)*other['thermalab'])-1)
	output['maxtemplv']=maxtemplv

	#maxtemphv
	maxtemphv=(other['windrise']+other['ambienttemp'])+(2*(other['windrise']+other['ambienttemp']+maxtemphv_ef))/((maxtemphv_ef2/(hv_cd*100/percentage_z)*(hv_cd*100/percentage_z)*other['thermalab'])-1)
	output['maxtemphv']=maxtemphv

	#totfinalcost
	totfinalcost=round((costing['othermat']+(cca['insuwt']*costing['insu'])+coolingtot+steelcost+oilcost+lvflatcost+hvcost+lvcost+corecost),2)

	#nllcap
	if(costing['capitalyn']=='yes'):
		nllcap=round((no_load_losses*costing['nllcap']),2)
	else:
		nllcap=0

	#llcap
	if(costing['capitalyn']=='yes'):
		llcap=round((load_losses*costing['llcap']),2)
	else:
		llcap=0

	#capcost
	capcost=round((totfinalcost+nllcap+llcap),2)
	output['totfinalcost']=totfinalcost

	output['main']=test
	output['get_stack_thk']=get_stack_thk
	output['no_load_check']=no_load_check
	output['load_check']=load_check
	output['no_load_losses']=no_load_losses
	output['load_losses']=load_losses
	output['percentage_z']=percentage_z
	output['costing']=totfinalcost
	output['capcosting']=capcost
	que.append(output)
