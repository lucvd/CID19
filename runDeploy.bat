call heroku git:remote -a connect-id-test
call git branch -d local_branch_for_heroku
call git checkout -b local_branch_for_heroku
call git add secrets.yml
call git commit -m "commit with secrets"
call git push heroku local_branch_for_heroku:master --force