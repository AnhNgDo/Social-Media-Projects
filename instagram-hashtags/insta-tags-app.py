# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:48:56 2021

use cd command in terminal to move to current folder
use streamlit run <file> to start the app
use Ctrl + C to stop the app

@author: anhng
"""

import streamlit as st
import pandas as pd
from pathlib import Path



MAX = 10000000
MIN = 5000
DEFAULT_TAG = 'Sydney'


def read_inputs():
    """
    Read user inputs for Hashtag search

    """
    topic = st.text_input(label='Hashtag: ', value=DEFAULT_TAG, help='Enter your hashtag here, e.g.: Sydney')
    max_post = st.number_input(label='Maximum Posts: ', min_value=0, value=MAX, help='only show hashtag with number of posts less than this')
    min_post = st.number_input(label='Minimum Posts: ', min_value=0, value=MIN, help='only show hashtag with number of posts higher than this')
    
    return topic, max_post, min_post


def main():
    
    st.title('Instagram Hashtag Generator')
    st.write('This hashtag generator provides you with relevant hashtags for Instagram, based on your original tag')
    st.text('')  # empty line for spacing           
    st.header('Enter your hashtag and Search Criteria:')
    
    topic, max_post, min_post = read_inputs()
    
    
    path = Path.cwd() / 'insta-tags-DB-master.csv'
    tag_db = pd.read_csv(path)
    
    temp_result = tag_db[(tag_db['Related Topic'].str.contains(topic.lower())) 
                    & (tag_db['Number of Posts'] >= min_post)
                    & (tag_db['Number of Posts'] <= max_post)]
    
    result = temp_result[['Instagram Tag', 'Number of Posts']].sort_values(by=['Number of Posts'], ascending=False, ignore_index=True)

    st.text('')  # empty line for spacing    
    st.header('Suggested Instagram Hashtags:')
    st.dataframe(data=result.style.format({'Number of Posts': '{:,.0f}'}))
    
    tags = list(result.iloc[:30, :]['Instagram Tag'])
    selected_tags = st.multiselect(label='Select', options=tags, default=tags)
    
    st.text('')  # empty line for spacing
    st.header('Copy selected Hashtags here:')
    st.write(' '.join(selected_tags))
    

if __name__ == '__main__':
    main()