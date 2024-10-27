#!/usr/bin/env python
import click
# run ./main.py --help or specify function (e.g., ./main.py add-todo --help)

# ./main.py list-todos
# ./main.py list-todos -p m (will delete what's not m priority)
@click.group
def mycommands():
    pass

@click.command()
@click.option("--name", prompt="Enter your name", help="The name of the user")
def hello(name):
    click.echo(f"Hello {name}!")


# priority sequence for type
PRIORITIES = {
    "o": "Optional",
    "l": "Low",
    "m": "Medium",
    "h": "High",
    "c": "Crucial"
}

# connect parameters with click
@click.command()
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="m") # medium priority
@click.argument("todofile", type=click.Path(exists=False), required=0) # if exists=True, this type would be file that exists (required=0 to note that we don't have to specify a todo file)
@click.option("-n", "--name", prompt="Enter the todo name", help="The name of the todo item")
@click.option("-d", "--description", prompt="Describe the todo", help="The description of the todo item")
def add_todo(name, description, priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "a+") as f:
        f.write(f"{name}: {description} [Priority: {PRIORITIES[priority]}]\n")

@click.command()
@click.argument("idx", type=int, required=1) # required since otherwise we wouldn't know what to delete
def delete_todo(inx):
    with open("mytodos.txt", "r") as f:
        todo_list = f.read().splitlines()
        todo_list.pop(idx)
    with open("mytodos.txt", "w") as f: # open in writing mode; we want to overwrite everything, replace file with new text
        f.write("\n".join(todo_list))
        f.write("\n")

@click.command()
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()))
@click.argument("todofile", type=click.Path(exists=True), required=0) # we cannot list todos of nonexisting file; if path does not exist, this func will not trigger; required is 0 since default is no file provided
def list_todos(priority, todofile): # want to only see to dos of a certain priority unless we don't have one specified, list all of them
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "r") as f:
        todo_list = f.read().splitlines()
    if priority is None:
        for idx, todo in enumerate(todo_list):
            print(f"({idx}) - {todo}")
    else: # if priority is not None
        for idx, todo in enumerate(todo_list):
            if f"[Priority: {PRIORITIES[priority]}]" in todo:
                print(f"({idx}) - {todo}")

mycommands.add_command(hello)
mycommands.add_command(add_todo)
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)

if __name__ == "__main__":
    mycommands()