import argparse
import shlex
import re
from data_manager import DataManager

class TreeSQL:
    ASSIGN_PATTERN = re.compile(r"(\w+)\s*=\s*('([^']*)'|\"([^\"]*)\"|[^ ]+)")

    def __init__(self):
        self.data_manager = DataManager()

    def parse_command(self, command: str):
        tokens = shlex.split(command)
        if not tokens:
            return None

        up = [t.upper() for t in tokens]
        cmd = up[0]

        if cmd == 'CREATE':
            if up[1] == 'DATABASE':
                return self.data_manager.create_database(tokens[2])
            if up[1] == 'TABLE':
                return self._create_table(tokens)
        if cmd == 'USE':
            return self.data_manager.use_database(tokens[1])
        if cmd == 'INSERT':
            return self._insert_into(tokens, up)
        if cmd == 'SELECT':
            return self._select_from(tokens, up)
        if cmd == 'UPDATE':
            return self._update_table(tokens, up)
        if cmd == 'DELETE':
            return self._delete_from(tokens, up)

        return None

    def _create_table(self, tokens):
        low = [t.lower() for t in tokens]
        name = tokens[2]
        tree_type = 'avl'
        if 'using' in low:
            idx = low.index('using')
            tree_type = tokens[idx + 1]
        start = low.index('(')
        end = low.index(')')
        cols = ' '.join(tokens[start+1:end]).split(',')
        columns = [c.strip() for c in cols]
        return self.data_manager.create_table(name, columns, tree_type)

    def _insert_into(self, tokens, up):
        name = tokens[2]
        idx = up.index('VALUES')
        vals_str = ' '.join(tokens[idx+1:]).strip('()')
        raw = [v.strip().strip("'\"") for v in vals_str.split(',')]
        values = [self._parse_value(v) for v in raw]
        return self.data_manager.insert(name, values)

    def _select_from(self, tokens, up):
        name = tokens[up.index('FROM')+1]
        conditions = self._extract_conditions(tokens, up)
        return self.data_manager.select(name, conditions)

    def _update_table(self, tokens, up):
        name = tokens[1]
        set_i = up.index('SET')
        where_i = up.index('WHERE') if 'WHERE' in up else len(tokens)
        assigns_str = ' '.join(tokens[set_i+1:where_i])
        updates = self._parse_dict(assigns_str)
        conditions = self._extract_conditions(tokens, up)
        return self.data_manager.update(name, updates, conditions)

    def _delete_from(self, tokens, up):
        name = tokens[up.index('FROM')+1]
        conditions = self._extract_conditions(tokens, up)
        return self.data_manager.delete(name, conditions)

    def _extract_conditions(self, tokens, up):
        if 'WHERE' not in up:
            return None
        idx = up.index('WHERE')
        cond_str = ' '.join(tokens[idx+1:])
        return self._parse_dict(cond_str)

    def _parse_dict(self, s: str):
        s = s.replace('(', '').replace(')', '')
        d = {}
        for m in self.ASSIGN_PATTERN.finditer(s):
            key = m.group(1)
            val = m.group(3) or m.group(4) or m.group(2)
            val = val.strip("'\"")
            d[key] = self._parse_value(val)
        return d if d else None

    def _parse_value(self, v: str):
        if v.isdigit():
            return int(v)
        try:
            return float(v)
        except ValueError:
            return v

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TreeSQL CLI")
    parser.add_argument('--cmd', type=str, help="SQL-like command")
    args = parser.parse_args()
    sql = TreeSQL()
    if args.cmd:
        print(sql.parse_command(args.cmd))
    else:
        while True:
            try:
                line = input('>>> ')
                if line.lower() in ('exit','quit'):
                    break
                print(sql.parse_command(line))
            except KeyboardInterrupt:
                break