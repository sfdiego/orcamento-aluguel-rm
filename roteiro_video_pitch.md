# Roteiro do vídeo-pitch (até 4 minutos)

## 0:00-0:30 - Apresentação

“Olá! Meu nome é Diego Ferreira e apresentarei o projeto Orçamento de Aluguel, desenvolvido para a Imobiliária R.M. O objetivo é automatizar o cálculo das mensalidades de apartamentos, casas e estúdios, incluindo adicionais, descontos, contrato e geração de CSV.”

## 0:30-1:10 - Estrutura e orientação a objetos

“O projeto foi dividido em módulos. Em `modelos.py`, criei classes de dados para representar a solicitação e o resultado. Em `servicos.py`, a classe `CalculadoraOrcamento` concentra as regras do negócio, enquanto `GeradorCSV` cria o cronograma de 12 meses. Em `interface.py`, está a tela utilizada pelo usuário. Essa separação facilita manutenção e testes.”

## 1:10-2:10 - Demonstração da interface

1. Execute `python main.py`.
2. Digite o nome de um cliente.
3. Selecione “Apartamento”, 2 quartos, garagem e desmarque crianças.
4. Escolha 5 parcelas para o contrato.
5. Clique em “Calcular orçamento”.

“A aplicação parte de R$ 700,00, adiciona R$ 200,00 pelo segundo quarto e R$ 300,00 pela garagem. O subtotal é R$ 1.200,00. Como o cliente não possui crianças, é aplicado desconto de 5%, ou R$ 60,00, resultando em R$ 1.140,00 mensais. O contrato de R$ 2.000,00 fica em cinco parcelas de R$ 400,00.”

## 2:10-2:50 - CSV

1. Clique em “Gerar CSV”.
2. Escolha o local.
3. Abra o arquivo em uma planilha.

“O arquivo possui 12 registros. O aluguel aparece em todos os meses e as parcelas do contrato aparecem nos cinco primeiros, em colunas separadas, junto ao total mensal.”

## 2:50-3:30 - Código e testes

“As decisões são realizadas com estruturas condicionais de acordo com o tipo de imóvel. Os dados são validados antes do cálculo. Também criei testes automatizados que verificam apartamento, casa, estúdio, desconto, parcelamento e a quantidade de linhas do CSV.”

Mostre no terminal:

```bash
python -m unittest discover -s tests -v
```

## 3:30-3:55 - Encerramento

“O projeto atende aos requisitos do desafio, aplica pensamento algorítmico e orientação a objetos e oferece uma interface simples para uso real. Obrigado pela atenção.”

