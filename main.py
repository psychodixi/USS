import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")


st.markdown(
    """
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

with st.container():
    image_url = "https://i.redd.it/36sr31w5cqud1.gif"
    st.markdown(
        f"""
        <style>
        .header {{
            background-image: url('{image_url}');
            background-size: 100%;
            background-position: center;
            height: 500px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="header"></p>', unsafe_allow_html=True)



#st.title("PokeApiDex")
st.markdown(
    '''
    <h1 style="text-align: center;">PokeApiDex</h1>
    ''',
    unsafe_allow_html=True
)


st.header("Bienvenid@ a nuestra Pokedex Fan Made", divider="violet")
st.write("En nuestra API, podras consultar datos de Pokémon específicos, tales como: Sus habilidades, Estadisticas bases, Tipos, Generaciones y sus Sprites del videojuego. \n")
st.write("También podrás ver en gráficos detallados comparaciones entre estadísticas de los tipos de Pokémon, la distribución segun sus tipos, Promedios de estadísticas para comparar los niveles de poder de los tipos de Pokémon")
st.write("y ver todos los Pokémon únicos de cada generación")
url_imagen = "https://pokemon-project.com/pokedex/img/sprite/Home/256/132.png"
st.markdown(f"Recuerda ingresar bien los datos! ![Imagen]({url_imagen})")

st.divider()

st.html(
    '''
    <style>
    hr {
        border-color: indigo;
    }
    </style>
    '''
)


st.logo("https://www.pngplay.com/wp-content/uploads/2/Pokeball-PNG-Photo-Image.png", size="large")

nombre_poke = st.text_input("Ingrese el nombre del Pokémon: ")

def obtener_pokemon(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}/"
    res = requests.get(url)

    if res.status_code == 200:
        return res.json()
    else:
        st.error("Pokémon no encontrado o error en la API.")
        return None

if st.button("Habilidades"):
    datos_poke = obtener_pokemon(nombre_poke)
    if datos_poke:
        habilidades = datos_poke['abilities']
        habilidades_list = [habilidad['ability']['name'] for habilidad in habilidades]
        st.write("Habilidades:")
        for habilidad in habilidades_list:
            st.write(f"- {habilidad}")

if st.button("Estadisticas"):
    datos_poke = obtener_pokemon(nombre_poke)
    if datos_poke:
        Estadisticas = datos_poke['stats']
        st.write("Estadísticas:")
        for Estadistica in Estadisticas:
            stat_name = Estadistica['stat']['name']
            base_stat = Estadistica['base_stat']
            st.write(f"- {stat_name}: {base_stat}")

if st.button("Tipo"):
    datos_poke = obtener_pokemon(nombre_poke)
    if datos_poke:
        Tipos = datos_poke["types"]
        Tipos_list = [Tipo["type"]["name"] for Tipo in Tipos]
        st.write("Tipos:")
        for tipo in Tipos_list:
            st.write(f"- {tipo}")

if st.button("Altura y Peso"):
    datos_poke = obtener_pokemon(nombre_poke)
    if datos_poke:
        Altura = datos_poke["height"]
        Peso = datos_poke["weight"]
        st.write("Altura:", f"{round(Altura * 3.048,1)} cm")
        st.write("Peso:", f"{round(Peso * 0.454,1)} kg")

#imagenes poke

if st.button("Sprites"):
    datos_poke = obtener_pokemon(nombre_poke)
    if datos_poke:
        Imagenes = datos_poke['sprites']
        st.write('Sprites')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            Sprite_def_front = Imagenes["front_default"]
            if Sprite_def_front:
                st.image(Sprite_def_front, caption="Sprite Default Frontal de " + nombre_poke)
            else:
                st.write("No hay sprite default frontal disponible.")
        with col2:
            Sprite_def_back = Imagenes["back_default"]
            if Sprite_def_back:
                st.image(Sprite_def_back, caption="Sprite Default Trasero de " + nombre_poke)
            else:
                st.write("No hay sprite default trasero disponible.")
        with col3:
            Sprite_shiny_front = Imagenes["front_shiny"]
            if Sprite_shiny_front:
                st.image(Sprite_shiny_front, caption="Sprite Shiny Frontal de " + nombre_poke)
            else:
                st.write("No hay sprite shiny frontal disponible.")
        with col4:
            Sprite_shiny_back = Imagenes["back_shiny"]
            if Sprite_shiny_back:
                st.image(Sprite_shiny_back, caption="Sprite Shiny Trasero de " + nombre_poke)
            else:
                st.write("No hay sprite shiny trasero disponible.")

st.divider()

#todos los tipos de pokemon(1-18)

def obtener_tipos_poke(tipo):
    url = f"https://pokeapi.co/api/v2/type/{tipo}/"
    res = requests.get(url)

    if res.status_code == 200:
        return res.json()
    else:
        st.error("Pokémon no encontrado o error en la API.")
        return None

with st.expander("Menú de todos los tipos de Pokémon", expanded=False):
    tipos_pokemon = ['1. Normal','2. Luchador','3. Volador','4. Veneno','5. Tierra','6. Roca','7. Bicho','8. Fantasma','9. Acero','10. Fuego','11. Agua','12. Hoja','13. Electrico','14. Psíquico','15. Hielo','16. Dragón','17. Siniestro','18. Hada']
    st.write("Tipos disponibles:")
    for opc in tipos_pokemon:
        st.write(" - " + opc)


seleccion_tipo = st.text_input("Ingrese el número tipo del Pokémon: \n")

if st.button("Todos los Pokémon del tipo seleccionado"):
    datos_poke = obtener_tipos_poke(seleccion_tipo)
    if datos_poke:
        pokes_de_ese_tipo = datos_poke["pokemon"]
        total_pokes = len(pokes_de_ese_tipo)
        st.write(f"El total de pokemones del tipo seleccionado son: {total_pokes}")

#grafico de torta distribucion pokemons
st.divider()

gif_espera = "https://images.gamebanana.com/img/ico/sprays/pikachu.gif"

if st.button("Generar gráfico de torta de la distribución de todos los tipos de Pokémon"):
    gif_aux = st.empty()

    with st.spinner("Cargando ..."):
        gif_aux.image(gif_espera)
        contador_tipos = []
        etiquetas_tipos = []
        for i in range(1, 19):
            datos_poke = obtener_tipos_poke(i)
            if datos_poke:
                pokes_de_ese_tipo = datos_poke["pokemon"]
                total_pokes = len(pokes_de_ese_tipo)
                contador_tipos.append(total_pokes)
                etiquetas_tipos.append(tipos_pokemon[i-1])

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.pie(contador_tipos, labels=etiquetas_tipos, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

    gif_aux.empty()
    with st.container(height=600):
        st.pyplot(fig)
    

#grafico de barras distribucion poke

st.divider()

if st.button("Generar gráfico de barras de la distribución de todos los tipos de Pokemon"):
    gif_aux = st.empty()

    with st.spinner("Cargando ..."):
        gif_aux.image(gif_espera)
        contador_tipos = []
        etiquetas_tipos = []

        for i in range(1, 19):
            datos_poke = obtener_tipos_poke(i)
            if datos_poke:
                pokes_de_ese_tipo = datos_poke["pokemon"]
                total_pokes = len(pokes_de_ese_tipo)
                contador_tipos.append(total_pokes)
                etiquetas_tipos.append(tipos_pokemon[i-1])

        # Crear el gráfico de barras
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(etiquetas_tipos, contador_tipos, color='skyblue')
        ax.set_xlabel('Tipos de Pokemon')
        ax.set_ylabel('Total de Pokemon')
        ax.set_title('Distribución de Pokemon por Tipo')
        ax.set_xticklabels(etiquetas_tipos, rotation=90)

    gif_aux.empty()
    with st.container(height=600):
        st.pyplot(fig)

#Filtros para listar Pokémon según su región (Kanto, Johto, etc.) o generación.
def pokes_por_region(gen):
    url = f"https://pokeapi.co/api/v2/generation/{gen}/"
    res = requests.get(url)

    if res.status_code == 200:
        return res.json()
    else:
        st.error("Pokémon no encontrado o error en la API.")
        return None

st.divider()
opciones = st.multiselect(
    "Pokemones y su generación",
    ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Paldea"]
)

col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9, gap="small")

def columnas_poke_gen(col, gen, genNum):
    with col:
        if gen in opciones:
            datos_poke = pokes_por_region(genNum)
            if datos_poke:
                poke_region = datos_poke['pokemon_species']
                st.write(f"Pokemones de la región: {gen}")
                for poke in poke_region:
                    nombre_poke = poke['name']
                    st.write(f"- {nombre_poke}")

columnas_poke_gen(col1, "Kanto", 1)
columnas_poke_gen(col2, "Johto", 2)
columnas_poke_gen(col3, "Hoenn", 3)
columnas_poke_gen(col4, "Sinnoh", 4)
columnas_poke_gen(col5, "Unova", 5)
columnas_poke_gen(col6, "Kalos", 6)
columnas_poke_gen(col7, "Alola", 7)
columnas_poke_gen(col8, "Galar", 8)
columnas_poke_gen(col9, "Paldea", 9)

st.divider()

tipo_seleccionado = st.selectbox("Selecciona un tipo de Pokémon para comparar:", tipos_pokemon)

if st.button("Comparar estadísticas promedio por tipo"):
    gif_aux = st.empty()

    with st.spinner("Cargando ..."):
        gif_aux.image(gif_espera)
        tipo_numero = tipos_pokemon.index(tipo_seleccionado) + 1  

        stats_promedio = {}

        for i in range(1, 19):
            datos_tipo = obtener_tipos_poke(i)
            if datos_tipo:
                pokes_de_ese_tipo = datos_tipo["pokemon"]
                total_stats = {stat: 0 for stat in ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']}
                total_pokemon = len(pokes_de_ese_tipo)

                for poke in pokes_de_ese_tipo:
                    nombre_poke = poke['pokemon']['name']
                    datos_poke = obtener_pokemon(nombre_poke)
                    if datos_poke:
                        for stat in total_stats.keys():
                            total_stats[stat] += next((s['base_stat'] for s in datos_poke['stats'] if s['stat']['name'] == stat), 0)

                stats_promedio[i] = {stat: total / total_pokemon for stat, total in total_stats.items()}

        stats_tipo_seleccionado = stats_promedio[tipo_numero]

        df_comparacion = pd.DataFrame(stats_promedio).T.fillna(0) 

        df_comparacion.loc[tipo_seleccionado] = stats_tipo_seleccionado

        df_comparacion = df_comparacion.T

    gif_aux.empty()
    st.write("Comparación de estadísticas promedio por tipo:")
    st.dataframe(df_comparacion)

    fig, ax = plt.subplots(figsize=(10, 6))  # Ajustar el tamaño de la figura
    df_comparacion.plot(kind='bar', ax=ax, width=0.8)  # Ajustar el ancho de las barras
    ax.set_title('Comparación de Estadísticas Promedio de Pokémon por Tipo')
    ax.set_ylabel('Base Stat Promedio')
    ax.set_xlabel('Estadísticas')

    ax.set_xticklabels(df_comparacion.index, rotation=45, ha='right')

    plt.tight_layout()

    st.pyplot(fig)
