import streamlit as st
import numpy as np
import pandas as pd

# Попробуем импортировать seaborn и matplotlib, но если их нет, программа не сломается
try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    SEABORN_AVAILABLE = True
except ModuleNotFoundError:
    SEABORN_AVAILABLE = False

# Настройки страницы
st.set_page_config(page_title="ASDAS & BASDAI Калькулятор", layout="centered")

# Заголовок
st.title("Калькулятор активности заболевания (ASDAS & BASDAI)")

# Ввод значений от врача
asdai = st.number_input("Введите значение ASDAS (от врача):", min_value=0.0, max_value=10.0, step=0.1)
basdai = st.number_input("Введите значение BASDAI (от врача):", min_value=0.0, max_value=10.0, step=0.1)

# Функция для определения уровня активности
def get_activity_level(asdai, basdai):
    if asdai < 1.3 and basdai < 4:
        return "🟢 Низкая активность (рекомендуется наблюдение)"
    elif 1.3 <= asdai < 2.1 or 4 <= basdai < 6:
        return "🟡 Умеренная активность (возможен пересмотр терапии)"
    else:
        return "🔴 Высокая активность (рекомендуется консультация ревматолога)"

# Кнопка для расчёта
if st.button("Рассчитать"):
    result = get_activity_level(asdai, basdai)
    st.subheader("Результат:")
    st.write(result)

    # Визуализация шкалы активности, если seaborn доступен
    if SEABORN_AVAILABLE:
        fig, ax = plt.subplots(figsize=(6, 1))
        cmap = sns.color_palette(["green", "yellow", "red"])
        activity_index = np.clip((asdai + basdai) / 2 / 10, 0, 1)  # нормируем в диапазон 0-1
        sns.heatmap([[activity_index]], cmap=cmap, annot=False, cbar=False, ax=ax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Шкала активности", fontsize=12)
        st.pyplot(fig)
    else:
        st.warning("⚠️ Библиотека seaborn не установлена, график не отображается.")

# Информация о шкалах
st.markdown("""
### 📝 Оценка активности
- **ASDAS < 1.3 и BASDAI < 4** → Низкая активность ✅  
- **ASDAS 1.3-2.1 или BASDAI 4-6** → Умеренная активность ⚠️  
- **ASDAS > 2.1 или BASDAI > 6** → Высокая активность ❗  

### 📌 Рекомендации:
- **Низкая активность** → наблюдение каждые 6 месяцев  
- **Умеренная активность** → возможен пересмотр терапии  
- **Высокая активность** → необходимо усиление терапии и консультация специалиста  
""")
