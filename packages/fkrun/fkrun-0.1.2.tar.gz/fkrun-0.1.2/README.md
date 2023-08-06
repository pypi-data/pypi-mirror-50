# FKRUN
##### run tool for dl experiments

1. create a folder saving all your experiment code in your root directory, default 'exps', could be specified as in command '--exp-dir'
2. create a experiment folder(exp folder) under the dir created in first step.
3. copy all the code you need into the exp folder, except the ones in the .fkignore file.

example:

fkrun --exp-dir [root dir] --exp-name [experiment name] python [some py file]