from shiny import App, ui, render, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import linregress

# =========================
# ESTILIZAÇÃO CSS CUSTOMIZADA
# =========================
CSS_PREMIUM = """
/* Fundo Geral e Tipografia */
body {
    background-color: #F2F2F0 !important;
    color: #2D2D2D !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Barra de Navegação */
.navbar {
    background-color: #2F6073 !important;
    border-bottom: 2px solid #499CA6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.navbar-brand {
    color: #F2F2F0 !important;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.nav-link {
    color: rgba(242, 242, 240, 0.75) !important;
    font-weight: 500;
    transition: color 0.2s ease;
}
.nav-link:hover {
    color: #7EF2B0 !important;
}
.nav-link.active {
    color: #F2F2F0 !important;
    border-bottom: 3px solid #6AD9B9;
    background-color: rgba(255,255,255,0.05) !important;
}

/* Sidebar (Painel Lateral) */
.sidebar {
    background-color: #F2F2F0 !important;
    border-right: 1px solid rgba(45, 45, 45, 0.1);
    padding: 20px;
}
.sidebar .form-label {
    color: #2D2D2D !important;
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

/* Inputs e Controles */
.form-control, .form-select {
    border: 1px solid rgba(47, 96, 115, 0.2) !important;
    border-radius: 6px !important;
    background-color: #FFFFFF !important;
    color: #2D2D2D !important;
    padding: 0.6rem 0.75rem;
}
.form-control:focus, .form-select:focus {
    border-color: #499CA6 !important;
    box-shadow: 0 0 0 3px rgba(73, 156, 166, 0.2) !important;
}

/* Customização de Radio Buttons e Sliders */
.form-check-input:checked {
    background-color: #499CA6 !important;
    border-color: #499CA6 !important;
}
.irs--shiny .irs-bar {
    background: #499CA6 !important;
    top: 25px !important;
    height: 8px !important;
}
.irs--shiny .irs-handle {
    border: 2px solid #499CA6 !important;
    background-color: #FFFFFF !important;
    width: 18px !important;
    height: 18px !important;
    top: 20px !important;
}
.irs--shiny .irs-single {
    background-color: #2F6073 !important;
}

/* Cards de Gráficos e Conteúdo */
.card {
    background-color: #FFFFFF !important;
    border: 1px solid rgba(45, 45, 45, 0.05) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(45, 45, 45, 0.03) !important;
    margin-bottom: 20px;
    overflow: hidden;
}
.card-header {
    background-color: #FFFFFF !important;
    border-bottom: 1px solid rgba(45, 45, 45, 0.08) !important;
    color: #2F6073 !important;
    font-weight: 600;
    font-size: 1rem;
    padding: 15px 20px !important;
}

/* Value Boxes (Métricas) */
.bslib-value-box {
    background-color: #FFFFFF !important;
    border: 1px solid rgba(47, 96, 115, 0.15) !important;
    border-left: 5px solid #2F6073 !important;
    border-radius: 6px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}
.bslib-value-box .value-box-title {
    color: #499CA6 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px;
    font-weight: 600 !important;
}
.bslib-value-box .value-box-value {
    color: #2D2D2D !important;
    font-weight: 700 !important;
}
"""

# =========================
# UI
# =========================

app_ui = ui.page_navbar(

    ui.nav_panel(
        "Análise Descritiva",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_file("arquivo", "Selecione um arquivo CSV", accept=[".csv"]),
                ui.input_select("variavel_desc", "Variável Quantitativa", choices=[]),
            ),

            ui.layout_columns(
                ui.value_box("Média", ui.output_text("media")),
                ui.value_box("Mediana", ui.output_text("mediana")),
                ui.value_box("Desvio-padrão", ui.output_text("desvio")),
            ),

            ui.layout_columns(
                ui.value_box("Tamanho da Amostra", ui.output_text("n")),
                ui.value_box("Mínimo", ui.output_text("minimo")),
                ui.value_box("Máximo", ui.output_text("maximo")),
            ),

            ui.card(
                ui.card_header("Histograma"),
                ui.output_plot("histograma")
            ),

            ui.card(
                ui.card_header("Boxplot"),
                ui.output_plot("boxplot")
            ),
        )
    ),

    ui.nav_panel(
        "Teste de Hipóteses",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select("variavel_teste", "Variável", choices=[]),
                ui.input_numeric("variancia", "Variância Populacional", value=1),
                ui.input_radio_buttons(
                    "tipo_teste",
                    "Tipo de Teste",
                    {
                        "bilateral": "Bilateral",
                        "direita": "Unilateral à Direita",
                        "esquerda": "Unilateral à Esquerda"
                    }
                ),
                ui.input_slider("mu0", "μ0", min=-100, max=100, value=0),
                ui.input_slider("alpha", "Nível de Significância", min=0.01, max=0.10, value=0.05, step=0.01),
            ),

            ui.layout_columns(
                ui.value_box("Estatística Z", ui.output_text("estatistica_z")),
                ui.value_box("Decisão", ui.output_text("decisao"))
            )
        )
    ),

    ui.nav_panel(
        "Intervalo de Confiança",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select("variavel_ic", "Variável", choices=[]),
                ui.input_numeric("variancia_ic", "Variância Populacional", value=1),
                ui.input_slider("confianca", "Nível de Confiança", min=0.80, max=0.99, value=0.95, step=0.01)
            ),

            ui.layout_columns(
                ui.value_box("Limite Inferior", ui.output_text("li")),
                ui.value_box("Limite Superior", ui.output_text("ls")),
                ui.value_box("Confiança", ui.output_text("conf"))
            )
        )
    ),

    ui.nav_panel(
        "Regressão Linear",
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_select("x", "Variável X", choices=[]),
                ui.input_select("y", "Variável Y", choices=[])
            ),

            ui.layout_columns(
                ui.value_box("Correlação R", ui.output_text("r")),
                ui.value_box("R²", ui.output_text("r2"))
            ),

            ui.card(
                ui.card_header("Equação da Reta"),
                ui.output_text("equacao")
            ),

            ui.card(
                ui.card_header("Gráfico de Dispersão"),
                ui.output_plot("grafico_regressao")
            )
        )
    ),

    title="Dashboard Estatístico - Shiny for Python",
    header=ui.tags.style(CSS_PREMIUM)
)


# =========================
# SERVER
# =========================

def server(input, output, session):

    @reactive.calc
    def dados():
        arq = input.arquivo()
        if arq is None:
            return None

        caminho = arq[0]["datapath"]

        try:
            df = pd.read_csv(caminho)
        except Exception:
            df = pd.read_excel(caminho)

        return df

    @reactive.calc
    def colunas_numericas():
        df = dados()
        if df is None:
            return []
        return list(df.select_dtypes(include=np.number).columns)

    @reactive.effect
    def _():
        cols = colunas_numericas()

        ui.update_select("variavel_desc", choices=cols)
        ui.update_select("variavel_teste", choices=cols)
        ui.update_select("variavel_ic", choices=cols)
        ui.update_select("x", choices=cols)
        ui.update_select("y", choices=cols)

    def obter_serie(nome):
        df = dados()
        if df is None or nome is None or nome == "":
            return pd.Series(dtype=float)
        return pd.to_numeric(df[nome], errors="coerce").dropna()

    # ===== Descritiva =====

    @output
    @render.text
    def media():
        s = obter_serie(input.variavel_desc())
        return "-" if len(s) == 0 else f"{s.mean():.4f}"

    @output
    @render.text
    def mediana():
        s = obter_serie(input.variavel_desc())
        return "-" if len(s) == 0 else f"{s.median():.4f}"

    @output
    @render.text
    def desvio():
        s = obter_serie(input.variavel_desc())
        return "-" if len(s) == 0 else f"{s.std():.4f}"

    @output
    @render.text
    def n():
        s = obter_serie(input.variavel_desc())
        return str(len(s))

    @output
    @render.text
    def minimo():
        s = obter_serie(input.variavel_desc())
        return "-" if len(s) == 0 else f"{s.min():.4f}"

    @output
    @render.text
    def maximo():
        s = obter_serie(input.variavel_desc())
        return "-" if len(s) == 0 else f"{s.max():.4f}"

    @output
    @render.plot
    def histograma():
        fig, ax = plt.subplots(figsize=(7,4), facecolor="#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        s = obter_serie(input.variavel_desc())
        if len(s):
            ax.hist(s, bins=20, color="#499CA6", edgecolor="#2F6073", alpha=0.85)
        ax.set_title("Histograma", color="#2D2D2D", fontsize=12, pad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color((0.176, 0.176, 0.176, 0.2)) # Correção efetuada aqui
        ax.spines['bottom'].set_color((0.176, 0.176, 0.176, 0.2)) # Correção efetuada aqui
        ax.tick_params(colors='#2D2D2D')
        return fig

    @output
    @render.plot
    def boxplot():
        fig, ax = plt.subplots(figsize=(7,4), facecolor="#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        s = obter_serie(input.variavel_desc())
        if len(s):
            prox_box = ax.boxplot(s, patch_artist=True)
            for box in prox_box['boxes']:
                box.set(facecolor="#6AD9B9", color="#2F6073", linewidth=1.5)
            for median in prox_box['medians']:
                median.set(color="#2F6073", linewidth=2)
        ax.set_title("Boxplot", color="#2D2D2D", fontsize=12, pad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color((0.176, 0.176, 0.176, 0.2)) # Correção efetuada aqui
        ax.spines['bottom'].set_color((0.176, 0.176, 0.176, 0.2)) # Correção efetuada aqui
        ax.tick_params(colors='#2D2D2D')
        return fig

    # ===== Teste Hipótese =====

    @reactive.calc
    def resultado_teste():
        s = obter_serie(input.variavel_teste())

        if len(s) == 0:
            return None

        n = len(s)
        media = s.mean()
        sigma = np.sqrt(input.variancia())
        mu0 = input.mu0()

        z = (media - mu0) / (sigma / np.sqrt(n))

        alpha = input.alpha()
        tipo = input.tipo_teste()

        if tipo == "bilateral":
            crit = stats.norm.ppf(1 - alpha/2)
            decisao = "Rejeita H0" if abs(z) > crit else "Não Rejeita H0"

        elif tipo == "direita":
            crit = stats.norm.ppf(1 - alpha)
            decisao = "Rejeita H0" if z > crit else "Não Rejeita H0"

        else:
            crit = stats.norm.ppf(alpha)
            decisao = "Rejeita H0" if z < crit else "Não Rejeita H0"

        return z, decisao

    @output
    @render.text
    def estatistica_z():
        r = resultado_teste()
        return "-" if r is None else f"{r[0]:.4f}"

    @output
    @render.text
    def decisao():
        r = resultado_teste()
        return "-" if r is None else r[1]

    # ===== Intervalo =====

    @reactive.calc
    def intervalo():
        s = obter_serie(input.variavel_ic())

        if len(s) == 0:
            return None

        media = s.mean()
        n = len(s)

        sigma = np.sqrt(input.variancia_ic())

        conf = input.confianca()
        alpha = 1 - conf

        z = stats.norm.ppf(1 - alpha/2)

        erro = z * sigma / np.sqrt(n)

        return media - erro, media + erro

    @output
    @render.text
    def li():
        r = intervalo()
        return "-" if r is None else f"{r[0]:.4f}"

    @output
    @render.text
    def ls():
        r = intervalo()
        return "-" if r is None else f"{r[1]:.4f}"

    @output
    @render.text
    def conf():
        return f"{input.confianca()*100:.0f}%"

    # ===== Regressão =====

    @reactive.calc
    def regressao():
        df = dados()

        if df is None:
            return None

        xvar = input.x()
        yvar = input.y()

        if not xvar or not yvar:
            return None

        temp = df[[xvar, yvar]].dropna()

        if len(temp) < 2:
            return None

        return linregress(temp[xvar], temp[yvar])

    @output
    @render.text
    def r():
        reg = regressao()
        return "-" if reg is None else f"{reg.rvalue:.4f}"

    @output
    @render.text
    def r2():
        reg = regressao()
        return "-" if reg is None else f"{reg.rvalue**2:.4f}"

    @output
    @render.text
    def equacao():
        reg = regressao()
        if reg is None:
            return "-"
        return f"ŷ = {reg.intercept:.4f} + {reg.slope:.4f}x"

    @output
    @render.plot
    def grafico_regressao():
        fig, ax = plt.subplots(figsize=(7,4), facecolor="#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        df = dados()

        if df is not None and input.x() and input.y():
            temp = df[[input.x(), input.y()]].dropna()

            if len(temp) > 1:
                reg = regressao()

                ax.scatter(temp[input.x()], temp[input.y()], color="#499CA6", alpha=0.7, edgecolors="none")

                x_line = np.linspace(temp[input.x()].min(),
                                     temp[input.x()].max(), 100)

                y_line = reg.intercept + reg.slope * x_line

                ax.plot(x_line, y_line, color="#2F6073", linewidth=2)

                ax.set_xlabel(input.x(), color="#2D2D2D")
                ax.set_ylabel(input.y(), color="#2D2D2D")

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color((0.176, 0.176, 0.176, 0.2)) # Correção efetuada aqui
        ax.spines['bottom'].set_color((0.176, 0.176, 0.176, 0.2)) # Correção efetuada aqui
        ax.tick_params(colors='#2D2D2D')
        return fig


app = App(app_ui, server)