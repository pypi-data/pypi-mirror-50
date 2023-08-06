import os
import shutil
import argparse


def cp_with_ignore(file_name_ignore, source_dir, target_dir, ignore_path='exps'):
    """
    ignoring all files and dirs which starts with '.'
    :param file_name:
    :param top_dir:
    :return:
    """

    # file_names = os.listdir(source_dir)
    if file_name_ignore is not None:
        with open(file_name_ignore, 'r') as f:
            ignore_files = f.readlines()
        ignore_files = [ignore_file.strip('\r').strip('\n') for ignore_file in ignore_files]
        ignore_files.append('.*')
        if not ignore_path in ignore_files:
            ignore_files.append(ignore_path)
    else:
        ignore_files = [ignore_path, '.*']
    # print(file_names)
    shutil.copytree(source_dir, target_dir, ignore=shutil.ignore_patterns(*ignore_files))


def main():
    parser = argparse.ArgumentParser()
    parser.description = 'Copy files to isolate experiments'
    parser.add_argument('--exp-dir', help='top experiment directory', type=str, default='exps')
    parser.add_argument('--exp-name', help='experiment name', type=str, default='experiment_mmm')
    parser.add_argument('--command', '-c', type=str, default=None,
                        help='the python command line, e.g. srun -p ... python ...')
    parser.add_argument('--create-ignore', action='store_true', help='if create .fkignore file in the current dir')

    args = parser.parse_args()

    if args.create_ignore:
        with open('.fkignore', 'a+') as f:
            f.writelines(args.exp_dir + '\n')
    else:
        assert args.command is not None, "Command needed. Please refer to help."

        now_dir = os.getcwd()
        print('now in dir:{}'.format(now_dir))

        ## create some dirs if not exists
        if not os.path.exists(args.exp_dir):
            os.mkdir(args.exp_dir)

        exp_dir = os.path.join(args.exp_dir, args.exp_name)
        if os.path.exists(exp_dir):
            for _ in range(5):
                cc = input(
                    "Target experiment folder exists, please enter your command\n\'y\' for overwrite\n\'n\' for exit:")
                if cc.lower() == 'y':
                    print('Overwriting files in {}'.format(exp_dir))
                    shutil.rmtree(exp_dir)
                    break
                elif cc.lower() == 'n':
                    print('Exiting....')
                    exit()
                else:
                    if _ == 4:
                        print('Too many failing, exit.')
                        exit()
                    else:
                        print('Please enter again.')

        ## copy files to target dir
        ignore_path = os.path.join(now_dir, '.fkignore') if os.path.exists(os.path.join(now_dir, '.fkignore')) else None
        cp_with_ignore(ignore_path, now_dir, exp_dir, ignore_path=args.exp_dir)
        print('copy target dir finished: {}'.format(exp_dir))

        ## change folder into target dir
        os.chdir(exp_dir)
        print('changed dir to {}'.format(os.getcwd()))

        ## run target command
        os.system(args.command)


if __name__ == '__main__':
    main()
