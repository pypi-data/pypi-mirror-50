from tinydb import TinyDB


class EventModel(object):
    def __init__(self, uri):
        self.uri = uri
        self.db = None
        self.reload()

    def reload(self):
        if self.db is not None:
            self.db.close()
        self.db = TinyDB(self.uri, indent=2)
        self._actions = self.db.table("actions")
        self._alarms = self.db.table("alarms")

    def get_action_by_id(self, action_id):
        return self._actions.get(eid=action_id)

    def get_alarm_by_id(self, alarm_id):
        return self._alarms.get(eid=alarm_id)

    def get_actions_by_alarm(self, alarm):
        for action_id in alarm.get("actions", []):
            action = self.get_action_by_id(action_id)
            if action is None:
                continue
            yield action

    def get_all_alarms(self):
        return self._alarms.all()

    def get_all_actions(self):
        return self._actions.all()

    def get_all_alarms_expanded(self):
        for alarm in self.get_all_alarms():
            for action in self.get_actions_by_alarm(alarm):
                yield alarm, action

    def add_event(self, alarm, actions):
        action_ids = [self.add_action(a) for a in actions]
        alarm["actions"] = action_ids
        return self._alarms.insert(alarm)

    def add_action(self, action):
        return self._actions.insert(action)

    def add_alarm(self, alarm):
        return self.add_event(alarm, [])

    def update_alarm(self, alarmid, new_fields={}):
        return self._alarms.update(new_fields, eids=[alarmid])

    def update_action(self, actionid, new_fields={}):
        return self._actions.update(new_fields, eids=[actionid])

    def delete_alarm(self, alarmid):
        return self._alarms.remove(eids=[alarmid])

    def delete_action(self, actionid):
        return self._actions.remove(eids=[actionid])
