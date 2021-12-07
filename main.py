import requests
from databox import Client
import pandas as pd

google_api = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
url = 'https://www.databox.com'
api_key = 'AIzaSyCm4wXpCvV5vvqfIifQCffmbOZeQg-ohpw'
dbox_token = 'jrfxjrihrish0t9h2243'

#API Parameters
#Available Categories: ['accessibility', 'best-practices', 'performance', 'pwa', 'seo']
parameters_desktop = {'url': url, 'category': ['accessibility', 'best-practices', 'performance', 'pwa', 'seo'], 'key': api_key}
parameters_mobile = {'url': url, 'category': ['accessibility', 'best-practices', 'performance', 'pwa', 'seo'], 'strategy': 'mobile', 'key': api_key}

#API responses
response_desktop = requests.get(google_api, params=parameters_desktop)
response_mobile = requests.get(google_api, params=parameters_mobile)

# Desktop CLS 
cls_desktop = (response_desktop.json().get('loadingExperience').get('metrics').get('CUMULATIVE_LAYOUT_SHIFT_SCORE').get('distributions'))
# Desktop FID
fid_desktop = (response_desktop.json().get('loadingExperience').get('metrics').get('FIRST_INPUT_DELAY_MS').get('distributions'))
# Desktop LCP
lcp_desktop = (response_desktop.json().get('loadingExperience').get('metrics').get('LARGEST_CONTENTFUL_PAINT_MS').get('distributions'))
# Desktop SEO
seo_desktop = (response_desktop.json().get('lighthouseResult').get('categories').get('seo').get('score'))


# Mobile CLS 
cls_mobile = (response_mobile.json().get('loadingExperience').get('metrics').get('CUMULATIVE_LAYOUT_SHIFT_SCORE').get('distributions'))
# Mobile FID
fid_mobile = (response_mobile.json().get('loadingExperience').get('metrics').get('FIRST_INPUT_DELAY_MS').get('distributions'))
# Mobile LCP
lcp_mobile = (response_mobile.json().get('loadingExperience').get('metrics').get('LARGEST_CONTENTFUL_PAINT_MS').get('distributions'))
# Mobile SEO
seo_mobile = (response_mobile.json().get('lighthouseResult').get('categories').get('seo').get('score'))


# Data wrangling

# CLS
cls_rate = {0: 'Good', 10: 'Needs Improvement', 25: 'Poor'}

clsm_df = pd.DataFrame(cls_mobile)
clsm_df = clsm_df.drop('max', axis=1)
clsm_df.rename({'min': 'rating', 'proportion': 'percentage'}, axis=1, inplace=True)
clsm_df.rating = [cls_rate[i] for i in clsm_df.rating]
clsm_df['percentage'] = clsm_df['percentage']*100

clsd_df = pd.DataFrame(cls_desktop)
clsd_df = clsd_df.drop('max', axis=1)
clsd_df.rename({'min': 'rating', 'proportion': 'percentage'}, axis=1, inplace=True)
clsd_df.rating = [cls_rate[i] for i in clsd_df.rating]
clsd_df['percentage'] = clsd_df['percentage']*100

# FID
fid_rate = {0: 'Good', 100: 'Needs Improvement', 300: 'Poor'}

fidm_df = pd.DataFrame(fid_mobile)
fidm_df = fidm_df.drop('max', axis=1)
fidm_df.rename({'min': 'rating', 'proportion': 'percentage'}, axis=1, inplace=True)
fidm_df.rating = [fid_rate[i] for i in fidm_df.rating]
fidm_df['percentage'] = fidm_df['percentage']*100

fidd_df = pd.DataFrame(fid_desktop)
fidd_df = fidd_df.drop('max', axis=1)
fidd_df.rename({'min': 'rating', 'proportion': 'percentage'}, axis=1, inplace=True)
fidd_df.rating = [fid_rate[i] for i in fidd_df.rating]
fidd_df['percentage'] = fidd_df['percentage']*100

# LCP
lcp_rate = {0: 'Good', 2500: 'Needs Improvement', 4000: 'Poor'}

lcpm_df = pd.DataFrame(lcp_mobile)
lcpm_df = lcpm_df.drop('max', axis=1)
lcpm_df.rename({'min': 'rating', 'proportion': 'percentage'}, axis=1, inplace=True)
lcpm_df.rating = [lcp_rate[i] for i in lcpm_df.rating]
lcpm_df['percentage'] = lcpm_df['percentage']*100

lcpd_df = pd.DataFrame(lcp_desktop)
lcpd_df = lcpd_df.drop('max', axis=1)
lcpd_df.rename({'min': 'rating', 'proportion': 'percentage'}, axis=1, inplace=True)
lcpd_df.rating = [lcp_rate[i] for i in lcpd_df.rating]
lcpd_df['percentage'] = lcpd_df['percentage']*100

#Sending the data to Databox
client = Client(dbox_token)
client.insert_all([
    {'key': 'LCP_Desktop' , 'value': str(lcpd_df['percentage'][0]), 'attributes': {
      'rating': str(lcpd_df['rating'][0]),
    }},
    {'key': 'LCP_Desktop' , 'value': str(lcpd_df['percentage'][1]), 'attributes': {
      'rating': str(lcpd_df['rating'][1]),
    }},
    {'key': 'LCP_Desktop' , 'value': str(lcpd_df['percentage'][2]), 'attributes': {
      'rating': str(lcpd_df['rating'][2]),
    }},
    {'key': 'LCP_Mobile' , 'value': str(lcpm_df['percentage'][0]), 'attributes': {
      'rating': str(lcpm_df['rating'][0]),
    }},
    {'key': 'LCP_Mobile' , 'value': str(lcpm_df['percentage'][1]), 'attributes': {
      'rating': str(lcpm_df['rating'][1]),
    }},
    {'key': 'LCP_Mobile' , 'value': str(lcpm_df['percentage'][2]), 'attributes': {
      'rating': str(lcpm_df['rating'][2]),
    }},
    {'key': 'CLS_Desktop' , 'value': str(clsd_df['percentage'][0]), 'attributes': {
      'rating': str(clsd_df['rating'][0]),
    }},
    {'key': 'CLS_Desktop' , 'value': str(clsd_df['percentage'][1]), 'attributes': {
      'rating': str(clsd_df['rating'][1]),
    }},
    {'key': 'CLS_Desktop' , 'value': str(clsd_df['percentage'][2]), 'attributes': {
      'rating': str(clsd_df['rating'][2]),
    }},
    {'key': 'CLS_Mobile' , 'value': str(clsm_df['percentage'][0]), 'attributes': {
      'rating': str(clsm_df['rating'][0]),
    }},
    {'key': 'CLS_Mobile' , 'value': str(clsm_df['percentage'][1]), 'attributes': {
      'rating': str(clsm_df['rating'][1]),
    }},
    {'key': 'CLS_Mobile' , 'value': str(clsm_df['percentage'][2]), 'attributes': {
      'rating': str(clsm_df['rating'][2]),
    }},
    {'key': 'FID_Desktop' , 'value': str(fidd_df['percentage'][0]), 'attributes': {
      'rating': str(fidd_df['rating'][0]),
    }},
    {'key': 'FID_Desktop' , 'value': str(fidd_df['percentage'][1]), 'attributes': {
      'rating': str(fidd_df['rating'][1]),
    }},
    {'key': 'FID_Desktop' , 'value': str(fidd_df['percentage'][2]), 'attributes': {
      'rating': str(fidd_df['rating'][2]),
    }},
    {'key': 'FID_Mobile' , 'value': str(fidm_df['percentage'][0]), 'attributes': {
      'rating': str(fidm_df['rating'][0]),
    }},
    {'key': 'FID_Mobile' , 'value': str(fidm_df['percentage'][1]), 'attributes': {
      'rating': str(fidm_df['rating'][1]),
    }},
    {'key': 'FID_Mobile' , 'value': str(fidm_df['percentage'][2]), 'attributes': {
      'rating': str(fidm_df['rating'][2]),
    }},
    {'key': 'SEO_Desktop', 'value': str(seo_desktop),},
    {'key': 'SEO_Mobile', 'value': str(seo_mobile),},
])