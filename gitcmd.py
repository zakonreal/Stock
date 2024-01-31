#!/usr/bin/env python
# coding: utf-8

# In[1]:


import git, os, sys


# In[7]:


get_ipython().system('git add --all')


# In[8]:


get_ipython().system('git commit -a -m "update"')


# In[10]:


get_ipython().system('git push -u origin main')

