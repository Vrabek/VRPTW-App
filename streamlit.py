"""Vehicles Routing Problem (VRP) with Time Windows streamlit."""

from VRPT import create_data_model, VRPTW_Algorithm, solution_cost_json, solution_routes_json, solution_full_json, calculate_distance_matrix
import streamlit as st
import matplotlib.pyplot as plt


# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)


st.title('VRPTW-APP')

if 'plot_routes' not in st.session_state:
    st.session_state.plot_routes = False

if 'count' not in st.session_state:
    st.session_state.count = 0

if 'data_model' not in st.session_state:
    st.session_state.data_model = create_data_model()


#TODO BUTTON Wczytaj z pliku
if st.button('Przeładuj data model'):
    st.session_state.data_model = create_data_model()

#TODO FIELD Wstaw plik

# Get some data.
#data = np.random.randn(10, 2)

# Show the data as a chart.
# @st.cache 
# def define_chart():
#     data = np.random.randn(10, 2)
#     return data

# define_chart()

# Wait 1 second, so the change is clearer.
#time.sleep(1)


#text = st.text_input("Type here")

# ext2 = st.text_input("Type here", key = "last_name")




if st.checkbox('Macierze czasu między punktami'):
    #TODO FIELD właściwości punktu, xyz,...
    if st.checkbox('Pokaż macierz czasu'):
        st.table(st.session_state.data_model['time_matrix'])

    if st.checkbox('Edycja czasu'):
        matrix_col1, matrix_col2, matrix_col3, matrix_col4 = st.columns(4)

        with st.container():
            st.write("Właściwości punktu")
            #coord_x = st.number_input('Koordynat X (wiersz)', step=1, key = "")
            #coord_y = st.number_input('Koordynat Y (kolumna)', step=1)
            #czas = st.number_input('czas', step=1)
            coord_x = matrix_col1.number_input('Koordynat X (wiersz)', step=1)#, key = "")
            coord_y = matrix_col2.number_input('Koordynat Y (kolumna)', step=1)
            czas = matrix_col3.number_input('czas', step=1)
            matrix_col4.write(" ")

            if matrix_col4.button('zaktualizuj czas punktu'):
                st.session_state.data_model['time_matrix'][coord_x][coord_y]=czas

                

if st.checkbox('Okna czasowe'):
    #TODO FIELD właściwości punktu, xyz,...
    if st.checkbox('Pokaż okna czasowe'):
        #st.table(st.session_state.data_model['time_windows'])
        for idx, time_window in enumerate(st.session_state.data_model['time_windows']):
            if idx == 0:
                st.write(f"Baza, otwarcie {time_window[0]} zamkniecie {time_window[1]}")
            else:
                st.write(f"Punkt czasowy {idx}, otwarcie {time_window[0]} zamkniecie {time_window[1]}")
        

    if st.checkbox('Edycja okna czasowego'):
        window_col1, window_col2, window_col3, window_col4 = st.columns(4)

        with st.container():
            st.write("Właściwości punktu")
            #coord_x = st.number_input('Koordynat X (wiersz)', step=1, key = "")
            #coord_y = st.number_input('Koordynat Y (kolumna)', step=1)
            #czas = st.number_input('czas', step=1)
            time_point_index = window_col1.number_input('Indeks punktu', step=1)#, key = "")
            time_point_start = window_col2.number_input('Czas otwarcia', step=1)
            time_point_stop = window_col3.number_input('Czas zamkniecia', step=1)
            window_col4.write(" ")

            if window_col4.button('zaktualizuj czas okna'):
                st.session_state.data_model['time_windows'][time_point_index] = (time_point_start, time_point_stop)

import numpy as np

def add_point_to_data_model(data_model, x, y, tw_start, tw_stop):
    data_model['point_coords'] = np.concatenate((data_model['point_coords'],[[x,y]]), axis=0)
    print(data_model['time_windows'])
    data_model['time_windows'] = np.vstack((data_model['time_windows'], (tw_start,tw_stop)))
    print(data_model['time_windows'])
    #TODO refactor quick fix - list of list into list of tuples
    data_model['time_windows'] = [tuple((xyz[0], xyz[1])) for xyz in data_model['time_windows']]
    print(data_model['time_windows'])
    data_model['time_matrix'] = calculate_distance_matrix(data_model['point_coords'])

if st.checkbox('Dodawanie punktu'):
    add_col1, add_col2, add_col3, add_col4, add_col5 = st.columns(5)

    with st.container():
        st.write("Właściwości punktu")
        #coord_x = st.number_input('Koordynat X (wiersz)', step=1, key = "")
        #coord_y = st.number_input('Koordynat Y (kolumna)', step=1)
        #czas = st.number_input('czas', step=1)
        add_point_x = add_col1.number_input('Współrzędne X punktu', step=1)#, key = "")
        add_point_y = add_col2.number_input('Współrzędne y punktu', step=1)
        add_time_point_start = add_col3.number_input('Czas otwarcia punktu', step=1)
        add_point_stop = add_col4.number_input('Czas zamkniecia punktu', step=1)
        add_col5.write(" ")

        if add_col5.button('dodaj punkt'):

            add_point_to_data_model(st.session_state.data_model, int(add_point_x), int(add_point_y), int(add_time_point_start), int(add_point_stop))

        #time_window_start = st.number_input('Początek okna czasowego')
        #time_window_stop = st.number_input('Koniec okna czasowego')

##TODO BUTTON dodaj punkt
#if st.button('zaktualizuj czas punktu'):
#    #continue
#    st.session_state.data_model['time_matrix'][coord_x][coord_y]=czas

    # arr = np.random.normal(1, 1, size=100)
    # fig, ax = plt.subplots()
    # ax.hist(arr, bins=20)


#BUTTON Oblicz trasy
if st.button('Oblicz trasy'):


    data = create_data_model()

    points_coords = st.session_state.data_model['point_coords']

    json = solution_routes_json()
    print(json)
    
    #col = get_N_HexCol(len(json))
    col='bgrcmyk'
    colors = {vehicle: col[idx] for idx, vehicle in enumerate(json)}

    fig, ax = plt.subplots()

    for vehicle, route in json.items():
        prev_point=-1
        for point in route:
            if prev_point>=0:
                #print(points_coords[point])
                #print(points_coords)
                ax.scatter(points_coords[point][0],points_coords[point][1], c=colors[vehicle], label=vehicle)
                ax.annotate(point, (points_coords[point][0], points_coords[point][1]), color=colors[vehicle])

                plt.arrow(points_coords[prev_point][0], points_coords[prev_point][1], points_coords[point][0]-points_coords[prev_point][0],points_coords[point][1]-points_coords[prev_point][1], width = 0.01, label=vehicle,color=colors[vehicle])



                prev_point=point

            else:
                ax.scatter(points_coords[point][0], points_coords[point][1], label=vehicle, c=colors[vehicle])
                prev_point=point

        #plt.plot(x,y,label=vehicle)
        

        #ax.scatter(z, y)

        #plt.arrow(2, 4, 2, 2, width = 0.05)

    #plt.legend()
    st.pyplot(fig)

#1232312
    # y = [2.56422, 3.77284, 3.52623, 3.51468, 3.02199]
    # z = [0.15, 0.3, 0.45, 0.6, 0.75]
    # label = [58, 651, 393, 203, 123]

    # 
    # 

    # for i, txt in enumerate(n):
    #     ax.annotate(txt, (z[i], y[i])

    #ax.annotate(n[1], (z[1], y[1]), xytext=(z[1]-0.05, y[1]-0.3), 
    #arrowprops = dict(  arrowstyle="->",
    #                    connectionstyle="angle3,angleA=0,angleB=-90"))

    # 

    
#TODO BUTTON eksport tras

#TODO BUTTON Wyświetl listę punktów
#TODO FIELD Lista punktów

#TODO BUTTON Wyświetl trasy
#TODO FIELD Lista tras





if st.button('solution_cost_json'):
    json = solution_cost_json()
    st.write(json)


if st.button('solution_routes_json'):
    json = solution_routes_json()
    print(json)
    st.write(json)


if st.button('solution_full_json'):
    json = solution_full_json()
    st.write(json)