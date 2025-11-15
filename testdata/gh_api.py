#!/usr/bin/env python
# coding: utf-8

# ## imports

# In[1]:


import json
from pathlib import Path
import requests


# ## constants and config

# In[2]:


#user_term='GH_USER'
user_term='GH_USER_TEST'

#api_key_term1='GH_API_KEY_CREATE'
#api_key_term2='GH_API_KEY'
api_key_term3='GH_API_KEY_TEST'
api_key_term=api_key_term3

homepage='https://github.com/{user}/{name}'
post_url='https://api.github.com/user/repos'
get_url='https://api.github.com/repos/{user}/{name}'

del_term='allow_del_by_api=true'


# ## helpers

# In[3]:


def _remove_auth(headers, vb=0):
    """remove auth token from header"""
    h={k:v for k,v in headers.items() if 'auth' not in k.lower()}
    h1=[v for k,v in headers.items() if 'auth' in k.lower()]
    if h1:
        h1=h1[0]
        if h1:
            h1=f'{h1[:15]}..{h1[-2:]}' , len(h1)
    h1=f'{h1[0]} {h1[1]}'
    h['authorization']=h1
    return h


# In[4]:


def _get_env_value(env_path=None, term=None):
    """get value from env file"""
    if not term:
        print(f'fatal: no term specified')
        return
    if env_path is None:
        env_path = Path.home() / '.env'
    env_path = Path(env_path)
    while env_path.is_dir():
        env_path=env_path/'.env'
    if not Path(env_path).is_file():
        print(f'user warning: {str(env_path)} not a file or not accessible')
        return
    with env_path.open() as f:
        for line in f:
            if line.startswith(f'{term}='):
                return line.split('=')[1].strip().strip('"')
    return


# In[5]:


def _get_user(env_path=None, user_key=None):
    """get github user"""
    ut=user_key if user_key else user_term
    return _get_env_value(env_path, ut)


# In[6]:


def _get_token(env_path=None, api_key_value=None):
    """get github token. must include administration read/write privilege for all repos"""
    akt=api_key_value if api_key_value else api_key_term
    return _get_env_value(env_path, akt)


# In[7]:


def _get_headers(vb=0):
    token=_get_token()
    if not token:
        if vb:
            print('error getting token')
        return
    headers = {'Authorization': f'token {token}',}
    return headers


# In[42]:


def _paginate(url, headers, max_items=30, vb=0):
    if max_items=='max':
        max_items=float('inf')
    url1=url
    p=0
    pp=30
    if max_items>30:
        pp=100 if max_items>100 else max_items
        p=1
        url1=url+f'?per_page={pp}&page={p}'
        if vb>1:
            print(url)
    nxt=True
    ret=[]
    while nxt and len(ret)<max_items:
        r=requests.get(url1, headers=headers)  
        ret.extend(r.json())
        h=r.headers.get('link','')
        h=h.split(',')[0].split(';')[1].strip() if h else h
        nxt='rel="next"'in h
        p+=1
        url1=url+f'?per_page={pp}&page={p}'
        if vb>1: print(f'link:{h}, page:{p}, nxt: {nxt}, url: {url1}')
    return ret


# ## github api

# In[18]:


def get_commits(name, user=None, max_commits=30, dry_run=None, return_all=False, vb=0):
    user = user or _get_user()
    headers=_get_headers()
    if not headers or not user:
        if vb:
            print(f'fatal: one of headers and user is missing')
        return
    headers |= {'Accept': 'application/vnd.github+json','X-GitHub-Api-Version': '2022-11-28',}
    url=get_url.format(user=user,name=name)
    url=f'{url}/commits'
    r=None
    if dry_run:
        return _remove_auth(headers), url
    r=requests.get(url, headers=headers)
    s=r.status_code
    if s==409:
        if vb:
            msg=r.json().get('message')
            print(msg)
        return [] if return_all else 0
    elif s==200:
        ret1=r.json()
        ret2=_paginate(url, headers=headers, max_items=max_commits, vb=vb)
        ret=ret2
        if vb:
            p=f'{len(ret)} commits'
            if vb>1:
                print(f'max_commits: {max_commits}, return_all: {return_all},',p)
            else:
                print(p)

        if return_all:
            if isinstance(max_commits,int):
                return ret[:max_commits]
            else:
                return ret
        else:
            return len(ret)
    elif s==404:
        if vb:
            print('repo not found')
            return
    else:
        print(f'error: unknown status code {s}')
        if return_all:
            return r
        else:
            return None


# In[19]:


def list_repos(user=None, vb=0, dry_run=None, max_repos=30):
    """get all repos as list"""
    user=_get_user()
    headers=_get_headers()

    if not user or not headers:
        if vb:
            print('missing user or cant get headers')
        return
    headers |= {'Accept': 'application/vnd.github+json','X-GitHub-Api-Version': '2022-11-28',}
    url=post_url.format(user=user)

    ret=_paginate(url=url, headers=headers, max_items=max_repos, vb=vb)
    return ret


# In[11]:


def create_repo(name, user=None, description='simple repo', private=True, is_template=False, auto_init=True, dry_run=True, vb=0):
    user=user or _get_user()
    description+=f' {del_term} '
    headers=_get_headers(vb)
    if not headers:
        if vb:print(f'fatal: cannot get headers')
        return
    headers |= {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {'name':name,'description':description,'homepage':homepage.format(user=user, name=name),
            'private':private,'is_template':is_template}
    data=json.dumps(data)
    if vb>1:
        print (_remove_auth(headers))
        print(data)

    if not dry_run:
        if vb>1:print('preparing request')
        url=post_url
        #url='https://api.github.com/user/repos'
        response = requests.post(url, headers=headers, data=data)
        d=response.json()
        s=response.status_code
        if vb>1:print('status', s)
        if 200<=s<300:
            if d.get('name', None)==name:
                if vb:print(f'{name} created')
                return True
            return False
        else:
            if 'errors' in d:
                if vb:print(f'error: {d["errors"][0]["message"]}')
                return False
            else:
                print('no errors')
                if vb:print(f'status {s}: {d.get("message",None)}')
                return False


# In[12]:


def delete_repo(name, user=None, dry_run=True, force=False, vb=0):
    user= user or _get_user()
    headers=_get_headers(vb)

    if not headers or not user:
        if vb>1:
            print('fatal: missing headers or user')
        return
    url=get_url.format(user=user,name=name)
    if vb>1:
        print(f'user: {user}')
        print(f'headers: {_remove_auth(headers)}')
        print(f'url: {url}')

    allow_delete=False

    # safeguard
    c=get_commits(name=name, user=user, dry_run=False)
    if vb>2:
        print(f'commits: {c}')
    if c is None:
        if vb:
            print(f'cant delete: {name} not found')
        return
    if c==0:
        if vb>1:
            print(f'allow delete reason: no commits')
        allow_delete=True
    if not allow_delete and force:
        d=get_repo_data(name=name, user=user, dry_run=False, return_all=True)
        try:
            dd=d.json()
            desc=dd.get('description', '')
            allow_delete=del_term in desc
            if vb>1 and allow_delete:
                print(f'allow delete reason: {del_term} in description')
        except Exception as e:
            print(f'error getting data for {name}: {str(e)}')

    if allow_delete and not dry_run:
        response = requests.delete(url, headers=headers)
        s=response.status_code
        if s==204:
            print(f'{name} deleted')
            return True
        d=response.json()
        if s>=300:
            print(f'error: {d['message']}')     
        return False
    else:
        if not dry_run:
            if vb:
                print('not allowed: not empty and missing allow term in desc. try force=True to override if you are sure')
        else:
            if vb:
                print(f'not deleted: dry_run')


# In[13]:


def get_repo_data(name, user=None, return_all=False, dry_run=True, vb=0):
    user=_get_user() if not user else user
    headers=_get_headers(vb)
    if not headers or not user:
        if vb>1:
            print('fatal: mising headers or user')
        return

    url=get_url.format(user=user, name=name)
    if vb>2:
        print(f'user: {user}')
        h=_remove_auth(headers)
        print(f'headers: {_remove_auth(headers)}')
        print(f'url: {url}')

    #f'https://api.github.com/repos/{user}/{name}'
    if not dry_run:
        r=requests.get(url, headers=headers)
        if return_all:
            return r
        s=r.status_code
        if s==200:
            d=r.json()
            private='private' if d['private'] else 'public'
            owner=d.get('owner', {}).get('login', None)
            git_url=d.get('git_url')
            ssh_url=d.get('ssh_url')
            if vb:
                t=f"name: {d['name']}, owner: {owner}, {private}"
                if vb>1:
                    t=f'response: {s}, '+t
                print(t)
            return {'name':d['name'], 'owner':owner, 'private':d['private'], 'git_url':git_url, 'ssh_url':ssh_url}
        else:
            try:
                d=r.json()
                msg=d.get('message')
                if 'not found' in msg.lower():
                    print(f'{name} {msg.lower()}')
                else:
                    print(f'error: {msg}')
            except Exception as e:
                if vb>1:print(str(e))
    return {}


# In[ ]:





# ## tests

# In[14]:


if __name__=='__main__':
    r=get_repo_data(name='coron', vb=1, dry_run=False)
    print(r)
    r=create_repo(name='coron', vb=1, dry_run=False)
    print(r)
    r=get_repo_data(name='coron', vb=1, dry_run=False)
    print(r)
    r=delete_repo(name='coron', vb=1, dry_run=False)
    print(r)


# In[15]:


if __name__=='__main__':
    d=get_repo_data(name='coron', vb=3, dry_run=False, return_all=True)
    print(d)
    d=create_repo(name='coron6', vb=2, dry_run=False)
    print(d)

    


# In[17]:


if __name__=='__main__':
    def test_get_commits():
        r=get_commits(name='coron', vb=1, dry_run=False)
        assert r is None
        r=get_commits(name='coron6', vb=1, dry_run=False)
        print( r)
        r=get_commits(name='coron234', vb=1, dry_run=False)
        assert r is None
    test_get_commits()



# In[21]:


if __name__=='__main__':
    d=_get_user(env_path='example.txt_alt')
    print(d)



# In[28]:


if __name__=='__main__':
    r=list_repos(max_repos=30,vb=1)
    l=len(r)
    print(f'{l} repo{"s" if l>1 or l==0 else ""}')
    for rp in r:
        print(rp['name'])



# In[30]:


if __name__=='__main__':
    # existing repo, limited commits
    r=get_commits('example',max_commits=50,return_all=True,vb=1)
    print(len(r) if isinstance(r,list) else r) 
    # existing repo, max commits
    r=get_commits('coron',max_commits='max',return_all=True,vb=3)
    print(len(r) if isinstance(r,list) else r) 
    # existing repo, no commits


# In[33]:


if __name__=='__main__':
    user='gh4144'
    api_key_term=api_key_term3
    r=list_repos(user=user, max_repos=110)
    l=len(r)
    print(f'{l} repo{"s" if l>1 or l==0 else ""}')

