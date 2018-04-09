import cmd
import sys

import picker


class LunchShell(cmd.Cmd):
    intro = 'Where Shall We Have Lunch?'
    prompt = '> '
    absentees = []

    def do_missing(self, arg):
        print('Adding {a} to absentees'.format(a=arg))
        self.absentees.append(arg)

    def do_pick(self, arg):
        picker.pick_a_lunch(absentees=self.absentees)

    def do_last_week(self, arg):
        picker.print_last_week()

    def do_EOF(self, arg):
        self.exit()

    def do_exit(self,arg):
        return True


def main():
    LunchShell().cmdloop()


if __name__ == '__main__':
    main()

