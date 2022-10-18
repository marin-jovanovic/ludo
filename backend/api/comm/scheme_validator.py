class SchemeValidator:
    """check if role can perform given action"""

    def __init__(self, role_validation_cfg):
        self.scheme = role_validation_cfg
        self.serialization_connector = ";"

    # pass url and action, remove url from action
    def check_action(self, role, action):
        # print(f"check action {role=} {action=}")
        if isinstance(action, str):
            action = self.deserialize(action)

        if len(action) == 1:
            return False

        if isinstance(role, list):
            if len(role) != 1:
                return any([self.check_action(r, action) for r in role])

            role = role[0]

        if role not in self.scheme["roles"]:
            return False

        t = self.scheme["roles"][role]
        table = action[0]
        action = action[1]
        if table not in t:
            return False
        t = t[table]
        if action not in t:
            return False
        return t[action]

    def get_all_tables(self):
        r = []
        for role, tables in self.scheme["roles"].items():

            for t, actions in tables.items():
                r.append(t)

        return r

    # todo remove
    def deserialize(self, payload):

        splitters = [self.serialization_connector, " ", ":"]

        if not any([payload.__contains__(i) for i in splitters]):
            """assumption: already deserialized"""
            return [payload]

        for j in splitters:
            if payload.__contains__(j):
                return [i.strip() for i in
                        payload.split(j, 1)]


#
def main():
    from backend.api.comm.json_loader import role_validation_cfg

    scheme_validator = SchemeValidator(role_validation_cfg)

    print("test ok")


if __name__ == '__main__':
    main()
