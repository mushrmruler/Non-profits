# %%
import pandas as pd
import numpy as np
from scipy import stats

# %% [markdown]
# Этот модуль нужно будет подставить вместо того кода, который сейчас находится в проекте по адресу: /example/index/views/py. Начиная со строк `import pandas`, до `context={`

# %%
# Функция которая приравнивает два значения по доверительному интервалу 0.95
# Нужна чтобы у нас значения типа 2.84 и 2.83 были равны 
def Equals(value, comparison, confidence=0.95):
    mean, sigma = np.mean(comparison), np.std(comparison)
    conf_int = stats.norm.interval(confidence, loc=mean, scale=sigma/np.sqrt(len(comparison)))
    if (value >= conf_int[0]) & (value <= conf_int[1]):
        return True
    else:
        return False

# %%
# Функция для проверки на nan
def CheckNan(value, comparison):
    if (np.isnan(value)) or (np.isnan(comparison)):
        return True
    else:
        return False

# %%
df = pd.read_csv('/Users/denispavlenko/Downloads/HSE_DB.csv',decimal=",") # Нужно будет скачать выгрузку с данными в формате 1-5 и загрузить её себе

# %%
# У нас там в качестве уникаольного идентификатора стоит аксес-ключ, так что я использую его как индекс
# Это не суперудобно, поэтому его стоит или заменить или писать код умнее
df.set_index('ac',inplace=True)

# %%
# Оставляем только те варианты ответов, которые нас интересуют -- табличные
Table = df[['Направление', 
   'Q03_r1','Q03_r2','Q03_r3','Q03_r4','Q03_r5','Q03_r6',
   'Q07_r1','Q07_r2','Q07_r3','Q07_r4','Q07_r5',
   'Q09_r1','Q09_r2','Q09_r3','Q09_r4','Q09_r5',
   'Q12_r1','Q12_r2','Q12_r3','Q12_r4','Q12_r5','Q12_r6','Q12_r7','Q12_r8',
   'Q14_r1','Q14_r2','Q14_r3','Q14_r4','Q14_r5','Q14_r6', 'Q15original_for_index', 'Q14_15_mean',
   'Q18_r1','Q18_r2','Q18_r3',
   'Q20_r1','Q20_r2','Q20_r3',
   'Q22_r1','Q22_r2','Q22_r3','Q22_r4',
   'Q27_r1','Q27_r2','Q27_r3','Q27_r4',
   'Q28_r1','Q28_r2','Q28_r3','Q28_r4','Q28_r5','Q28_r6',
   'Q30_r1','Q30_r2','Q30_r3','Q30_r4','Q30_r5',
   'Q31_r1','Q31_r2','Q31_r3', 
   'FIN_mean', 'risk', 'openness','ocenka','OD_mean']]

# 999 (затруднились с ответом) и пустые значения заполняем как nan
Table = Table.fillna(999).replace(999,np.nan).replace('',np.nan)

# %%
# Собираем группы вопросов 
TableGroups = pd.DataFrame({'Стратегия и планирование':[['Q03_r1','Q03_r2','Q03_r3','Q03_r4','Q03_r5','Q03_r6']],
    'Управление организацией':[['Q07_r1','Q07_r2','Q07_r3','Q07_r4','Q07_r5']],
    'Организационная культура':[['Q09_r1','Q09_r2','Q09_r3','Q09_r4','Q09_r5']],
    'Проекты и мероприятия':[['Q12_r1','Q12_r2','Q12_r3','Q12_r4','Q12_r5','Q12_r6','Q12_r7','Q12_r8']],
    'Сотрудники':[['Q14_r1','Q14_r2','Q14_r3','Q14_r4','Q14_r5','Q14_r6']],
    'Волонтеры':[['Q18_r1','Q18_r2','Q18_r3']],
    'Финансовая устойчивость':[['Q20_r1','Q20_r2','Q20_r3','Q22_r1','Q22_r2','Q22_r3','Q22_r4','Q27_r1','Q27_r2','Q27_r3','Q27_r4']],
    'Внешние коммуникации':[['Q28_r1','Q28_r2','Q28_r3','Q28_r4','Q28_r5','Q28_r6','Q30_r1','Q30_r2','Q30_r3','Q30_r4','Q30_r5']],
    'Адвокация':[['Q31_r1','Q31_r2','Q31_r3']],
    'Открытость изменениям':[['Q09_r4', 'Q12_r4', 'Q12_r5', 'Q14_r4']],
    'Работа с рисками':[['Q03_r6', 'Q07_r2', 'Q09_r3', 'Q14_r6', 'Q15original_for_index', 'Q22_r1', 'Q22_r3', 'Q28_r4' ]], 
    'Оценка и мониторинг':[['Q03_r5', 'Q12_r6', 'Q12_r7', 'Q14_r5', 'Q18_r3', 'Q27_r4']]})

# %%
# Датафрейм, в котором содержатся направления НКО
Table_main = pd.DataFrame(Table['Направление'])

# %%
# Таблица со средними значениями по видам деятельности и по группам вопросам 
# (Таблица 1 в гугл доке)
for c in TableGroups.columns:
        Table_main[c] = Table[TableGroups[c][0]].mean(axis=1)

Table_main = Table_main.groupby(by='Направление').mean().round(2)
Table_main = Table_main.T

# %%
# Table_main.loc['Стратегия и планирование'].mean().round(2)
Table_main.mean(axis=1).round(2)

# %%
# Эта функция получает номер вопроса, номер аксес ключа организации 
# Опциально: округление(round в документе) и название вида деятельности 
class Search:
    def __init__(self, index, ac, activity = None, multiple=False):
        self.index = index
        self.ac = ac
        self.activity = activity
        self.multiple = multiple
    
        self.dataframe = Table 
        if self.activity != None: # Получаем название направления и фильтруем по нему
            self.dataframe = Table[Table['Направление'].str.contains(self.activity)]
        
        self.nonprofit =  self.dataframe.loc[ac,index]
        self.mean = self.dataframe.loc[:,index].mean().round(2)
        self.general = self.dataframe.loc[:,self.index]

        if self.multiple == True:
            self.dataframe = self.dataframe.loc[:,self.index]
            self.nonprofit =  round(self.dataframe.loc[self.ac,:].mean(),2)
            self.mean = round(self.dataframe.mean(axis=1).mean(), 2)
            self.general = round(self.dataframe.loc[:,self.index].mean(axis=1),2)

    def return_comparison(self, round=False, activity=None):
        if round == True: # Иногда нам нужно округлять сравниваемое значение до целого
          self.mean = self.mean.round()

        if CheckNan(self.nonprofit, self.mean):
            return ('nan')
        # Equals получает на вход столбец для подсчета доверительного интервала
        elif Equals(self.nonprofit, self.general):
            return ('equals')
        elif self.nonprofit > self.mean:
            return ('more')
        elif self.nonprofit < self.mean:
            return ('less')
    
    def return_value(self):
        return (self.nonprofit)

    def is_upper(self):
        if CheckNan(self.nonprofit, self.mean):
            return None
        if (self.nonprofit.round() >= 4) & (self.mean.round() >= 4):
            return True
        else:
            return False
    def is_lower(self):
        if CheckNan(self.nonprofit, self.mean):
            return None
        if (self.nonprofit.round() <= 3) & (self.mean.round() <= 3):
            return True
        else:
            return False

# %%
Table.loc[:,'OD_mean'].mean().round(2)

# %%
ac = 4
SearchResults = Search(['OD_mean','risk'],ac,multiple=True)
SearchResults.return_comparison() #SearchResults.return_value(), SearchResults.is_upper()

# %%
# Ответы на вопросы хранятся в этом классе
class Answer():
    def __init__(self,more,less,equals,nan):
        self.more = more
        self.less = less
        self.equals = equals
        self.nan = nan

    def answertext(self, state): #по какой-то причине питон не даёт мне назвать её через _ или с другой капитализацией :(
        match state:
            case 'nan':
                return self.nan
            case 'equals':
                return self.equals
            case 'more':
                return self.more
            case 'less':
                return self.less 

# %%
# Итоговая функция
# Нужно дополнить
def Get_text(search, answer):
    #SearchResults = Search(index, ac)
    return answer.answertext(search.return_comparison()).format(personal_value=search.return_value())

# %%
OD = Answer('Уровень организационного развития вашей НКО выше и составляет {personal_value}',
    'Уровень организационного развития вашей НКО ниже и составляет {personal_value}',
    'Уровень организационного развития вашей НКО сопоставимый и составляет {personal_value}',
    'На большую часть утверждений вы затруднились ответить. К сожалению, мы не смогли рассчитать значение уровня организационного развития вашей НКО.')

# %%
SearchResults = Search('OD_mean',4)
Get_text(SearchResults, OD)

# %%
# Функция проверяет содержит ли группа 
def Check_search(indexes,ac, state=None, is_upper=None):
    group = Table.loc[:,indexes]
    group_comparison = []
    for index in group:
        SearchResults = Search(index, ac)
        # Опциональная проверка на то, является ли НКО в "верху". 
        if is_upper == None:
            group_comparison.append(SearchResults.return_comparison())
        if is_upper == True:
            if SearchResults.is_upper() == True:
                group_comparison.append(SearchResults.return_comparison())
        if is_upper == False:
            if SearchResults.is_lower() == True:
                group_comparison.append(SearchResults.return_comparison())
    match state:
            case 'nan':
                if 'nan' in group_comparison:
                    return True
                else:
                    return False
            case 'equals':
                if 'equals' in group_comparison:
                    return True
                else:
                    return False
            case 'more':
                if 'more' in group_comparison:
                    return True
                else:
                    return False
            case 'less':
                if 'less' in group_comparison:
                    return True
                else:
                    return False 

# %%
Check_search(['OD_mean'],4,state='more',is_upper=True)

# %% [markdown]
# **Что делать дальше?**
# 
# 1. ~~Сделать обработку "Составляет ()"~~ готово. Сделано с помощью {} и формат
# 2. ~~Добавить Equals как проверку на доверительный интервал~~ Готово, сделал с помощью модуля scipy и 
# 3. *Создать lists с названиями параметров для того, чтобы по ним нарисовать график*
# 1. Перенести большую часть вопросов в класс вопросов
# 1. Добавить для Get_text доп функции для модификации ответа
# 4. ~~Расширить функцию Search на проверку значений группы вопросов~~ Готово, сделано с помощью Check_group
# 4. ~~Расширить функцию Search на обработку группы вопросов~~ Готово, сделано с помощью атрибута multiple в Search
# 4. ~~Расширить функцию Search на обработку значений, которые сравнивают значения персональные с общими, а их с 1,2,3 и 4,5~~ Готово, сделал с помощью проверки is_upper
# 5. Собрать всё это вместе


# %%

# Файл с
# Стуктура названий следующая <Тема на английском>_<Номер вопроса>

Risk = Answer('Показатель для вашей организации {personal_value}, что говорит о том, что ваша организация более устойчива к рискам.',
'Показатель для вашей организации {personal_value}, что говорит о том, что ваша организация менее устойчива к рискам.',
'У вашей организации сопоставимое значение данного показателя и составляет {personal_value}.',
'На большую часть вопросов вы затруднились ответить, к сожалению, мы не можем рассчитать для вас среднее значение по данному показателю.')

OD1 = Answer('Уровень организационного развития вашей НКО выше и составляет {personal_value}',
    'Уровень организационного развития вашей НКО ниже и составляет {personal_value}',
    'Уровень организационного развития вашей НКО сопоставимый и составляет {personal_value}',
    'На большую часть утверждений вы затруднилисответить. К сожалению, мы не смогли рассчитать значение уровня организационного развития вашей НКО.')

Strategy1 = Answer('Этот показатель выше у вашей организации и составляет {personal_value}.',
'Этот показатель ниже у вашей организации и составляет {personal_value}.',
'У вашей организации сопоставимое значение данного показателя и составляет {personal_value}}.',
'На большую часть вопросов вы затруднились ответить, к сожалению, мы не можем рассчитать для вас среднее значение по данному показателю.')