# Documentação Técnica do GineRisk

## Introdução
O GineRisk é um sistema projetado para automatizar a análise de anamnese e fornecer cálculos de risco para várias condições ginecológicas usando modelos de linguagem avançados.

## Arquitetura do Sistema
O sistema utiliza Flask para servir a aplicação web, com modelos de linguagem BioClinicalBERT para extração de entidades e BioGPT para geração de texto.

## Modelos Utilizados
- **BioClinicalBERT:** Usado para extrair entidades relevantes da anamnese.
- **BioGPT:** Usado para gerar texto explicativo baseado nos resultados da calculadora de risco.

## Calculadoras de Risco Implementadas
- **Risco de Pré-eclâmpsia**
  - **Inputs Necessários:** Pressão arterial, histórico familiar, índice de massa corporal (IMC), idade, peso.
  - **Cálculo:** Pendente.

- **Risco de Diabetes Gestacional**
  - **Inputs Necessários:** Histórico familiar, IMC, idade, peso.
  - **Cálculo:** Pendente.

- **Risco de Parto Prematuro**
  - **Inputs Necessários:** Histórico de partos anteriores, condições pré-existentes, idade.
  - **Cálculo:** Pendente.

- **Risco de Restrição de Crescimento Fetal**
  - **Inputs Necessários:** Histórico médico, medições de crescimento fetal.
  - **Cálculo:** Pendente.

- **Risco de Anomalias Cromossômicas**
  - **Inputs Necessários:** Exames genéticos, histórico familiar.
  - **Cálculo:** Pendente.

## Medidas de Desempenho e Validação
Pendentes.

## Conclusão
O GineRisk é uma ferramenta inovadora que utiliza IA para auxiliar médicos na avaliação de riscos ginecológicos. Testes adicionais são necessários para validar a eficácia dos cálculos de risco.