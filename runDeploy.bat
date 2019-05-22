call heroku git:remote -a connect-id-test
call git add secrets.yml
call git commit -m "commit with secrets"
call git push heroku 92b69e98:master --force