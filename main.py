import argparse
import re
from datetime import datetime


class File:
    def __init__(self, path=''):
        self.path: str = path + 'todo.txt'
        self.tasks: list = []

    def load(self, list_to_load):
        try:
            with open(self.path, 'r') as f:
                list_to_load = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(
                f"""File {self.path} doesn't exist. """
            )

    def save(self, list_to_save):
        with open(self.path, 'w') as f:
            for task in list_to_save:
                f.write(task + '\n')

    def remove_task(self, task_id):
        if 0 <= task_id - 1 < len(self.tasks):
            print(f"""TODO: removing task '{self.tasks[task_id - 1]}'""")
            del self.tasks[task_id - 1]
        else:
            print(f"""{task_id} is wrong number of the task. There're {len(self.tasks)} tasks in total.""")

    def sort_tasks(self):
        return sorted(self.tasks)

    def add_priority(self, task_id, priority):
        if 0 <= task_id - 1 < len(self.tasks):
            print(f"""TODO: Adding priority {priority} to task: '{self.tasks[task_id - 1]}'.""")
            pri = f"""({priority.upper()}) {self.tasks[task_id - 1]}"""
            del self.tasks[task_id - 1]
            self.tasks.insert(task_id - 1, pri)
        else:
            print(f"""{task_id} is wrong number of the task. There're {len(self.tasks)} tasks in total.""")

    def change_priority(self, task_id, priority):
        priority_pattern = re.compile(r'(\([A-Z]\))')
        txt_raw = self.tasks[task_id - 1]
        new_txt = re.sub(priority_pattern, f'({priority.upper()})', txt_raw)
        del self.tasks[task_id - 1]
        self.tasks.insert(task_id - 1, new_txt)
        print(f"TODO: Changed priority in task {task_id} to: {priority}")

    def remove_priority(self, task_id):
        priority_pattern = re.compile(r'(\([A-Z]\))')
        txt_raw = self.tasks[task_id - 1]
        new_txt = re.sub(priority_pattern, '', txt_raw)
        if new_txt == txt_raw:
            print(f"TODO: Task {task_id} has no priority.")
        else:
            del self.tasks[task_id - 1]
            self.tasks.insert(task_id - 1, new_txt)
            print(f"TODO: Deleted priority in task {task_id}.")

    def mark_done(self, task_id):
        curr_date = datetime.now()
        date_format = curr_date.strftime('%d/%m/%y, %H:%M')
        txt_raw = self.tasks[task_id - 1]
        new_txt = f"x {date_format} - {txt_raw}"
        del self.tasks[task_id - 1]
        self.tasks.append(new_txt)
        print(f"TODO: Marked task {task_id}. '{txt_raw}' as done.")


class Task:
    def __init__(self):
        self.file = File()
        self.tasks = []
        self.file.load(self.tasks)

    def add_task(self, desc):
        if desc:
            self.file.tasks.append(desc)
        else:
            print("""No task given.""")
        print(f"TODO: '{desc}' added on line: {len(self.file.tasks)}")

    def remove_task(self, task_id):
        self.file.remove_task(task_id)

    def add_priority(self, task_id, priority):
        if 0 <= task_id - 1 < len(self.file.tasks):
            print(f"""TODO: Adding priority {priority} to task: '{self.file.tasks[task_id - 1]}'.""")
            pri = f"""({priority.upper()}) {self.file.tasks[task_id - 1]}"""
            del self.file.tasks[task_id - 1]
            self.file.tasks.insert(task_id - 1, pri)
        else:
            print(f"""{task_id} is wrong number of the task. There're {len(self.file.tasks)} tasks in total.""")

    def change_priority(self, task_id, priority):
        priority_pattern = re.compile(r'(\([A-Z]\))')
        txt_raw = self.file.tasks[task_id - 1]
        new_txt = re.sub(priority_pattern, f'({priority.upper()})', txt_raw)
        del self.file.tasks[task_id - 1]
        self.file.tasks.insert(task_id - 1, new_txt)
        print(f"TODO: Changed priority in task {task_id} to: {priority}")

    def remove_priority(self, task_id):
        priority_pattern = re.compile(r'(\([A-Z]\))')
        txt_raw = self.file.tasks[task_id - 1]
        new_txt = re.sub(priority_pattern, '', txt_raw)
        if new_txt == txt_raw:
            print(f"TODO: Task {task_id} has no priority.")
        else:
            del self.file.tasks[task_id - 1]
            self.file.tasks.insert(task_id - 1, new_txt)
            print(f"TODO: Deleted priority in task {task_id}.")

    def mark_done(self, task_id):
        curr_date = datetime.now()
        date_format = curr_date.strftime('%d/%m/%y, %H:%M')
        txt_raw = self.file.tasks[task_id - 1]
        new_txt = f"x {date_format} - {txt_raw}"
        del self.file.tasks[task_id - 1]
        self.file.tasks.append(new_txt)
        print(f"TODO: Marked task {task_id}. '{txt_raw}' as done.")


class Operations:
    def __init__(self):
        self.file = File()
        self.task = Task()
        self.file.load(self.task.tasks)
        self.marked_task_pattern = re.compile(r'(x \d{2}\/\d{2}\/\d{2}, \d{2}:\d{2} -)')

    def add_task(self, task):
        self.task.add_task(task)
        self.file.save(self.task.tasks)

    def list_tasks(self, filter=''):
        tasks_sorted = self.file.sort_tasks()
        tasks = self.file.tasks
        mtp = self.marked_task_pattern

        if not filter:
            for task in tasks_sorted:
                if not re.findall(mtp, task):
                    print(f"{tasks.index(task) + 1}. {task}")
        else:
            for task in tasks_sorted:
                if filter in task and not re.findall(mtp, task):
                    print(f"{tasks.index(task) + 1}. {task}")

    def todo_footer(self):
        mtp = self.marked_task_pattern
        tasks_len = 0

        for task in self.file.tasks:
            if not re.findall(mtp, task):
                tasks_len += 1

        if tasks_len == 1:
            is_task_or_tasks = 'task'
        else:
            is_task_or_tasks = 'tasks'

        print(f"""--
TODO: {tasks_len} {is_task_or_tasks} in {self.file.path}""")

    def give_priority(self, task_id, priority):
        priority_pattern = re.compile(r'(\([A-Z]\))')

        if re.findall(priority_pattern, self.file.tasks[task_id - 1]):
            self.task.change_priority(task_id, priority)
            self.file.save()
        else:
            self.task.add_priority(task_id, priority)
            self.file.save()

    def remove_priority(self, task_id):
        self.file.remove_priority(task_id)
        self.file.save()

    def mark_done(self, task_id):
        self.file.mark_done(task_id)
        self.file.save()


def main():
    parser = argparse.ArgumentParser(description='CLI TODO manager. Inspired by todo.txt')
    subparser = parser.add_subparsers(dest='command', help='commands')

    parser_ls = subparser.add_parser('ls', help='Dislay all tasks')
    parser_ls_arg = parser_ls.add_argument('ls_filter', nargs='?', help='Filter')
    parser_txt = subparser.add_parser('add', help='Add task to the list')
    parser_txt_arg = parser_txt.add_argument('txt', type=str, help='Your task')
    parser_rm = subparser.add_parser('rm', help='Remove taks from the list')
    parser_rm_arg = parser_rm.add_argument('rm_id', type=int, help='ID of a task to rid of')
    parser_pri = subparser.add_parser('pri', help='Give priority to the task.')
    parser_pri_index = parser_pri.add_argument('pri_index', type=int, help='Number of the line.') 
    parser_pri_letter = parser_pri.add_argument('pri_letter',nargs='?', type=str, help='letter of priority')
    parser_pri_rm = parser_pri.add_argument('-rm', '--remove', action='store_true', help='Remove priority')
    parser_do = subparser.add_parser('do', help='Mark task as done')
    parser_do_arg = parser_do.add_argument('task_id', type=int, help='Number of the line')
    args = parser.parse_args()

    o = Operations()

    if args.command == 'add':
        o.add_task(args.txt)
    elif args.command == 'rm':
        o.remove_task(args.rm_id)
        o.todo_footer()
    elif args.command == 'ls':
        o.list_tasks(args.ls_filter)
        o.todo_footer()
    elif args.command == 'pri':
        if args.remove:
            o.remove_priority(args.pri_index)
        else:
            o.give_priority(args.pri_index, args.pri_letter)
    elif args.command == 'do':
        o.mark_done(args.task_id)
        o.todo_footer()


if __name__ == "__main__":
    main()

# TODO: Refactoring. Poprzenosić metody odpowiedzialne za modyfikowanie zadań do klasy Task
# TODO: bulk operations na zadaniach
