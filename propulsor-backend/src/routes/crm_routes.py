from flask import Blueprint, jsonify, request, current_app
import os
import json
from src.models.crm_models import (
    DatabaseManager, PessoaModel, ContratoModel, 
    InstituicaoModel, RequisicaoModel, DashboardModel
)

crm_bp = Blueprint('crm', __name__)

def get_db_manager():
    """Obtém instância do gerenciador de banco de dados"""
    db_folder = os.path.join(current_app.root_path, 'database')
    return DatabaseManager(db_folder)

def load_colors():
    """Carrega configurações de cores"""
    colors_path = os.path.join(current_app.root_path, 'cores.json')
    try:
        with open(colors_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "name": "Propulsor",
            "dataColors": ["#000100", "#5001b4", "#f7f7f7", "#65b1ff", "#007dff"],
            "background": "#000100",
            "foreground": "#f7f7f7",
            "tableAccent": "#007dff"
        }

@crm_bp.route('/dashboard/stats')
def get_dashboard_stats():
    """Obtém estatísticas para o dashboard"""
    try:
        db_manager = get_db_manager()
        dashboard_model = DashboardModel(db_manager)
        
        stats = dashboard_model.get_estatisticas()
        contratos_situacao = dashboard_model.get_contratos_por_situacao()
        pessoas_tipo = dashboard_model.get_pessoas_por_tipo()
        
        return jsonify({
            'success': True,
            'data': {
                'stats': stats,
                'contratos_por_situacao': contratos_situacao,
                'pessoas_por_tipo': pessoas_tipo,
                'colors': load_colors()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crm_bp.route('/pessoas')
def get_pessoas():
    """Lista pessoas com paginação e busca"""
    try:
        db_manager = get_db_manager()
        pessoa_model = PessoaModel(db_manager)
        
        # Parâmetros de paginação
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search = request.args.get('search', '').strip()
        
        offset = (page - 1) * per_page
        
        if search:
            pessoas = pessoa_model.search(search)
        else:
            pessoas = pessoa_model.get_all(per_page, offset)
        
        return jsonify({
            'success': True,
            'data': pessoas,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(pessoas)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crm_bp.route('/pessoas/<pessoa_id>')
def get_pessoa_detalhes(pessoa_id):
    """Obtém detalhes de uma pessoa específica"""
    try:
        db_manager = get_db_manager()
        pessoa_model = PessoaModel(db_manager)
        
        pessoa = pessoa_model.get_by_id(pessoa_id)
        
        if not pessoa:
            return jsonify({'success': False, 'error': 'Pessoa não encontrada'}), 404
        
        return jsonify({
            'success': True,
            'data': pessoa
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crm_bp.route('/contratos')
def get_contratos():
    """Lista contratos com paginação e busca"""
    try:
        db_manager = get_db_manager()
        contrato_model = ContratoModel(db_manager)
        
        # Parâmetros de paginação
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search = request.args.get('search', '').strip()
        
        offset = (page - 1) * per_page
        
        if search:
            contratos = contrato_model.search(search)
        else:
            contratos = contrato_model.get_all(per_page, offset)
        
        return jsonify({
            'success': True,
            'data': contratos,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(contratos)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crm_bp.route('/instituicoes')
def get_instituicoes():
    """Lista instituições com paginação"""
    try:
        db_manager = get_db_manager()
        instituicao_model = InstituicaoModel(db_manager)
        
        # Parâmetros de paginação
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        offset = (page - 1) * per_page
        
        instituicoes = instituicao_model.get_all(per_page, offset)
        
        return jsonify({
            'success': True,
            'data': instituicoes,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(instituicoes)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crm_bp.route('/requisicoes')
def get_requisicoes():
    """Lista requisições com paginação"""
    try:
        db_manager = get_db_manager()
        requisicao_model = RequisicaoModel(db_manager)
        
        # Parâmetros de paginação
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        offset = (page - 1) * per_page
        
        requisicoes = requisicao_model.get_all(per_page, offset)
        
        return jsonify({
            'success': True,
            'data': requisicoes,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(requisicoes)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crm_bp.route('/search')
def search_global():
    """Busca global em todas as entidades"""
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({'success': False, 'error': 'Termo de busca é obrigatório'}), 400
        
        db_manager = get_db_manager()
        
        # Buscar em pessoas
        pessoa_model = PessoaModel(db_manager)
        pessoas = pessoa_model.search(search_term)[:5]  # Limitar a 5 resultados
        
        # Buscar em contratos
        contrato_model = ContratoModel(db_manager)
        contratos = contrato_model.search(search_term)[:5]  # Limitar a 5 resultados
        
        return jsonify({
            'success': True,
            'data': {
                'pessoas': pessoas,
                'contratos': contratos,
                'total_results': len(pessoas) + len(contratos)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crm_bp.route('/config/colors')
def get_colors():
    """Obtém configurações de cores"""
    try:
        colors = load_colors()
        return jsonify({
            'success': True,
            'data': colors
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

