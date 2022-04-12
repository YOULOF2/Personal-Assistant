from typing import Union

__all__ = ["ToDoItem", "ToDoList"]


class ToDoItem:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class ToDoList:
    def __init__(self, title: str, desc: str, tags: list):
        self.title = title
        self.description = desc
        self.tags = tags
        self.items = []

    def add_item(self, item: Union[ToDoItem, "ToDoList"]):
        self.items.append(item)

    def remove_item(self, item: ToDoItem):
        self.items.remove(item)

    def __str__(self):
        final_str = f"Title: {self.title}\n" \
                    f"Description: {self.description}\n\n"
        for todo_item in self.items:
            final_str += f"=====\n" \
                         f"->{todo_item.title}\n" \
                         f"->{todo_item.content}\n"
        final_str += "====="

        return final_str
