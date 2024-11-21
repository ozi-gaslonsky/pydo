import argparse
import re
from datetime import datetime


class File:
    '''Operations on file'''

    def __init__(self):
        self.path: str = 'todo.txt'
        self.tasks: list = []
        self.check = Checks()

    def load(self) -> str:
        try:
            with open(self.path, 'r') as f:
                self.tasks = [line.strip() for line in f.readlines()]
                return self.tasks
        except FileNotFoundError:
            print(f"""TODO: {self.path} doesn't exist.""")

    def save(self) -> str:
        with open(self.path, 'w') as f:
            for task in self.tasks:
                f.write(task + '\n')

    def list(self, filter: str = '') -> str:
        # displays sorted file content, ommiting tasks that are marked as done.
        tasks_sorted: list = sorted(self.tasks)
        tasks_filtered: list = []

        if not filter:
            for task in self.tasks:
                if not self.check.is_task_marked(task):
                    tasks_filtered.append(task)
        else:
            for task in self.tasks:
                if not self.check.is_task_marked(task) and filter in task:
                    tasks_filtered.append(task)

        for task in tasks_sorted:
            if task in tasks_filtered:
                print(f"{tasks_filtered.index(task) + 1}. {task}")

    def format_file(self) -> list:
        # todo.txt file format.
        self.tasks: list = []


class Task:
    '''Operations on task'''

    def __init__(self, file_instance):
        self.file = file_instance
        self.check = Checks()

    def add(self, task=''):
        if task:
            # insert new task as last task that is not marked as done.
            self.file.tasks.insert(self.check.active_task_count(self.file.tasks
                                                                ), task)
            print(f"TODO: '{task}' added on line "
                  f"{self.check.active_task_count(self.file.tasks)}."
                  )
        else:
            print("TODO: No task given.")

    def remove_task(self, task_id):
        del self.file.tasks[task_id - 1]

    def mark_done(self, task_id):
        curr_date = datetime.now()
        date_format = curr_date.strftime('%d/%m/%y, %H:%M')
        task_to_done = self.file.tasks[task_id - 1]
        task_done_string = f"x {date_format} - {task_to_done}"

        del self.file.tasks[task_id - 1]
        self.file.tasks.append(task_done_string)
        print(f"TODO: Marked task {task_id}. '{task_to_done} as done.'")

    def prioritize(self, task_id, priority: str = ''):
        task_to_pri = self.file.tasks[task_id - 1]
        task_pri = f"({priority.capitalize()}) {task_to_pri}"

        self.file.tasks[task_id - 1] = task_pri

    def deprioritize(self, task_id):
        priority_pattern = re.compile(r'^\([A-Z]\)')
        task_to_depri = self.file.tasks[task_id - 1]
        depri_task = re.sub(priority_pattern, '', task_to_depri)

        self.file.tasks[task_id - 1] = depri_task.strip()


class Checks:

    @staticmethod
    def id_wrong(user_input, tasks):
        active_tasks_count = Checks.active_task_count(tasks)
        if user_input < 0 or user_input > active_tasks_count:
            print("TODO: Wrong task number."
                  f" Current active tasks:{active_tasks_count}")
            return True
        else:
            return False

    @staticmethod
    def path_wrong():
        # ścieżka do pliku jest zła
        pass

    @staticmethod
    def is_task_marked(task=''):
        marked_task_pattern = re.compile(r'(x \d{2}\/\d{2}\/\d{2},'
                                         r' \d{2}:\d{2} -)')
        if re.findall(marked_task_pattern, task):
            return True
        else:
            return False

    @staticmethod
    def active_task_count(tasks):
        count = 0
        for task in tasks:
            if not Checks.is_task_marked(task):
                count += 1
        return count

    @staticmethod
    def has_priority(self, tasks: list, task_id):
        priority_pattern = re.compile(r'^\([A-Z]\)')
        if re.findall(priority_pattern, tasks[task_id - 1]):
            return True
        else:
            return False


class Operations:
    def __init__(self):
        self.file = File()
        # self.file.load_config()
        self.task = Task(self.file)
        self.check = Checks()
        self.file.load()

    def add(self, task):
        self.task.add(task)
        self.file.save()

    def ls(self, filter):
        self.file.list(filter)

    def do(self, task_id):
        if self.check.id_wrong(task_id, self.file.tasks):
            return

        self.task.mark_done(task_id)
        self.file.save()

    def pri(self, task_id, priority):
        if self.check.id_wrong(task_id, self.file.tasks):
            return

        if not self.check.has_priority(self.file.tasks, task_id):
            self.task.prioritize(task_id, priority)
        else:
            self.task.deprioritize(task_id)
            self.task.prioritize(task_id, priority)

        self.file.save()
        print(f"TODO: Changed priority on Task '{task_id}.'")

    def depri(self, task_id):
        if self.check.id_wrong(task_id, self.file.tasks):
            return

        if self.check.has_priority(self.file.tasks, task_id):
            self.task.deprioritize(task_id)
            self.file.save()
            print(f"TODO: Deleted priority on Task '{task_id}'")
        else:
            print(f"Task '{task_id}' has no priority.")

    def rm(self, task_id):
        if self.check.id_wrong(task_id, self.file.tasks):
            return

        self.task.remove_task(task_id)
        self.file.save()
        print(f"TODO: Task '{task_id}' removed.")

    def format_file(self):
        self.file.format_file()
        self.file.save()
        print("TODO: File cleared.")

    def filter_tasks(self, filter):
        pass


def main():
    parser = argparse.ArgumentParser(description='CLI TODO menager. Inspired by todo.txt')
    subparser = parser.add_subparsers(dest='command', help='commands')

    parser_add = subparser.add_parser('add',  help='Add task to file.')
    parser_add_arg = parser_add.add_argument('task', type=str, help='Task string.')
    parser_ls = subparser.add_parser('ls', help='List tasks to do.')
    parser_ls_filter = parser_ls.add_argument('ls_filter', nargs='?', help='Optional filter.')
    parser_do = subparser.add_parser('do', help='Mark task as done.')
    parser_do_arg = parser_do.add_argument('task_number',type=int, help='Task number.')
    parser_pri = subparser.add_parser('pri', help='Give priority to the Task.')
    parser_pri_number = parser_pri.add_argument('pri_number', type=int, help='Number of Task  to prioritize.')
    parser_pri_letter = parser_pri.add_argument('pri_letter', nargs='?', type=str, help='Letter of priority.')
    parser_pri_rm = parser_pri.add_argument('-rm', '--remove', action='store_true', help='Remove given priority.')
    parser_rm = subparser.add_parser('rm', help='Remove the Task.')
    parser_rm_number = parser_rm.add_argument('rm_number', nargs='?', type=int, help='Number of Task to remove.')
    parser_rm_all = parser_rm.add_argument('-A', '--all',action='store_true', help='Clear entire file.')
    parser_path = subparser.add_parser('path', help="Change the 'todo.txt' file path.")
    parser_path_str = parser_path.add_argument('path', nargs='?', type=str, help="path to 'todo.txt' file.")
    args = parser.parse_args()

    o = Operations()

    if args.command == 'add':
        o.add(args.task)
    elif args.command == 'ls':
        o.ls(args.ls_filter)
    elif args.command == 'do':
        o.do(args.task_number)
    elif args.command == 'pri':
        if args.remove:
            o.depri(args.pri_number)
        else:
            o.pri(args.pri_number, args.pri_letter)
    elif args.command == 'rm':
        if args.all:
            o.format_file()
        else:
            o.rm(args.rm_number)
    elif args.command == "path":
        o.file_dir(args.path)


if __name__ == "__main__":
    main()

# TODO: Stworzyć plik konfiguracyjny. Zapisać do niego domyślną ścieżkę.
# Rozbudować program o możliwość zmiany ścieżki przez edycję pliku konfiguracyjnego.
