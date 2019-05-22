call heroku git:remote -a connect-id-test
call git add .
call git commit -m "commit with secrets"
call git push heroku master:master