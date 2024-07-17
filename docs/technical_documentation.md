# Documentação Técnica do GineRisk

## Visão Geral
O GineRisk é um sistema de avaliação de risco ginecológico desenvolvido por Thiago Roque Ragazzo. Utiliza processamento de linguagem natural para extrair informações relevantes de anamneses e calcular riscos específicos.

## Componentes Principais
1. Modelo NER (BioBERT-PT)
2. Processador de Dados
3. Calculadora de Risco
4. API RESTful
5. Interface de Usuário

## Fluxo de Dados
1. O texto da anamnese é enviado através da interface de usuário.
2. O modelo NER extrai entidades relevantes do texto.
3. O processador de dados estrutura as entidades extraídas.
4. A calculadora de risco avalia os dados estruturados.
5. Os resultados são retornados e exibidos na interface.

## Configuração e Execução
1. Clone o repositório: `git clone https://github.com/thiagorragazzo/GineRisk.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o servidor: `python src/api/endpoints.py`
4. Acesse a interface web em `http://localhost:5000`

## Manutenção e Atualização
- Atualize regularmente as dependências do projeto.
- Realize fine-tuning periódico do modelo NER com novos dados.
- Mantenha as calculadoras de risco atualizadas com as últimas diretrizes médicas.
- Implemente um sistema de feedback para melhorias contínuas.

## Segurança e Conformidade
- Todos os dados são processados localmente para garantir a privacidade.
- Implemente medidas de segurança adicionais antes do uso em ambiente de produção.
- Certifique-se de estar em conformidade com as regulamentações de saúde locais.
