# collection of cqrs_c
# not intended to be run as a script

pip3 freeze > requirements.txt


# delete all non existing branches
git fetch -p && git branch -vv | awk '/: gone]/{print $1}' | xargs git branch -D


$ npm -g install js-beautify
$ find . -type f -name "*.js" -exec js-beautify -r {} \;


# headers data body


select * from
api_gamelog left join
api_acceptancelog on
api_gamelog.game_id = api_acceptancelog.level_id and
api_gamelog.id = api_acceptancelog.log_entry_id
where api_gamelog.game_id=16
order by -api_gamelog.id