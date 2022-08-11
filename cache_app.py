from stringprep import in_table_a1
from flask import Flask, request, jsonify

app = Flask(__name__)

in_memory_cache = {}

@app.route('/')
def landing_page():
    return 'This is an empty key-value store. Please set data before you can get any key value or search for prefix/suffix.'

@app.get('/get/<key>')
def get_key_value(key):
    
    if key in in_memory_cache:
        return in_memory_cache[key]
    else:
        return 'Invalid key'

@app.route('/set', methods=['POST'])
def set_key_value():

    new_item = request.get_json(force=True)
    for item in new_item.keys():
        in_memory_cache[item] = new_item[item]

    return jsonify(new_item)

@app.route('/search', methods=['GET'])
def search_prefix_suffix():

    prefix = request.args.get('prefix') or ''
    suffix = request.args.get('suffix') or ''
    len_prefix = len(prefix)
    len_suffix = len(suffix)
    values = []

    if prefix != '' and suffix != '':

        for item in in_memory_cache.keys():
            if len(item) >= len_prefix + len_suffix:
                if item[:len_prefix] == prefix and item[len(item)-len_suffix:] == suffix:
                    values.append(item)
        return values if values != [] else 'Invalid prefix/suffix'

    elif prefix == '' and suffix != '':

        for item in in_memory_cache.keys():
            if len(item) >= len_suffix:
                if item[len(item)-len_suffix:] == suffix:
                    values.append(item)
        return values if values != [] else 'Invalid prefix/suffix'

    elif prefix != '' and suffix == '':

        for item in in_memory_cache.keys():
            if len(item) >= len_prefix:
                if item[:len_prefix] == prefix:
                    values.append(item)
        return values if values != [] else 'Invalid prefix/suffix'

    return 'Invalid prefix/suffix'

if __name__ == "__main__":
    app.run(port=8090, host='0.0.0.0', debug=True)
