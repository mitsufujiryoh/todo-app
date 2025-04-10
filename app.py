from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'time': self.time.isoformat(),
            'description': self.description,
            'completed': self.completed
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.date, Task.time).all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'データがありません'}), 400

        required_fields = ['date', 'time', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field}が必要です'}), 400

        try:
            task_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            task_time = datetime.strptime(data['time'], '%H:%M').time()
        except ValueError as e:
            return jsonify({'error': f'日付または時間の形式が正しくありません: {str(e)}'}), 400

        if not data['description'].strip():
            return jsonify({'error': '説明を入力してください'}), 400

        task = Task(
            date=task_date,
            time=task_time,
            description=data['description'].strip()
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'タスクの作成中にエラーが発生しました: {str(e)}'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        data = request.json
        if not data:
            return jsonify({'error': 'データがありません'}), 400

        try:
            if 'date' in data:
                task.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if 'time' in data:
                # 時間から秒を削除してから処理
                time_without_seconds = data['time'].split(':')[:2]
                time_str = ':'.join(time_without_seconds)
                task.time = datetime.strptime(time_str, '%H:%M').time()
            if 'description' in data:
                if not data['description'].strip():
                    return jsonify({'error': '説明を入力してください'}), 400
                task.description = data['description'].strip()
            if 'completed' in data:
                task.completed = data['completed']

            db.session.commit()
            return jsonify(task.to_dict())
        except ValueError as e:
            return jsonify({'error': f'日付または時間の形式が正しくありません: {str(e)}'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'タスクの更新中にエラーが発生しました: {str(e)}'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)