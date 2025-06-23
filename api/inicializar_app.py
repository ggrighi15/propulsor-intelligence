def inicializar_app():
    print("🔄 Iniciando sistema do Propulsor...")

    # Exemplo de chamadas reais
    try:
        from .distribuidor_emails import distribuir_emails
        distribuir_emails()
    except Exception as e:
        print(f"Erro ao distribuir e-mails: {e}")

    print("✅ Sistema do Propulsor pronto.")
