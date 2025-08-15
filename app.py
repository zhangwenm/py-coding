from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 示例数据存储
data_store = [
    {'id': 1, 'name': '项目1', 'description': '这是第一个项目', 'created_at': '2024-01-01'},
    {'id': 2, 'name': '项目2', 'description': '这是第二个项目', 'created_at': '2024-01-02'},
    {'id': 3, 'name': '项目3', 'description': '这是第三个项目', 'created_at': '2024-01-03'}
]

@app.route('/')
def home():
    """API 根路由 - 返回 API 信息"""
    return jsonify({
        'message': 'Python Web API 服务',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'API 信息',
            'GET /api/data': '获取所有数据',
            'GET /api/data/<id>': '获取指定 ID 的数据',
            'POST /api/data': '创建新数据',
            'PUT /api/data/<id>': '更新指定 ID 的数据',
            'DELETE /api/data/<id>': '删除指定 ID 的数据'
        }
    })

@app.route('/api/data', methods=['GET'])
def get_all_data():
    """获取所有数据"""
    return jsonify({
        'status': 'success',
        'message': '数据获取成功',
        'count': len(data_store),
        'data': data_store
    })

@app.route('/api/data/<int:data_id>', methods=['GET'])
def get_data_by_id(data_id):
    """根据 ID 获取单条数据"""
    item = next((item for item in data_store if item['id'] == data_id), None)
    if item:
        return jsonify({
            'status': 'success',
            'message': '数据获取成功',
            'data': item
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'未找到 ID 为 {data_id} 的数据'
        }), 404

@app.route('/api/data', methods=['POST'])
def create_data():
    """创建新数据"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({
                'status': 'error',
                'message': '缺少必需字段: name'
            }), 400
        
        # 生成新 ID
        new_id = max([item['id'] for item in data_store]) + 1 if data_store else 1
        
        new_item = {
            'id': new_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        data_store.append(new_item)
        
        return jsonify({
            'status': 'success',
            'message': '数据创建成功',
            'data': new_item
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'创建失败: {str(e)}'
        }), 400

@app.route('/api/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    """更新指定 ID 的数据"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': '请提供要更新的数据'
            }), 400
        
        item = next((item for item in data_store if item['id'] == data_id), None)
        if not item:
            return jsonify({
                'status': 'error',
                'message': f'未找到 ID 为 {data_id} 的数据'
            }), 404
        
        # 更新字段
        if 'name' in data:
            item['name'] = data['name']
        if 'description' in data:
            item['description'] = data['description']
        item['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'status': 'success',
            'message': '数据更新成功',
            'data': item
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'更新失败: {str(e)}'
        }), 400

@app.route('/api/data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    """删除指定 ID 的数据"""
    global data_store
    item = next((item for item in data_store if item['id'] == data_id), None)
    if not item:
        return jsonify({
            'status': 'error',
            'message': f'未找到 ID 为 {data_id} 的数据'
        }), 404
    
    data_store = [item for item in data_store if item['id'] != data_id]
    
    return jsonify({
        'status': 'success',
        'message': f'ID 为 {data_id} 的数据已删除'
    })

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        'status': 'error',
        'message': 'API 端点未找到'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
