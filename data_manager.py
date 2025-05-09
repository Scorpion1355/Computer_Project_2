from tree_factory import TreeFactory
import json
import os
import pickle

class DataManager:
    def __init__(self, db_dir="./db"):
        self.db_dir = db_dir
        self.databases = {}
        self.current_db = None
        self._init_storage()

    def _init_storage(self):
        os.makedirs(self.db_dir, exist_ok=True)
        self._load_databases()

    def _load_databases(self):
        meta_path = os.path.join(self.db_dir, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                self.databases = json.load(f)
        else:
            self.databases = {}

    def _save_databases(self):
        meta_path = os.path.join(self.db_dir, 'meta.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(self.databases, f, ensure_ascii=False, indent=2)

    def create_database(self, db_name):
        if db_name in self.databases:
            raise ValueError(f"Database '{db_name}' already exists")
        db_path = os.path.join(self.db_dir, db_name)
        os.makedirs(db_path)
        self.databases[db_name] = {}
        self._save_databases()

    def use_database(self, db_name):
        if db_name not in self.databases:
            raise ValueError(f"Database '{db_name}' does not exist")
        self.current_db = db_name

    def create_table(self, table_name, columns, tree_type="avl"):
        if self.current_db is None:
            raise ValueError("No database selected")
        db_meta = self.databases[self.current_db]
        if table_name in db_meta:
            raise ValueError(f"Table '{table_name}' already exists in database '{self.current_db}'")
        primary_key = columns[0]
        db_meta[table_name] = {
            'columns': columns,
            'tree_type': tree_type,
            'primary_key': primary_key
        }
        self._save_databases()
        tree = TreeFactory.create_tree(tree_type)
        tree_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.tree")
        with open(tree_path, 'wb') as f:
            pickle.dump(tree, f)
        data_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.json")
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    def insert(self, table_name, values):
        if self.current_db is None:
            raise ValueError("No database selected")
        db_meta = self.databases[self.current_db]
        if table_name not in db_meta:
            raise ValueError(f"Table '{table_name}' does not exist")
        meta = db_meta[table_name]
        columns = meta['columns']
        if len(values) != len(columns):
            raise ValueError("Column count does not match value count")
        record = dict(zip(columns, values))
        key = record[meta['primary_key']]
        tree_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.tree")
        with open(tree_path, 'rb') as f:
            tree = pickle.load(f)
        if not tree.is_empty() and tree.search(key):
            raise ValueError(f"Key '{key}' already exists in table '{table_name}'")
        tree.insert(key)
        data_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.json")
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append(record)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(tree_path, 'wb') as f:
            pickle.dump(tree, f)

    def select(self, table_name, conditions=None):
        if self.current_db is None:
            raise ValueError("No database selected")
        db_meta = self.databases[self.current_db]
        if table_name not in db_meta:
            raise ValueError(f"Table '{table_name}' does not exist")
        data_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.json")
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if conditions is None:
            return data
        if not isinstance(conditions, dict):
            raise TypeError("conditions must be a dict")
        return [rec for rec in data if all(rec.get(col) == val for col, val in conditions.items())]

    def update(self, table_name, updates, conditions=None):
        if self.current_db is None:
            raise ValueError("No database selected")
        db_meta = self.databases[self.current_db]
        if table_name not in db_meta:
            raise ValueError(f"Table '{table_name}' does not exist")
        if not isinstance(updates, dict):
            raise TypeError("updates must be a dict")
        meta = db_meta[table_name]
        pk = meta['primary_key']
        tree_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.tree")
        data_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.json")
        with open(tree_path, 'rb') as f:
            tree = pickle.load(f)
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for rec in data:
            if conditions is None or all(rec.get(col) == val for col, val in conditions.items()):
                old_key = rec[pk]
                for col, val in updates.items():
                    rec[col] = val
                new_key = rec[pk]
                if new_key != old_key:
                    tree.delete(old_key)
                    tree.insert(new_key)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(tree_path, 'wb') as f:
            pickle.dump(tree, f)

    def delete(self, table_name, conditions=None):
        if self.current_db is None:
            raise ValueError("No database selected")
        db_meta = self.databases[self.current_db]
        if table_name not in db_meta:
            raise ValueError(f"Table '{table_name}' does not exist")
        meta = db_meta[table_name]
        pk = meta['primary_key']
        tree_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.tree")
        data_path = os.path.join(self.db_dir, self.current_db, f"{table_name}.json")
        with open(tree_path, 'rb') as f:
            tree = pickle.load(f)
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        new_data = []
        for rec in data:
            if conditions is not None and not isinstance(conditions, dict):
                raise TypeError("conditions must be a dict")
            if conditions and all(rec.get(col) == val for col, val in conditions.items()):
                tree.delete(rec[pk])
            else:
                new_data.append(rec)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        with open(tree_path, 'wb') as f:
            pickle.dump(tree, f)