# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:08:01 2016

@author: U505118
"""
from bs4 import BeautifulSoup
import pandas as pd
import re


def BasicParse(path):

    df = pd.DataFrame([],columns  = ['elementId', 'contextId', 'unitId', 'fact', 'decimals', 'scale', 'sign', 'factid', 'ns'])
    
    handle = open(path)
    
    soup = BeautifulSoup(handle)
    
    result = soup.findAll()
    
    y = soup.find('xbrl')

    if not y:
	y = soup.find('xbrli:xbrl').attrs
    else:
        y = y.attrs

    for i in xrange(0, result.__len__()):
        tag = result[i].attrs
        
        if tag.has_key('contextref'):
            
            sen1 = result[i].name
            if tag.has_key('contextref'):
                sen2 = tag['contextref']
            else:
                sen2 = None
            if tag.has_key('unitref'):
                sen3 = tag['unitref']
            else:
                sen3 = None
            if result[i].text.encode('ascii','ignore') != None:
                t = result[i].text.encode('ascii','ignore').split('\n')
                te = ''.join(t)
                sen4 = te 
            else:
                sen4 = None
            if tag.has_key('decimals'):
                sen5 = tag['decimals']
            else:
                sen5 = None
                    
            if tag.has_key('scale'):
                sen6 = tag['scale']
            else:
                sen6 = None
                    
            if tag.has_key('sign'):
                sen7 = tag['sign']
            else:
                sen7 = None
                    
            if tag.has_key('factid'):
                sen8 = tag['factid']
            else:
                sen8 = None
                
            if result[i].name != None:
                SplitName = result[i].name.split(':')
                if any(SplitName[0] in x for x in y.keys()):
                    key = 'xmlns:' + SplitName[0]
                    sen9 = y[key]
            else:
                sen9 = None
            
            df.loc[i] = [sen1,sen2,sen3,sen4,sen5,sen6,sen7,sen8,sen9]
        
    return df
    
df = BasicParse('C:/Users/U505118/Desktop/P/Hormel/RalphLauren_10K.htm')
df = df.reset_index(drop = True)

p = re.compile('aggregate')

parse = []

for i in xrange(0, df.__len__()):
    if df.loc[i,'fact'].__len__() >100:
        if p.search(df.loc[i, 'fact']) != None:
            print 'Exists' + str(i)
            l = p.search(df.ix[i, 'fact']).span()
            for j in xrange(0, 1000):
                if df.loc[i, 'fact'][l[0]-j-2:l[0]-j] == '. ':
                    startl = j
                    break
                elif df.loc[i, 'fact'][l[0]-j] == '>':
                    startl = j-1
                    break
            for k in xrange(0, 1000):
                if df.loc[i, 'fact'][l[1]+k : l[1]+k+2] == '. ' or df.loc[i, 'fact'][l[1]+k] == '<':
                    endl = k
                    break
            sen = df.loc[i, 'fact'][l[0]-startl:l[1]+endl].lstrip(' ')
            sen = re.sub('&#x2019;', "'", sen)
            sen = re.sub('&nbsp;', ' ', sen)
            parse.append(sen)

#CIK = str(df[df['elementId'] == 'dei:entitycentralindexkey'].reset_index().ix[0,'fact'].lstrip('0'))
#year = str(df[df['elementId'] == 'dei:documentfiscalyearfocus'].reset_index().ix[0,'fact'])

#doc = df[df['elementId'] == 'dei:documenttype'].reset_index().ix[0,'fact']

"""df.to_csv('C:/Users/U505118/Desktop/P/Hormel/Test1.csv', sep = '|', index = False)"""