import pandas as pd
import matplotlib.pyplot as plt

# 从文档中提取的评分数据
ratings = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,  # 最高评分Top10
           1.0, 1.0, 1.0, 1.0, 1.4, 1.6, 1.7, 1.7, 1.7, 1.7]  # 最低评分Top10

# 计算描述性统计
rating_series = pd.Series(ratings)
mean_val = rating_series.mean()
median_val = rating_series.median()
std_val = rating_series.std()
min_val = rating_series.min()
max_val = rating_series.max()

print('描述性统计结果:')
print(f'均值: {mean_val:.2f}')
print(f'中位数: {median_val:.2f}')
print(f'标准差: {std_val:.2f}')
print(f'最小值: {min_val:.2f}')
print(f'最大值: {max_val:.2f}')

# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.hist(ratings, bins=10, edgecolor='black', alpha=0.7)
plt.title('APP评分分布柱状图')
plt.xlabel('评分')
plt.ylabel('频率')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()