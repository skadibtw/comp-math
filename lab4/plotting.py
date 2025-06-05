import matplotlib.pyplot as plt
import numpy as np

def plot(x, y, plot_x, plot_ys, labels):
    """ Отрисовать графики полученных функций """
    plt.figure(figsize=(10, 6)) # Увеличим размер графика

    ax = plt.gca()
    # Настройка осей
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Стрелки на концах осей
    ax.plot(1, 0, marker=">", ms=5, color='k', transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k', transform=ax.get_xaxis_transform(), clip_on=False)

    # Исходные точки
    plt.plot(x, y, 'o', label='Исходные точки', markersize=5)

    # Аппроксимирующие функции
    colors = plt.cm.viridis(np.linspace(0, 1, len(plot_ys))) # Разные цвета для графиков
    for i in range(len(plot_ys)):
        # Проверка на NaN перед отрисовкой
        valid_indices = ~np.isnan(plot_ys[i]) & ~np.isinf(plot_ys[i]) # Добавим проверку на inf
        if np.any(valid_indices):
            plt.plot(plot_x[valid_indices], np.array(plot_ys[i])[valid_indices], label=labels[i], color=colors[i], linewidth=2)
        else:
             print(f"Предупреждение: Не удалось построить график для {labels[i]}, возможно все значения NaN или Inf.")

    plt.legend(loc='best') # Автоматический выбор лучшего места для легенды
    plt.grid(True, linestyle='--', alpha=0.6) # Сетка
    plt.title("Аппроксимация функций") # Заголовок графика
    plt.xlabel("X") # Подпись оси X
    plt.ylabel("Y") # Подпись оси Y

    # Установка пределов осей для лучшей видимости
    if len(x) > 0:
        x_margin = (np.max(x) - np.min(x)) * 0.1
        plt.xlim(np.min(x) - x_margin, np.max(x) + x_margin)
    if len(y) > 0:
        y_margin = (np.max(y) - np.min(y)) * 0.1
        # Учтем возможные NaN/Inf при расчете пределов y
        valid_y = y[~np.isnan(y) & ~np.isinf(y)]
        if len(valid_y) > 0:
             plt.ylim(np.min(valid_y) - y_margin, np.max(valid_y) + y_margin)


    plt.ion()

    plt.show(block=False) # Показать график
