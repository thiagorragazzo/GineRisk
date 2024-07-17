### README (Markdown)

```markdown
# GineRisk

## Descrição
O GineRisk é um sistema automatizado que utiliza modelos de linguagem para extrair informações de anamnese e calcular riscos ginecológicos. Desenvolvido para auxiliar médicos na avaliação de condições como pré-eclâmpsia, diabetes gestacional, parto prematuro, restrição de crescimento fetal e anomalias cromossômicas.

## Requisitos
- Python 3.8+
- Flask
- Transformers
- Torch
- Numpy
- Scikit-learn
- Pandas
- Spacy
- pt_core_news_lg

## Instalação
Clone o repositório e instale as dependências:
```bash
git clone https://github.com/thiagorragazzo/GineRisk.git
cd GineRisk
python -m venv ginerisk_env
source ginerisk_env/bin/activate
pip install -r requirements.txt

Uso

Ative o ambiente virtual e execute o servidor:

source ginerisk_env/bin/activate
python -m src.api.endpoints

Contribuição

Contribuições são bem-vindas. Para contribuir, faça um fork do repositório, crie um branch para suas modificações, e submeta um pull request.

Licença

Este projeto está licenciado sob a MIT License.