# wpisz w terminalu:  streamlit run anova_app.py
import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import altair as alt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

st.set_page_config(
    page_title="Interaktywna ANOVA",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interaktywna jednoczynnikowa ANOVA")

st.write(
    """
    Zmieniaj wyniki w trzech grupach i obserwuj,
    jak zmieniają się statystyka **F**, wartość **p**
    oraz wielkość efektu **η²**.
    """
)

st.divider()

# =========================================================
# DANE
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Grupa A")
    a1 = st.slider("A1", 0, 20, 4)
    a2 = st.slider("A2", 0, 20, 5)
    a3 = st.slider("A3", 0, 20, 5)
    a4 = st.slider("A4", 0, 20, 6)

with col2:
    st.subheader("Grupa B")
    b1 = st.slider("B1", 0, 20, 7)
    b2 = st.slider("B2", 0, 20, 8)
    b3 = st.slider("B3", 0, 20, 8)
    b4 = st.slider("B4", 0, 20, 9)

with col3:
    st.subheader("Grupa C")
    c1 = st.slider("C1", 0, 20, 10)
    c2 = st.slider("C2", 0, 20, 11)
    c3 = st.slider("C3", 0, 20, 11)
    c4 = st.slider("C4", 0, 20, 12)


A = np.array([a1, a2, a3, a4], dtype=float)
B = np.array([b1, b2, b3, b4], dtype=float)
C = np.array([c1, c2, c3, c4], dtype=float)

groups = [A, B, C]

# =========================================================
# PODSTAWOWE WARTOŚCI
# =========================================================

means = [np.mean(g) for g in groups]

all_values = np.concatenate(groups)

grand_mean = np.mean(all_values)

N = len(all_values)
k = len(groups)

# =========================================================
# SUMY KWADRATÓW
# =========================================================

SS_between = sum(
    len(g) * (np.mean(g) - grand_mean) ** 2
    for g in groups
)

SS_within = sum(
    np.sum((g - np.mean(g)) ** 2)
    for g in groups
)

SS_total = np.sum(
    (all_values - grand_mean) ** 2
)

# =========================================================
# STOPNIE SWOBODY
# =========================================================

df_between = k - 1
df_within = N - k
df_total = N - 1

# =========================================================
# ŚREDNIE KWADRATY
# =========================================================

MS_between = SS_between / df_between
MS_within = SS_within / df_within

# =========================================================
# F i p
# =========================================================

if MS_within > 0:
    F = MS_between / MS_within
    p = stats.f.sf(F, df_between, df_within)

elif MS_between > 0:
    F = np.inf
    p = 0.0

else:
    F = np.nan
    p = np.nan

# =========================================================
# ETA KWADRAT
# =========================================================

if SS_total > 0:
    eta_squared = SS_between / SS_total
else:
    eta_squared = 0

# =========================================================
# WYNIKI
# =========================================================

st.divider()

st.header("1. Średnie")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Średnia A", f"{means[0]:.2f}")
c2.metric("Średnia B", f"{means[1]:.2f}")
c3.metric("Średnia C", f"{means[2]:.2f}")
c4.metric("Średnia ogólna", f"{grand_mean:.2f}")


# =========================================================
# WYKRES
# =========================================================

st.header("2. Jak wyglądają grupy?")

df_plot = pd.DataFrame({
    "Grupa": ["A", "B", "C"],
    "Średnia": means
})

chart = alt.Chart(df_plot).mark_bar().encode(
    x=alt.X(
        "Grupa:N",
        axis=alt.Axis(labelAngle=0)
    ),
    y=alt.Y(
        "Średnia:Q",
        title="Średnia"
    )
)

st.altair_chart(chart, width="stretch")

# =========================================================
# TABELA ANOVA
# =========================================================

st.header("3. Tabela ANOVA")

anova_table = pd.DataFrame(
    {
        "Źródło zmienności": [
            "Między grupami",
            "Wewnątrz grup",
            "Całkowita"
        ],
        "SS": [
            SS_between,
            SS_within,
            SS_total
        ],
        "df": [
            df_between,
            df_within,
            df_total
        ],
        "MS": [
            MS_between,
            MS_within,
            np.nan
        ],
        "F": [
            F,
            np.nan,
            np.nan
        ],
        "p": [
            p,
            np.nan,
            np.nan
        ]
    }
)

st.dataframe(
    anova_table.style.format(
        {
            "SS": "{:.2f}",
            "MS": "{:.2f}",
            "F": "{:.2f}",
            "p": "{:.4f}"
        },
        na_rep="—"
    ),
    width="stretch",
    hide_index=True
)


# =========================================================
# INTERPRETACJA F
# =========================================================

st.header("4. Skąd bierze się F?")

st.latex(
    r"F = \frac{MS_{between}}{MS_{within}}"
)

st.write(
    f"""
    W naszym przykładzie:

    **MS między grupami = {MS_between:.2f}**

    **MS wewnątrz grup = {MS_within:.2f}**
    """
)

if MS_within > 0:
    st.latex(
        rf"F = \frac{{{MS_between:.2f}}}{{{MS_within:.2f}}}"
        rf" = {F:.2f}"
    )

st.info(
    """
    Im większa zmienność **między grupami**
    w stosunku do zmienności **wewnątrz grup**,
    tym większa statystyka F.
    """
)


# =========================================================
# ZAPIS WYNIKU
# =========================================================

st.header("5. Jak zapisać wynik?")

st.success(
    f"F({df_between}, {df_within}) = {F:.2f}, "
    f"p = {p:.4f}, η² = {eta_squared:.3f}"
)


# =========================================================
# ETA SQUARED
# =========================================================

st.header("6. Eta kwadrat")

st.latex(
    r"\eta^2 = \frac{SS_{between}}{SS_{total}}"
)

st.latex(
    rf"\eta^2 = \frac{{{SS_between:.2f}}}"
    rf"{{{SS_total:.2f}}}"
    rf" = {eta_squared:.3f}"
)

st.write(
    f"""
    Oznacza to, że około **{eta_squared * 100:.1f}%**
    całkowitej wariancji wyników wiąże się
    z przynależnością do grupy.
    """
)


# =========================================================
# INTERPRETACJA
# =========================================================

st.header("7. Interpretacja")

if p < 0.05:
    st.success(
        "p < 0,05 → odrzucamy H₀. "
        "Co najmniej dwie średnie różnią się istotnie."
    )
else:
    st.warning(
        "p ≥ 0,05 → brak podstaw do odrzucenia H₀."
    )

if eta_squared < 0.01:
    effect = "bardzo mały"
elif eta_squared < 0.06:
    effect = "mały"
elif eta_squared < 0.14:
    effect = "średni"
else:
    effect = "duży"

st.write(
    f"Wielkość efektu: **{effect}** "
    f"(η² = {eta_squared:.3f})."
)


# =========================================================
# PODSUMOWANIE
# =========================================================

st.divider()

st.subheader("Zapamiętaj")

st.markdown(
    """
    **Schemat ANOVA:**

    **SS → df → MS → F**

    - `SS` – suma kwadratów
    - `df` – stopnie swobody
    - `MS = SS / df`
    - `F = MS między grupami / MS wewnątrz grup`
    - `η² = SS między grupami / SS całkowite`
    """
)
# =========================================================
# TEST POST-HOC TUKEYA
# =========================================================

st.header("8. Test post-hoc Tukeya")

values = np.concatenate([A, B, C])

labels = (
    ["A"] * len(A)
    + ["B"] * len(B)
    + ["C"] * len(C)
)

if p < 0.05:

    tukey = pairwise_tukeyhsd(
        endog=values,
        groups=labels,
        alpha=0.05
    )

    tukey_df = pd.DataFrame(
        data=tukey.summary().data[1:],
        columns=tukey.summary().data[0]
    )

    tukey_df = tukey_df.rename(columns={
        "group1": "Grupa 1",
        "group2": "Grupa 2",
        "meandiff": "Różnica średnich",
        "p-adj": "p skorygowane",
        "lower": "Dolna granica CI",
        "upper": "Górna granica CI",
        "reject": "Istotna różnica"
    })

    st.dataframe(
        tukey_df,
        width="stretch",
        hide_index=True
    )

    st.info(
        """
        Kolumna **Istotna różnica** informuje, czy różnica między daną parą grup
        jest istotna statystycznie.

        - `True` → grupy różnią się istotnie
        - `False` → brak istotnej różnicy
        """
    )

    st.info(
        """
        **Jak interpretować przedział ufności?**

        Jeśli przedział ufności dla różnicy średnich
        **nie zawiera zera**, to różnica między grupami
        jest istotna statystycznie.

        Przykład:
        - CI = [1.4, 4.6] → różnica istotna
        - CI = [-0.8, 3.2] → brak istotnej różnicy
        """
    )

    significant_pairs = tukey_df[
        tukey_df["Istotna różnica"] == True
    ]

    if len(significant_pairs) > 0:
        st.success("Istotne różnice występują pomiędzy:")

        for _, row in significant_pairs.iterrows():
            st.write(
                f"**{row['Grupa 1']} vs {row['Grupa 2']}** "
                f"(p = {row['p skorygowane']})"
            )

    else:
        st.info(
            "Nie stwierdzono istotnych różnic pomiędzy parami grup."
        )

else:

    st.warning(
        """
        ANOVA nie jest istotna statystycznie (p ≥ 0,05),
        dlatego test post-hoc nie jest wykonywany.
        """
    )