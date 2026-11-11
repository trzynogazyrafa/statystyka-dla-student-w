# wpisz w terminalu:  streamlit run korelacja_regresja.py
import io
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy import stats
import statsmodels.api as sm

st.set_page_config(page_title='Korelacja i regresja', page_icon='📈', layout='wide')
st.title('📈 Korelacja i regresja')
st.caption('Ćwiczenia dla studentów · dane symulowane lub własny plik CSV')

@st.cache_data(show_spinner=False)
def generate(n, r, seed, pattern, outlier):
    rng = np.random.default_rng(seed)
    z = rng.normal(size=n)
    z = (z - z.mean()) / z.std(ddof=1)
    e = rng.normal(size=n)
    e = e - (e @ z) / (z @ z) * z
    e = (e - e.mean()) / e.std(ddof=1)
    x = 5 + 2*z
    y = 50 + 10*(r*z + np.sqrt(1-r*r)*e)
    if pattern == 'Krzywoliniowy (U)':
        y = 44 + 5.5*z*z + 3.5*e + 6*r*z
    elif pattern == 'Zmiana nachylenia':
        y += 9*np.maximum(0, x-np.median(x))
    df = pd.DataFrame({'X': x, 'Y': y})
    if outlier:
        df.loc[len(df)] = [x.max()+2, y.min()-30]
    return df

@st.cache_data(show_spinner=False)
def read_csv(raw):
    return pd.read_csv(io.BytesIO(raw), sep=None, engine='python')

def p_text(p):
    return 'p < 0,001' if p < .001 else f'p = {p:.3f}'.replace('.', ',')

def model_fit(x, y):
    return sm.OLS(y, sm.add_constant(x, has_constant='add')).fit()

def scatter(x, y, x_label, y_label, model=None, prediction=None):
    fig = go.Figure()
    fig.add_scatter(x=x, y=y, mode='markers', name='Obserwacje', marker={'size': 8, 'opacity': .75})
    if model is not None:
        xx = np.array([x.min(), x.max()])
        fig.add_scatter(x=xx, y=model.params[0]+model.params[1]*xx,
                        mode='lines', name='Regresja', line={'width': 3})
        if prediction is not None:
            fig.add_scatter(x=[prediction], y=[model.params[0]+model.params[1]*prediction],
                            mode='markers', name='Prognoza', marker={'size': 13, 'symbol': 'diamond'})
    fig.update_layout(height=420, xaxis_title=x_label, yaxis_title=y_label,
                      margin={'t': 30, 'b': 30}, legend={'orientation': 'h', 'y': 1.15})
    return fig

with st.sidebar:
    st.header('⚙️ Ustawienia danych')
    source = st.radio('Źródło', ['Symulacja', 'Własny CSV'])
    if source == 'Symulacja':
        n = st.slider('Liczba obserwacji', 10, 500, 60, step=10)
        r = st.slider('Docelowe r Pearsona', -.95, .95, -.60, step=.05)
        pattern = st.selectbox('Rodzaj zależności', ['Liniowy', 'Krzywoliniowy (U)', 'Zmiana nachylenia'])
        outlier = st.checkbox('Dodaj obserwację odstającą')
        seed = st.number_input('Ziarno losowe', min_value=0, max_value=100000, value=42)
        raw_data = generate(n, r, int(seed), pattern, outlier)
        xcol, ycol = raw_data.columns[:2]
    else:
        upload = st.file_uploader('Wybierz CSV', type='csv')
        if upload is None:
            st.info('Wczytaj CSV, aby kontynuować.')
            st.stop()
        try:
            raw_data = read_csv(upload.getvalue())
        except Exception as ex:
            st.error(f'Nie można odczytać CSV: {ex}')
            st.stop()
        numeric = []
        for col in raw_data.columns:
            converted = pd.to_numeric(raw_data[col], errors='coerce')
            if converted.notna().sum() >= 5:
                numeric.append(col)
        if len(numeric) < 2:
            st.error('Plik wymaga co najmniej dwóch kolumn liczbowych.')
            st.stop()
        xcol = st.selectbox('Predyktor X', numeric)
        ycol = st.selectbox('Zmienna zależna Y', [c for c in numeric if c != xcol])
    st.divider()
    st.caption('Wyniki symulacji są dydaktyczne i nie stanowią danych klinicznych.')

# W przeciwieństwie do st.tabs() ten przełącznik renderuje TYLKO wybrany widok.
section = st.segmented_control(
    'Temat', ['Korelacja', 'Regresja prosta', 'Diagnostyka', 'Regresja wieloraka'],
    default='Korelacja', key='section', selection_mode='single'
)
if section is None:
    st.stop()

# Konwersja tylko dwóch aktywnych kolumn; bez zbędnego przeliczania wszystkich modeli.
d = raw_data[[xcol, ycol]].apply(pd.to_numeric, errors='coerce')
d = d.replace([np.inf, -np.inf], np.nan).dropna()
if len(d) < 5 or d[xcol].nunique() < 3 or d[ycol].nunique() < 3:
    st.warning('Zbyt mało poprawnych i zróżnicowanych obserwacji.')
    st.stop()
x = d[xcol].to_numpy(dtype=float)
y = d[ycol].to_numpy(dtype=float)

if section == 'Korelacja':
    st.subheader('🔗 Korelacja Pearsona i Spearmana')
    pearson = stats.pearsonr(x, y)
    spearman = stats.spearmanr(x, y)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('r Pearsona', f'{pearson.statistic:.3f}')
    c2.metric('Istotność r', p_text(pearson.pvalue))
    c3.metric('ρ Spearmana', f'{spearman.statistic:.3f}')
    c4.metric('Liczebność n', len(d))
    st.plotly_chart(scatter(x, y, xcol, ycol), width='stretch')

    with st.expander("📐 Wzory na współczynniki korelacji"):

        st.markdown("### Korelacja Pearsona")

        st.latex(
            r"r_{xy} = "
            r"\frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}"
            r"{\sqrt{\sum_{i=1}^{n}(x_i-\bar{x})^2"
            r"\sum_{i=1}^{n}(y_i-\bar{y})^2}}"
        )

        st.markdown(
            "Współczynnik Pearsona mierzy kierunek "
            "i siłę liniowej zależności między zmiennymi."
        )

        st.markdown("### Korelacja Spearmana")

        st.latex(
            r"\rho_s = "
            r"1-\frac{6\sum_{i=1}^{n}d_i^2}"
            r"{n(n^2-1)}"
        )

        st.markdown(
            "gdzie dᵢ oznacza różnicę między rangami "
            "dwóch obserwacji. Ten wzór jest właściwy, "
            "gdy nie występują rangi wiązane."
        )

        st.markdown(
            "Korelacja Spearmana mierzy kierunek "
            "i siłę zależności monotonicznej. "
            "Przy występowaniu rang wiązanych "
            "oblicza się korelację Pearsona "
            "między rangami zmiennych."
        )
    ci = pearson.confidence_interval(.95)
    st.info(f'95% przedział ufności dla r: [{ci.low:.3f}; {ci.high:.3f}].')
    st.markdown('**Do sprawdzenia:** zmień liczebność próby, znak i siłę korelacji, dodaj punkt odstający, a następnie ustaw zależność w kształcie litery U. Czy korelacja oznacza przyczynowość?')

elif section == 'Regresja prosta':
    st.subheader('📉 Regresja prosta')
    model = model_fit(x, y)
    predict = st.slider('X dla prognozy', float(x.min()), float(x.max()), float(np.median(x)))
    st.plotly_chart(scatter(x, y, xcol, ycol, model, predict), width='stretch')
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Wyraz wolny b₀', f'{model.params[0]:.3f}')
    c2.metric('Nachylenie b₁', f'{model.params[1]:.3f}')
    c3.metric('R²', f'{model.rsquared:.3f}')
    c4.metric('Prognoza Ŷ', f'{model.params[0]+model.params[1]*predict:.2f}')
    st.latex(r'\hat{Y}=b_0+b_1X')
    st.write(f'Przy wzroście X o 1, przewidywana wartość Y zmienia się o {model.params[1]:.3f} jednostki. Model wyjaśnia {100*model.rsquared:.1f}% wariancji Y w próbie.')
    ci = np.asarray(model.conf_int())
    results = pd.DataFrame({
        'Parametr': ['Wyraz wolny', xcol], 'B': model.params,
        'SE': model.bse, 't': model.tvalues, 'p': model.pvalues,
        '95% CI dolny': ci[:, 0], '95% CI górny': ci[:, 1]
    }).round(4)
    st.dataframe(results, hide_index=True, width='stretch')
    st.write(f'F({int(model.df_model)}, {int(model.df_resid)}) = {model.fvalue:.3f}; {p_text(model.f_pvalue)}. Skorygowane R² = {model.rsquared_adj:.3f}.')
    st.caption('Dla regresji prostej z wyrazem wolnym R² = r².')

elif section == 'Diagnostyka':
    st.subheader('🔍 Diagnostyka regresji')
    model = model_fit(x, y)
    residuals = np.asarray(model.resid)
    fitted = np.asarray(model.fittedvalues)
    left, right = st.columns(2)
    with left:
        fig = go.Figure()
        fig.add_scatter(x=fitted, y=residuals, mode='markers', name='Reszty')
        fig.add_hline(y=0, line_dash='dash')
        fig.update_layout(height=390, title='Reszty a wartości przewidywane',
                          xaxis_title='Ŷ', yaxis_title='Y − Ŷ')
        st.plotly_chart(fig, width='stretch')
    with right:
        ordered = np.sort(residuals)
        theor = stats.norm.ppf((np.arange(len(ordered))+.5)/len(ordered))
        quantiles = np.quantile(ordered, [.25, .75])
        theo_q = np.quantile(theor, [.25, .75])
        slope = (quantiles[1]-quantiles[0])/(theo_q[1]-theo_q[0])
        intercept = quantiles[0]-slope*theo_q[0]
        fig = go.Figure()
        fig.add_scatter(x=theor, y=ordered, mode='markers', name='Reszty')
        fig.add_scatter(x=[theor.min(), theor.max()],
                        y=[slope*theor.min()+intercept, slope*theor.max()+intercept],
                        mode='lines', name='Linia odniesienia')
        fig.update_layout(height=390, title='Wykres Q–Q reszt',
                          xaxis_title='Kwantyle normalne', yaxis_title='Kwantyle reszt')
        st.plotly_chart(fig, width='stretch')
    st.metric('RMSE (mianownik n)', f'{np.sqrt(np.mean(residuals**2)):.3f}')
    # Odległość Cooka wymaga osobnego, cięższego rachunku, więc liczymy ją po żądaniu.
    if st.checkbox('Pokaż odległość Cooka (dodatkowe obliczenie)'):
        cook = model.get_influence().cooks_distance[0]
        st.metric('Maksymalna odległość Cooka', f'{np.max(cook):.3f}')
    st.markdown('Szukaj krzywizny, lejka, ekstremalnych punktów i odejść od prostej Q–Q. Niezależność obserwacji ocenia się również na podstawie projektu badania.')

elif section == 'Regresja wieloraka':
    st.subheader('➕ Regresja wieloraka – porównanie dwóch modeli')
    if source == 'Własny CSV':
        extras = [c for c in raw_data.columns if c not in [xcol, ycol]
                  and pd.to_numeric(raw_data[c], errors='coerce').notna().sum() >= 5]
        if not extras:
            st.warning('Brak trzeciej kolumny liczbowej w CSV. Przejdź do symulacji.')
            st.stop()
        extra = st.selectbox('Drugi predyktor', extras)
        dm = raw_data[[xcol, ycol, extra]].apply(pd.to_numeric, errors='coerce')
        dm = dm.replace([np.inf, -np.inf], np.nan).dropna()
    else:
        relation = st.slider('Powiązanie Z z X (parametr symulacji)', -.9, .9, .6, .1)
        effect = st.slider('Dodatkowy składnik Y związany z Z', -12., 12., 5., .5)
        rng = np.random.default_rng(int(seed)+17)
        zx = (x-x.mean())/x.std(ddof=1)
        independent = rng.normal(size=len(x))
        z = relation*zx + np.sqrt(1-relation**2)*independent
        extra = 'Z'
        dm = pd.DataFrame({xcol: x, ycol: y+effect*z, extra: z})
    if len(dm) < 8 or np.linalg.matrix_rank(sm.add_constant(dm[[xcol, extra]].to_numpy())) < 3:
        st.warning('Za mało kompletnych danych albo idealna współliniowość predyktorów.')
        st.stop()
    first = sm.OLS(dm[ycol], sm.add_constant(dm[[xcol]])).fit()
    second = sm.OLS(dm[ycol], sm.add_constant(dm[[xcol, extra]])).fit()
    comparison = pd.DataFrame({
        'Model': ['Tylko X', 'X oraz Z'], 'R²': [first.rsquared, second.rsquared],
        'Skorygowane R²': [first.rsquared_adj, second.rsquared_adj],
        'współczynnik dla X': [first.params[xcol], second.params[xcol]]
    }).round(3)
    st.dataframe(comparison, hide_index=True, width='stretch')
    coefficients = pd.DataFrame({'Predyktor': second.params.index,
                                 'współczynnik': second.params.values, 'p': second.pvalues.values}).round(4)
    st.dataframe(coefficients, hide_index=True, width='stretch')
    st.markdown('Współczynnik dla X oznacza związek X z Y przy **stałej wartości Z**. Sam wzrost R² nie świadczy o lepszym przewidywaniu nowych danych.')

st.divider()
st.download_button('⬇️ Pobierz analizowane dane do CSV',
                   d.to_csv(index=False).encode('utf-8-sig'),
                   file_name='korelacja_regresja_dane.csv', mime='text/csv',
                   on_click='ignore')
