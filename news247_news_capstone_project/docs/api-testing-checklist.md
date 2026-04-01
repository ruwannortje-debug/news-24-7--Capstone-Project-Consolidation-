# API testing checklist

## Successful requests covered

- Reader can retrieve approved articles
- Reader gets only subscribed content
- Journalist can create an article
- Editor can approve and delete an article
- Editor-group member can approve an article
- Newsletter endpoint returns expected article data
- Approval signal sends email and logs the article

## Failed requests covered

- Unauthenticated request to article list returns 401
- Reader cannot create an article
- Journalist cannot delete another journalist's article
