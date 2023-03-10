from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import requests
import json



#read channel data from file
with open('channels.txt') as f:
    channels = f.readlines()

# clean channels list from unwanted characters
channels = [x.strip() for x in channels]

header = {'Client-Id': '31'}
transport = AIOHTTPTransport(url="https://gql.twitch.tv/gql/", headers=header)
client = Client(transport=transport, fetch_schema_from_transport=False)


with open("ispartner.txt", "w") as partner_outfile, open("still_partner.txt", "w") as still_partner:
    for channel in channels:
        query = gql(f'''
        query {{
          user(login:"{channel}"){{
            roles {{
              isAffiliate
              isPartner
            }}
            cheer {{
              id
            }}            
          }}
        }}
        ''')
        try:
            result = client.execute(query)
        except Exception as e:
            print(f"Error Occured while fetching result for channel : {channel}")
            print(e)
            continue
        
        user = result.get('user', {})
        if user is None:
            continue
        roles = user.get("roles", {})
        if roles.get('isPartner') == True:
            if user.get('cheer') is None:
                still_partner.write(f"{channel} is a Partner but cheer value is None\n")
            else:
                still_partner.write(f"{channel} is a Partner\n")
        elif roles.get('isAffiliate') == True:
            if user.get('cheer') is None:
                still_partner.write(f"{channel} is an Affiliate but cheer value is None\n")
            else:
                still_partner.write(f"{channel} is an Affiliate\n")
        else:
            partner_outfile.write(f"{channel} is not a Partner or Affiliate\n")
#loky aç abone olsana <3 
# btw: ytd: bit long to the moon
