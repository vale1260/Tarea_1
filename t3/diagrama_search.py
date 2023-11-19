import graphviz

def crear_diagrama():
    grafo = graphviz.Digraph('diagrama', format='png', engine='dot', strict=True)

    # Nodos
    grafo.node('Inicio')
    grafo.node('Conectar a PostgreSQL')
    grafo.node('Insertar Datos')
    grafo.node('Buscar Palabra')
    grafo.node('Imprimir Resultados')
    grafo.node('Cerrar Conexión')
    grafo.node('Fin')

    # Conexiones
    grafo.edge('Inicio', 'Conectar a PostgreSQL')

    # Subflujo: Insertar Datos
    grafo.edge('Conectar a PostgreSQL', 'Insertar Datos')
    grafo.edge('Insertar Datos', 'Conectar a PostgreSQL', label='Loop')
    grafo.edge('Insertar Datos', 'Buscar Palabra')

    # Subflujo: Buscar Palabra
    grafo.edge('Buscar Palabra', 'Imprimir Resultados')
    grafo.edge('Imprimir Resultados', 'Cerrar Conexión')
    grafo.edge('Cerrar Conexión', 'Fin')

    return grafo

def principal():
    grafo = crear_diagrama()
    grafo.render(filename='diagrama_completo', cleanup=True, format='png', engine='dot')

if __name__ == '__main__':
    principal()
