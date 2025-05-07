from fastapi.responses import HTMLResponse

def render_painel():
    html_content = '''
    <html>
        <head>
            <title>Painel do Propulsor</title>
        </head>
        <body>
            <h1>✅ Painel do Propulsor</h1>
            <p>Status: Tudo rodando com sucesso.</p>
            <ul>
                <li>Distribuidor de e-mails: Ativo</li>
                <li>Peticionamentos: Aguardando integração</li>
                <li>Atualizações do Espaider: Monitoradas</li>
            </ul>
        </body>
    </html>
    '''
    return HTMLResponse(content=html_content, status_code=200)
