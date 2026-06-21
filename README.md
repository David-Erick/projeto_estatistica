# Dashboard Estatístico com Shiny for Python

## Descrição

Este projeto consiste no desenvolvimento de um dashboard interativo utilizando **Shiny for Python** para análise estatística de dados. O sistema permite que o usuário carregue arquivos CSV diretamente pela interface e realize diferentes análises estatísticas sem a necessidade de programação adicional.

O dashboard foi desenvolvido como atividade prática da disciplina de Estatística, contemplando conceitos de estatística descritiva, inferência estatística e regressão linear simples.

---

## Funcionalidades

### 1. Análise Descritiva

Permite selecionar uma variável quantitativa da base de dados para análise.

São apresentados:

* Média
* Mediana
* Desvio-padrão
* Tamanho da amostra
* Valor mínimo
* Valor máximo

Além disso, são gerados automaticamente:

* Histograma
* Boxplot

---

### 2. Teste de Hipóteses para a Média (Variância Conhecida)

O usuário pode configurar:

* Variância populacional
* Valor hipotético μ₀
* Nível de significância α
* Tipo de teste:

  * Bilateral
  * Unilateral à direita
  * Unilateral à esquerda

O sistema retorna:

* Estatística Z
* Decisão do teste

Hipóteses consideradas:

#### Teste bilateral

H₀: μ = μ₀

H₁: μ ≠ μ₀

#### Teste unilateral à direita

H₀: μ = μ₀

H₁: μ > μ₀

#### Teste unilateral à esquerda

H₀: μ = μ₀

H₁: μ < μ₀

---

### 3. Intervalo de Confiança para a Média

O usuário informa:

* Variância populacional
* Nível de confiança

O dashboard calcula:

* Limite inferior
* Limite superior
* Nível de confiança utilizado

Assumindo distribuição normal e variância populacional conhecida.

---

### 4. Regressão Linear Simples

Permite selecionar:

* Variável explicativa (X)
* Variável resposta (Y)

O dashboard retorna:

* Coeficiente de correlação (R)
* Coeficiente de determinação (R²)
* Equação da reta ajustada

Também é exibido:

* Gráfico de dispersão
* Linha de regressão ajustada

---

## Tecnologias Utilizadas

* Python 3
* Shiny for Python
* Pandas
* NumPy
* SciPy
* Matplotlib

---

## Estrutura do Projeto

```text
dashboard_estatistico/
│
├── app.py
├── requirements.txt
├── README.md
├── dados_teste_dashboard.csv
│
└── assets/
```

---

## Instalação

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

### 2. Entrar na pasta do projeto

```bash
cd projeto_estatistica
```

### 3. Criar ambiente virtual

Windows:

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

ou

```bash
pip install shiny pandas numpy scipy matplotlib
```

---

## Execução

Inicie a aplicação com:

```bash
shiny run --reload app.py
```

ou

```bash
python -m shiny run --reload app.py
```

Após iniciar, abra o navegador:

```text
http://127.0.0.1:8000
```

---

## Formato dos Dados

O dashboard aceita arquivos CSV contendo colunas numéricas.

Exemplo:

```csv
idade,salario,peso,altura
20,2500,70,1.75
21,2800,72,1.80
22,3000,68,1.72
23,3200,74,1.78
24,3500,80,1.85
```

---

## Exemplo de Uso

### Análise Descritiva

1. Carregue um arquivo CSV.
2. Selecione uma variável quantitativa.
3. Visualize:

   * Histograma
   * Boxplot
   * Estatísticas descritivas

### Teste de Hipótese

1. Selecione a variável.
2. Informe a variância populacional.
3. Defina μ₀.
4. Escolha o nível de significância.
5. Analise a decisão do teste.

### Intervalo de Confiança

1. Selecione a variável.
2. Informe a variância populacional.
3. Escolha o nível de confiança.
4. Consulte os limites do intervalo.

### Regressão Linear

1. Escolha as variáveis X e Y.
2. Visualize:

   * Gráfico de dispersão
   * Linha de regressão
   * R
   * R²
   * Equação ajustada

---

## Equipe

### Integrantes

* Nome do Integrante 1
* Nome do Integrante 2
* Nome do Integrante 3

---

## Vídeo de Demonstração

YouTube:

```text
INSERIR_LINK_DO_VIDEO
```

---

## Repositório GitHub

GitHub:

```text
INSERIR_LINK_DO_GITHUB
```

---

## Referências

* Shiny for Python Documentation:
  https://shiny.posit.co/py/

* SciPy Documentation:
  https://docs.scipy.org/

* Pandas Documentation:
  https://pandas.pydata.org/

* NumPy Documentation:
  https://numpy.org/

* Matplotlib Documentation:
  https://matplotlib.org/

---

## Licença

Projeto desenvolvido exclusivamente para fins acadêmicos.
