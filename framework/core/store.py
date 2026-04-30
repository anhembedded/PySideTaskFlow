class TaskRuntimeStore:
    def __init__(self):
        self._presenters = {}

    def add(self, view_id: int, presenter):
        self._presenters[view_id] = presenter

    def remove(self, view_id: int):
        if view_id in self._presenters:
            del self._presenters[view_id]

    def get(self, view_id: int):
        return self._presenters.get(view_id)
