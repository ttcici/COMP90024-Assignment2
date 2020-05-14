# API for Back-end and Front-end
## 1. Get Tweet by document name
#### Get a assigned number of tweets by document name.

Request url: ```http://127.0.0.1:8000/get_tweet_by_name/<database_name>/<count>```

Request method: ```GET```

Response body example:
```json
{
  "name": "database_name",
  "msg": "success",
  "data": [
    {
      (tweet1)
    },
    {
      (tweet2)
    }
  ]
}
```

## 2.