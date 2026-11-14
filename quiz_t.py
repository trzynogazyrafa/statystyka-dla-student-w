# Uruchom: streamlit run quiz_t.py

import streamlit as st

st.set_page_config(page_title="Quiz – test t-Studenta", page_icon="📊", layout="centered")

QUESTIONS = [
    {
        "q": "Czy p = 0,04 oznacza, że prawdopodobieństwo prawdziwości H₀ wynosi 4%?",
        "options": [
            "Tak, H₀ ma 4% szans na bycie prawdziwą.",
            "Nie, p opisuje prawdopodobieństwo wyniku co najmniej tak skrajnego przy założeniu H₀.",
            "Tak, ale tylko w teście dwustronnym.",
            "Nie, p = 0,04 oznacza, że prawdopodobieństwo H₁ wynosi 96%.",
        ],
        "correct": 1,
        "explanation": "Wartość p dotyczy prawdopodobieństwa uzyskania statystyki co najmniej tak skrajnej, przy założeniu prawdziwości H₀ i założeń modelu. Nie jest prawdopodobieństwem prawdziwości H₀ ani H₁.",
    },
    {
        "q": "Czy dwie niezależne grupy po 20 osób można porównać testem t dla prób zależnych? Uzasadnij.",
        "options": [
            "Tak, bo liczebności grup są identyczne.",
            "Tak, jeśli średnie obu grup są podobne.",
            "Nie, test dla prób zależnych wymaga sparowanych obserwacji.",
            "Nie, bo test t wymaga co najmniej 30 osób w każdej grupie.",
        ],
        "correct": 2,
        "explanation": "Dwie rzeczywiście niezależne grupy porównuje się testem t dla prób niezależnych, często w wersji Welcha. Test sparowany wymaga rzeczywistych par pomiarów.",
    },
    {
        "q": "Czy brak istotności statystycznej dowodzi braku różnicy między populacjami?",
        "options": [
            "Tak, jeśli p > 0,05.",
            "Nie; może brakować mocy, aby wykryć rzeczywistą różnicę.",
            "Tak, o ile liczebności obu grup są równe.",
            "Nie; oznacza to zawsze, że błędnie wybrano test.",
        ],
        "correct": 1,
        "explanation": "Nieodrzucenie H₀ nie dowodzi jej prawdziwości. Warto uwzględnić moc, przedział ufności i wielkość efektu. Do wykazywania równoważności służą odpowiednio zaplanowane testy równoważności.",
    },
    {
        "q": "Czy test t można stosować do danych, które nie mają idealnie normalnego rozkładu?",
        "options": [
            "Nie; każda drobna asymetria wyklucza test t.",
            "Tak; założenia normalności nie mają żadnego znaczenia.",
            "Tak, bywa odporny na umiarkowane odchylenia, zwłaszcza przy większych próbach i bez silnych obserwacji odstających.",
            "Nie, chyba że wariancje obu grup są dokładnie identyczne.",
        ],
        "correct": 2,
        "explanation": "Test t bywa odporny na umiarkowane naruszenia normalności. Duża skośność i wartości odstające, zwłaszcza przy małych próbach, wymagają większej ostrożności. Dla prób zależnych ważny jest rozkład różnic.",
    },
    {
        "q": "Co oznacza wartość t = −3,5? Czy znak minus oznacza brak istotności?",
        "options": [
            "Znak minus oznacza automatycznie wynik nieistotny.",
            "Statystyka wskazuje kierunek różnicy zgodny z kolejnością odejmowania; o istotności decydują m.in. |t|, df i kierunek testu.",
            "Wynik oznacza, że średnia pierwszej grupy jest mniejsza dokładnie o 3,5 punktu.",
            "Oznacza, że p = −3,5.",
        ],
        "correct": 1,
        "explanation": "Ujemne t oznacza ujemny licznik po przyjęciu określonej kolejności odejmowania. Wielkość |t| = 3,5 wyraża liczbę błędów standardowych, a istotność zależy od rozkładu odniesienia i hipotezy.",
    },
    {
        "q": "Czy wraz ze wzrostem liczebności próby łatwiej wykryć niewielką, rzeczywistą różnicę? Dlaczego?",
        "options": [
            "Zwykle tak, ponieważ maleje błąd standardowy i rośnie moc testu przy pozostałych warunkach podobnych.",
            "Nie, ponieważ wartość p nie zależy od liczebności.",
            "Tak, ponieważ średnia różnica zawsze rośnie wraz z n.",
            "Nie, ponieważ większa próba zwiększa błąd standardowy.",
        ],
        "correct": 0,
        "explanation": "Przy stałej niezerowej różnicy i podobnej zmienności większe n zmniejsza błąd standardowy i na ogół zwiększa moc testu. Nie gwarantuje istotności w każdej realizacji badania.",
    },
    {
        "q": "Który test wybierzesz, aby sprawdzić, czy średni wynik studentów różni się od ustalonej normy 50 punktów?",
        "options": [
            "Test t dla prób zależnych.",
            "Test t dla dwóch prób niezależnych.",
            "Test t dla jednej próby.",
            "Test Levene’a.",
        ],
        "correct": 2,
        "explanation": "Porównujemy średnią jednej próby z ustaloną wartością referencyjną μ₀ = 50, dlatego wybieramy test t dla jednej próby.",
    },
    {
        "q": "U tych samych 24 osób zmierzono ciśnienie tętnicze przed treningiem i po treningu. Jaki test t należy zastosować i dlaczego?",
        "options": [
            "Test t dla prób niezależnych, bo są dwa pomiary.",
            "Test t dla jednej próby, bo badamy 24 osoby.",
            "Test t Welcha, bo pomiary odbyły się w różnym czasie.",
            "Test t dla prób zależnych, bo oba pomiary dotyczą tych samych osób.",
        ],
        "correct": 3,
        "explanation": "W pomiarach przed–po analizujemy różnice wewnątrz 24 par obserwacji, czyli test t dla prób zależnych.",
    },
    {
        "q": "Porównujesz średni wynik skali stresu u 30 osób z grupy A i 35 innych osób z grupy B. Jaki test t rozważysz?",
        "options": [
            "Test t dla prób zależnych, ponieważ obie grupy mają podobne liczebności.",
            "Test t dla dwóch prób niezależnych, często w wersji Welcha.",
            "Test t dla jednej próby z normą 35.",
            "Wyłącznie test t dla prób niezależnych z założeniem równych wariancji.",
        ],
        "correct": 1,
        "explanation": "Grupy zawierają różne osoby, więc są niezależne. Test Welcha jest często dobrym wyborem, bo nie wymaga równości wariancji populacyjnych.",
    },
    {
        "q": "Zapisz hipotezę zerową i dwustronną alternatywną dla porównania średnich wyników dwóch niezależnych grup.",
        "options": [
            "H₀: μ₁ = μ₂; H₁: μ₁ ≠ μ₂.",
            "H₀: μ₁ ≠ μ₂; H₁: μ₁ = μ₂.",
            "H₀: μ₁ > μ₂; H₁: μ₁ < μ₂.",
            "H₀: x̄₁ = x̄₂; H₁: x̄₁ > x̄₂.",
        ],
        "correct": 0,
        "explanation": "Hipotezy dotyczą średnich populacyjnych μ₁ i μ₂: H₀ zakłada zerową różnicę, a dwustronna H₁ dopuszcza oba kierunki różnicy.",
    },
    {
        "q": "Wyjaśnij własnymi słowami, czym różnią się odchylenie standardowe (SD) i błąd standardowy średniej (SE).",
        "options": [
            "SD mierzy niepewność średniej, a SE rozrzut pojedynczych wyników.",
            "SD i SE to dwie nazwy tej samej miary.",
            "SD opisuje rozrzut obserwacji, a SE niepewność oszacowania średniej; zwykle SE = SD/√n.",
            "SE zawsze rośnie wraz z liczebnością próby.",
        ],
        "correct": 2,
        "explanation": "SD charakteryzuje rozproszenie obserwacji. SE opisuje precyzję średniej jako estymatora; dla niezależnych obserwacji SE = s/√n.",
    },
    {
        "q": "Dla testu t dla jednej próby przy n = 16, x̄ = 66, s = 8 i μ₀ = 60 oblicz t oraz df.",
        "options": [
            "t = 0,75; df = 16",
            "t = 3; df = 16",
            "t = 3; df = 15",
            "t = 6; df = 15",
        ],
        "correct": 2,
        "explanation": "SE = 8/√16 = 2; t = (66 − 60)/2 = 3; df = 16 − 1 = 15. Dla testu dwustronnego p ≈ 0,009.",
    },
    {
        "q": "W teście t dla jednej próby badano 21 osób. Ile wynosi liczba stopni swobody (df)?",
        "options": ["19", "20", "21", "22"],
        "correct": 1,
        "explanation": "Dla testu t dla jednej próby df = n − 1 = 21 − 1 = 20.",
    },
    {
        "q": "Co oznacza dwustronna hipoteza alternatywna i czym różni się od jednostronnej?",
        "options": [
            "Dwustronna zakłada tylko wzrost, a jednostronna dopuszcza dwa kierunki.",
            "Dwustronna dotyczy różnicy w obu kierunkach, a jednostronna określa jeden kierunek przed analizą.",
            "Dwustronna wymaga dwóch prób, a jednostronna jednej próby.",
            "Dwustronna ma zawsze niższą wartość p niż jednostronna.",
        ],
        "correct": 1,
        "explanation": "Dwustronna H₁ może mieć postać μ₁ ≠ μ₂, a jednostronna np. μ₁ > μ₂. Kierunek wybiera się przed analizą danych.",
    },
    {
        "q": "Kiedy test Welcha jest bardziej odpowiedni niż klasyczny test t dla prób niezależnych z łączoną wariancją?",
        "options": [
            "Gdy dane są sparowane (przed–po).",
            "Gdy porównujemy średnią jednej próby z normą.",
            "Gdy badane grupy mają potencjalnie różne wariancje, szczególnie przy nierównych liczebnościach.",
            "Wyłącznie wtedy, gdy w obu grupach jest taka sama liczba obserwacji.",
        ],
        "correct": 2,
        "explanation": "Test Welcha nie wymaga równości wariancji populacyjnych. Stosuje zmodyfikowany błąd standardowy i przybliżone stopnie swobody, często niecałkowite.",
    },
]

assert len(QUESTIONS) == 15

st.title("📊 Quiz: testy t-Studenta")
st.caption("15 pytań jednokrotnego wyboru • przyjmujemy poziom α = 0,05")
st.info("Po zaznaczeniu odpowiedzi kliknij **Sprawdź odpowiedzi** na dole strony.")

if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "saved_answers" not in st.session_state:
    st.session_state.saved_answers = {}

with st.form("quiz_form"):
    for i, item in enumerate(QUESTIONS):
        st.markdown(f"#### Pytanie {i + 1} / {len(QUESTIONS)}")
        st.write(item["q"])
        st.radio(
            label=f"Odpowiedź na pytanie {i + 1}",
            options=list(range(len(item["options"]))),
            format_func=lambda index, opts=item["options"]: opts[index],
            index=None,
            key=f"answer_{i}",
            label_visibility="collapsed",
            disabled=st.session_state.submitted,
        )
        st.divider()
    send = st.form_submit_button("Sprawdź odpowiedzi", type="primary", disabled=st.session_state.submitted)

if send:
    answers = {i: st.session_state.get(f"answer_{i}") for i in range(len(QUESTIONS))}
    missing = [i + 1 for i, value in answers.items() if value is None]
    if missing:
        st.warning("Odpowiedz na wszystkie pytania. Brakuje odpowiedzi na: " + ", ".join(map(str, missing)))
    else:
        st.session_state.saved_answers = answers
        st.session_state.submitted = True
        st.rerun()

if st.session_state.submitted:
    responses = st.session_state.saved_answers
    score = sum(responses[i] == item["correct"] for i, item in enumerate(QUESTIONS))
    st.header("Twój wynik")
    st.metric("Zdobyte punkty", f"{score} / {len(QUESTIONS)}")
    st.progress(score / len(QUESTIONS))
    st.write(f"Poprawne odpowiedzi: **{score / len(QUESTIONS) * 100:.0f}%**")
    st.subheader("Odpowiedzi i wyjaśnienia")
    for i, item in enumerate(QUESTIONS):
        chosen = responses[i]
        correct = chosen == item["correct"]
        with st.expander(f"{'✅' if correct else '❌'} Pytanie {i + 1}: {'1 pkt' if correct else '0 pkt'}", expanded=not correct):
            st.write("**Pytanie:**", item["q"])
            st.write("**Twoja odpowiedź:**", item["options"][chosen])
            st.write("**Prawidłowa odpowiedź:**", item["options"][item["correct"]])
            st.write("**Wyjaśnienie:**", item["explanation"])
    if st.button("Rozpocznij quiz od nowa", type="secondary"):
        for i in range(len(QUESTIONS)):
            st.session_state.pop(f"answer_{i}", None)
        st.session_state.submitted = False
        st.session_state.saved_answers = {}
        st.rerun()
