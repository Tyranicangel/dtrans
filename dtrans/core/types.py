from __future__ import division
from django.db import models
import math

class Design(object):
	no_load_check=True;
	get_volt_turn=0
	get_stack_thk=0
	get_turn_layer=0
	daihen=0
	ssel=0
	get_hv_coils=0
	get_hvturns=0
	lvdaihen=0
	lvssel=0
	lv_axial_phy=0
	lv_axial_pack=0
	get_hv_insu=0
	get_hv_nolayers=0
	get_lv_insu=0
	get_hv_turn_layer=0
	rdlv=0
	rdhv=0
	lv_rd_nonlead=0
	hv_rd_nonlead=0
	hv_axial_phy=0
	hv_axial_elect=0
	hv_axial_pack=0
	get_big_loop_ww=0
	get_small_loop_ww=0
	get_window_height=0
	get_core_area=0
	small_loop_mlt=0
	big_loop_mlt=0
	small_loop_wt=0
	big_loop_wt=0
	total_weight=0
	no_load_losses=0
	load_losses=0
	lv_l2r_loss=0
	hv_l2r_loss=0
	lv_stray_loss=0
	hv_stray_loss=0
	hv_eddy=0
	lv_eddy=0
	hv_bushing=0
	lv_bushing=0
	lead_wire_loss=0
	lead_wire_loss_hv=0
	hv_misc_loss=0
	lv_misc_loss=0
	hv_cond_wt=0
	lv_cond_wt=0
	bfactor_eddy=0
	lv_axial_elect=0
	phase_lv=0
	phase_hv=0
	lv_resi_ph=0
	hv_resi_ph=0
	line_hv=0
	line_lv=0
	lv_cond_area=0
	hv_cond_area=0
	lv_lmt=0
	hv_lmt=0
	lv_rd=0
	hv_rd=0
	get_mandril_a=0
	get_mandril_b=0
	percentage_r=0
	percentage_x_delta=0
	percentage_x_k=0
	percentage_x=0
	percentage_z=0
	get_lv_hv_mlt=0
	main={}

	def __init__(self,basic,core,tapping,lv,hv,cca,cooling,tank,other,check,costing,test):
		self.main=test
		if(hv['condtype']=='round'):
			test['hvkmain']=test['hvwmain']
			hv['radials']=hv['flats']=1;
			hv['transpos']=0;

		if(hv['connectiontype']=='star' or hv['connectiontype']=='zigzag'):
			hv['phvolt']=(basic['hvvoltage']/math.sqrt(3));
		elif(hv['connectiontype']=='delta'):
			hv['phvolt']=basic['hvvoltage']
		elif(hv['connectiontype']=='parallel' or hv['connectiontype']=='series'):
			hv['phvolt']=basic['hvvoltage']

		if(lv['connectiontype']=='star' or lv['connectiontype']=='zigzag'):
			lv['phvolt']=(basic['lvvoltage']/math.sqrt(3));
		elif(lv['connectiontype']=='delta'):
			lv['phvolt']=basic['lvvoltage'];
		elif(lv['connectiontype']=='parallel' or lv['connectiontype']=='series'):
			lv['phvolt']=basic['lvvoltage'];

		#get_volt_turn
		if(lv['connectiontype']=='delta' or lv['connectiontype']=='delta_delta' or lv['connectiontype']=='series' or lv['connectiontype']=='parallel'):
			self.get_volt_turn=basic['lvvoltage']/test['lvtmain']
		else:
			self.get_volt_turn=basic['lvvoltage']/(math.sqrt(3)*test['lvtmain'])

		#stack_thk
		if(core['subtype']=='CRGO'):
			stackthk_ef=0.97
		else:
			stackthk_ef=0.86
		sthk=(self.get_volt_turn*1000000)/(4.44*basic['frequency']*test['fmain']*stackthk_ef *test['cmain'])
		stack_thk=math.ceil(sthk/core['platethk'])
		bytwo=stack_thk%2
		if(bytwo!=0):
			stack_thk=stack_thk-1
		self.get_stack_thk=round(stack_thk*core['platethk'],2)

		#lv_axial_elect
		self.lv_axial_elect=round(((test['lvwmain']+lv['coveringthk'])*((test['lvtmain']/lv['nolayers']*lv['flats'])+lv['transpos'])),2)

		#lv_axial_phy
		lv_axial_phy_out=(test['lvwmain']+lv['coveringthk'])*((((test['lvtmain']/lv['nolayers'])+1)*lv['flats'])+lv['transpos'])
		lv_axial_phy_out2=round(lv_axial_phy_out)
		if(lv_axial_phy_out2<lv_axial_phy_out):
			self.lv_axial_phy=lv_axial_phy_out2+1
		else:
			self.lv_axial_phy=lv_axial_phy_out2

		#lv_axial_pack
		self.lv_axial_pack=self.lv_axial_phy+(cca['lvedge']*2)

		#get_turn_layer
		self.get_turn_layer=round((test['lvtmain']/lv['nolayers']),2)

		#get_hv_turn_layer
		if(hv['condtype']=='round'):
			self.get_hv_turn_layer=int(((self.lv_axial_pack-(cca['hvedge']*2))/(test['hvwmain']+hv['coveringthk']))-1)

		#get_hv_coils
		self.get_hv_coils=hv['mcoils']+hv['tcoils']

		#get_hvturns
		self.get_hvturns=test['lvtmain']*hv['phvolt']/lv['phvolt']

		#daihen
		if(hv['condtype']=='round' and hv['connectiontype']=='delta'):
			self.daihen=((other['hvimpulse']*4.5*self.get_hv_turn_layer*self.get_hv_coils/self.get_hvturns)-(7*math.sqrt(test['hvwmain'])))/50
		elif(hv['condtype']=='round' and (hv['connectiontype']=='star' or hv['connectiontype']=='zigzag')):
			self.daihen=((other['hvimpulse']*3.15*self.get_hv_turn_layer*self.get_hv_coils/self.get_hvturns)-(7*math.sqrt(test['hvwmain'])))/50
		elif(hv['condtype']=='rectangular' and hv['connectiontype']=='delta'):
			self.daihen=((other['hvimpulse']*4.5*self.get_hv_turn_layer*self.get_hv_coils/self.get_hvturns)-(hv['coveringthk']))/50
		elif(hv['condtype']=='rectangular' and (hv['connectiontype']=='star'or hv['connectiontype']=='zigzag')):
			self.daihen=((other['hvimpulse']*3.15*self.get_hv_turn_layer*self.get_hv_coils/self.get_hvturns)-(hv['coveringthk']))/50

		#ssel
		if(hv['coveringmat']=='dpc' and (hv['condtype']=='round' or hv['condtype']=='rectangular')):
			self.ssel=(4*self.get_volt_turn*self.get_hv_turn_layer/6000)-hv['coveringthk']
		elif(hv['coveringmat']=='enamel' and hv['condtype']=='round'):
			self.ssel=(((4*self.get_volt_turn*self.get_hv_turn_layer)-1500)/6000)
		elif(hv['coveringmat']=='enamel' and hv['condtype']=='rectangular'):
			self.ssel=(((4*self.get_volt_turn*self.get_hv_turn_layer)-500)/6000)

		#lvdaihen
		if(lv['condtype']=='round' and lv['connectiontype']=='delta'):
			out=((other['lvimpulse']*4.5*self.get_turn_layer*lv['mcoils']/test['lvtmain'])-(7*math.sqrt(test['lvwmain'])))/50
		elif(lv['condtype']=='round' and (lv['connectiontype']=='star' or lv['connectiontype']=='zigzag')):
			out=((other['lvimpulse']*3.15*self.get_turn_layer*lv['mcoils']/test['lvtmain'])-(7*math.sqrt(test['lvwmain'])))/50
		elif(lv['condtype']=='rectangular' and lv['connectiontype']=='delta'):
			out=((other['lvimpulse']*4.5*self.get_turn_layer*lv['mcoils']/test['lvtmain'])-(lv['coveringthk']))/50
		elif(lv['condtype']=='rectangular' and (lv['connectiontype']=='star'or lv['connectiontype']=='zigzag')):
			out=((other['lvimpulse']*3.15*self.get_turn_layer*lv['mcoils']/test['lvtmain'])-(lv['coveringthk']))/50

		#lvssel
		if(lv['coveringmat']=='dpc' and (lv['condtype']=='round' or lv['condtype']=='rectangular')):
			self.lvssel=(4*self.get_volt_turn*self.get_turn_layer/6000)-lv['coveringthk']
		elif(lv['coveringmat']=='enamel' and lv['condtype']=='round'):
			self.lvssel=(((4*self.get_volt_turn*self.get_turn_layer)-1500)/6000)
		elif(lv['coveringmat']=='enamel' and lv['condtype']=='rectangular'):
			self.lvssel=(((4*self.get_volt_turn*self.get_turn_layer)-500)/6000)

		#get_hv_insu
		if(other['hvimpulse']<95):
			get_hv_insu_out=self.daihen if (self.daihen<self.ssel) else self.ssel
		else:
			get_hv_insu_out=self.daihen
		if(get_hv_insu_out<0.15):
			self.get_hv_insu=0.15
		else:
			self.get_hv_insu=round(math.ceil(get_hv_insu_out/0.025)*0.025,3)

		#get_hv_nolayers
		get_hv_nolayers_out=(self.get_hvturns/self.get_hv_coils)/(self.get_hv_turn_layer)
		get_hv_nolayers_c=math.ceil(get_hv_nolayers_out)
		get_hv_nolayers_b=((get_hv_nolayers_c*self.get_hv_turn_layer)-(self.get_hvturns/self.get_hv_coils))/get_hv_nolayers_c
		if(test['hvwmain']<=1):
			if(get_hv_nolayers_b<4):
				self.get_hv_nolayers=get_hv_nolayers_c+1
			else:
				self.get_hv_nolayers=get_hv_nolayers_c
		elif(test['hvwmain']<=1.5):
			if(get_hv_nolayers_b<3):
				self.get_hv_nolayers=get_hv_nolayers_c+1
			else:
				self.get_hv_nolayers=get_hv_nolayers_c
		elif(test['hvwmain']>1.5):
			if(get_hv_nolayers_b<2):
				self.get_hv_nolayers=get_hv_nolayers_c+1
			else:
				self.get_hv_nolayers=get_hv_nolayers_c

		#get_lv_insu
		if(lv['insulshow']==True):
			self.get_lv_insu=lv['layerinsu']
		else:
			if(other['lvimpulse']<95):
				get_lv_insu_out=self.lvdaihen if (self.lvdaihen<self.lvssel) else self.lvssel
			else:
				get_lv_insu_out=self.lvdaihen
			if(get_lv_insu_out<0.15):
				self.get_lv_insu=0.15
			else:
				self.get_lv_insu=round(math.ceil(get_lv_insu_out/0.025)*0.025,3)

		#rdlv
		self.rdlv=((test['lvkmain']+lv['coveringthk'])*lv['radials']*lv['nolayers'])+(self.get_lv_insu*(lv['nolayers']-1))+(lv['fullthk']*lv['nofull'])

		#rdhv
		self.rdhv=((test['hvkmain']+hv['coveringthk'])*hv['radials']*self.get_hv_nolayers)+(self.get_hv_insu*(self.get_hv_nolayers-1-hv['nofull']))+((hv['fullthk']+0.25)*hv['nofull'])

		#lv_rd_nonlead
		self.lv_rd_nonlead=self.ceiling(self.rdlv*1.02)

		#hv_rd_nonlead
		self.hv_rd_nonlead=self.ceiling(self.rdhv*1.02)

		#hv_axial_elect
		self.hv_axial_elect=(test['hvwmain']+hv['coveringthk'])*self.get_hv_turn_layer

		#hv_axial_phy
		self.hv_axial_phy=math.ceil(self.hv_axial_elect+test['hvwmain']+hv['coveringthk'])

		#hv_axial_pack
		self.hv_axial_pack=self.hv_axial_phy+(cca['hvedge']*2)

		#get_small_loop_ww
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			self.get_small_loop_ww=cca['corelvgap']+self.lv_rd_nonlead+test['lvhmain']+self.hv_rd_nonlead+cca['hvend']
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			self.get_small_loop_ww=2*(cca['corelvgap']+self.lv_rd_nonlead+test['lvhmain']+self.hv_rd_nonlead)+cca['hvhvgap']
		elif(self.core.subtype=='Amorphous' and self.core.structure=='Shell'):
			self.get_small_loop_ww=cca['corelvgap']+self.lv_rd_nonlead+test['lvhmain']+self.hv_rd_nonlead+cca['hvend']+2
		elif(self.core.subtype=='Amorphous' and self.core.structure=='Core'):
			self.get_small_loop_ww=2*(cca['corelvgap']+self.lv_rd_nonlead+test['lvhmain']+self.hv_rd_nonlead)+cca['hvhvgap']+4
		self.get_small_loop_ww=math.ceil(self.get_small_loop_ww)

		#get_big_loop_ww
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			self.get_big_loop_ww=2*(cca['corelvgap']+self.lv_rd_nonlead+test['lvhmain']+hv_rd_nonlead)+cca['hvhvgap']
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			if(basic['rating']<=63):
				get_big_loop_ww_ef=8
			elif(basic['rating']<=100):
				get_big_loop_ww_ef=9
			else:
				get_big_loop_ww_ef=10
			self.get_big_loop_ww=(self.get_small_loop_ww*2)+(self.get_stack_thk*2)+get_big_loop_ww_ef
		elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			self.get_big_loop_ww=2*(cca['corelvgap']+self.lv_rd_nonlead+test['lvhmain']+self.hv_rd_nonlead)+cca['hvhvgap']+4
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			self.get_big_loop_ww=(self.get_small_loop_ww*2)+(self.get_stack_thk*2)+6
		self.get_big_loop_ww=math.ceil(self.get_big_loop_ww)

		#get_window_height
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			get_window_height_ef=4
			self.get_window_height=self.hv_axial_pack+cca['coilyokegap']+(get_window_height_ef*2)
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			get_window_height_ef=4
			get_window_height_out1=self.hv_axial_pack+cca['coilyokegap']+(get_window_height_ef*2)
			get_window_height_out2=get_window_height_out1+self.get_stack_thk+2
			self.get_window_height=str(math.ceil(get_window_height_out1))+'/'+str(math.ceil(get_window_height_out2))
		elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			get_window_height_ef=6.5
			self.get_window_height=self.hv_axial_pack+cca['coilyokegap']+(get_window_height_ef*2)
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			get_window_height_ef=6.5
			get_window_height_out1=self.hv_axial_pack+cca['coilyokegap']+(get_window_height_ef*2)
			get_window_height_out2=get_window_height_out1+(self.get_stack_thk*1.25)+2
			self.get_window_height=str(math.ceil(get_window_height_out1))+'/'+str(math.ceil(get_window_height_out2))

		#get_core_area
		if(core['subtype']=='CRGO'):
			get_core_area_ef=0.97
		else:
			get_core_area_ef=0.86
		self.get_core_area=round((test['cmain']*self.get_stack_thk*get_core_area_ef*0.01),3)

		#small_loop_mlt
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			self.small_loop_mlt=2*(self.get_window_height+5.6)+(2*self.get_small_loop_ww)+(1.7*self.get_stack_thk)
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			small_loop_mlt_data=self.get_window_height.split('/')
			self.small_loop_mlt=2*(float(small_loop_mlt_data[0])+5.6)+(2*self.get_small_loop_ww)+(1.7*self.get_stack_thk)
		elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			if(basic['rating']<315):
				small_loop_mlt_ef=15
			else:
				small_loop_mlt_ef=20
			self.small_loop_mlt=2*(self.get_window_height)+(2*self.get_small_loop_ww)-(52)+(2*math.pi*(6.5+self.get_stack_thk*0.25*1.1))+small_loop_mlt_ef
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			if(basic['rating']<315):
				small_loop_mlt_ef=15
			else:
				small_loop_mlt_ef=20
			small_loop_mlt_data=self.get_window_height.split('/')
			self.small_loop_mlt=2*float(small_loop_mlt_data[0])+(2*self.get_small_loop_ww)-(52)+(2*math.pi*(6.5+self.get_stack_thk*0.25*1.1))+small_loop_mlt_ef

		#big_loop_mlt
		if(core['subtype']=='CRGO' and core['structure']=='Shell'):
			self.big_loop_mlt=2*(self.get_window_height+5.6)+(2*self.get_big_loop_ww)+(1.7*self.get_stack_thk)
		elif(core['subtype']=='CRGO' and core['structure']=='Core'):
			big_loop_mlt_data=self.get_window_height.split('/')
			self.big_loop_mlt=2*(float(big_loop_mlt_data[1])+5.6)+(2*self.get_big_loop_ww)+(1.7*self.get_stack_thk)
		elif(core['subtype']=='Amorphous' and core['structure']=='Shell'):
			if(basic['rating']<315):
				big_loop_mlt_ef=15
			else:
				big_loop_mlt_ef=20
			self.big_loop_mlt=2*(self.get_window_height)+(2*self.get_big_loop_ww)-(52)+(2*math.pi*(6.5+self.get_stack_thk*0.25*1.1))+big_loop_mlt_ef
		elif(core['subtype']=='Amorphous' and core['structure']=='Core'):
			if(basic['rating']<315):
				big_loop_mlt_ef=15
			else:
				big_loop_mlt_ef=20
			big_loop_mlt_data=self.get_window_height.split('/')
			self.big_loop_mlt=2*(float(big_loop_mlt_data[1]))+(2*self.get_big_loop_ww)-(52)+(2*math.pi*(6.5+self.get_stack_thk*0.25*1.1))+big_loop_mlt_ef

		#big_loop_wt
		if(core['subtype']=='CRGO'):
			self.big_loop_wt=round(((self.big_loop_mlt*7.65*self.get_core_area*0.96)/(10000*0.97)),2)
		else:
			self.big_loop_wt=round(((self.big_loop_mlt*7.18*self.get_core_area)/(10000)),2)

		#small_loop_wt
		if(core['subtype']=='CRGO'):
			self.small_loop_wt=round(((self.small_loop_mlt*7.65*self.get_core_area*0.96)/(10000*0.97)),2)
		else:
			self.small_loop_wt=round(((self.small_loop_mlt*7.18*self.get_core_area)/(10000)),2)

		#total_weight
		self.total_weight=self.big_loop_wt+self.small_loop_wt

		#no_load_losses
		self.no_load_losses=round((self.total_weight*core['factor']*0.62),2)
		no_load_cal=other['noload1']*(100-other['noload2'])/100;
		if(no_load_cal<=self.no_load_losses):
			self.no_load_check=False

		#get_mandril_a
		if(basic['rating']<=100):
			self.get_mandril_a=test['cmain']+7+cca['mandrila']
		else:
			self.get_mandril_a=test['cmain']+8+cca['mandrila']

		#get_mandril_b
		if(core['subtype']=='CRGO'):
			if(basic['rating']<=63):
				self.get_mandril_b=math.ceil((self.get_stack_thk+8+cca['mandrilb'])*2)/2
			elif(basic['rating']<=100):
				self.get_mandril_b=math.ceil((self.get_stack_thk+9+cca['mandrilb'])*2)/2
			else:
				self.get_mandril_b=math.ceil((self.get_stack_thk+10+cca['mandrilb'])*2)/2
		else:
			self.get_mandril_b=math.ceil((self.get_stack_thk+4+cca['mandrilb'])*2)/2

		#lv_rd
		self.lv_rd=self.ceiling(self.rdlv)

		#hv_rd
		self.hv_rd=self.ceiling(self.rdhv)

		#hv_cond_area
		if(hv['condtype']=='round'):
			self.hv_cond_area=round((math.pi*test['hvwmain']*test['hvwmain']/4),3)
		elif(hv['condtype']=='foil'):
			self.hv_cond_area=round((test['hvwmain']*test['hvkmain']*hv['radials']),3)
		else:
			if(test['hvkmain']>2.99):
				hv_cond_area_ef=0.9
			else:
				hv_cond_area_ef=0.5
			self.hv_cond_area=round((((test['hvwmain']*test['hvkmain'])-ef)*hv['flats']*hv['radials']),3)

		#lv_cond_area
		if(lv['condtype']=='round'):
			self.lv_cond_area=round((math.pi*test['lvwmain']*test['lvwmain']/4),3)
		elif(lv['condtype']=='foil'):
			self.lv_cond_area=round((test['lvwmain']*test['lvkmain']*lv['radials']),3)
		else:
			if(test['lvkmain']>2.99):
				lv_cond_area_ef=0.9
			else:
				lv_cond_area_ef=0.5
			self.lv_cond_area=round((((test['lvwmain']*test['lvkmain'])-lv_cond_area_ef)*lv['flats']*lv['radials']),3)

		#lv_lmt
		if(lv['coveringmat']=='enamel'):
			lmt_ef=3
		else:
			lmt_ef=4
		self.lv_lmt=round((2*(self.get_mandril_a+self.get_mandril_b-(4*lmt_ef))+2*math.pi*(lmt_ef+cca['corelvgap']+(self.lv_rd*0.5))+2*(lv['nofnb']*(lv['fnbthk']+0.125))),3)
		self.hv_lmt=round((2*(self.get_mandril_a+self.get_mandril_b-(4*lmt_ef))+2*math.pi*(lmt_ef+cca['corelvgap']+self.lv_rd+test['lvhmain']+(self.hv_rd*0.5))+4*(lv['nofnb']*(lv['fnbthk']+0.125))+2*(hv['nofnb']*(hv['fnbthk']+0.25))),3)

		#lv_cond_wt
		if(basic['phases']=='3'):
			lv_cond_wt_pf=3
		else:
			lv_cond_wt_pf=1
		if(lv['material']=='copper'):
			lv_cond_wt_ef=8.9
		else:
			lv_cond_wt_ef=2.7
		self.lv_cond_wt=round((self.lv_lmt*test['lvtmain']*lv_cond_wt_ef*self.lv_cond_area*lv_cond_wt_pf/1000000),2)

		#hv_cond_wt
		if(basic['phases']=='3'):
			hv_cond_wt_pf=3
		else:
			hv_cond_wt_pf=1
		if(lv['material']=='copper'):
			hv_cond_wt_ef=8.9
		else:
			hv_cond_wt_ef=2.7
		self.hv_cond_wt=round((self.hv_lmt*self.get_hvturns*hv_cond_wt_ef*self.hv_cond_area*hv_cond_wt_pf/1000000),2)

		#phase_lv
		if(lv['connectiontype']=='star' or lv['connectiontype']=='zigzag'):
			self.phase_lv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['lvvoltage'])),4)
		elif(lv['connectiontype']=='delta'):
			self.phase_lv=round(((basic['rating']*1000)/(3*basic['lvvoltage'])),4)
		elif(lv['connectiontype']=='series' or lv['connectiontype']=='parallel'):
			self.phase_lv=round(((basic['rating']*1000)/(basic['lvvoltage'])),4)

		#phase_hv
		if (hv['connectiontype']=='star' or hv['connectiontype']=='zigzag'):
			self.phase_hv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['hvvoltage'])),4)
		elif (hv['connectiontype']=='delta'):
			self.phase_hv=round(((basic['rating']*1000)/(3*basic['hvvoltage'])),4)
		elif (hv['connectiontype']=='series' or hv['connectiontype']=='parallel'):
			self.phase_hv=round(((basic['rating']*1000)/(basic['hvvoltage'])),4)

		#line_hv
		if(hv['connectiontype']=='series' or hv['connectiontype']=='parallel'):
			self.line_hv=round(((basic['rating']*1000)/(basic['hvvoltage'])),4)
		else:
			self.line_hv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['hvvoltage'])),4)

		#line_lv
		if(lv['connectiontype']=='series' or lv['connectiontype']=='parallel'):
			self.line_lv=round(((basic['rating']*1000)/(basic['lvvoltage'])),4)
		else:
			self.line_lv=round(((basic['rating']*1000)/(math.sqrt(3)*basic['lvvoltage'])),4)

		#hv_resi_ph
		if(hv['material']=='copper'):
			hv_resi_ph_ef=2.1
		else:
			hv_resi_ph_ef=3.46
		self.hv_resi_ph=round((hv_resi_ph_ef*self.hv_lmt*self.get_hvturns/(100000*self.hv_cond_area)),4)

		#lv_resi_ph
		if(lv['material']=='copper'):
			lv_resi_ph_ef=2.1
		else:
			lv_resi_ph_ef=3.46
		self.lv_resi_ph=round((lv_resi_ph_ef*self.lv_lmt*test['lvtmain']/(100000*self.lv_cond_area)),6)

		#bfactor_eddy
		self.bfactor_eddy=self.phase_lv*test['lvtmain']*1.78/(1000*(self.lv_axial_elect+self.hv_axial_elect)*0.5)

		#lv_l2r_loss
		if(basic['phases']=='3'):
			lv_l2r_loss_pf=3
		else:
			lv_l2r_loss_pf=1
		self.lv_l2r_loss=round(lv_l2r_loss_pf*self.phase_lv*self.phase_lv*self.lv_resi_ph*2)/2

		#lv_eddy
		if(lv['material']=='copper'):
			lv_eddy_ef=9
		else:
			lv_eddy_ef=19
		if(lv['condtype']=='round'):
			lv_eddy_ef1=0.4
		else:
			lv_eddy_ef1=1
		self.lv_eddy=round((lv_eddy_ef1*lv_eddy_ef*basic['frequency']*basic['frequency']*self.bfactor_eddy*self.bfactor_eddy*test['lvkmain']*test['lvkmain']*self.lv_cond_wt/1000),2)

		#lv_bushing
		if(basic['rating']<=400):
			lv_bushing_ef=1
		else:
			lv_bushing_ef=0.5
		self.lv_bushing=round((math.pow(self.line_lv,1.25)*0.045*lv_bushing_ef),2)

		#lead_wire_loss
		self.lead_wire_loss=round((0.02*self.lv_l2r_loss),2)

		#lv_misc_loss
		self.lv_misc_loss=round(((self.lv_l2r_loss+self.lv_bushing+self.lead_wire_loss+self.lv_eddy)*1.5),2)

		#lv_stray_loss
		self.lv_stray_loss=round((self.lv_eddy+self.lv_bushing+self.lead_wire_loss+self.lv_misc_loss),2)

		#hv_l2r_loss
		if(basic['phases']=='3'):
			hv_l2r_loss_pf=3
		else:
			hv_l2r_loss_pf=1
		self.hv_l2r_loss=round(hv_l2r_loss_pf*self.phase_hv*self.phase_hv*self.hv_resi_ph*2)/1

		#hv_eddy
		if(hv['material']=='copper'):
			hv_eddy_ef=9
		else:
			hv_eddy_ef=19
		if(hv['condtype']=='round'):
			hv_eddy_ef1=0.4
		else:
			hv_eddy_ef1=1
		self.hv_eddy=round((hv_eddy_ef1*hv_eddy_ef*basic['frequency']*basic['frequency']*self.bfactor_eddy*self.bfactor_eddy*test['hvkmain']*test['hvkmain']*self.hv_cond_wt/1000),2)

		#hv_bushing
		if(basic['rating']<=400):
			hv_bushing_ef=1
		else:
			hv_bushing_ef=1
		self.hv_bushing=round((math.pow(self.line_hv,1.25)*0.045*hv_bushing_ef),2)

		#lead_wire_loss_hv
		self.lead_wire_loss_hv=round((0.005*self.hv_l2r_loss),2)

		#hv_misc_loss
		self.hv_misc_loss=round(((self.hv_l2r_loss+self.hv_bushing+self.lead_wire_loss_hv+self.hv_eddy)*1.5),2)

		#hv_stray_loss
		self.hv_stray_loss=round((self.hv_eddy+self.hv_bushing+self.lead_wire_loss_hv+self.hv_misc_loss),2)

		#load_losses
		if(other['stray']==0):
			self.load_losses=self.lv_l2r_loss+self.hv_l2r_loss+self.lv_stray_loss+self.hv_stray_loss
		else:
			self.load_losses=self.lv_l2r_loss+self.hv_l2r_loss+other['stray']

		#get_lv_hv_mlt
		if(hv['coveringmat']=='enamel'):
			get_lv_hv_mlt_ef=3
		else:
			get_lv_hv_mlt_ef=4
		self.get_lv_hv_mlt=round((2*(self.get_mandril_a+self.get_mandril_b-(4*get_lv_hv_mlt_ef))+2*math.pi*(get_lv_hv_mlt_ef+cca['corelvgap']+self.lv_rd+test['lvhmain']*0.5)+4*(lv['nofnb']*(lv['fnbthk']+0.125))),3)

		#percentage_r
		self.percentage_r=round((self.load_losses/(basic['rating']*10)),3)

		#percentage_x_delta
		self.percentage_x_delta=(self.lv_lmt*self.lv_rd/(3*self.lv_axial_elect))+(self.hv_lmt*self.hv_rd/(3*self.hv_axial_elect))+(self.get_lv_hv_mlt*test['lvhmain']/(0.5*(self.lv_axial_elect+self.hv_axial_elect)))

		#percentage_x_k
		self.percentage_x_k=1-((self.lv_rd+test['lvhmain']+self.hv_rd)/(math.pi*0.5*(self.lv_axial_elect+self.hv_axial_elect)))

		#percentage_x
		self.percentage_x=round((8*math.pi*math.pi*basic['frequency']*self.phase_lv*test['lvtmain']*test['lvtmain']*self.percentage_x_k*self.percentage_x_delta*0.00000001/lv['phvolt']),2)

		#percentage_z
		self.percentage_z=round((math.sqrt((self.percentage_x*self.percentage_x)+(self.percentage_r*self.percentage_r))),3)

	def ceiling(self,a):
		if(a-int(a)<0.1):
			return int(a)
		elif(a-int(a)>0.5):
			return int(a)+1
		else:
			return int(a)+0.5

	def get_output(self):
		output={}
		output['main']=self.main
		output['main']['lvkmain']=round(self.main['lvkmain'],2)
		output['main']['lvwmain']=round(self.main['lvwmain'],2)
		output['main']['hvkmain']=round(self.main['hvkmain'],2)
		output['get_stack_thk']=self.get_stack_thk
		output['no_load_losses']=self.no_load_losses
		output['load_losses']=self.load_losses
		output['percentage_z']=self.percentage_z
		return output