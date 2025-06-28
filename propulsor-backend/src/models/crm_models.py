import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_folder: str):
        self.db_folder = db_folder
        
    def get_connection(self, db_name: str):
        """Obtém conexão com banco de dados específico"""
        db_path = os.path.join(self.db_folder, f"{db_name}.db")
        return sqlite3.connect(db_path)
    
    def execute_query(self, db_name: str, query: str, params: tuple = ()) -> List[Dict]:
        """Executa query e retorna resultados como lista de dicionários"""
        conn = self.get_connection(db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        finally:
            conn.close()

class PessoaModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtém lista de pessoas com paginação"""
        query = """
        SELECT 
            nome_ou_razao_social,
            cpf,
            cnpj,
            telefone,
            endereco_padrao_2 as endereco,
            tipo_3 as tipo,
            status_6 as status
        FROM pessoas 
        WHERE nome_ou_razao_social IS NOT NULL 
        ORDER BY nome_ou_razao_social
        LIMIT ? OFFSET ?
        """
        return self.db_manager.execute_query('pessoas', query, (limit, offset))
    
    def search(self, termo: str) -> List[Dict]:
        """Busca pessoas por nome, CPF ou CNPJ"""
        query = """
        SELECT 
            nome_ou_razao_social,
            cpf,
            cnpj,
            telefone,
            endereco_padrao_2 as endereco,
            tipo_3 as tipo,
            status_6 as status
        FROM pessoas 
        WHERE nome_ou_razao_social LIKE ? 
           OR cpf LIKE ? 
           OR cnpj LIKE ?
        ORDER BY nome_ou_razao_social
        LIMIT 50
        """
        termo_like = f"%{termo}%"
        return self.db_manager.execute_query('pessoas', query, (termo_like, termo_like, termo_like))
    
    def get_by_id(self, pessoa_id: str) -> Optional[Dict]:
        """Obtém pessoa por ID (CPF ou CNPJ)"""
        query = """
        SELECT * FROM pessoas 
        WHERE cpf = ? OR cnpj = ?
        """
        results = self.db_manager.execute_query('pessoas', query, (pessoa_id, pessoa_id))
        return results[0] if results else None

class ContratoModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtém lista de contratos com paginação"""
        query = """
        SELECT 
            pasta,
            titulo,
            contratante,
            contratado,
            situacao,
            classificacao,
            nucleo,
            objetocontratual as objeto_contratual
        FROM contratos 
        WHERE titulo IS NOT NULL 
        ORDER BY pasta
        LIMIT ? OFFSET ?
        """
        return self.db_manager.execute_query('contratos', query, (limit, offset))
    
    def search(self, termo: str) -> List[Dict]:
        """Busca contratos por título, contratante ou contratado"""
        query = """
        SELECT 
            pasta,
            titulo,
            contratante,
            contratado,
            situacao,
            classificacao,
            nucleo,
            objetocontratual as objeto_contratual
        FROM contratos 
        WHERE titulo LIKE ? 
           OR contratante LIKE ? 
           OR contratado LIKE ?
        ORDER BY pasta
        LIMIT 50
        """
        termo_like = f"%{termo}%"
        return self.db_manager.execute_query('contratos', query, (termo_like, termo_like, termo_like))

class InstituicaoModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtém lista de instituições com paginação"""
        query = """
        SELECT * FROM instituicoes 
        ORDER BY nome_ou_razao_social
        LIMIT ? OFFSET ?
        """
        return self.db_manager.execute_query('instituicoes', query, (limit, offset))

class RequisicaoModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtém lista de requisições com paginação"""
        query = """
        SELECT * FROM requisicoes 
        ORDER BY numero
        LIMIT ? OFFSET ?
        """
        return self.db_manager.execute_query('requisicoes', query, (limit, offset))

class DashboardModel:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_estatisticas(self) -> Dict:
        """Obtém estatísticas gerais para o dashboard"""
        stats = {}
        
        # Total de pessoas
        pessoas_query = "SELECT COUNT(*) as total FROM pessoas WHERE nome_ou_razao_social IS NOT NULL"
        pessoas_result = self.db_manager.execute_query('pessoas', pessoas_query)
        stats['total_pessoas'] = pessoas_result[0]['total'] if pessoas_result else 0
        
        # Total de contratos
        contratos_query = "SELECT COUNT(*) as total FROM contratos WHERE titulo IS NOT NULL"
        contratos_result = self.db_manager.execute_query('contratos', contratos_query)
        stats['total_contratos'] = contratos_result[0]['total'] if contratos_result else 0
        
        # Total de instituições
        instituicoes_query = "SELECT COUNT(*) as total FROM instituicoes"
        instituicoes_result = self.db_manager.execute_query('instituicoes', instituicoes_query)
        stats['total_instituicoes'] = instituicoes_result[0]['total'] if instituicoes_result else 0
        
        # Total de requisições
        requisicoes_query = "SELECT COUNT(*) as total FROM requisicoes"
        requisicoes_result = self.db_manager.execute_query('requisicoes', requisicoes_query)
        stats['total_requisicoes'] = requisicoes_result[0]['total'] if requisicoes_result else 0
        
        return stats
    
    def get_contratos_por_situacao(self) -> List[Dict]:
        """Obtém distribuição de contratos por situação"""
        query = """
        SELECT 
            situacao,
            COUNT(*) as quantidade
        FROM contratos 
        WHERE situacao IS NOT NULL
        GROUP BY situacao
        ORDER BY quantidade DESC
        """
        return self.db_manager.execute_query('contratos', query)
    
    def get_pessoas_por_tipo(self) -> List[Dict]:
        """Obtém distribuição de pessoas por tipo"""
        query = """
        SELECT 
            CASE 
                WHEN cnpj IS NOT NULL AND cnpj != '' THEN 'Pessoa Jurídica'
                WHEN cpf IS NOT NULL AND cpf != '' THEN 'Pessoa Física'
                ELSE 'Não Definido'
            END as tipo,
            COUNT(*) as quantidade
        FROM pessoas 
        WHERE nome_ou_razao_social IS NOT NULL
        GROUP BY tipo
        ORDER BY quantidade DESC
        """
        return self.db_manager.execute_query('pessoas', query)

