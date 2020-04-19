# from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from functools import wraps
import requests
import json
import datetime
import pandas as pd
import platform
import shutil
import datetime

if platform.system() == "Windows":
    # Local 端
	path = 'static/data/Data.csv'
else:
    # AWS 端
	path = "/home/cathaylife04/smartphone/iphone11/static/data/Data.csv"


# path = 'static/data/Data.csv'
Data = pd.read_csv(path)
Old_Data = Data.to_dict('records')


# 'Iphone11Pro'
# 'IPhone11Pro-Max'
# 'IPhone11'
# 'Ipad'
# 'AppleWatch5'
countries = {
'IphoneSE':{
	'Tw':['MX9T2TA/A','MXD12TA/A','MXVU2TA/A',
		'MX9R2TA/A','MXD02TA/A','MXVT2TA/A',
		'MX9U2TA/A','MXD22TA/A','MXVV2TA/A'],

	'Cn':['MXAN2CH/A','MXD72CH/A','MXW12CH/A',
	'MXAM2CH/A','MXD62CH/A','MXW02CH/A',
	'MXAP2CH/A','MXD82CH/A','MXW22CH/A'],

	'Jp':['MX9T2J/A','MXD12J/A','MXVU2J/A',
	'MX9R2J/A','MXD02J/A','MXVT2J/A',
	'MX9U2J/A','MXD22J/A','MXVV2J/A'],

	'Hk':['MX9T2ZP/A','MXD12ZP/A','MXVU2ZP/A',
	'MX9R2ZP/A','MXD02ZP/A','MXVT2ZP/A',
	'MX9U2ZP/A','MXD22ZP/A','MXVV2ZP/A'],

	'Uk':['MX9T2B/A','MXD12B/A','MXVU2B/A',
	'MX9R2B/A','MXD02B/A','MXVT2B/A',
	'MX9U2B/A','MXD22B/A','MXVV2B/A'],

	'De':['MX9T2ZD/A','MXD12ZD/A','MXVU2ZD/A',
	'MX9R2ZD/A','MXD02ZD/A','MXVT2ZD/A',
	'MX9U2ZD/A','MXD22ZD/A','MXVV2ZD/A'],

	'Ru':['MX9T2RU/A','MXD12RU/A','MXVU2RU/A',
	'MX9R2RU/A','MXD02RU/A','MXVT2RU/A',
	'MX9U2RU/A','MXD22RU/A','MXVV2RU/A'],

	'Fr':['MX9T2ZD/A','MXD12ZD/A','MXVU2ZD/A',
	'MX9R2ZD/A','MXD02ZD/A','MXVT2ZD/A',
	'MX9U2ZD/A','MXD22ZD/A','MXVV2ZD/A']
},

'AirPodPro':{'Tw':['MWP22TA/A'],

'Cn':['MWP22CH/A'],

'Jp':['MWP22J/A'],

'Hk':['MWP22ZP/A'],

'Uk':['MWP22ZM/A'],

'De':['MWP22ZM/A'],

'Ru':['MWP22RU/A'],

'Fr':['MWP22ZM/A']
},

'Iphone11Pro':{
'Tw':['MWC22TA/A','MWC72TA/A','MWCD2TA/A','MWC32TA/A','MWC82TA/A','MWCE2TA/A','MWC62TA/A','MWCC2TA/A',
'MWCG2TA/A','MWC52TA/A','MWC92TA/A','MWCF2TA/A'],

'Cn':['MWD92CH/A','MWDE2CH/A','MWDJ2CH/A','MWDA2CH/A','MWDF2CH/A','MWDK2CH/A','MWDD2CH/A','MWDH2CH/A',
'MWDM2CH/A','MWDC2CH/A','MWDG2CH/A','MWDL2CH/A'],

'Jp':['MWC22J/A','MWC72J/A','MWCD2J/A','MWC32J/A','MWC82J/A','MWCE2J/A','MWC62J/A','MWCC2J/A',
'MWCG2J/A','MWC52J/A','MWC92J/A','MWCF2J/A'],

'Hk':['MWD92ZA/A','MWDE2ZA/A','MWDJ2ZA/A','MWDA2ZA/A','MWDF2ZA/A','MWDK2ZA/A','MWDD2ZA/A','MWDH2ZA/A',
'MWDM2ZA/A','MWDC2ZA/A','MWDG2ZA/A','MWDL2ZA/A'],

'Uk':['MWC22B/A','MWC72B/A','MWCD2B/A','MWC32B/A','MWC82B/A','MWCE2B/A','MWC62B/A','MWCC2B/A',
'MWCG2B/A','MWC52B/A','MWC92B/A','MWCF2B/A'],

'De':['MWC22ZD/A','MWC72ZD/A','MWCD2ZD/A','MWC32ZD/A','MWC82ZD/A','MWCE2ZD/A','MWC62ZD/A','MWCC2ZD/A',
'MWCG2ZD/A','MWC52ZD/A','MWC92ZD/A','MWCF2ZD/A'],

'Ru':['MWC22RU/A','MWC72RU/A','MWCD2RU/A','MWC32RU/A','MWC82RU/A','MWCE2RU/A','MWC62RU/A','MWCC2RU/A',
'MWCG2RU/A','MWC52RU/A','MWC92RU/A','MWCF2RU/A'],

'Fr':['MWC22ZD/A','MWC72ZD/A','MWCD2ZD/A','MWC32ZD/A','MWC82ZD/A','MWCE2ZD/A','MWC62ZD/A','MWCC2ZD/A',
'MWCG2ZD/A','MWC52ZD/A','MWC92ZD/A','MWCF2ZD/A']
},

'IPhone11Pro-Max':{
'Tw':['MWHD2TA/A','MWHJ2TA/A','MWHN2TA/A','MWHF2TA/A','MWHK2TA/A','MWHP2TA/A','MWHH2TA/A','MWHM2TA/A','MWHR2TA/A','MWHG2TA/A','MWHL2TA/A','MWHQ2TA/A'],
'Cn':['MWEV2CH/A','MWF12CH/A','MWF52CH/A','MWEW2CH/A','MWF22CH/A','MWF62CH/A','MWF02CH/A','MWF42CH/A','MWF82CH/A','MWEX2CH/A','MWF32CH/A','MWF72CH/A'],
'Jp':['MWHD2J/A','MWHJ2J/A','MWHN2J/A','MWHF2J/A','MWHK2J/A','MWHP2J/A','MWHH2J/A','MWHM2J/A','MWHR2J/A','MWHG2J/A','MWHL2J/A','MWHQ2J/A'],
'Hk':['MWEV2ZA/A','MWF12ZA/A','MWF52ZA/A','MWEW2ZA/A','MWF22ZA/A','MWF62ZA/A','MWF02ZA/A','MWF42ZA/A','MWF82ZA/A','MWEX2ZA/A','MWF32ZA/A','MWF72ZA/A'],
'Uk':['MWHD2B/A','MWHJ2B/A','MWHN2B/A','MWHF2B/A','MWHK2B/A','MWHP2B/A','MWHH2B/A','MWHM2B/A','MWHR2B/A','MWHG2B/A','MWHL2B/A','MWHQ2B/A'],
'De':['MWHD2ZD/A','MWHJ2ZD/A','MWHN2ZD/A','MWHF2ZD/A','MWHK2ZD/A','MWHP2ZD/A','MWHH2ZD/A','MWHM2ZD/A','MWHR2ZD/A','MWHG2ZD/A','MWHL2ZD/A','MWHQ2ZD/A'],
'Ru':['MWHD2RU/A','MWHJ2RU/A','MWHN2RU/A','MWHF2RU/A','MWHK2RU/A','MWHP2RU/A','MWHH2RU/A','MWHM2RU/A','MWHR2RU/A','MWHG2RU/A','MWHL2RU/A','MWHQ2RU/A'],
'Fr':['MWHD2ZD/A','MWHJ2ZD/A','MWHN2ZD/A','MWHF2ZD/A','MWHK2ZD/A','MWHP2ZD/A','MWHH2ZD/A','MWHM2ZD/A','MWHR2ZD/A','MWHG2ZD/A','MWHL2ZD/A','MWHQ2ZD/A']
},

'IPhone11':{
'Tw':['MWLU2TA/A','MWM22TA/A','MWM82TA/A','MWLT2TA/A','MWM02TA/A','MWM72TA/A','MWLY2TA/A','MWM62TA/A','MWMD2TA/A','MWLW2TA/A','MWM42TA/A','MWMA2TA/A','MWLX2TA/A','MWM52TA/A','MWMC2TA/A','MWLV2TA/A','MWM32TA/A','MWM92TA/A'],
'Cn':['MWN12CH/A','MWN82CH/A','MWNG2CH/A','MWN02CH/A','MWN72CH/A','MWNF2CH/A','MWN62CH/A','MWNE2CH/A','MWNL2CH/A','MWN32CH/A','MWNC2CH/A','MWNJ2CH/A','MWN52CH/A','MWND2CH/A','MWNK2CH/A','MWN22CH/A','MWN92CH/A','MWNH2CH/A'],
'Jp':['MWLU2J/A','MWM22J/A','MWM82J/A','MWLT2J/A','MWM02J/A','MWM72J/A','MWLY2J/A','MWM62J/A','MWMD2J/A','MWLW2J/A','MWM42J/A','MWMA2J/A','MWLX2J/A','MWM52J/A','MWMC2J/A','MWLV2J/A','MWM32J/A','MWM92J/A'],
'Hk':['MWN12ZA/A','MWN82ZA/A','MWNG2ZA/A','MWN02ZA/A','MWN72ZA/A','MWNF2ZA/A','MWN62ZA/A','MWNE2ZA/A','MWNL2ZA/A','MWN32ZA/A','MWNC2ZA/A','MWNJ2ZA/A','MWN52ZA/A','MWND2ZA/A','MWNK2ZA/A','MWN22ZA/A','MWN92ZA/A','MWNH2ZA/A'],
'Uk':['MWLU2B/A','MWM22B/A','MWM82B/A','MWLT2B/A','MWM02B/A','MWM72B/A','MWLY2B/A','MWM62B/A','MWMD2B/A','MWLW2B/A','MWM42B/A','MWMA2B/A','MWLX2B/A','MWM52B/A','MWMC2B/A','MWLV2B/A','MWM32B/A','MWM92B/A'],
'De':['MWLU2ZD/A','MWM22ZD/A','MWM82ZD/A','MWLT2ZD/A','MWM02ZD/A','MWM72ZD/A','MWLY2ZD/A','MWM62ZD/A','MWMD2ZD/A','MWLW2ZD/A','MWM42ZD/A','MWMA2ZD/A','MWLX2ZD/A','MWM52ZD/A','MWMC2ZD/A','MWLV2ZD/A','MWM32ZD/A','MWM92ZD/A'],
'Ru':['MWLU2RU/A','MWM22RU/A','MWM82RU/A','MWLT2RU/A','MWM02RU/A','MWM72RU/A','MWLY2RU/A','MWM62RU/A','MWMD2RU/A','MWLW2RU/A','MWM42RU/A','MWMA2RU/A','MWLX2RU/A','MWM52RU/A','MWMC2RU/A','MWLV2RU/A','MWM32RU/A','MWM92RU/A'],
'Fr':['MWLU2ZD/A','MWM22ZD/A','MWM82ZD/A','MWLT2ZD/A','MWM02ZD/A','MWM72ZD/A','MWLY2ZD/A','MWM62ZD/A','MWMD2ZD/A','MWLW2ZD/A','MWM42ZD/A','MWMA2ZD/A','MWLX2ZD/A','MWM52ZD/A','MWMC2ZD/A','MWLV2ZD/A','MWM32ZD/A','MWM92ZD/A']
},

'Ipad':{
'Tw':['MW742TA/A','MW6A2TA/A','MW772TA/A','MW6E2TA/A','MW752TA/A','MW6C2TA/A','MW782TA/A','MW6F2TA/A','MW762TA/A','MW6D2TA/A','MW792TA/A','MW6G2TA/A'],
'Cn':['MW742CH/A','MW6P2CH/A','MW772CH/A','MW6T2CH/A','MW752CH/A','MW6Q2CH/A','MW782CH/A','MW6U2CH/A','MW762CH/A','MW6R2CH/A','MW792CH/A','MW6V2CH/A'],
'Jp':['MW742J/A','MW6A2J/A','MW772J/A','MW6E2J/A','MW752J/A','MW6C2J/A','MW782J/A','MW6F2J/A','MW762J/A','MW6D2J/A','MW792J/A','MW6G2J/A'],
'Hk':['MW742ZP/A','MW6A2ZP/A','MW772ZP/A','MW6E2ZP/A','MW752ZP/A','MW6C2ZP/A','MW782ZP/A','MW6F2ZP/A','MW762ZP/A','MW6D2ZP/A','MW792ZP/A','MW6G2ZP/A'],
'Uk':['MW742B/A','MW6A2B/A','MW772B/A','MW6E2B/A','MW752B/A','MW6C2B/A','MW782B/A','MW6F2B/A','MW762B/A','MW6D2B/A','MW792B/A','MW6G2B/A'],
'De':['MW742FD/A','MW6A2FD/A','MW772FD/A','MW6E2FD/A','MW752FD/A','MW6C2FD/A','MW782FD/A','MW6F2FD/A','MW762FD/A','MW6D2FD/A','MW792FD/A','MW6G2FD/A'],
'Ru':['MW742RU/A','MW6A2RU/A','MW772RU/A','MW6E2RU/A','MW752RU/A','MW6C2RU/A','MW782RU/A','MW6F2RU/A','MW762RU/A','MW6D2RU/A','MW792RU/A','MW6G2RU/A'],
'Fr':['MW742NF/A','MW6A2NF/A','MW772NF/A','MW6E2NF/A','MW752NF/A','MW6C2NF/A','MW782NF/A','MW6F2NF/A','MW762NF/A','MW6D2NF/A','MW792NF/A','MW6G2NF/A']
},

'AppleWatch5':{
'Tw': ['MWV82TA/A','MWVF2TA/A'],
'Cn': ['MWV82CH/A','MWX32CH/A','MWVF2CH/A','MWWE2CH/A'],
'Jp': ['MWV82J/A','MWX32J/A','MWVF2J/A','MWWE2J/A'],
'Hk': ['MWV82ZP/A','MWX32ZP/A','MWVF2ZP/A','MWWE2ZP/A'],
'Uk': ['MWV82B/A','MWX32B/A','MWVF2B/A','MWWE2B/A'],
'De': ['MWV82FD/A','MWX32FD/A','MWVF2FD/A','MWWE2FD/A'],
'Ru': ['MWV82RU/A','MWVF2RU/A'],
'Fr': ['MWV82NF/A','MWX32NF/A','MWVF2NF/A','MWWE2NF/A']
},


'AppleWatch4':{
'Cn': ['MU642CH/A','MTVA2CH/A','MU6A2CH/A','MTVR2CH/A'],
'Jp': ['MU642J/A','MU6A2J/A','MTVA2J/A','MTVR2J/A'],
'Hk': ['MU642ZP/A','MU6A2ZP/A','MTVA2ZP/A','MTVR2ZP/A'],
'Uk': ['MU642B/A','MU6A2B/A','MTVA2B/A','MTVR2B/A'],
'De': ['MU642FD/A','MU6A2FD/A','MTVA2FD/A','MTVR2FD/A'],
'Ru': ['MU642RU/A','MU6A2RU/A'], #38.42 GPS
'Fr': ['MU642NF/A','MU6A2NF/A','MTVA2NF/A','MTVR2NF/A']
# 'Sg': ['MU642ZA/A','MU6A2ZA/A','MTVA2ZA/A','MTVR2ZA/A']
},


'AppleWatch3':{
'Tw': ['MTEY2TA/A','MTGN2TA/A', 'MTF22TA/A', 'MTH12TA/A'],
'Cn': ['MTEY2CH/A','MTGK2CH/A','MTF22CH/A','MTGX2CH/A'],
'Jp': ['MTEY2J/A', 'MTGN2J/A','MTF22J/A','MTH12J/A'],
'Hk': ['MTEY2ZP/A', 'MTGN2ZP/A', 'MTF22ZP/A','MTH12ZP/A'],
'Uk': ['MTEY2B/A','MTGN2B/A','MTF22B/A','MTH12B/A'],
'De': ['MTEY2ZD/A','MTGN2ZD/A','MTF22ZD/A','MTH12ZD/A'],
'Ru': ['MTEY2RU/A','MTF22RU/A'], #38.42 GPS
'Fr': ['MTEY2ZD/A','MTGN2ZD/A','MTF22ZD/A','MTH12ZD/A']
# 'Sg': ['MTEY2ZP/A','MTGN2ZP/A','MTF22ZP/A','MTH12ZP/A']
},

'IphoneXs-Max':{
'Tw':['MT512TA/A','MT542TA/A','MT572TA/A','MT502TA/A','MT532TA/A','MT562TA/A','MT522TA/A','MT552TA/A','MT582TA/A'],
'Cn':['MT722CH/A','MT752CH/A','MT782CH/A','MT712CH/A','MT742CH/A','MT772CH/A','MT732CH/A','MT762CH/A','MT792CH/A'],
'Jp':['MT6R2J/A','MT6V2J/A','MT6Y2J/A','MT6Q2J/A','MT6U2J/A','MT6X2J/A','MT6T2J/A','MT6W2J/A','MT702J/A'],
'Hk':['MT722ZA/A','MT752ZA/A','MT782ZA/A','MT712ZA/A','MT742ZA/A','MT772ZA/A','MT732ZA/A','MT762ZA/A','MT792ZA/A'],
'Uk':['MT512B/A','MT542B/A','MT572B/A','MT502B/A','MT532B/A','MT562B/A','MT522B/A','MT552B/A','MT582B/A'],
'De':['MT512ZD/A','MT542ZD/A','MT572ZD/A','MT502ZD/A','MT532ZD/A','MT562ZD/A','MT522ZD/A','MT552ZD/A','MT582ZD/A'],
'Ru':['MT512RU/A','MT542RU/A','MT572RU/A','MT502RU/A','MT532RU/A','MT562RU/A','MT522RU/A','MT552RU/A','MT582RU/A'],
'Fr':['MT512ZD/A','MT542ZD/A','MT572ZD/A','MT502ZD/A','MT532ZD/A','MT562ZD/A','MT522ZD/A','MT552ZD/A','MT582ZD/A']
# 'Sg':['MT512ZP/A','MT542ZP/A','MT572ZP/A','MT502ZP/A','MT532ZP/A','MT562ZP/A','MT522ZP/A','MT552ZP/A','MT582ZP/A']
},

'IphoneXs':{
'Tw':['MT9F2TA/A','MT9J2TA/A','MT9M2TA/A','MT9E2TA/A','MT9H2TA/A','MT9L2TA/A','MT9G2TA/A','MT9K2TA/A','MT9N2TA/A'],
'Cn':['MT9Q2CH/A','MT9U2CH/A','MT9X2CH/A','MT9P2CH/A','MT9T2CH/A','MT9W2CH/A','MT9R2CH/A','MT9V2CH/A','MT9Y2CH/A'],
'Jp':['MTAX2J/A','MTE12J/A','MTE42J/A','MTAW2J/A','MTE02J/A','MTE32J/A','MTAY2J/A','MTE22J/A','MTE52J/A'],
'Hk':['MT952ZA/A','MT982ZA/A','MT9C2ZA/A','MT942ZA/A','MT972ZA/A','MT9A2ZA/A','MT962ZA/A','MT992ZA/A','MT9D2ZA/A'],
'Uk':['MT9F2B/A','MT9J2B/A','MT9M2B/A','MT9E2B/A','MT9H2B/A','MT9L2B/A','MT9G2B/A','MT9K2B/A','MT9N2B/A'],
'De':['MT9F2ZD/A','MT9J2ZD/A','MT9M2ZD/A','MT9E2ZD/A','MT9H2ZD/A','MT9L2ZD/A','MT9G2ZD/A','MT9K2ZD/A','MT9N2ZD/A'],
'Ru':['MT9F2RU/A','MT9J2RU/A','MT9M2RU/A','MT9E2RU/A','MT9H2RU/A','MT9L2RU/A','MT9G2RU/A','MT9K2RU/A','MT9N2RU/A'],
'Fr':['MT9F2ZD/A','MT9J2ZD/A','MT9M2ZD/A','MT9E2ZD/A','MT9H2ZD/A','MT9L2ZD/A','MT9G2ZD/A','MT9K2ZD/A','MT9N2ZD/A']
# 'Sg':['MT9F2ZP/A','MT9J2ZP/A','MT9M2ZP/A','MT9E2ZP/A','MT9H2ZP/A','MT9L2ZP/A','MT9G2ZP/A','MT9K2ZP/A','MT9N2ZP/A']
},

'IphoneXr':{
'Tw': ['MRY52TA/A', 'MRYD2TA/A','MRYL2TA/A','MRY42TA/A','MRY92TA/A', 'MRYJ2TA/A','MRYA2TA/A','MRYH2TA/A',
	'MRYQ2TA/A','MRY72TA/A','MRYF2TA/A','MRYN2TA/A', 'MRY82TA/A','MRYG2TA/A','MRYP2TA/A', 'MRY62TA/A','MRYE2TA/A','MRYM2TA/A'],

'Cn': ['MT132CH/A', 'MT1A2CH/A','MT1J2CH/A','MT122CH/A','MT192CH/A', 'MT1H2CH/A','MT182CH/A','MT1G2CH/A', 
	'MT1Q2CH/A','MT162CH/A','MT1E2CH/A','MT1M2CH/A', 'MT172CH/A','MT1F2CH/A','MT1P2CH/A' ,'MT142CH/A','MT1D2CH/A','MT1L2CH/A'],

'Jp': ['MT032J/A', 'MT0J2J/A','MT0W2J/A','MT002J/A','MT0G2J/A', 'MT0V2J/A','MT0E2J/A','MT0U2J/A', 'MT112J/A',
'MT082J/A','MT0Q2J/A','MT0Y2J/A', 'MT0A2J/A','MT0T2J/A','MT102J/A', 'MT062J/A','MT0N2J/A','MT0X2J/A'],

'Hk': ['MT132ZA/A', 'MT1A2ZA/A','MT1J2ZA/A','MT122ZA/A','MT192ZA/A', 'MT1H2ZA/A','MT182ZA/A','MT1G2ZA/A',
 'MT1Q2ZA/A','MT162ZA/A','MT1E2ZA/A','MT1M2ZA/A', 'MT172ZA/A','MT1F2ZA/A','MT1P2ZA/A', 'MT142ZA/A','MT1D2ZA/A','MT1L2ZA/A'],

'Uk': ['MRY52B/A', 'MRYD2B/A','MRYL2B/A','MRY42B/A','MRY92B/A', 'MRYJ2B/A','MRYA2B/A','MRYH2B/A', 'MRYQ2B/A',
'MRY72B/A','MRYF2B/A','MRYN2B/A', 'MRY82B/A','MRYG2B/A','MRYP2B/A', 'MRY62B/A','MRYE2B/A','MRYM2B/A'],

'De': ['MRY52ZD/A','MRYD2ZD/A','MRYL2ZD/A','MRY42ZD/A','MRY92ZD/A', 'MRYJ2ZD/A','MRYA2ZD/A','MRYH2ZD/A',
 'MRYQ2ZD/A','MRY72ZD/A','MRYF2ZD/A','MRYN2ZD/A', 'MRY82ZD/A','MRYG2ZD/A','MRYP2ZD/A', 'MRY62ZD/A','MRYE2ZD/A','MRYM2ZD/A'],

'Ru': ['MRY52RU/A','MRYD2RU/A','MRYL2RU/A','MRY42RU/A','MRY92RU/A', 'MRYJ2RU/A','MRYA2RU/A','MRYH2RU/A',
 'MRYQ2RU/A','MRY72RU/A','MRYF2RU/A','MRYN2RU/A', 'MRY82RU/A','MRYG2RU/A','MRYP2RU/A', 'MRY62RU/A','MRYE2RU/A','MRYM2RU/A'],

'Fr': ['MRY52ZD/A','MRYD2ZD/A','MRYL2ZD/A','MRY42ZD/A','MRY92ZD/A', 'MRYJ2ZD/A','MRYA2ZD/A','MRYH2ZD/A',
 'MRYQ2ZD/A','MRY72ZD/A','MRYF2ZD/A','MRYN2ZD/A', 'MRY82ZD/A','MRYG2ZD/A','MRYP2ZD/A', 'MRY62ZD/A','MRYE2ZD/A','MRYM2ZD/A']
 },


'Iphone8-plus':{
'Tw': ['MQ8M2TA/A', 'MQ8Q2TA/A','MQ8L2TA/A','MQ8P2TA/A','MQ8N2TA/A', 'MQ8R2TA/A'],
'Cn': ['MQ8E2CH/A','MQ8H2CH/A','MQ8F2CH/A','MQ8J2CH/A','MQ8D2CH/A','MQ8G2CH/A'],
'Jp': ['MQ9L2J/A','MQ9P2J/A','MQ9M2J/A','MQ9Q2J/A','MQ9K2J/A','MQ9N2J/A'],
'Hk': ['MQ8E2ZP/A','MQ8H2ZP/A','MQ8F2ZP/A','MQ8J2ZP/A','MQ8D2ZP/A','MQ8G2ZP/A'],
'Uk': ['MQ8M2B/A','MQ8Q2B/A','MQ8N2B/A','MQ8R2B/A','MQ8L2B/A','MQ8P2B/A'],
'De': ['MQ8M2ZD/A','MQ8Q2ZD/A','MQ8N2ZD/A','MQ8R2ZD/A','MQ8L2ZD/A','MQ8P2ZD/A'],
'Ru': ['MQ8M2RU/A','MQ8Q2RU/A','MQ8N2RU/A','MQ8R2RU/A','MQ8L2RU/A','MQ8P2RU/A'],
'Fr': ['MQ8M2ZD/A','MQ8Q2ZD/A','MQ8N2ZD/A','MQ8R2ZD/A','MQ8L2ZD/A','MQ8P2ZD/A']
},


'Iphone8':{
'Tw': ['MQ6H2TA/A', 'MQ7D2TA/A','MQ6J2TA/A','MQ7E2TA/A','MQ6G2TA/A', 'MQ7C2TA/A'],
'Cn': ['MQ6L2CH/A', 'MQ7G2CH/A','MQ6M2CH/A','MQ7H2CH/A','MQ6K2CH/A', 'MQ7F2CH/A'],
'Jp': ['MQ792J/A', 'MQ852J/A','MQ7A2J/A','MQ862J/A','MQ782J/A', 'MQ842J/A'],
'Hk': ['MQ6L2ZP/A', 'MQ7G2ZP/A','MQ6M2ZP/A','MQ7H2ZP/A','MQ6K2ZP/A', 'MQ7F2ZP/A'],
'Uk': ['MQ6H2B/A', 'MQ7D2B/A','MQ6J2B/A','MQ7E2B/A','MQ6G2B/A', 'MQ7C2B/A'],
'De': ['MQ6H2ZD/A','MQ7D2ZD/A','MQ6J2ZD/A','MQ7E2ZD/A','MQ6G2ZD/A', 'MQ7C2ZD/A'],
'Ru': ['MQ6H2RU/A','MQ7D2RU/A','MQ6J2RU/A','MQ7E2RU/A','MQ6G2RU/A', 'MQ7C2RU/A'],
'Fr': ['MQ6H2ZD/A','MQ7D2ZD/A','MQ6J2ZD/A','MQ7E2ZD/A','MQ6G2ZD/A', 'MQ7C2ZD/A']
},

'IpadPro':{
'Tw': ['MTXR2TA/A','MTXU2TA/A','MTFN2TA/A','MTFQ2TA/A'],
'Cn': ['MTXR2CH/A','MTXU2CH/A','MTFN2CH/A','MTFQ2CH/A'],
'Jp': ['MTXR2J/A','MTXU2J/A','MTFN2J/A','MTFQ2J/A'],
'Hk': ['MTXR2ZP/A','MTXU2ZP/A','MTFN2ZP/A','MTFQ2ZP/A'],
'Uk': ['MTXR2B/A','MTXU2B/A','MTFN2B/A','MTFQ2B/A'],
'De': ['MTXR2FD/A','MTXU2FD/A','MTFN2FD/A','MTFQ2FD/A'],
'Ru': ['MTXR2RU/A','MTXU2RU/A','MTFN2RU/A','MTFQ2RU/A'],
'Fr': ['MTXR2NF/A','MTXU2NF/A','MTFN2NF/A','MTFQ2NF/A'],
'Br': ['MTXQ2BZ/A','MTXT2BZ/A','MTFL2BZ/A','MTFP2BZ/A'],
'Mx': ['MTXR2LZ/A','MTXU2LZ/A','MTFN2LZ/A','MTFQ2LZ/A']
}
	}
#country ditionary end



Us ={
	'IphoneSE':[
	'MX9P2LL/A','MXCX2LL/A','MXVQ2LL/A',
	'MX9N2LL/A','MXCW2LL/A','MXVP2LL/A',
	'MX9Q2LL/A','MXCY2LL/A','MXVR2LL/A'],

	'AirPodPro':['MWP22AM/A'],
	'IphoneXr':[
	'MT3L2LL/A', 'MT3U2LL/A','MT412LL/A','MT3K2LL/A','MT3T2LL/A', 'MT402LL/A','MT3R2LL/A','MT3Y2LL/A', 'MT462LL/A',
	'MT3N2LL/A','MT3W2LL/A','MT442LL/A', 'MT3Q2LL/A','MT3X2LL/A','MT452LL/A', 'MT3M2LL/A','MT3V2LL/A','MT422LL/A'],

	'IphoneXs-Max':['MT5A2LL/A','MT5E2LL/A','MT5H2LL/A','MT592LL/A','MT5D2LL/A','MT5G2LL/A','MT5C2LL/A','MT5F2LL/A','MT5J2LL/A'],
	'IphoneXs':['MT952LL/A','MT982LL/A','MT9C2LL/A','MT942LL/A','MT972LL/A','MT9A2LL/A','MT962LL/A','MT992LL/A','MT9D2LL/A'],
	'Iphone8-plus':['MQ8E2LL/A','MQ8H2LL/A','MQ8F2LL/A','MQ8J2LL/A','MQ8D2LL/A','MQ8G2LL/A'],
	'Iphone8':['MQ6L2LL/A', 'MQ7G2LL/A','MQ6M2LL/A', 'MQ7H2LL/A','MQ6K2LL/A','MQ7F2LL/A'],
	'AppleWatch3':['MTEY2LL/A', 'MTGG2LL/A', 'MTF22LL/A', 'MTGR2LL/A'],
	'AppleWatch4':['MU642LL/A',	'MU6A2LL/A','MTUD2LL/A','MTUU2LL/A'],
	'IpadPro':['MTXR2LL/A','MTXU2LL/A','MTFN2LL/A','MTFQ2LL/A'],

	'Iphone11Pro':['MWCH2LL/A','MWCM2LL/A','MWCR2LL/A','MWCJ2LL/A','MWCN2LL/A','MWCT2LL/A','MWCL2LL/A','MWCQ2LL/A','MWCV2LL/A','MWCK2LL/A','MWCP2LL/A','MWCU2LL/A'],

	'IPhone11Pro-Max':['MWGY2LL/A','MWH42LL/A','MWH82LL/A','MWH02LL/A','MWH52LL/A','MWH92LL/A','MWH22LL/A','MWH72LL/A','MWHC2LL/A',
	'MWH12LL/A','MWH62LL/A','MWHA2LL/A'],

	'IPhone11':['MWL82LL/A','MWLF2LL/A','MWLM2LL/A','MWL72LL/A','MWLE2LL/A','MWLL2LL/A','MWLD2LL/A','MWLK2LL/A','MWLR2LL/A','MWLA2LL/A',
	'MWLH2LL/A','MWLP2LL/A','MWLC2LL/A','MWLJ2LL/A','MWLQ2LL/A','MWL92LL/A','MWLG2LL/A','MWLN2LL/A'],

	'Ipad':['MW742LL/A','MW6W2LL/A','MW772LL/A','MW702LL/A','MW752LL/A','MW6X2LL/A','MW782LL/A','MW712LL/A',
	'MW762LL/A','MW6Y2LL/A','MW792LL/A','MW722LL/A'],

	'AppleWatch5':['MWV82LL/A','MWWQ2LL/A','MWVF2LL/A','MWW12LL/A']
	}
Product_Us_R = {k: key for key, value in Us.items() for k in value}
# for key,value in Us.items()
	# for k in value
		# k = key
#---------------------------------------------------------------- Colors-----------------------------------------------------------#
Colors = {


'Silver' : ['MQ8E2', 'MQ9E2', 'MQ972', 'MQ8H2', 'MQ9A2', 'MQ9H2', 'MQ8M2', 'MQ8U2', 'MQ912', 'MQ8Q2', 'MQ8X2', 'MQ942','MQ9L2','MQ9P2',
		'MQAK2', 'MQAR2', 'MQAD2', 'MQAN2', 'MQAV2', 'MQAG2', 'MQCT2', 'MQCL2', 'MQAY2', 'MQA62','MQCW2', 'MQCP2', 'MQC22', 'MQA92',
		#iphone8
		'MQ6H2', 'MQ6W2', 'MQ702','MQ7D2', 'MQ7R2', 'MQ7V2','MQ6L2', 'MQ732', 'MQ762','MQ7G2', 'MQ7Y2', 'MQ822','MQ792','MQ852',
		#iphoneXs
		'MT952','MT982','MT9C2','MT9F2','MT9J2','MT9M2','MT9Q2','MT9U2','MT9X2','MTAX2','MTE12','MTE42',
		#iphoneXsMax
		'MT512','MT542','MT572','MT5A2','MT5E2','MT5H2','MT6R2','MT6V2','MT6Y2','MT722','MT752','MT782',
		#iphone11Pro
		'MWCJ2','MWCN2','MWCT2','MWC32','MWC82','MWCE2','MWDA2','MWDF2','MWDK2',
		#iphone11ProMax
		'MWH02','MWH52','MWH92','MWHF2','MWHK2','MWHP2','MWEW2','MWF22','MWF62',
		#iPad
		'MW752','MW6X2','MW782','MW712','MW6C2','MW6F2','MW6Q2','MW6U2'],

'Gold' : ['MQ8F2', 'MQ9F2', 'MQ982','MQ8J2', 'MQ9C2', 'MQ9J2', 'MQ8N2', 'MQ8V2', 'MQ922','MQ8R2', 'MQ8Y2', 'MQ952','MQ9M2','MQ9Q2',
		#iphone8
		'MQ6M2', 'MQ742', 'MQ772', 'MQ7H2', 'MQ802', 'MQ832', 'MQ6J2', 'MQ6X2', 'MQ712', 'MQ7E2', 'MQ7T2', 'MQ7W2','MQ7A2','MQ862',
		#iphoneXs
		'MT962','MT992','MT9D2','MT9G2','MT9K2','MT9N2','MT9R2','MT9V2','MT9Y2','MTAY2','MTE22','MTE52',
		#iphoneXsMax
		'MT522','MT552','MT5F2','MT582','MT5C2','MT6W2','MT5J2','MT6T2','MT762','MT702','MT732','MT792',
		#iphone11Pro
		'MWCK2','MWCP2','MWCU2','MWC52','MWC92','MWCF2','MWDC2','MWDG2','MWDL2',
		#iphone11ProMax
		'MWH12','MWH62','MWHA2','MWHG2','MWHL2','MWHQ2','MWEX2','MWF32','MWF72',
		#iPad
		'MW762','MW6Y2','MW792','MW722','MW6D2','MW6G2','MW6R2','MW6V2'],


'Gray' : ['MQ8D2', 'MQ9D2', 'MQ962', 'MQ8G2', 'MQ9G2', 'MQ992', 'MQ8L2', 'MQ8T2', 'MQ902', 'MQ8P2', 'MQ8W2', 'MQ932','MQ9K2','MQ9N2',
		'MQAJ2', 'MQAQ2', 'MQAC2', 'MQAM2', 'MQAU2', 'MQAF2','MQCR2', 'MQCK2', 'MQAX2', 'MQA52','MQCV2', 'MQCN2', 'MQC12', 'MQA82',
		#iphone8
		'MQ6K2','MQ722','MQ752','MQ7F2','MQ7X2','MQ812','MQ6G2','MQ6V2', 'MQ6Y2','MQ7C2','MQ7Q2','MQ7U2','MQ782','MQ842',
		#iphoneXs
		'MT942','MT972','MT9A2','MT9E2','MT9H2','MT9L2','MT9P2','MT9T2','MT9W2','MTAW2','MTE02','MTE32',
		#iphoneXsMax
		'MT502','MT532','MT562','MT592','MT5D2','MT5G2','MT6Q2','MT6U2','MT6X2','MT712','MT742','MT772',
		#iphone11Pro
		'MWCH2','MWCM2','MWCR2','MWC22','MWC72','MWCD2','MWD92','MWDE2','MWDJ2',
		#iphone11ProMax
		'MWGY2','MWH42','MWH82','MWHD2','MWHJ2','MWHN2','MWEV2','MWF12','MWF52',
		#iPad
		'MW742','MW6W2','MW772','MW702','MW6A2','MW6E2','MW6P2','MW6T2'],

'Red' : ['MRTG2', 'MRTJ2', 'MRT72', 'MRTH2', 'MRTK2', 'MRT82', 'MRTC2', 'MRTE2', 'MRT92', 'MRTA2', 'MRTD2', 'MRTF2','MRTL2','MRTM2',
		#iphone8
		'MRRK2', 'MRRR2', 'MRRT2', 'MRRL2', 'MRRW2', 'MRRX2', 'MRRM2', 'MRRP2', 'MRRQ2', 'MRRN2', 'MRRU2', 'MRRV2',
		#iphoneXr
		 'MT3M2','MT3V2','MT422','MRY62','MRYE2','MRYM2','MT142','MT1D2','MT1L2','MT062','MT0N2','MT0X2',
		#iphon11
		'MWL92','MWLG2','MWLN2','MWLV2','MWM32','MWM92','MWN22','MWN92','MWNH2',
		#iphoneSE
		'MX9Q2','MXCY2','MXVR2','MX9U2','MXD22','MXVV2','MXAP2','MXD82','MXW22'],

'White' : [#iphoneXr
		'MT3L2', 'MT3U2','MT412','MRY52', 'MRYD2', 'MRYL2', 'MT132', 'MT1A2', 'MT1J2', 'MT032', 'MT0J2', 'MT0W2',
		#iphone11
		'MWL82','MWLF2','MWLM2','MWLU2','MWM22','MWM82','MWN12','MWN82','MWNG2',
		#iphoneSE
		'MX9P2','MXCX2','MXVQ2','MX9T2','MXD12','MXVU2','MXW12','MXAN2','MXD72'],

'Black' : [#iphoneXr
		'MT3K2','MT3T2', 'MT402','MRY42','MRY92', 'MRYJ2','MT122','MT192', 'MT1H2','MT002','MT0G2', 'MT0V2',
		#iphone11
		'MWL72','MWLE2','MWLL2','MWLT2','MWM02','MWM72','MWN02','MWN72','MWNF2',
		#iphoneSE
		'MX9N2','MXCW2','MXVP2','MX9R2','MXD02','MXVT2','MXAM2','MXD62','MXW02'],

'Green' : [#iphone11
			'MWLD2','MWLK2','MWLR2','MWLY2','MWM62','MWMD2','MWN62','MWNE2','MWNL2',
			#iphone11Pro
			'MWCL2','MWCQ2','MWCV2','MWC62','MWCC2','MWCG2','MWDD2','MWDH2','MWDM2',
			#iphone11ProMax
			'MWH22','MWH72','MWHC2','MWHH2','MWHM2','MWHR2','MWF02','MWF42','MWF82'],

'Purple' : [#iphone11
		'MWLC2','MWLJ2','MWLQ2','MWLX2','MWM52','MWMC2','MWN52','MWND2','MWNK2'],

'Blue' : [#iphoneXr
		'MT3R2','MT3Y2', 'MT462','MRYA2','MRYH2', 'MRYQ2','MT182','MT1G2', 'MT1Q2','MT0E2','MT0U2', 'MT112'],

'Yellow' : [#iphoneXr 
		'MT3N2','MT3W2','MT442', 'MRY72','MRYF2','MRYN2','MT162','MT1E2','MT1M2','MT082','MT0Q2','MT0Y2',
		#iphone11
		'MWLA2','MWLH2','MWLP2','MWLW2','MWM42','MWMA2','MWN32','MWNC2','MWNJ2'],

'Coral' : [#iphoneXr
		'MT3Q2','MT3X2','MT452','MRY82','MRYG2','MRYP2','MT172','MT1F2','MT1P2','MT0A2','MT0T2','MT102'],


'GPS' : [# Iphone Watch 3
		'MTEY2', 'MTF22',
		# Iphone Watch 4
		'MU642','MU6A2',
		#Iphone Watch 5
		'MWV82','MWVF2'],

'GPSCelluar' :[# Iphone Watch 3
			'MTGG2', 'MTGN2', 'MTGK2','MTGR2','MTGX2','MTH12',
			# Iphone Watch 4
			'MTUD2','MTUU2','MTVA2','MTVR2',
			# Iphone Watch 5
			'MWWQ2','MWW12','MWX32','MWWE2'],

'11inch' :[	#Ipad Pro
			'MTXR2','MTXU2','MTXQ2','MTXT2'],
'12.9inch':[#Ipad Pro
			'MTFN2','MTFQ2','MTFL2','MTFP2'],
			}

#iphone11Pro
#iphone11ProMax
#iphone11
#Ipad
#Iphone Watch 5
print("1")
Color_R = {k: key for key, value in Colors.items() for k in value}
#---------------------------------------------------------------- SIZE -------------------------------------------------------------#
Size = {

'32GB' : [#Ipad
			'MW742','MW6W2','MW752','MW6X2','MW762','MW6Y2','MW6A2','MW6C2','MW6D2','MW6P2','MW6Q2','MW6R2'],
'64GB' : [
			'MQ8F2', 'MQ9F2', 'MQ982', 'MQ8E2', 'MQ9E2', 'MQ972', 'MQ8D2', 'MQ9D2', 'MQ962', 'MRTG2', 'MRTJ2', 'MRT72',
			'MQ8N2', 'MQ8V2', 'MQ922', 'MQ8M2', 'MQ8U2', 'MQ912', 'MQ8L2', 'MQ8T2', 'MQ902', 'MRTC2', 'MRTE2', 'MRT92',
			'MQ9L2', 'MQ9M2', 'MQ9K2', 'MRTL2', 'MQAK2', 'MQAR2', 'MQAD2', 'MQCT2', 'MQCL2', 'MQAY2', 'MQA62', 'MQCR2',
			'MQCK2', 'MQAX2', 'MQA52', 'MQAJ2', 'MQAQ2', 'MQAC2',
			#Iphone8
			'MQ6M2', 'MQ742', 'MQ772','MQ6L2', 'MQ732', 'MQ762','MQ6K2', 'MQ722', 'MQ752','MRRK2', 'MRRR2', 'MRRT2','MQ6J2',
			 'MQ6X2', 'MQ712','MQ6H2', 'MQ6W2', 'MQ702','MQ6G2', 'MQ6V2','MQ6Y2','MRRM2', 'MRRP2', 'MRRQ2','MQ792','MQ7A2','MQ782',

			#IphoneXr
			'MRY52','MRY42','MRYA2','MRY72','MRY82','MRY62','MT132','MT122','MT182','MT162','MT172','MT142','MT032','MT002','MT0E2',
			'MT082','MT0A2','MT062','MT3L2','MT3K2','MT3R2','MT3N2','MT3Q2', 'MT3M2',

			#IphoneXs
			'MT942','MT952','MT962','MT9E2','MT9F2','MT9G2','MT9P2','MT9Q2','MT9R2','MTAW2','MTAX2','MTAY2',

			#IphoneXsMax
			#'MT502','MT512','MT522','MT592','MT5A2','MT5C2','MT6Q2','MT6R2','MT6T2','MT712','MT722','MT732',
			#iphone11Pro
			'MWCH2','MWCJ2','MWCL2','MWCK2','MWC22','MWC32','MWC62','MWC52','MWD92','MWDA2','MWDD2','MWDC2',
			#iphone11ProMax
			'MWGY2','MWH02','MWH22','MWH12','MWHD2','MWHF2','MWHH2','MWHG2','MWEV2','MWEW2','MWF02','MWEX2',
			#iphone11
			'MWL82','MWL72','MWLD2','MWLA2','MWLC2','MWL92','MWLU2','MWLT2','MWLY2','MWLW2','MWLX2','MWLV2','MWN12','MWN02','MWN62','MWN32','MWN52','MWN22',
			#iphoneSE
			'MX9P2','MX9N2','MX9Q2','MX9T2','MX9R2','MX9U2','MXAN2','MXAM2','MXAP2'],

'128GB' : [
			#IphonXr
			'MRYD2','MRY92','MRYH2','MRYF2','MRYG2','MRYE2','MT1A2','MT192','MT1G2','MT1E2','MT1F2','MT1D2', 'MT0J2','MT0G2','MT0U2',
			'MT0Q2','MT0T2','MT0N2','MT3U2','MT3T2','MT3Y2','MT3W2','MT3X2','MT3V2',
			#Ipad
			'MW772','MW702','MW782','MW712','MW792','MW722','MW6E2','MW6F2','MW6G2','MW6T2','MW6U2','MW6V2',
			#Iphone11
			'MWLF2','MWLE2','MWLK2','MWLH2','MWLJ2','MWLG2','MWM22','MWM02','MWM62','MWM42','MWM52','MWM32','MWN82','MWN72','MWNE2','MWNC2','MWND2','MWN92',
			#iphoneSE
			'MXCX2','MXCW2','MXCY2','MXD12','MXD02','MXD22','MXD72','MXD62','MXD82'],
'256GB' : [
			#Iphone8 
			#'MQ7H2', 'MQ802', 'MQ832','MQ7G2', 'MQ7Y2', 'MQ822','MQ7F2', 'MQ7X2', 'MQ812','MRRL2', 'MRRW2', 'MRRX2','MQ7E2',
			#'MQ7T2', 'MQ7W2','MQ7D2', 'MQ7R2', 'MQ7V2',	'MQ7C2', 'MQ7Q2', 'MQ7U2','MRRN2', 'MRRU2', 'MRRV2',
			#Iphone8plus
			#'MQ8J2', 'MQ9C2', 'MQ9J2','MQ8H2', 'MQ9A2', 'MQ9H2','MQ8G2', 'MQ9G2', 'MQ992','MRTH2', 'MRTK2', 'MRT82','MQ8R2', 'MQ8Y2',
			#'MQ952','MQ8Q2', 'MQ8X2', 'MQ942','MQ8P2', 'MQ8W2', 'MQ932','MRTA2', 'MRTD2', 'MRTF2','MQ852','MQ862','MQ842','MQ9P2',
			#'MQ9Q2','MQ9N2',
			#IphoneXr
			#'MRYL2','MRYJ2','MRYQ2','MRYN2','MRYP2','MRYM2','MT1J2','MT1H2','MT1Q2','MT1M2','MT1P2','MT1L2','MT0W2','MT0V2',
			#'MT112','MT0Y2','MT102','MT0X2','MT412', 'MT402', 'MT462','MT442', 'MT452','MT422',
			#IphoneXs
			#'MT972','MT982','MT992','MT9H2','MT9J2','MT9K2','MT9T2','MT9U2','MT9V2','MTE02','MTE12','MTE22',
			#IphoneXsMax
			#'MT532','MT542','MT552','MT5D2','MT5E2','MT5F2','MT6U2','MT6V2','MT6W2','MT742','MT752','MT762',
			#IpadPro
			'MTXR2','MTFN2','MTXQ2','MTFL2',
			#iphone11Pro
			'MWCM2','MWCN2','MWCQ2','MWCP2','MWC72','MWC82','MWCC2','MWC92','MWDE2','MWDF2','MWDH2','MWDG2',
			#iphone11ProMax
			'MWH42','MWH52','MWH72','MWH62','MWHJ2','MWHK2','MWHM2','MWHL2','MWF12','MWF22','MWF42','MWF32',
			#iphone11
			'MWLM2','MWLL2','MWLR2','MWLP2','MWLQ2','MWLN2','MWM82','MWM72','MWMD2','MWMA2','MWMC2','MWM92','MWNG2','MWNF2','MWNL2','MWNJ2','MWNK2','MWNH2',
			#iphoneSE
			'MXVQ2','MXVP2','MXVR2','MXVU2','MXVT2','MXVV2','MXW12','MXW02','MXW22'],

'512GB' : [
			#IphoneXs
			'MT9A2','MT9C2','MT9D2','MT9L2','MT9M2','MT9N2','MT9W2','MT9X2','MT9Y2','MTE32','MTE42','MTE52',
			#IphoneXsMax
			#'MT562','MT572','MT582','MT5G2','MT5H2','MT5J2','MT6X2','MT6Y2','MT702','MT772','MT782','MT792',
			#IpadPro
			'MTXU2','MTFQ2','MTXT2','MTFP2',
			#iphone11Pro
			'MWCR2','MWCT2','MWCV2','MWCU2','MWCD2','MWCE2','MWCG2','MWCF2','MWDJ2','MWDK2','MWDM2','MWDL2',
			#iphone11ProMax
			'MWH82','MWH92','MWHC2','MWHA2','MWHN2','MWHP2','MWHR2','MWHQ2','MWF52','MWF62','MWF82','MWF72'],


#IphoneWatch3
'38mm': ['MTEY2','MTGG2','MTGN2','MTGK2'],
'42mm': ['MTF22','MTGR2','MTH12','MTGX2'],
#IphoneWatch4
'40mm': ['MTUD2','MTVA2','MU642',
#IphoneWqatch5
		'MWV82','MWWQ2','MWX32'],
'44mm': ['MTUU2','MTVR2','MU6A2',
#IphoneWqatch5
		'MWVF2','MWW12','MWWE2']}

#為了方便接下來 不同的 model 進行 Size 的對應 這裡將 key(size) 跟 value(model) 進行對調 變成 Key 為 model ,value 為 size 
# eg:'MQ8F2':'Size_SixFour'

Size_R = {k: key for key, value in Size.items() for k in value}
# for key, value in size.items
# 	for k in value
# 		k: key
#---------------------拿到所有 iphone 分 不同產品的 model 的型號--------------------------#

# 除了US以外 其他所有國家以 [產品] 為 key 對應到所有的 value [型號]
# "{}".format(Product_item) 會產生變數名稱 , eg:{'Iphone8':'MQ6H2TA/A'}
Product = {}
for Product_item in countries.keys(): #countries.keys 是全部的型號
	
	Product["{}".format(Product_item)]= sum([v for v in countries[Product_item].values()], [])

Product_R = {k: key for key, value in Product.items() for k in value}

#拿到所有以[國家] 為 key 對應到所有的 [型號]
Country = {}
for v in countries.values():
  for k in v.keys():
    Country.setdefault(k,[]) # added key
    Country[k] += v[k]

# print(Country)

#以[型號] 為 key 對應到所有的 [國家]
Country_R = {k: key for key, value in Country.items() for k in value}

# 除了US以外所有的 [型號] 併在一起 , 給for迴圈使用
Model_All = sum(list(Product.values()),[])
# 把US所有的 [型號] 併再一起 , 給for迴圈使用
Model_Us = sum(list(Us.values()),[])

res=[]

# 美國的要單獨跑 因為地址網址的dictionary 是空的
for Model in Model_Us:
	# if Product_Us_R[Model] == 'IpadPro':
	# print(Model)
	d = {} #清空dictionary


	d['Country'] = 'Us'
	d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")
	d['Product'] = Product_Us_R[Model]

	# 如果是AirPodPro 因為沒有Size也沒有Color的資訊所以 除了 AirPodPro 以外其他產品都有Color 跟 Size 的 key
	if Product_Us_R[Model] != 'AirPodPro':

		# 如果找不到 Size 就 不去做request. 產品都會對 Size 256GB做下架	
		try:
			d['Size'] = Size_R[Model[0:5]]
			d['Colors'] = Color_R[Model[0:5]]
			url = 'https://www.apple.com/shop/delivery-message?parts.0=%s&little=true' % ( Model )
			r = requests.get(url)
			response = json.loads(r.text)

			d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['quote']
			print(d)
			res.append(d)

		except:
			print(d,'下架')

	#如果是 AirPodPro 直接做 request
	else:
		url = 'https://www.apple.com/shop/delivery-message?parts.0=%s&little=true' % ( Model )
		r = requests.get(url)
		response = json.loads(r.text)

		d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['quote']
		print(d)
		res.append(d)


for Product in countries:
	#外迴圈跑國家
	for Country in countries[Product]:
	#內迴圈跑型號
		for Model in countries[Product][Country]:
			# if Product_R[Model] == 'IpadPro':
			d = {} #清空dictionary
			# 現在 要處理新增的選項一樣丟在color裡嗎XD
			d['Country'] = Country
			d['Product'] = Product_R[Model]
			d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")

			# 如果是AirPod 因為沒有Size也沒有Color的資訊所以單獨處理
			if Product_R[Model] != 'AirPodPro':
				# 如果找不到 Size 就 不去做request. 產品都會對 Size 256GB做下架	
				try:
					d['Size'] = Size_R[Model[0:5]]
					d['Colors'] = Color_R[Model[0:5]]

					url = 'https://www.apple.com/%s/shop/delivery-message?parts.0=%s&little=true' % (d['Country'].lower(), Model)
					r = requests.get(url)

					response = json.loads(r.text)
					d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['quote']
					print(d)
					res.append(d)

				except:
					print(d,'下架')

			else:
				url = 'https://www.apple.com/%s/shop/delivery-message?parts.0=%s&little=true' % (d['Country'].lower(), Model)
				r = requests.get(url)

				response = json.loads(r.text)
				d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['quote']
				print(d)
				res.append(d)
				

newres = res + Old_Data

df = pd.DataFrame(newres)

# Pivot value:欲處理的資訊(相加 取平均 等等等)
#index:列向量
#columns:行向量

df.to_csv(path,encoding='utf_8_sig', index=False)


# #要去哪裡
# destname = "/home/ec2-user/Mainweb/static/Data.csv"
# #來源資料
# fromname = "/home/ec2-user/Mainweb/Data.csv"
# shutil.copy2(fromname, destname)

print("ok")