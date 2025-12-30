import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 从对话中提取的数值数据
data = [3, 3, 5, 4, 6, 4, 2, 3, 2, 4, 4, 4, 1, 8, 35, 13]

# 创建pandas Series以便分析
series = pd.Series(data)

# 计算描述性统计
statistics = {
    'mean': series.mean(),
    'median': series.median(),
    'std': series.std(ddof=1),  # 样本标准差
    'min': series.min(),
    'max': series.max()
}

print('描述性统计:')
for key, value in statistics.items():
    print(f'{key}: {value:.4f}' if isinstance(value, float) else f'{key}: {value}')

# 绘制直方图展示数据分布
plt.figure(figsize=(10, 6))
plt.hist(series, bins=10, edgecolor='black', alpha=0.7, color='skyblue')
plt.title('对话中数值数据的分布直方图')
plt.xlabel('数值')
plt.ylabel('频数')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()