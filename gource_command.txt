git log --pretty=format:user:%aN%n%ct --reverse --raw --encoding=UTF-8 --no-renames > log.log

gource log.log