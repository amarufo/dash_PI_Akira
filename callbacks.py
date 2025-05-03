from dash.dependencies import Input, Output
from layout import build_fig_pob

# Lista de imágenes asociadas al dropdown
imagenes_por_variable = {
    "POB_TOTAL": "/assets/pob_total.png",
    "POB_REF": "/assets/pob_ref.png",
    "POB_POTE": "/assets/pob_pot.png",
    "POB_E_SP": "/assets/pob_e_sp.png",
    "POB_E_CP": "/assets/pob_e_cp.png",
    "POT_CP_SP": "/assets/pot_cp_sp.png"
}

# Lista para el segundo carrusel
ofertas = ["/assets/oferta1.png", "/assets/oferta2.png"]

def registrar_callbacks(app):
    # Callback 1: gráfico + imagen relacionada al dropdown
    @app.callback(
        [Output("grafico_poblacion", "figure"),
        Output("imagen_carrusel", "src")],
        Input("dropdown_poblacion", "value")
    )
    def update_poblacion_y_imagen(col):
        fig = build_fig_pob(col)
        img = imagenes_por_variable.get(col, "/assets/pob_total.png")
        return fig, img

    # Callback 2: cambiar imagen de carrusel
    @app.callback(
        Output("imagen_carrusel2", "src"),
        Input("btn-cambiar", "n_clicks"),
    )
    def cambiar_imagen(n):
        if not n:
            return ofertas[0]
        return ofertas[n % len(ofertas)]
