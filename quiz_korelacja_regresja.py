"""Osobna, lekka aplikacja Streamlit z quizem dla studentów."""
import streamlit as st

st.set_page_config(page_title='Quiz – korelacja i regresja', page_icon='🎓')
st.title('🎓 Quiz: korelacja i regresja')
st.caption('Samodzielne ćwiczenie – odpowiedzi i wyjaśnienia po sprawdzeniu.')

QUESTIONS = [
    ('Współczynnik r = −0,70 oznacza:',
     ['Dość silną ujemną zależność liniową', '70% wyjaśnionej wariancji', 'Ujemny wpływ przyczynowy'], 0,
     'Znak r wyznacza kierunek, a wartość bezwzględna siłę związku liniowego.'),
    ('W regresji prostej z wyrazem wolnym r = 0,60. R² wynosi:',
     ['0,60', '0,36', '0,77'], 1, 'R² = r² = 0,36.'),
    ('Co może wskazywać na źle dobraną postać liniową modelu?',
     ['Losowe reszty wokół zera', 'Systematyczna krzywizna na wykresie reszt', 'Skośny rozkład X'], 1,
     'Krzywizna reszt sugeruje, że relacja może być nieliniowa.'),
    ('W regresji wielorakiej współczynnik B dla X oznacza:',
     ['Efekt przyczynowy X', 'Związek z Y przy stałych innych predyktorach', 'Korelację Spearmana'], 1,
     'Współczynnik jest interpretowany warunkowo, po uwzględnieniu pozostałych predyktorów.'),
    ('Korelacja nieistotna statystycznie:',
     ['Dowodzi, że X i Y są niezależne', 'Nie pozwala odrzucić hipotezy zerowej przy danym progu α',
      'Dowodzi braku zależności nieliniowej'], 1,
     'Brak istotności nie jest dowodem braku jakiegokolwiek związku.'),
    ('Co oznacza R² = 0,40?',
     ['40% prognoz jest poprawnych', 'Model wyjaśnia 40% wariancji Y w próbie',
      'Korelacja wynosi 0,40'], 1,
     'R² jest miarą udziału wyjaśnionej wariancji, nie odsetkiem poprawnych prognoz.'),
]

with st.form('quiz'):
    answers = []
    for i, (question, options, _, _) in enumerate(QUESTIONS):
        answers.append(st.radio(f'{i+1}. {question}', options, index=None, key=f'answer_{i}'))
    submitted = st.form_submit_button('Sprawdź odpowiedzi', type='primary')

if submitted:
    score = sum(answer == options[correct] for answer, (_, options, correct, _) in zip(answers, QUESTIONS))
    st.subheader(f'Wynik: {score}/{len(QUESTIONS)}')
    for i, (answer, (question, options, correct, explanation)) in enumerate(zip(answers, QUESTIONS), 1):
        if answer == options[correct]:
            st.success(f'{i}. Poprawnie. {explanation}')
        else:
            st.error(f'{i}. Poprawna odpowiedź: {options[correct]}. {explanation}')
