# Manual do Usuário do GineRisk

## Introdução
Bem-vindo ao GineRisk, uma ferramenta desenvolvida para automatizar a análise de anamnese e calcular riscos ginecológicos. Este manual guiará você através das funcionalidades e do uso do sistema.

## Configuração Inicial
Para iniciar, ative o ambiente virtual e execute o servidor Flask:
```bash
source ginerisk_env/bin/activate
python -m src.api.endpoints

Uso da Interface Web

	1.	Acesse a aplicação web em http://127.0.0.1:5000.
	2.	Insira a anamnese da paciente no campo de texto fornecido.
	3.	Selecione o tipo de risco que deseja calcular (Pré-eclâmpsia, Diabetes Gestacional, etc.).
	4.	Clique em “Processar” para gerar os resultados.

Interpretação dos Resultados

Os resultados incluirão uma análise detalhada dos dados estruturados extraídos da anamnese e a avaliação de risco para a condição selecionada.

Contato e Suporte

Para dúvidas ou suporte, entre em contato com o desenvolvedor: Estudante de Medicina, Thiago Roque Ragazzo, Universidade de Medicina de Santo Amaro.

