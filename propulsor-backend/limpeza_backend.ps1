# Vá para a pasta do backend
cd C:\ulsor\propulsor-intelligence\propulsor-backend

# Remove arquivos desnecessários da raiz
Remove-Item *.png, *.jpg, *.zip, *.md, *.php, *.sqbpro, *.bat, *.log -ErrorAction SilentlyContinue

# Remove arquivos experimentais e backups da raiz
Remove-Item *-Copia* -ErrorAction SilentlyContinue
Remove-Item *historico* -ErrorAction SilentlyContinue
Remove-Item *todo* -ErrorAction SilentlyContinue
Remove-Item *guia* -ErrorAction SilentlyContinue

# Limpa a pasta database
cd database
Remove-Item *.db-journal, *historico*, *backup*, *.zip -ErrorAction SilentlyContinue
cd ..

# Opcional: Limpa outros lixos que surgirem
# Remove-Item static\* -Recurse -Force -ErrorAction SilentlyContinue
# Remove-Item temp\* -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Limpeza completa! Backend turbo para deploy."