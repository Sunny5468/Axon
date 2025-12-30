import pandas as pd
import matplotlib.pyplot as plt

# 假设数据文件为'bike_data.csv'，根据文档调整列名
df = pd.read_csv('bike_data.csv')

# 提取sale_price列并处理缺失值
sale_price = df['sale_price'].dropna()

# 计算描述性统计
statistics = {
    'mean': sale_price.mean(),
    'median': sale_price.median(),
    'std': sale_price.std(),
    'min': sale_price.min(),
    'max': sale_price.max()
}
print('Descriptive Statistics for Sale Price:')
print(statistics)

# 绘制直方图
plt.figure(figsize=(10, 6))
plt.hist(sale_price, bins=50, edgecolor='black', alpha=0.7)
plt.title('Distribution of Sale Price')
plt.xlabel('Sale Price')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()