from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_FOLDER = os.path.join(os.path.dirname(__file__), 'database')


def listar_tabelas(dbfile):
    conn = sqlite3.connect(dbfile)
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [r[0] for r in cur.fetchall()]
    conn.close()
    return tabelas


def query_rows(dbpath, query, params=()):
    conn = sqlite3.connect(dbpath)
    cur = conn.execute(query, params)
    rows = cur.fetchall()
    columns = [c[0] for c in cur.description] if cur.description else []
    conn.commit()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]


for dbfile in os.listdir(DB_FOLDER):
    if not dbfile.endswith('.db'):
        continue
    dbpath = os.path.join(DB_FOLDER, dbfile)
    for tab in listar_tabelas(dbpath):
        route = f'/api/{tab}'

        def list_all(tab=tab, dbpath=dbpath):
            return jsonify(query_rows(dbpath, f'SELECT * FROM {tab}'))
        app.add_url_rule(route, f'get_{tab}', list_all, methods=['GET'])

        def get_one(idx, tab=tab, dbpath=dbpath):
            rows = query_rows(dbpath, f'SELECT * FROM {tab} WHERE id=?', (idx,))
            return (jsonify(rows[0]) if rows else ('', 404))
        app.add_url_rule(f'{route}/<int:idx>', f'get_{tab}_id', get_one, methods=['GET'])

        def create(tab=tab, dbpath=dbpath):
            data = request.json or {}
            keys = ','.join(data.keys())
            placeholders = ','.join(['?'] * len(data))
            vals = tuple(data.values())
            conn = sqlite3.connect(dbpath)
            cur = conn.execute(
                f'INSERT INTO {tab} ({keys}) VALUES ({placeholders})', vals
            )
            conn.commit()
            conn.close()
            return jsonify({'id': cur.lastrowid})
        app.add_url_rule(route, f'post_{tab}', create, methods=['POST'])

        def update(idx, tab=tab, dbpath=dbpath):
            data = request.json or {}
            sets = ','.join(f"{k}=?" for k in data)
            vals = tuple(data.values()) + (idx,)
            conn = sqlite3.connect(dbpath)
            conn.execute(
                f'UPDATE {tab} SET {sets} WHERE id=?', vals
            )
            conn.commit()
            conn.close()
            return jsonify({'ok': True})
        app.add_url_rule(f'{route}/<int:idx>', f'put_{tab}', update, methods=['PUT'])

        def delete(idx, tab=tab, dbpath=dbpath):
            conn = sqlite3.connect(dbpath)
            conn.execute(f'DELETE FROM {tab} WHERE id=?', (idx,))
            conn.commit()
            conn.close()
            return jsonify({'ok': True})
        app.add_url_rule(f'{route}/<int:idx>', f'del_{tab}', delete, methods=['DELETE'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
