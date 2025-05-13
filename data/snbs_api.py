import flask
from flask import jsonify, make_response, request

from project.data import db_session
from project.data.snowboards import Snowboards
from project.data.users import User
from project.forms.snowboard import SnowboardsForm
from project.snb_search import check, find_snowboard

blueprint = flask.Blueprint(
    'snbs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/snbs', methods=['GET'])
def get_snbs():
    db_sess = db_session.create_session()
    snbs = db_sess.query(Snowboards).all()
    if not snbs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'snbs':
                [item.to_dict(only=("id", "owner", "owner_height", "owner_weight", "owner_level", "owner_style",
                                    "stiffness", "shape", "deflection", "height", "high_tramps")) for item in snbs]
        }
    )


@blueprint.route('/api/snbs/<int:snb_id>', methods=['GET'])
def get_one_snb(snb_id):
    db_sess = db_session.create_session()
    snb = db_sess.query(Snowboards).get(snb_id)
    if not snb:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return jsonify(
        {
            'snb': snb.to_dict(only=("id", "owner", "owner_height", "owner_weight", "owner_level", "owner_style",
                                     "stiffness", "shape", "deflection", "height", "high_tramps"))
        }
    )


@blueprint.route('/api/snbs', methods=['POST'])
def create_snb():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ["owner_id", "owner_height", "owner_weight", "owner_level", "owner_style", "high_tramps"]):
        return make_response(jsonify({'error': 'Bad request (not enough keys)'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(request.json['owner_id'])
    if not user:
        return make_response(jsonify({'error': f'Bad request (User {request.json["owner_id"]} not found)'}), 400)

    form = SnowboardsForm()
    form.weight.data = request.json['owner_weight']
    form.height.data = request.json['owner_height']
    form.level.data = request.json['owner_level']
    form.style.data = request.json['owner_style']
    form.high_tramps.data = request.json['high_tramps']

    message = check(form)

    if message == 'Все данные заполнены корректно':
        res = find_snowboard(form)

        snb = Snowboards(
            owner=request.json['owner_id'],
            owner_height=request.json['owner_height'],
            owner_weight=request.json['owner_weight'],
            owner_level=request.json['owner_level'],
            owner_style=request.json['owner_style'],
            stiffness=res[0],
            shape=res[1],
            deflection=res[2],
            height=res[3],
            high_tramps=request.json['high_tramps']
        )

        db_sess.add(snb)
        db_sess.commit()

        return make_response(jsonify({'id': snb.id, 'add': 'success'}))

    return make_response(jsonify({'error': f'Bad request ({message})'}), 404)


@blueprint.route('/api/snbs/<int:snb_id>', methods=['POST'])
def edit_snb(snb_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    elif not all(key in request.json for key in
                 ["owner_id", "owner_height", "owner_weight", "owner_level", "owner_style"]):
        return make_response(jsonify({'error': 'Bad request (not enough keys)'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(request.json['owner_id'])
    snb = db_sess.query(Snowboards).get(snb_id)
    if not user:
        return make_response(jsonify({'error': f'Bad request (User {request.json["owner_id"]} not found)'}), 400)
    elif not snb:
        return make_response(jsonify({'error': f"Bad request (User's snowboard {snb_id} not found)"}), 400)

    form = SnowboardsForm()
    form.weight.data = request.json['owner_weight']
    form.height.data = request.json['owner_height']
    form.level.data = request.json['owner_level']
    form.style.data = request.json['owner_style']
    form.high_tramps.data = request.json['high_tramps']

    message = check(form)
    if message == 'Все данные заполнены корректно':
        res = find_snowboard(form)

        snb.owner = request.json['owner_id']
        snb.owner_height = request.json['owner_height']
        snb.owner_weight = request.json['owner_weight']
        snb.owner_level = request.json['owner_level']
        snb.owner_style = request.json['owner_style']
        snb.stiffness = res[0]
        snb.shape = res[1]
        snb.deflection = res[2]
        snb.height = res[3]
        snb.high_tramps = request.json['high_tramps']

        db_sess.commit()

        return make_response(jsonify({'id': snb.id, 'edit': 'success'}))

    return make_response(jsonify({'error': f'Bad request ({message})'}), 404)


@blueprint.route('/api/snbs/<int:snb_id>', methods=['DELETE'])
def delete_snb(snb_id):
    db_sess = db_session.create_session()
    snb = db_sess.query(Snowboards).get(snb_id)
    if not snb:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(snb)
    db_sess.commit()
    return jsonify({'delete': 'success'})