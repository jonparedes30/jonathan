import io
from django.http import FileResponse
from django.utils import timezone
import pandas as pd

# Función Excel
def exportar_excel(datos, nombre_archivo='reporte.xlsx'):
    """
    Genera un Excel desde una lista de diccionarios o queryset convertido.
    """
    if not datos:
        return None

    df = pd.DataFrame(list(datos))
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Reporte', index=False)
    excel_file.seek(0)
    return FileResponse(excel_file, as_attachment=True, filename=nombre_archivo)

# PDF momentáneamente desactivado
# def exportar_pdf(...):
#     pass  # Comentado hasta que se instale correctamente WeasyPrint
