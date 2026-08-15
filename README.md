# Orçamento de Aluguel - Imobiliária R.M.

Projeto acadêmico da disciplina **Algorithmic Thinking & Introduction to Object-Oriented Programming**. A aplicação calcula o aluguel mensal de apartamentos, casas e estúdios, apresenta o parcelamento do contrato imobiliário e gera um CSV com o cronograma de 12 meses.

## Como executar

1. Instale o Python 3.10 ou superior.
2. Abra o terminal dentro desta pasta.
3. Execute:

```bash
python main.py
```

O projeto utiliza apenas módulos da biblioteca-padrão do Python e não exige instalação de pacotes.

## Executar os testes

```bash
python -m unittest discover -s tests -v
```

## Regras implementadas

- Apartamento de 1 quarto: R$ 700,00.
- Apartamento de 2 quartos: adicional de R$ 200,00.
- Casa de 1 quarto: R$ 900,00.
- Casa de 2 quartos: adicional de R$ 250,00.
- Garagem para casa ou apartamento: adicional de R$ 300,00.
- Estúdio: R$ 1.200,00.
- Estúdio com estacionamento: pacote de até 2 vagas por R$ 250,00; cada vaga acima da segunda custa R$ 60,00.
- Apartamento sem crianças: desconto de 5% sobre aluguel e adicionais.
- Contrato imobiliário: R$ 2.000,00, parcelável de 1 a 5 vezes.

## Organização

```text
projeto_orcamento_rm/
├── app/
│   ├── modelos.py       # Entidades e validações
│   ├── servicos.py      # Cálculos e geração do CSV
│   └── interface.py     # Interface gráfica Tkinter
├── tests/
│   └── test_orcamento.py
├── main.py
├── README.md
├── relatorio_teorico.pdf
└── roteiro_video_pitch.md
```

## Premissas adotadas

O enunciado não informa explicitamente como inserir o contrato no cronograma anual. Por isso, o CSV mantém o aluguel nos 12 meses e distribui o contrato nos primeiros 1 a 5 meses, conforme a escolha do cliente. As colunas são separadas para manter transparência.

Para publicar, crie um repositório no GitHub, envie esta pasta e substitua no documento de entrega o campo reservado pelo endereço real do repositório.

