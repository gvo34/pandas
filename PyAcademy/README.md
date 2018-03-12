
# Academy of Py Report


## Analysis

* Overall the district reading passing scores is at 100%.
* Students from Charter schools demonstrate higher overall scores rates than students from District type schools.
* School size shows an impact on the overall scores and passing percentage. Where smaller schools reported 100% math passing rate. The larger the school, the lower the overall passing rate.
* Funding per student is not directly proportional to the average test scores. On avererage passing rate did not increase with high budget per students. 

#### Retrieve data from raw CSV files for schools and students. Create data frames for each


```python
# Dependendencies
import pandas as pd
import os
```


```python
# Raw Schools data
raw_data_file_sch = "schools_complete.csv"
schools = os.path.join("raw_data",raw_data_file_sch)
```


```python
# get school data into a dataframe
sch_df = pd.read_csv(schools)
```


```python
# get number of schools
number_of_schools = sch_df['School ID'].count()
# get total budget
budget = sch_df['budget'].sum()
```


```python
# Raw Students data
raw_data_file_stu = "students_complete.csv"
students = os.path.join("raw_data",raw_data_file_stu)
```


```python
# get student data into a dataframe
stu_df = pd.read_csv(students)
```


```python
student_population = stu_df['Student ID'].count() 
# alternative: student_population = len(stu_df)
```


```python
# averages scores
r_avg = stu_df['reading_score'].mean()
m_avg = stu_df['math_score'].mean()

# passing grade must be >60
r_pass = stu_df.loc[stu_df['reading_score'] > 60,"reading_score"]
read_pass = r_pass.count()
m_pass = stu_df.loc[stu_df["math_score"] > 60,"math_score"]
math_pass = m_pass.count()
r_per = (read_pass/student_population)*100 
m_per = (math_pass/student_population)*100 
pass_rate = (r_per+m_per)/2

# put it all in a dictionay
district_df = pd.DataFrame({'Total Schools':[number_of_schools],
                            'Total Students':[student_population],
                            'Total Budget': ['${:,.2f}'.format(budget)],
                            'Average Math Score':[m_avg], 
                            'Average Reading Score':[r_avg],
                            '% Passing Math':['{:,.2f}%'.format(m_per)],
                            '% Passing Reading':['{:,.2f}%'.format(r_per)],
                            'Overall Passing Rate':['{:,.2f}%'.format(pass_rate)]                             
                            }
                          )
```

## District Summary


```python
# reorder columns
order_district = ['Total Schools','Total Students','Total Budget','Average Reading Score','% Passing Reading','Average Math Score','% Passing Math','Overall Passing Rate']
```


```python
district_df = district_df[order_district]
district_df
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
      <th>Total Schools</th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Average Reading Score</th>
      <th>% Passing Reading</th>
      <th>Average Math Score</th>
      <th>% Passing Math</th>
      <th>Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15</td>
      <td>39170</td>
      <td>$24,649,428.00</td>
      <td>81.87784</td>
      <td>100.00%</td>
      <td>78.985371</td>
      <td>90.91%</td>
      <td>95.45%</td>
    </tr>
  </tbody>
</table>
</div>




```python
# aggregate Schools and Students data into one dataframe
sch_df = sch_df.rename(columns={'name':'school'})
sch_stu_df = pd.merge(sch_df,stu_df,on='school',how='outer')
```


```python
#Students by Schools
bySchool = sch_stu_df.groupby('school')
students_sch = bySchool['Student ID'].count()

#Budget by school
school_budget = bySchool['budget'].unique().astype(int)
school_budget_ft = school_budget.map('${:,.2f}'.format)
budget_per_stu = school_budget/students_sch
budget_per_stu_ft = budget_per_stu.map('${:,.2f}'.format)

#Score averages by School
math_avg = bySchool['math_score'].mean()
read_avg = bySchool['reading_score'].mean()

#School type
school_type = bySchool['type'].unique()
school_type = school_type.map("%s".join)
```


```python
#Math pass percentage
mathpass = sch_stu_df.loc[sch_stu_df['math_score']>60]
mathpass_sch = mathpass['school'].value_counts()
mathpercentage = (mathpass_sch/students_sch)*100

#Reading pass percentage
readpass = sch_stu_df.loc[sch_stu_df['reading_score']>60]
readpass_sch = readpass['school'].value_counts()
readpercentage = (readpass_sch/students_sch)*100

#Overall passing rate
pass_rate = (readpercentage+mathpercentage)/2

#Collect all together
school_dict = {'type':school_type,
               'students':students_sch,
               'budget':school_budget_ft,
               'per student budget':budget_per_stu_ft,
               'Average Math Score':math_avg,
               'Average Reading Score': read_avg,
               '% passing Math':mathpercentage,
               '% passing Reading':readpercentage,
               'Overall passing':pass_rate
              }
schools_df = pd.DataFrame(school_dict)
```

## School Summary


```python
order_schools = ['type','students','budget','per student budget','Average Reading Score', '% passing Reading','Average Math Score','% passing Math','Overall passing']
schools_df = schools_df[order_schools]
schools_df
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
      <th>type</th>
      <th>students</th>
      <th>budget</th>
      <th>per student budget</th>
      <th>Average Reading Score</th>
      <th>% passing Reading</th>
      <th>Average Math Score</th>
      <th>% passing Math</th>
      <th>Overall passing</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
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
      <th>Bailey High School</th>
      <td>District</td>
      <td>4976</td>
      <td>$3,124,928.00</td>
      <td>$628.00</td>
      <td>81.033963</td>
      <td>100.0</td>
      <td>77.048432</td>
      <td>87.439711</td>
      <td>93.719855</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>$1,081,356.00</td>
      <td>$582.00</td>
      <td>83.975780</td>
      <td>100.0</td>
      <td>83.061895</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>$1,884,411.00</td>
      <td>$639.00</td>
      <td>81.158020</td>
      <td>100.0</td>
      <td>76.711767</td>
      <td>86.436080</td>
      <td>93.218040</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>2739</td>
      <td>$1,763,916.00</td>
      <td>$644.00</td>
      <td>80.746258</td>
      <td>100.0</td>
      <td>77.102592</td>
      <td>87.221614</td>
      <td>93.610807</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1468</td>
      <td>$917,500.00</td>
      <td>$625.00</td>
      <td>83.816757</td>
      <td>100.0</td>
      <td>83.351499</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>4635</td>
      <td>$3,022,020.00</td>
      <td>$652.00</td>
      <td>80.934412</td>
      <td>100.0</td>
      <td>77.289752</td>
      <td>86.450917</td>
      <td>93.225458</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>$248,087.00</td>
      <td>$581.00</td>
      <td>83.814988</td>
      <td>100.0</td>
      <td>83.803279</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>$1,910,635.00</td>
      <td>$655.00</td>
      <td>81.182722</td>
      <td>100.0</td>
      <td>76.629414</td>
      <td>86.835790</td>
      <td>93.417895</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>$3,094,650.00</td>
      <td>$650.00</td>
      <td>80.966394</td>
      <td>100.0</td>
      <td>77.072464</td>
      <td>86.704474</td>
      <td>93.352237</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>$585,858.00</td>
      <td>$609.00</td>
      <td>84.044699</td>
      <td>100.0</td>
      <td>83.839917</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3999</td>
      <td>$2,547,363.00</td>
      <td>$637.00</td>
      <td>80.744686</td>
      <td>100.0</td>
      <td>76.842711</td>
      <td>86.446612</td>
      <td>93.223306</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1761</td>
      <td>$1,056,600.00</td>
      <td>$600.00</td>
      <td>83.725724</td>
      <td>100.0</td>
      <td>83.359455</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>Charter</td>
      <td>1635</td>
      <td>$1,043,130.00</td>
      <td>$638.00</td>
      <td>83.848930</td>
      <td>100.0</td>
      <td>83.418349</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>2283</td>
      <td>$1,319,574.00</td>
      <td>$578.00</td>
      <td>83.989488</td>
      <td>100.0</td>
      <td>83.274201</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>Charter</td>
      <td>1800</td>
      <td>$1,049,400.00</td>
      <td>$583.00</td>
      <td>83.955000</td>
      <td>100.0</td>
      <td>83.682222</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
  </tbody>
</table>
</div>



### Top 5 Performing Schools (By Passing Rate)


```python
top_5 = schools_df.sort_values(by='Overall passing', ascending=False)[:5]
top_5
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
      <th>type</th>
      <th>students</th>
      <th>budget</th>
      <th>per student budget</th>
      <th>Average Reading Score</th>
      <th>% passing Reading</th>
      <th>Average Math Score</th>
      <th>% passing Math</th>
      <th>Overall passing</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
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
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>$1,081,356.00</td>
      <td>$582.00</td>
      <td>83.975780</td>
      <td>100.0</td>
      <td>83.061895</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1468</td>
      <td>$917,500.00</td>
      <td>$625.00</td>
      <td>83.816757</td>
      <td>100.0</td>
      <td>83.351499</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>$248,087.00</td>
      <td>$581.00</td>
      <td>83.814988</td>
      <td>100.0</td>
      <td>83.803279</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>$585,858.00</td>
      <td>$609.00</td>
      <td>84.044699</td>
      <td>100.0</td>
      <td>83.839917</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1761</td>
      <td>$1,056,600.00</td>
      <td>$600.00</td>
      <td>83.725724</td>
      <td>100.0</td>
      <td>83.359455</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
  </tbody>
</table>
</div>



### Bottom 5 Performing Schools (By Passing Rate)


```python
bottom_5 = schools_df.sort_values(by='Overall passing', ascending=True)[:5]
bottom_5
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
      <th>type</th>
      <th>students</th>
      <th>budget</th>
      <th>per student budget</th>
      <th>Average Reading Score</th>
      <th>% passing Reading</th>
      <th>Average Math Score</th>
      <th>% passing Math</th>
      <th>Overall passing</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
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
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>$1,884,411.00</td>
      <td>$639.00</td>
      <td>81.158020</td>
      <td>100.0</td>
      <td>76.711767</td>
      <td>86.436080</td>
      <td>93.218040</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3999</td>
      <td>$2,547,363.00</td>
      <td>$637.00</td>
      <td>80.744686</td>
      <td>100.0</td>
      <td>76.842711</td>
      <td>86.446612</td>
      <td>93.223306</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>4635</td>
      <td>$3,022,020.00</td>
      <td>$652.00</td>
      <td>80.934412</td>
      <td>100.0</td>
      <td>77.289752</td>
      <td>86.450917</td>
      <td>93.225458</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>$3,094,650.00</td>
      <td>$650.00</td>
      <td>80.966394</td>
      <td>100.0</td>
      <td>77.072464</td>
      <td>86.704474</td>
      <td>93.352237</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>$1,910,635.00</td>
      <td>$655.00</td>
      <td>81.182722</td>
      <td>100.0</td>
      <td>76.629414</td>
      <td>86.835790</td>
      <td>93.417895</td>
    </tr>
  </tbody>
</table>
</div>



### Math Scores by Grade


```python
# group by school and grade to obtain the math average
byGrade = sch_stu_df.groupby(['school','grade'])
bySchool_math_df = pd.DataFrame(byGrade['math_score'].mean().unstack())
reorder_grades = ['9th','10th','11th','12th']
bySchool_math_df = bySchool_math_df[reorder_grades]
bySchool_math_df
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
      <th>grade</th>
      <th>9th</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>77.083676</td>
      <td>76.996772</td>
      <td>77.515588</td>
      <td>76.492218</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>83.094697</td>
      <td>83.154506</td>
      <td>82.765560</td>
      <td>83.277487</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>76.403037</td>
      <td>76.539974</td>
      <td>76.884344</td>
      <td>77.151369</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>77.361345</td>
      <td>77.672316</td>
      <td>76.918058</td>
      <td>76.179963</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>82.044010</td>
      <td>84.229064</td>
      <td>83.842105</td>
      <td>83.356164</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>77.438495</td>
      <td>77.337408</td>
      <td>77.136029</td>
      <td>77.186567</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>83.787402</td>
      <td>83.429825</td>
      <td>85.000000</td>
      <td>82.855422</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>77.027251</td>
      <td>75.908735</td>
      <td>76.446602</td>
      <td>77.225641</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>77.187857</td>
      <td>76.691117</td>
      <td>77.491653</td>
      <td>76.863248</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>83.625455</td>
      <td>83.372000</td>
      <td>84.328125</td>
      <td>84.121547</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>76.859966</td>
      <td>76.612500</td>
      <td>76.395626</td>
      <td>77.690748</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>83.420755</td>
      <td>82.917411</td>
      <td>83.383495</td>
      <td>83.778976</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>83.590022</td>
      <td>83.087886</td>
      <td>83.498795</td>
      <td>83.497041</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>83.085578</td>
      <td>83.724422</td>
      <td>83.195326</td>
      <td>83.035794</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>83.264706</td>
      <td>84.010288</td>
      <td>83.836782</td>
      <td>83.644986</td>
    </tr>
  </tbody>
</table>
</div>



### Reading Scores by Grade


```python
# groups by school and grade to obtain the reading average
bySchool_reading_df = pd.DataFrame(byGrade['reading_score'].mean().unstack())
bySchool_reading_df = bySchool_reading_df[reorder_grades]
bySchool_reading_df
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
      <th>grade</th>
      <th>9th</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>81.303155</td>
      <td>80.907183</td>
      <td>80.945643</td>
      <td>80.912451</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>83.676136</td>
      <td>84.253219</td>
      <td>83.788382</td>
      <td>84.287958</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>81.198598</td>
      <td>81.408912</td>
      <td>80.640339</td>
      <td>81.384863</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>80.632653</td>
      <td>81.262712</td>
      <td>80.403642</td>
      <td>80.662338</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>83.369193</td>
      <td>83.706897</td>
      <td>84.288089</td>
      <td>84.013699</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>80.866860</td>
      <td>80.660147</td>
      <td>81.396140</td>
      <td>80.857143</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>83.677165</td>
      <td>83.324561</td>
      <td>83.815534</td>
      <td>84.698795</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>81.290284</td>
      <td>81.512386</td>
      <td>81.417476</td>
      <td>80.305983</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>81.260714</td>
      <td>80.773431</td>
      <td>80.616027</td>
      <td>81.227564</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>83.807273</td>
      <td>83.612000</td>
      <td>84.335938</td>
      <td>84.591160</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>80.993127</td>
      <td>80.629808</td>
      <td>80.864811</td>
      <td>80.376426</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>84.122642</td>
      <td>83.441964</td>
      <td>84.373786</td>
      <td>82.781671</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>83.728850</td>
      <td>84.254157</td>
      <td>83.585542</td>
      <td>83.831361</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>83.939778</td>
      <td>84.021452</td>
      <td>83.764608</td>
      <td>84.317673</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>83.833333</td>
      <td>83.812757</td>
      <td>84.156322</td>
      <td>84.073171</td>
    </tr>
  </tbody>
</table>
</div>



### Scores by School Spending


```python
schools_df['per student budget'] = budget_per_stu
topspend = schools_df['per student budget'].max()
bottomspend = schools_df['per student budget'].min()
bottomspend = budget_per_stu.min()

t2 = (topspend - bottomspend)/4
spending = [0, bottomspend + t2, bottomspend+(2*t2), bottomspend+(3*t2), topspend]
spending_labels = ['<$598','$598-616','$616-635','>$635']

school_spending = pd.cut(schools_df['per student budget'], spending, labels=spending_labels)
scores_dict = {"Spending":school_spending,
                 'Overall passing rate':pass_rate,
                "Average Math Score":math_avg,
                "Average Reading Score":read_avg,
                "% passing math":mathpercentage,
                "% passing read":readpercentage}
spending_df = pd.DataFrame(scores_dict)
reorder_scores = ['Spending','Overall passing rate','Average Reading Score','% passing read','Average Math Score','% passing math']
spending_df = spending_df[reorder_columns]
spending_df.groupby('Spending').mean()
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
      <th>Overall passing rate</th>
      <th>Average Reading Score</th>
      <th>% passing read</th>
      <th>Average Math Score</th>
      <th>% passing math</th>
    </tr>
    <tr>
      <th>Spending</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;$598</th>
      <td>100.000000</td>
      <td>83.933814</td>
      <td>100.0</td>
      <td>83.455399</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>$598-616</th>
      <td>100.000000</td>
      <td>83.885211</td>
      <td>100.0</td>
      <td>83.599686</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>$616-635</th>
      <td>96.859928</td>
      <td>82.425360</td>
      <td>100.0</td>
      <td>80.199966</td>
      <td>93.719855</td>
    </tr>
    <tr>
      <th>&gt;$635</th>
      <td>94.292535</td>
      <td>81.368774</td>
      <td>100.0</td>
      <td>77.866721</td>
      <td>88.585069</td>
    </tr>
  </tbody>
</table>
</div>



## Scores by School Size


```python
sch_size = [0,1500,3000,5000]
name_size = ['Small(<1500)', 'Medium(1500-3000)','Large(3000-5000)']
school_size = pd.cut(schools_df['students'],sch_size, labels=name_size)
scores_dict['Size'] = school_size
reorder_scores[0]='Size'
size_df = pd.DataFrame(scores_dict)
size_df = size_df[reorder_scores]
size_df.groupby("Size").mean()
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
      <th>Overall passing rate</th>
      <th>Average Reading Score</th>
      <th>% passing read</th>
      <th>Average Math Score</th>
      <th>% passing math</th>
    </tr>
    <tr>
      <th>Size</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Small(&lt;1500)</th>
      <td>100.000000</td>
      <td>83.892148</td>
      <td>100.0</td>
      <td>83.664898</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>Medium(1500-3000)</th>
      <td>97.530843</td>
      <td>82.822740</td>
      <td>100.0</td>
      <td>80.904987</td>
      <td>95.061685</td>
    </tr>
    <tr>
      <th>Large(3000-5000)</th>
      <td>93.380214</td>
      <td>80.919864</td>
      <td>100.0</td>
      <td>77.063340</td>
      <td>86.760428</td>
    </tr>
  </tbody>
</table>
</div>



## Scores by School Type


```python
scores_dict['type']=school_type
reorder_scores[0]='type'
type_df = pd.DataFrame(scores_dict)
type_df = type_df[reorder_scores]
type_df.groupby('type').mean()
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
      <th>Overall passing rate</th>
      <th>Average Reading Score</th>
      <th>% passing read</th>
      <th>Average Math Score</th>
      <th>% passing math</th>
    </tr>
    <tr>
      <th>type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>100.000000</td>
      <td>83.896421</td>
      <td>100.0</td>
      <td>83.473852</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>District</th>
      <td>93.395371</td>
      <td>80.966636</td>
      <td>100.0</td>
      <td>76.956733</td>
      <td>86.790742</td>
    </tr>
  </tbody>
</table>
</div>


