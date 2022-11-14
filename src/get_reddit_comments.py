import requests
from datetime import datetime as dt
import pandas as pd
import time


# we use this function to convert responses to dataframes
def df_from_response(res, parent_title='', parent_selftext=''):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()
    # loop through each post pulled from res and append to df
    r_json = res.json()
    if type(r_json) == dict:
        range_to_look_through = r_json['data']['children']
    else:
        l = len(r_json)
        range_to_look_through = r_json[l-1]['data']['children']
    for post in range_to_look_through:
        if 'created_utc'  not in post['data'].keys(): break

        _dict = {'subreddit': post['data']['subreddit'] if 'subreddit' in post['data'].keys() else '',
            'author': post['data']['author'] if 'author' in post['data'].keys() else '',
            'domain': post['data']['domain'] if 'domain' in post['data'].keys() else '',
            'num_comments': post['data']['num_comments'] if 'num_comments' in post['data'].keys() else '',
            'title': post['data']['title'].lower() if 'title' in post['data'].keys() else '',
            'selftext': post['data']['selftext'].lower() if 'selftext' in post['data'].keys() else
                            parent_title + parent_selftext + post['data']['body'].lower()
                            if 'body' in post['data'].keys() else '',
            'upvote_ratio': post['data']['upvote_ratio'] if 'upvote_ratio' in post['data'].keys() else '',
            'ups': post['data']['ups'] if 'ups' in post['data'].keys() else '',
            'downs': post['data']['downs'] if 'downs' in post['data'].keys() else '',
            'score': post['data']['score'] if 'score' in post['data'].keys() else '',
            'link_flair_css_class': post['data']['link_flair_css_class'] if 'link_flair_css_class' in post['data'].keys() else '',
            'created_utc': dt.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ')
                        if 'created_utc' in post['data'].keys() else '',
            'id': post['data']['id'],
            'kind': post['kind'] if 'kind' in post.keys() else ''
            }
        #skip short comments (<30 symbols)
        if (len(_dict['selftext']) - len(parent_title) - len(parent_selftext) < 30 and
            len(parent_title) + len(parent_selftext) > 0): break
        df = pd.concat([df, pd.DataFrame([_dict])]) if len(df.values) != 0 else pd.DataFrame([_dict])
    return df

def serve_cycle(iter_dict):
    params = iter_dict["params"]
    SUBREDDIT = iter_dict["SUBREDDIT"]
    SUB_TYPE = iter_dict["SUB_TYPE"]
    fullname_for_before_movement = None
    df_comment = pd.DataFrame()
    for i in range(iter_dict["cur_iter"], HUNDREDS):
        # make request



        res = requests.get(f"https://oauth.reddit.com/r/{SUBREDDIT}/{SUB_TYPE}",
                           headers=headers,
                           params=params)

        # get dataframe from response
        new_df = df_from_response(res)
        # take the final row (oldest entry)
        print(i, len(new_df))




        if i == 0 and "before" not in params.keys():
            row = new_df.iloc[0]

            fullname_for_before_movement = row['kind'] + '_' + row['id']
            row = new_df.iloc[len(new_df) - 1]
            fullname = row['kind'] + '_' + row['id']
            params['after'] = fullname
        if len(new_df) < params["limit"]:
            #print(new_df)
            #print(res.text)
            print(len(new_df), "<=", params["limit"])
            iter_dict["cur_iter"] = i
            params.pop("after", 2000)
            if fullname_for_before_movement:
                params["before"] = fullname_for_before_movement
            params["limit"] = 3
            iter_dict["params"] = params
            print("break:", params, iter_dict)

            break



        if "after" in params.keys():
            row = new_df.iloc[len(new_df) - 1]
            fullname = row['kind'] + '_' + row['id']
            params['after'] = fullname
        if "before" in params.keys():
            row = new_df.iloc[0]
            fullname = row['kind'] + '_' + row['id']
            params['before'] = fullname
        # create fullname

        print(fullname)

        # +++++++++++++++++++++++++++++++++++++
        # try to get comments for post from the first row
        for _, r in new_df.iterrows():
            res_comment = requests.get(f"https://oauth.reddit.com/comments/{r['id']}",
                                       headers=headers,
                                       params=params)
            df_comment = pd.concat([df_comment,df_from_response(res_comment, r['title'], r['selftext'])])


        # append new_df to data
        #data = data.append(new_df, ignore_index=True)
        df_comment.to_csv(f"../data/comment_{SUBREDDIT}_{SUB_TYPE}_" + NOW[:4] + ".csv", mode="a", sep='\t', index=False)
        new_df.to_csv(f"../data/r_{SUBREDDIT}_{SUB_TYPE}_" + NOW[:4] + ".csv", mode="a", sep='\t', index=False)
        print(res.headers['x-ratelimit-remaining'],
                res.headers['x-ratelimit-used'],
                res.headers['x-ratelimit-reset'], dt.now())
        time.sleep(2)

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('0bRC0ZO6kEbkQetQomwU4g', 'lJrmM8jymrRZgOJcmEg9nXALnuh_KQ')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'Koba_69',
        'password': 'Ko1969ba'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'python:kokEternity script:v1.0 (by /u/Koba_69)'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

#===================================
#data = pd.DataFrame()



params = {'limit': 100}
iterations = [{"cur_iter": 0, "SUBREDDIT": "wallstreetbets", "SUB_TYPE": "new", "params": {'limit': 100}}]



# loop through 10 times (returning 1K posts)
NOW = str(dt.now())
HUNDREDS = 15000000
ind = 0
step = 0
while True and step < 2:
    NOW = str(dt.now())
    serve_cycle(iterations[ind])
    ind = (ind + 1) % len(iterations)
    step += 1
    time.sleep(3)




