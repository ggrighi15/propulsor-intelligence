from flask import Blueprint, jsonify, request
from models.crm_models import (
    DatabaseManager, PessoaModel, ContratoModel, 
    InstituicaoModel, RequisicaoModel, DashboardModel,
    ConsorcioModel, ContenciosoModel, ProcuracaoModel, DepositoModel
)

crm_bp = Blueprint('crm', __name__)

def get_db_manager():
    # Retorna instância centralizada do DatabaseManager para todos os módulos
    return DatabaseManager()

# Endpoint para retornar o número de registros de cada módulo (cards do dashboard)
@crm_bp.route('/dashboard/cards', methods=['GET'])
def get_dashboard_cards():
    db = get_db_manager()
    # Conta cada módulo, priorizando sempre a tabela mais atual do contencioso
    result = {
        'pessoas': db.count(PessoaModel),
        'contratos': db.count(ContratoModel),
        'instituicoes': db.count(InstituicaoModel),
        'requisicoes': db.count(RequisicaoModel),
        'procuracoes': db.count(ProcuracaoModel),
        'consorcios': db.count(ConsorcioModel),
        'depositos': db.count(DepositoModel),
        'contencioso': db.count(ContenciosoModel, ultima_tabela=True)
    }
    return jsonify(result)

# Detalhamento por módulo
@crm_bp.route('/modulo/<modulo>', methods=['GET'])
def get_modulo(modulo):
    db = get_db_manager()
    if modulo == 'pessoas':
        dados = db.list(PessoaModel)
    elif modulo == 'contratos':
        dados = db.list(ContratoModel)
    elif modulo == 'instituicoes':
        dados = db.list(InstituicaoModel)
    elif modulo == 'requisicoes':
        dados = db.list(RequisicaoModel)
    elif modulo == 'procuracoes':
        dados = db.list(ProcuracaoModel)
    elif modulo == 'consorcios':
        dados = db.list(ConsorcioModel)
    elif modulo == 'depositos':
        dados = db.list(DepositoModel)
    elif modulo == 'contencioso':
        # Retorna da tabela mais atual
        dados = db.list(ContenciosoModel, ultima_tabela=True)
    else:
        return jsonify({'erro': 'Módulo não encontrado'}), 404
    return jsonify(dados)

# PATCH para atualizar qualquer registro de qualquer módulo
@crm_bp.route('/modulo/<modulo>/<int:registro_id>', methods=['PATCH'])
def patch_modulo(modulo, registro_id):
    db = get_db_manager()
    dados = request.get_json()
    model_map = {
        'pessoas': PessoaModel,
        'contratos': ContratoModel,
        'instituicoes': InstituicaoModel,
        'requisicoes': RequisicaoModel,
        'procuracoes': ProcuracaoModel,
        'consorcios': ConsorcioModel,
        'depositos': DepositoModel,
        'contencioso': ContenciosoModel
    }
    model = model_map.get(modulo)
    if not model:
        return jsonify({'erro': 'Módulo não encontrado'}), 404
    ok, msg = db.patch(model, registro_id, dados)
    if ok:
        return jsonify({'status': 'ok', 'msg': msg})
    else:
        return jsonify({'erro': msg}), 400

# Endpoint para histórico do contencioso (lista todas as tabelas e contagens)
@crm_bp.route('/contencioso/historico', methods=['GET'])
def contencioso_historico():
    db = get_db_manager()
    tabelas = db.list_contencioso_tables()
    hist = []
    for nome_tab in tabelas:
        hist.append({
            'tabela': nome_tab,
            'total': db.count(ContenciosoModel, tabela=nome_tab)
        })
    return jsonify(hist)
