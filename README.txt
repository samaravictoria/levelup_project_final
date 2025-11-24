# LevelUp

## 🌟 Sobre o Projeto
**LevelUp** é um aplicativo inovador que integra **bem-estar, sociabilidade e produtividade no trabalho** de forma gamificada.  
O objetivo é engajar equipes, permitindo que as empresas designem **Quests (tasks)** para seus times e recompensem os usuários conforme completam tarefas.

A experiência é gamificada:  
- Concluir tarefas gera **pontos**.  
- Pontos podem ser trocados por **prêmios**.  
- As quests variam entre **trabalho**, **bem-estar** ou **socialização**.

O diferencial do projeto é o uso de **Inteligência Artificial** para personalizar a experiência do usuário:  
- Detecta a **emoção** do usuário (ex.: estresse, felicidade).  
- Sugere **tasks de bem-estar** automaticamente.  
- Todas as tasks geradas são registradas no banco de dados.

---

## 🛠 Tecnologias Utilizadas
- **Frontend:** React.js  
- **Backend / Tasks:** Java  
- **Backend / Cadastro e Prêmios:** .NET  
- **Inteligência Artificial:** Python (DeepFace)  
- **Banco de Dados:** SQLite (desenvolvimento)  
- **API REST:** FastAPI para integração Python  
- **Gamificação:** Sistema de pontos e recompensas  

---

## 🔄 Fluxo do Sistema
1. O usuário abre o aplicativo frontend.  
2. A câmera é acionada e a IA detecta a **emoção** do usuário.  
3. Com base na emoção, a IA gera uma **task personalizada** (ex.: pausa, socialização).  
4. A task é registrada na tabela de **Tasks** do banco.  
5. Usuário completa as tasks → ganha **pontos**.  
6. Usuário pode trocar pontos por **prêmios** cadastrados no sistema .NET.  

Exemplo de mapeamento de emoções:

| Emoção  | Task sugerida            | Tipo      |
|---------|-------------------------|-----------|
| Estresse| Pausa de 5 minutos      | Wellness  |
| Tristeza| Conversar com um colega | Social    |
| Feliz   | Focar na próxima tarefa | Trabalho  |
| Surpresa| Respiração guiada       | Wellness  |
| Neutro  | Check-in rápido         | Social    |

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Frontend (React)
1. Abra o terminal na pasta `frontend`.  
2. Instale as dependências:
```bash
npm install

	Inicie o servidor de desenvolvimento:
npm start

O aplicativo será aberto no navegador:
http://localhost:3000

2️⃣Backend e IA

Observação: O backend de Tasks (Java) e Cadastro/Prêmios (.NET) devem estar ativos para o correto funcionamento do sistema.

	•	IA (Python): detecta emoções e cria tasks automaticamente.
	•	Tasks (Java): gerencia tasks da equipe.
	•	Cadastro e Prêmios (.NET): gerencia usuários e recompensas.

3️⃣ Docker (Opcional)

Para subir todos os serviços em containers:
docker-compose build
docker-compose up -d

Acessos:
	•	Frontend: http://localhost:3000
	•	AI Service: http://localhost:8000
	•	Tasks Service: http://localhost:8001
	•	Rewards Service: http://localhost:8002

📌 Observações
	•	Na primeira execução, o DeepFace fará download dos modelos necessários (pode levar alguns minutos).
	•	O projeto é um MVP e pode ser expandido para produção com autenticação, TLS, filas e políticas de privacidade.
	•	A gamificação permite engajar usuários com recompensas e incentiva a saúde mental e socialização no trabalho.


👥 Autores
	•	@samaravictoria
	•	@vanessayukari
	•	@SunaUezuri



