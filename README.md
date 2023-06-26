# Social Network
The objective of this test task is to create a simple REST API using Python. The Django Rest Framework is recommended for this task. You are free to use any libraries or frameworks of your preference in combination with Django Rest Framework.

## Basic Models
User
Post (always created by a user)

## Basic Features
User signup
User login
Post like
Post unlike
Analytics: Retrieve the number of likes made within a specific date range. Example API endpoint: /api/analytics/?date_from=2020-02-02&date_to=2020-02-15. The API should return aggregated analytics by day.
User activity: Implement an endpoint that shows the user's last login time and their last request made to the service.
## Requirements
Implement token authentication, with JWT (JSON Web Token) preferred.

## Endpoints
For all requests user should be authenticated.
### User
```
POST: ~/api/user/ - Create user.
```

### Post
```
GET: ~/api/post/ - Returns list of all user posts.
GET: ~/api/post/{pk}/ - Returns detail of post.
POST: ~/api/action/{pk}/ - Post like-unlike.
```

### Analytics
```
GET: ~/api/analitics/?date_from****-**-**&date_to****-**-**/ - Returns total likes from current span of date.
GET: ~/api/activity/ - Returns user last login and request
```

# JWT-Authentication
```
GET: ~/api/token/
GET: ~/api/token/refresh/
GET: ~/api/token/verify/
```
