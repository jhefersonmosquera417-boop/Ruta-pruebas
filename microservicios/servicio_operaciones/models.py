# Los modelos eran de Spyne (SOAP). Spyne ya no se usa en la versión REST y no es
# compatible con las versiones recientes de Python, así que se reemplaza por esta
# clase mínima: mismas clases, mismos campos, mismo constructor por nombre.
class _Tipo:
    def __init__(self, doc=""):
        self.doc = doc

Integer = Unicode = Float = Boolean = _Tipo


class ComplexModel:
    def __init__(self, **kwargs):
        for cls in reversed(type(self).__mro__):
            for nombre, valor in vars(cls).items():
                if isinstance(valor, _Tipo):
                    setattr(self, nombre, kwargs.get(nombre))

NAMESPACE = 'popayan.transporte.operaciones'

class Stop(ComplexModel):
    """Representa un paradero o punto de referencia en la ruta."""
    __namespace__ = NAMESPACE

    id = Integer(doc="Identificador único del paradero")
    route_id = Integer(doc="ID de la ruta a la que pertenece")
    name = Unicode(doc="Nombre del paradero o punto de parada")
    landmark_reference = Unicode(doc="Punto de referencia cercano")
    stop_order = Integer(doc="Posición u orden en la secuencia del recorrido")


class Incident(ComplexModel):
    """Representa un reporte o novedad vial en la ruta."""
    __namespace__ = NAMESPACE

    id = Integer(doc="Identificador del incidente")
    route_id = Integer(doc="ID de la ruta afectada")
    incident_type = Unicode(doc="Tipo de evento (ej: CONGESTION, ACCIDENTE, DESVIO)")
    description = Unicode(doc="Detalle o descripción de lo ocurrido")
    reported_by = Unicode(doc="Entidad o persona que realiza el reporte")
    reported_at = Unicode(doc="Fecha y hora de registro")
    status = Unicode(doc="Estado de la novedad (ACTIVO, RESUELTO)")


class BusTimeDifferenceResult(ComplexModel):
    """Resultado del cálculo de diferencia de tiempos entre despachos."""
    __namespace__ = NAMESPACE

    route_id = Integer(doc="ID de la ruta consultada")
    bus_plate_1 = Unicode(doc="Placa del primer bus")
    departure_time_1 = Unicode(doc="Hora de salida del primer bus")
    bus_plate_2 = Unicode(doc="Placa del segundo bus")
    departure_time_2 = Unicode(doc="Hora de salida del segundo bus")
    difference_minutes = Integer(doc="Diferencia de tiempo en minutos")
    summary_message = Unicode(doc="Mensaje explicativo del intervalo entre despachos")
