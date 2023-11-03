import pandas as pd
import matplotlib.pyplot as plt
import os
import sys


months = sys.argv[1:]


def plot_info(df, value, index, agg, ylabel, xlabel, opcao=None):
    if opcao == None:
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=agg).plot(figsize=(15, 6))
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=agg).unstack().plot(figsize=(15, 6))
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=agg).sort_values(
            value).plot(figsize=(15, 6))

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    return None


for month in months:
    for s in os.listdir('./input'):
        if s.split('.')[0].endswith(month) == True:

            df = pd.read_csv('./input/' + s)

            os.makedirs('./output/figs/' + df.DTNASC.max(), exist_ok=True)

            day = df.DTNASC.max()[:7]

            plot_info(df, 'IDADEMAE', 'DTNASC', 'mean',
                      'Data nascimento', 'Idade média mãe')
            plt.savefig('./output/figs/' + df.DTNASC.max() +
                        '/Idade média mãe por nascimento.png')

            plot_info(df, 'PESO', 'IDADEMAE', 'mean',
                      'Peso', 'Idade média mãe')
            plt.savefig('./output/figs/' + df.DTNASC.max() +
                        '/Peso médio por idade mãe.png')

            plot_info(df, 'IDADEMAE', 'ESCMAE', 'count',
                      'Idade mãe', 'Escolaridade')
            plt.savefig('./output/figs/' + df.DTNASC.max() +
                        '/Escolaridade por idade mãe.png')

            plot_info(df, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean',
                      'Idade média mãe', 'Data nascimento', 'unstack')
            plt.savefig('./output/figs/' + df.DTNASC.max() +
                        '/Idade média mãe por data de nascimento para cada sexo.png')

            plot_info(df, 'IDADEPAI', ['DTNASC', 'SEXO'], 'mean',
                      'Idade média mãe', 'Data nascimento', 'unstack')
            plt.savefig('./output/figs/' + df.DTNASC.max() +
                        '/Idade média pai por data de nascimento para cada sexo.png')

            plt.close()

            print(day)
