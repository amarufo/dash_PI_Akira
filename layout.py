#%%
# layout.py
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

#%%
estilo_cabecera = {
    "color": "white",
    "backgroundColor": "black",
    "borderRadius": "0.1vw",
    "fontWeight": "bold",
    "textAlign": "center",
    "width": "100%",
    "fontSize": "0.7vw"    
}
estilo_cuerpo ={
    "color": "black",
    "textAlign": "left",
    "width": "100%",
    "fontSize": "0.7vw",
    "padding": "0.1vw"                        
}

fases_horizonte = [
    dict(type="rect", xref="x", yref="paper", x0=2019, x1=2024.9, y0=0, y1=1, fillcolor="#d4b40e", opacity=0.89, layer="below", line_width=0),
    dict(type="rect", xref="x", yref="paper", x0=2025, x1=2026.9, y0=0, y1=1, fillcolor="#bcbcac", opacity=0.89, layer="below", line_width=0),
    dict(type="rect", xref="x", yref="paper", x0=2027, x1=2028.9, y0=0, y1=1, fillcolor="#d4b40e", opacity=0.89, layer="below", line_width=0),
    dict(type="rect", xref="x", yref="paper", x0=2029, x1=2038.9, y0=0, y1=1, fillcolor="#efe30e", opacity=0.89, layer="below", line_width=0),
]

db_path = "db.xlsx"
poblaciones = pd.read_excel(db_path, sheet_name="poblaciones")

# ── Diccionarios de etiquetas y rutas ────────────────────────────────────────────
columnas = [c for c in poblaciones.columns if c != "AÑO"]
nombres_pob = {
    "POB_TOTAL": "Población total",
    "POB_REF":   "Población demandada referencial",
    "POB_POTE":  "Población demandada potencial",
    "POB_E_SP":  "Población efectiva sin proyecto",
    "POB_E_CP":  "Población efectiva con proyecto / DEMANDA"
}
#%%############ GRÁFICO DE POBLACIONES
###############-------------------------------------------------------------------------------------
def build_fig_pob(col):
    y = poblaciones[col]
    fig = go.Figure(go.Bar(
        x=poblaciones["AÑO"], y=y,
        text=[f"{valor:,.0f}" for valor in y], textposition="inside",
        marker=dict(color=y, colorscale="Turbo", colorbar=dict(title="Valor"))
    ))
    
    y_min = poblaciones[col][poblaciones[col].notnull()].min()*0.79
    y_max = poblaciones[col][poblaciones[col].notnull()].max()*1.03

    fig.update_layout(
        yaxis=dict(
            tickformat=",",
            range=[y_min, y_max]),
        xaxis=dict(dtick=1),
        margin=dict(l=0, r=0, t=0, b=0),
        bargap=0.1,
        plot_bgcolor="white"
    )
    # Rectángulos de color y opacos para diferencias los años dentro del horizonte
    fig.update_layout(shapes=fases_horizonte)
    fig.add_annotation(
        x=1, y=0,  # esto es esquina derecha (1)inferior(0)
        xref="paper", yref="paper", # se usa como referencia el papel
        text="<span style='color:#507294;'>⛊</span> Antes de la intervención<br>"
        "<span style='color:#bcbcac;'>⛊</span> Preinversión y Estudios Definitivos<br>"
        "<span style='color:#d4b40e;'>⛊</span> Ejecución física<br>"
        "<span style='color:#efe30e;'>⛊</span> Funcionamiento",
        showarrow=False,
        align="left",
        font=dict(size=12),
        bgcolor="white",
        opacity=0.8
    )
    fig.update_traces(
        textfont=dict(
            size=16,
            family="Arial Black")  # Cambia 12 por el tamaño que desees
    )

    
    return fig
#%%############ GRÁFICO DE DONAS
###############-------------------------------------------------------------------------------------
def crear_donut_valor(titulo, valor, total, color="#007f7f"):
    restante = total - valor

    fig = go.Figure(go.Pie(
        values=[valor, restante],
        hole=0.6,
        marker=dict(colors=[color, "#f0f0f0"]),
        textinfo="none",       # <--- no muestra porcentajes
        showlegend=False       # <--- oculta leyenda
    ))

    fig.update_layout(
        annotations=[dict(
            text=str(valor),   # <--- muestra solo el valor absoluto
            x=0.5, y=0.5,
            font_size=22,
            showarrow=False
        )],
        margin=dict(t=0, b=0, l=0, r=0)
    )

    return html.Div([
        html.Div(titulo, style={
            "textAlign": "center",
            "fontWeight": "bold",
            "fontSize": "0.8rem",
            "marginBottom": "5px",
            "marginTop": "5px"
        }),
        dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "100px"})
    ], style={
        "width": "100%",
        "display": "inline-block",
        "textAlign": "center"
    })

#%%############ GRÁFICO DE BRECHAS
brechas = pd.read_excel(db_path, sheet_name="brecha")

años_brecha = list(brechas["AÑO"])
oferta_brecha = list(brechas["OFERTA_O"])
demanda_brecha = list(brechas["DEMANDA_CP"])
brecha = list(brechas["BRECHA"])

fig_brecha = go.Figure()

# Oferta (azul)
fig_brecha.add_trace(go.Bar(
    x=años_brecha, y=oferta_brecha,
    name="oferta optimizada",
    marker_color="#005bbc"  # azul más profesional
))

# Demanda (rojo)
fig_brecha.add_trace(go.Bar(
    x=años_brecha, y=demanda_brecha,
    name="Demanda con proyecto",
    marker_color="#ffd600"  # rojo estándar
))

# Brecha (verde) como línea
fig_brecha.add_trace(go.Scatter(
    x=años_brecha, y=brecha,
    mode="lines+markers+text",
    name="Brecha",
    line=dict(color="#2ca02c", width=3),
    marker=dict(size=7),
    text=[str(b) for b in brecha],
    textposition="top center",
    textfont=dict(
        size=12,
        family="Verdana",
        color="black"
    )
))

# Layout
fig_brecha.update_layout(
    barmode="group",
    plot_bgcolor="white",
    legend=dict(orientation="h", y=1.1),
    xaxis=dict(dtick=1),
    margin=dict(t=0, l=0, r=0, b=0)
)


#%%############ LOYAOUT
layout = html.Div(style={
    "display": "flex",
    "flexDirection": "column",
    "width": "100vw",
    "height": "100vh",
    "fontFamily": "Arial, sans-serif",
    "backgroundColor": "white"
    },
    children=[
        # ── Encabezado ────────────────────────────────────────────────────────────────
        html.Div([
            html.Div("CÁLCULO DE OFERTA, DEMANDA Y BRECHAS DE UN PROYECTO DE INVERSIÓN", style={
                "marginLeft": "0.5vw",
                "color": "white",
                "fontWeight": "bold",
                "textAlign": "center",
                "width": "100%",
                "fontSize": "1vw",
                "padding": "0px 0px"  # opcional: agrega algo de espacio interno
                }
            )
        ], style={
            "display": "flex",
            "width": "100%",
            "height": "3%",
            "backgroundColor": "black",
            "alignItems": "center"
            }
        ),
        # ── Cuerpo principal ─────────────────────────────────────────────────────────
        html.Div(style={
            "display": "flex",
            "width": "100vw",
            "height": "100vh",
            "borderRadius": "0",
            "marginTop":"0px",
            #"border": "1px solid red"
        }, children=[
            #PRIMERA COLUMNA
            html.Div(style={ 
                    "width": "30%",
                    "padding": "0.5rem",
                    "textAlign": "center",
                    "borderRadius": "0.1vw",
            }, children=[
                # Datos iniciales
                html.Div(style={
                    "border": "2px solid black"
                    }, children=[
                        html.Div("CURSO", style={**estilo_cabecera}
                        ),
                        html.Div("Taller de proyectos II - Maestría en Sc. Proyectos de Inversión", style={
                            "color": "white",
                            "fontWeight": "bold",
                            "backgroundColor": "gray",
                            "textAlign": "center",
                            "width": "100%",
                            "fontSize": "0.7vw",
                            "padding": "0.1vw"                      
                            }
                        ),
                        html.Div("Integrantes", style={**estilo_cabecera
                        }),
                        html.Div("Wilbert Amaru Fernandez Olmedo", style={**estilo_cuerpo}
                        ),
                        html.Div("Steven Cristian Rodas Tenazoa", style={**estilo_cuerpo}
                        ),
                        html.Div("Cesar Humberto Blas Neyra", style={**estilo_cuerpo}
                        ),                                
                        html.Div("Datos iniciales", style={**estilo_cabecera}
                        ),
                        html.Div("Nombre de la I.E secundaira: Akira Kato", style={**estilo_cuerpo}
                        ),
                        html.Div("Ubicación: Lima - Lima - Ate", style={**estilo_cuerpo}
                        ),
                        html.Div("Fuente de información: BD personal - INEI - SIAGIA", style={**estilo_cuerpo}
                        ),                                                                               
                        html.Div("Unidad de servicio", style={**estilo_cabecera}
                        ),
                        html.Div("Estudiantes atendidos anualmente en condiciones estándar de servicio", style={**estilo_cuerpo}
                        ),
                        html.Div("MINEDU: Servicio de Educación Secundaria", style={**estilo_cuerpo}
                        ),
                        html.Div("Brechas", style={**estilo_cabecera}
                        ),
                        html.Div("Brecha asumida: Estudiantes no atendidos anualmente en condiciones estándar de servicio", style={**estilo_cuerpo}
                        ),                        
                        html.Div("Brecha de cobertura: Porcentaje de personas no matriculadas en el nivel secundario respecto a la demanda potencial", style={**estilo_cuerpo}
                        ),
                        html.Div("Brecha de calidad: Porcentaje de locales educativos con el servicio de educación secundaria con capacidad instalada inadecuada", style={**estilo_cuerpo}
                        ),
                    ]
                ),
                html.Div(style={
                    "display": "flex",
                    "width": "100%",
                    "gap": "1rem"
                }, children=[
                    html.Div(style={#COLUMNA DE 70% DE LA COLUMNA 1
                        "width": "65%",
                        "borderRadius": "0rem",
                        "padding": "0rem",
                        "boxSizing": "border-box"
                    }, children=[
                        html.Table([
                            html.Tbody([
                                html.Th("Sobre el Área de influencia", colSpan=2, style={
                                    "textAlign": "center",
                                    "backgroundColor": "#507294",
                                    "color": "black"
                                }),
                                html.Tr([
                                    html.Td("Área del AI", style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                }), html.Td("10.589 km2", style={
                                    "height": "15px",
                                    "textAlign": "center",
                                    "border": "1px solid #ccc"
                                })]),
                                html.Tr([html.Td("Cantidad de colegios públicos y privados", style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                }), html.Td("37", style={
                                    "height": "15px",
                                    "textAlign": "center",
                                    "border": "1px solid #ccc"
                                })]),
                                html.Tr([html.Td("Privados", style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                }), html.Td("33", style={
                                    "height": "15px",
                                    "textAlign": "center",
                                    "border": "1px solid #ccc"
                                })]),
                                html.Tr([html.Td("Públicos", style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                }), html.Td("4", style={
                                    "height": "15px",
                                    "textAlign": "center",
                                    "border": "1px solid #ccc"
                                })]),
                                html.Tr([html.Td("Cantidad de estudiantes del AI", style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                }), html.Td("6867", style={
                                    "height": "15px",
                                    "textAlign": "center",
                                    "border": "1px solid #ccc"
                                })]),
                                html.Tr([html.Td("Estudiantes en colegios públicos", style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                }), html.Td("3190", style={
                                    "height": "15px",
                                    "textAlign": "center",
                                    "border": "1px solid #ccc"
                                })]),
                                html.Th("Datos de la I.E.", colSpan=2, style={
                                    "textAlign": "center",
                                    "backgroundColor": "#507294",
                                    "color": "black"
                                }),
                                html.Tr([
                                    html.Td("Estudiantes - 2024", style={
                                        "height": "15px",
                                        "textAlign": "left",
                                        "border": "1px solid #ccc",
                                        "backgroundColor": "#faec4e",
                                        "color": "black",
                                        "fontWeight": "bold"
                                    }),
                                    html.Td("671", style={
                                        "height": "15px",
                                        "textAlign": "center",
                                        "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Docentes - 2024", style={
                                        "height": "15px",
                                        "textAlign": "left",
                                        "border": "1px solid #ccc",
                                        "backgroundColor": "#faec4e",
                                        "color": "black",
                                        "fontWeight": "bold"
                                    }),
                                    html.Td("34", style={
                                        "height": "15px",
                                        "textAlign": "center",
                                        "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Directivos - 2024", style={
                                        "height": "15px",
                                        "textAlign": "left",
                                        "border": "1px solid #ccc",
                                        "backgroundColor": "#faec4e",
                                        "color": "black",
                                        "fontWeight": "bold"
                                    }),
                                    html.Td("2", style={
                                        "height": "15px",
                                        "textAlign": "center",
                                        "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Secciones totales",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("21",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Turnos",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("2",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),                            
                                html.Tr([
                                    html.Td("Aulas totales",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("11",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Capacidad de aulas*",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("30",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Th("Datos de diagnóstico", colSpan=2, style={
                                    "textAlign": "center",
                                    "backgroundColor": "#507294",
                                    "color": "black"
                                }),
                                html.Tr([
                                    html.Td("Aulas diseñas de acuerdo a la norma",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("3",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Aulas en buen o regular estado",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("3",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Aulas nuevas con el proyecto",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("20",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Th("Datos de diagnóstico", colSpan=2, style={
                                    "textAlign": "center",
                                    "backgroundColor": "#507294",
                                    "color": "black"
                                }),
                                html.Tr([
                                    html.Td("Año de estudio de preinversión",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("2025",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    }),
                                ]),
                                html.Tr([
                                    html.Td("Año de estudio de Expediente Técnico",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("2026",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    }),
                                ]),
                                html.Tr([
                                    html.Td("Año de estudio de Ejecución física",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("2027-2028",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    })
                                ]),
                                html.Tr([
                                    html.Td("Inicio de del periodo de funcionamiento",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("2029",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    }),
                                ]),
                                html.Tr([
                                    html.Td("Estudiantes en I.E. públicas",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("46.45%",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    }),
                                ]),        
                                html.Tr([
                                    html.Td("Estudian en Akira Kato / I.E. públicas",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("21.72%",
                                            style={
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    }),
                                ]),                                
                                html.Tr([
                                    html.Td("Estudian en Akira Kato / Total",
                                            style={
                                                "height": "15px",
                                                "textAlign": "left",
                                                "border": "1px solid #ccc",
                                                "backgroundColor": "#faec4e",
                                                "color": "black",
                                                "fontWeight": "bold"
                                    }),
                                    html.Td("10.09%",
                                            style={
                                                "backgroundColor": "#faec4e",
                                                "height": "15px",
                                                "textAlign": "center",
                                                "border": "1px solid #ccc"
                                    }),
                                ]),                                
                                
                                ])
                        ], style={
                            "fontSize": "0.63vw",
                            "width": "100%",
                            "marginTop": "0rem",
                            "backgroundColor": "white"
                        }),  
                    ]),
                    html.Div(style={ #COLUMNA DE DONUUTS
                        "width": "35%"
                    }, children=[
                        html.Div([
                            crear_donut_valor("Capacidad de diseño = 3x30x2", 180, 1200, "#00ff9f"),
                            crear_donut_valor("Capacidad actual = 3x30x2", 180, 1200, "#00b8ff"),
                            crear_donut_valor("Capacidad óptima = 3x30x2", 180, 1200, "#001eff"),
                            crear_donut_valor("Capacidad final = 20x30x2", 1200, 1200, "red"),
                            ], style={
                                "display": "flex",
                                "flexDirection": "column",     # donuts en vertical
                                "gap": "0.6rem",               # espacio entre donuts
                                "width": "100%"
                        })
                    ])
                ])
            ])
            ,
            #SEGUNDA COLUMNA
            html.Div(
                style={
                    "width": "30%",
                    "borderRadius": "0rem",
                    "padding": "0rem",
                    "textAlign": "center"
                },
                children=[
                    # Imagen del carrusel
                    html.Img(
                        id="imagen_carrusel",
                        src="/assets/4.jpg",
                        style={
                            "width": "100%",
                            "height": "50%",
                            "objectFit": "contain",
                            "borderRadius": "0.5rem"
                        }
                    ),
                    html.Iframe(
                    src="/assets/isochrone_map.html",  # ruta relativa desde el navegador
                    style={
                        "width": "100%",
                        "height": "50%",
                        "padding": "0.5rem"
                    }
                    )
                    
                    
                    
            ]),
            # TERCERA COLUMNA
            html.Div(style={
                "width": "40%"
            }, children=[
                dcc.Dropdown(
                    id="dropdown_poblacion",
                    options=[{"label": nombres_pob.get(c, c), "value": c} for c in columnas],
                    value=columnas[0],
                    clearable=False,
                    style={"fontSize": "0.9rem"}
                ),
                html.Div(style={"borderRadius": "0rem"}, children=[
                    dcc.Graph(
                        id="grafico_poblacion",
                        figure=build_fig_pob(columnas[0]),
                        config={"displayModeBar": False},
                        style={
                            "width": "100%",
                            "height": "350px",
                            }
                    )
                ]),
                html.Div([
                    html.Button("Oferta optimizada", id="btn-cambiar", n_clicks=0, style={
                        "width": "100%",
                        "color": "white",
                        "backgroundColor": "#507294",
                        "fontSize": "0.8vw",
                        "borderRadius": "0.2vw",
                        "fontWeight": "bold",
                        "padding": "1px 1px",  # opcional: agrega algo de espacio interno
                        "display": "inline-block"  # clave para que el div se ajuste al texto
                    }),
                    html.Img(
                        id="imagen_carrusel2",
                        src="/assets/oferta1.png",  # Imagen inicial
                        style={"width": "100%", "height": "300px", "objectFit": "contain", "border": "px solid #507294"}
                    ),
                    html.Div("Evolución de la brecha", style={**estilo_cabecera
                    }),
                    dcc.Graph(figure=fig_brecha,
                            style={
                                "width": "100%",
                                "height": "250px",
                                "objectFit": "contain"
                            }  
                    )
                ], style={
                    "width": "100%",
                    "border": "px solid #ccc",
                    "padding": "0rem",
                    "borderRadius": "0.5rem",
                    "textAlign": "center"
                }),
                
            ]), 
        ])
])
