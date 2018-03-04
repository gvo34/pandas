
# Heroes


```python
import pandas as pd
import os
```


```python
filename = os.path.join('raw_data','purchase_data.json')
#filename = os.path.join('raw_data','purchase_data2.json')
```


```python
purchases = pd.read_json(filename)
```

### Player count


```python
total_players = purchases['SN'].nunique()
total_players
```




    573



### Purchasing Analysis (Total)



```python
items = len(purchases['Item Name'].unique())
```


```python
average_price = purchases['Price'].mean()
average_price = "${:,.2f}".format(average_price)
```


```python
total_revenue = purchases['Price'].sum()
total_revenue = "${:,.2f}".format(total_revenue)
```


```python
total_purchases = len(purchases)
items = purchases[['Item ID','Item Name','Price']]
items = items.sort_values(by='Item ID')
items = items.drop_duplicates()
items = items['Item ID'].count()
```


```python
purchases_dict = {'Number of Unique Items':[items],
                  'Average Purchase Price': [average_price],
                  'Total Number of Purchases':[total_purchases],
                  'Total Revenue':[total_revenue]
                 }
purchases_df = pd.DataFrame(purchases_dict)
purchases_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Number of Unique Items</th>
      <th>Total Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>$2.93</td>
      <td>183</td>
      <td>780</td>
      <td>$2,286.33</td>
    </tr>
  </tbody>
</table>
</div>



### Gender Demographics

Percentage and Count of Male Players
Percentage and Count of Female Players
Percentage and Count of Other / Non-Disclosed


```python
byGender = purchases.groupby('Gender')
```


```python
dem = pd.DataFrame(byGender['SN'].nunique())
```


```python
dem['percentage'] = dem['SN'].divide(total_players)
dem['percentage'] = dem['percentage'].multiply(100)
dem['percentage'] = dem['percentage'].map("{:,.2f}%".format)
```


```python
dem
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SN</th>
      <th>percentage</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>100</td>
      <td>17.45%</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>465</td>
      <td>81.15%</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>8</td>
      <td>1.40%</td>
    </tr>
  </tbody>
</table>
</div>



### Purchasing Analysis (Gender)



```python
purchase_count = byGender['SN'].count()
average_purchase_price = byGender['Price'].mean()
total_purchase_value = byGender['Price'].sum()
normalized_total = total_purchase_value / purchase_count
```


```python
dem['purchase count'] = purchase_count
dem['average purchase'] = average_purchase_price.map("${:,.2f}".format)
dem['total purchase'] = total_purchase_value.map("${:,.2f}".format)
dem['Normalized total'] = normalized_total.map("${:,.2f}".format)
dem
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SN</th>
      <th>percentage</th>
      <th>purchase count</th>
      <th>average purchase</th>
      <th>total purchase</th>
      <th>Normalized total</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>100</td>
      <td>17.45%</td>
      <td>136</td>
      <td>$2.82</td>
      <td>$382.91</td>
      <td>$2.82</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>465</td>
      <td>81.15%</td>
      <td>633</td>
      <td>$2.95</td>
      <td>$1,867.68</td>
      <td>$2.95</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>8</td>
      <td>1.40%</td>
      <td>11</td>
      <td>$3.25</td>
      <td>$35.74</td>
      <td>$3.25</td>
    </tr>
  </tbody>
</table>
</div>



### Age Demographics


```python
ages = [0,10,14,19,24,29,34,100]
age_buckets = ['<10','10-14','15-19','20-24','25-29','30-35','>35']

purchase_age = pd.cut(purchases['Age'],bins=ages,labels=age_buckets)
purchases['Age Group'] = purchase_age
byAge = purchases.groupby('Age Group')
age_purchase_count = byAge['Age Group'].count()
age_average_purchase_price = byAge['Price'].mean()
age_total_purchase_value = byAge['Price'].sum()
age_normalized_total = age_total_purchase_value / age_purchase_count
age_demog_df = pd.DataFrame({'Purchase Count':age_purchase_count,
                            'Average Purchase Price':age_average_purchase_price.map("${:,.2f}".format),
                            'Total Purchase Value':age_total_purchase_value.map("${:,.2f}".format),
                            'Normalized totals':age_normalized_total.map("${:,.2f}".format)})
```


```python
age_demog_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Normalized totals</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Age Group</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>$3.02</td>
      <td>$3.02</td>
      <td>32</td>
      <td>$96.62</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>$2.70</td>
      <td>$2.70</td>
      <td>31</td>
      <td>$83.79</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>$2.91</td>
      <td>$2.91</td>
      <td>133</td>
      <td>$386.42</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>$2.91</td>
      <td>$2.91</td>
      <td>336</td>
      <td>$978.77</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>$2.96</td>
      <td>$2.96</td>
      <td>125</td>
      <td>$370.33</td>
    </tr>
    <tr>
      <th>30-35</th>
      <td>$3.08</td>
      <td>$3.08</td>
      <td>64</td>
      <td>$197.25</td>
    </tr>
    <tr>
      <th>&gt;35</th>
      <td>$2.93</td>
      <td>$2.93</td>
      <td>59</td>
      <td>$173.15</td>
    </tr>
  </tbody>
</table>
</div>



# Top Spenders


```python

byName = purchases.groupby('SN')
total_spend = byName['Price'].sum()
purchase_count =byName['Price'].count()
average_price = byName['Price'].mean()

top_spend = pd.DataFrame({'Total Purchase Value':total_spend,
                             'Purchase Count':purchase_count,
                             'Average Purchase Price':average_price})

top_spend = top_spend.sort_values(by='Total Purchase Value', ascending=False)[:5]
top_spend['Total Purchase Value'] = top_spend['Total Purchase Value'].map("${:,.2f}".format)
top_spend['Average Purchase Price'] = top_spend['Average Purchase Price'].map("${:,.2f}".format)
```


```python
top_spend
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Purchase Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Undirrala66</th>
      <td>$3.41</td>
      <td>5</td>
      <td>$17.06</td>
    </tr>
    <tr>
      <th>Saedue76</th>
      <td>$3.39</td>
      <td>4</td>
      <td>$13.56</td>
    </tr>
    <tr>
      <th>Mindimnya67</th>
      <td>$3.18</td>
      <td>4</td>
      <td>$12.74</td>
    </tr>
    <tr>
      <th>Haellysu29</th>
      <td>$4.24</td>
      <td>3</td>
      <td>$12.73</td>
    </tr>
    <tr>
      <th>Eoda93</th>
      <td>$3.86</td>
      <td>3</td>
      <td>$11.58</td>
    </tr>
  </tbody>
</table>
</div>



### Most Popular Items


```python
byItem = purchases.groupby('Item ID')
item_name = byItem['Item Name'].unique()
item_name = item_name.map("%s".join)
item_price = byItem['Price'].unique()
total_spend = byItem['Price'].sum()
purchase_count =byItem['Price'].count()
average_price = byItem['Price'].mean()

popular_dict = pd.DataFrame({'Total Purchase Value':total_spend,
                             'Purchase Count':purchase_count,
                             'Item Name':item_name,
                             'Item Price':item_price
                             })

popular_df = pd.DataFrame(popular_dict)
popular_item = popular_df.sort_values(by='Purchase Count', ascending=False)[:5]


popular_item['Total Purchase Value']= popular_item['Total Purchase Value'].map("${:,.2f}".format)
popular_item['Item Price'] = popular_item['Item Price'].astype(float).map("${:,.2f}".format)
popular_item

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item Name</th>
      <th>Item Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>39</th>
      <td>Betrayal, Whisper of Grieving Widows</td>
      <td>$2.35</td>
      <td>11</td>
      <td>$25.85</td>
    </tr>
    <tr>
      <th>84</th>
      <td>Arcane Gem</td>
      <td>$2.23</td>
      <td>11</td>
      <td>$24.53</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Trickster</td>
      <td>$2.07</td>
      <td>9</td>
      <td>$18.63</td>
    </tr>
    <tr>
      <th>175</th>
      <td>Woeful Adamantite Claymore</td>
      <td>$1.24</td>
      <td>9</td>
      <td>$11.16</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Serenity</td>
      <td>$1.49</td>
      <td>9</td>
      <td>$13.41</td>
    </tr>
  </tbody>
</table>
</div>



### Most Profitable Items


```python
profitable_dict = pd.DataFrame({'Total Purchase Value':total_spend,
                             'Purchase Count':purchase_count,
                             'Item Name':item_name,
                             'Item Price':item_price.astype(float).map("${:,.2f}".format)
                             })
profitable_df = pd.DataFrame(profitable_dict)
profitable = profitable_df.sort_values(by='Total Purchase Value',ascending=False)[:5]

profitable['Total Purchase Value'] = profitable['Total Purchase Value'].map("${:,.2f}".format)
```


```python
profitable
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item Name</th>
      <th>Item Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>34</th>
      <td>Retribution Axe</td>
      <td>$4.14</td>
      <td>9</td>
      <td>$37.26</td>
    </tr>
    <tr>
      <th>115</th>
      <td>Spectral Diamond Doomblade</td>
      <td>$4.25</td>
      <td>7</td>
      <td>$29.75</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Orenmir</td>
      <td>$4.95</td>
      <td>6</td>
      <td>$29.70</td>
    </tr>
    <tr>
      <th>103</th>
      <td>Singed Scalpel</td>
      <td>$4.87</td>
      <td>6</td>
      <td>$29.22</td>
    </tr>
    <tr>
      <th>107</th>
      <td>Splitter, Foe Of Subtlety</td>
      <td>$3.61</td>
      <td>8</td>
      <td>$28.88</td>
    </tr>
  </tbody>
</table>
</div>


