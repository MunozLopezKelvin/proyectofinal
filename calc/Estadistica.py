import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

class Estadistica:
    """
    Clase estadistica que se encarga de realizar diferentes
    calculos estadisticos sobre el proyecto de importacion
    """
    def __init__(self):
        self.df = pd.read_excel('info/importaciones.xlsx')
        self.recombrarDistritos()
        self.recombrarPaises()
    
    def datosExcel(self):
        """
        funcion que retorna el dataframe con los datos
        """
        return self.df

    def graficoDistritoDolares(self):
        """
        Funcion que retorna la grafica referente al pais que 
        se realizan las importaciones
        """
        img = io.BytesIO()

        distritos = self.df['DISTRITO'].unique()
        dolares = []
        for i in distritos:
            suma = self.df.loc[self.df['DISTRITO'] == i, ['CIF (DÓLARES)']].sum()[0]
            dolares.append(suma)

        plt.figure(figsize=(10,5))
        plt.bar(distritos, dolares)
        plt.title('Importación en dolares por distrito')
        plt.xticks(rotation=10)
        plt.ylabel('dolares (M)')
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficoFrecuenciaDistrito(self):
        """
        Funcion que retorna la grafica de la frecuenta de los distritos
        """
        img = io.BytesIO()

        x = self.df['DISTRITO']
        plt.figure(figsize=(10,5))
        plt.hist(x, bins=None)
        plt.title('Frecuencia de importaciones por distrito')
        plt.xticks(rotation=10)
        plt.ylabel('frecuencia')

        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url
        
    def graficoTop10Paises(self):
        """
        Funcion que devuelve un diccionario con los datos sobre los paises que
        se realizan importaciones
        """
        img = io.BytesIO()
        lista = []
        for i in self.df['PAÍS ORIGEN'].unique():
            importaciones = self.df[self.df['PAÍS ORIGEN'] == i]['PAÍS ORIGEN'].value_counts().tolist().pop()
            dolares = self.df[self.df['PAÍS ORIGEN'] == 'CO-COLOMBIA']['CIF (DÓLARES)'].sum()
            lista.append((i, importaciones, dolares))
        lista.sort(reverse=True, key=lambda item: item[1])

        paises = [i[0] for i in lista[0:11]]
        importaciones = [i[1] for i in lista[0:11]]
        plt.figure(figsize=(10,5))
        plt.bar(paises, importaciones)
        plt.ylabel('Importaciones')
        plt.title('Top 10 paises con más importaciones')
        plt.xticks(rotation=15)
        
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def recombrarDistritos(self):
        """
        Funcion para renombrar los datos del distrito
        Por ejemplo 002-MANTA pasar a MANTA
        """
        for i in self.df.index:
            temp = self.df.loc[i,'DISTRITO'].split('-')
            nombre = ' '.join([temp[j].strip(' ') for j in range(1,len(temp))])
            self.df.loc[i,'DISTRITO'] = nombre

    def recombrarPaises(self):
        """
        Funcion para renombrar los datos de los paises
        Por ejemplo CO-COLOMBIA pasar a COLOMBIA
        """
        for i in self.df.index:
            temp = self.df.loc[i,'PAÍS ORIGEN'].split('-')
            self.df.loc[i,'PAÍS ORIGEN'] = temp[1]
