from datetime import datetime
import requests
import pandas as pd

base_url = "http://cranlogs.r-pkg.org/"
daily_url = base_url + "downloads/daily/"
top_url = base_url + "top/"

def cran_downloads(packages, when='', start="last-day", end="last-day"):
    """
    daily downloads of cran package data  

    """  
    # make sure packages is a list
    if isinstance(packages, list) == False:
        packages = list(packages.split(","))
        
    if when in (["last-day", "last-week", "last-month"]):
        interval = when
    elif start=="last-day" and end=="last-day":
        interval = "last-day"
    else:
        # check format and add zero padding if missing
        interval = datetime.strptime(start, '%Y-%m-%d').strftime("%Y-%m-%d")+':'+datetime.strptime(end, '%Y-%m-%d').strftime("%Y-%m-%d")
        # start time must be earlier than end time 
        assert datetime.strptime(start, '%Y-%m-%d') < datetime.strptime(end, '%Y-%m-%d')
        # start and end time must be not in future
        assert datetime.strptime(start, '%Y-%m-%d') <= datetime.utcnow()
        assert datetime.strptime(end, '%Y-%m-%d') <= datetime.utcnow()
        
    url = daily_url 
    r = requests.get('https://cranlogs.r-pkg.org/downloads/daily/'+interval+'/'+','.join(packages))
    
    if packages == ['R'] or packages == 'R':
        dfs = pd.DataFrame(r.json()[0]['downloads'])
    
    elif 'R' in packages:
        raise ValueError(f'R downloads cannot be mixed with package downloads. Delete either R or package from {packages}')
    
    else: 
        dfs = pd.DataFrame(columns=['date', 'count', 'package'])
        for i in range(len(r.json())):
            if r.json()[i]['downloads'] == None:
                raise ValueError(f"Download number returns NULL for {r.json()[i]['package']}.")
            else:
                df = pd.DataFrame(r.json()[i]['downloads']).rename(columns={"day": "date", "downloads": "count"})
                df['package'] = r.json()[i]['package']

                # fill in missing dates  
                missing_dates = [i for i in pd.date_range(min(df.date), max(df.date)).map(lambda x: x.strftime('%Y-%m-%d')) if i not in df.date.to_list()]
                df_missing = pd.DataFrame(missing_dates, columns=['date'])
                df_missing['count']=0
                df_missing['package']='ggplot2'
                df_all = df.append(df_missing)

                dfs = dfs.append(df_all)
                dfs = dfs.reset_index(drop=True)
    return dfs

