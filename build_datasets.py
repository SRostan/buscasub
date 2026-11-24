#!/usr/bin/env python3
"""
Script de extracción y consolidación para BuscaSUB (Sociedad Uruguaya de Biociencias)
Lee la base de datos maestra unificada de socios y genera los datasets optimizados
para GitHub Pages (versión pública estricta y versión interna para seccionales).
"""

import openpyxl
import json
import re
import os

EXCEL_PATH = '/Users/santiagorostan/Library/CloudStorage/GoogleDrive-santir13@gmail.com/Mi unidad/Antigravity/Asistente FQ/Asistentes/SUB/Nuevo sistema/Base_de_datos_maestra_unificada_29oct26_rutilo.xlsx'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

OFFICIAL_SECCIONALES = [
    ('ATGC-U', 'ATGC-U - Terapia Génica y Celular'),
    ('CODEUy', 'CODEUy - Ecología'),
    ('LimnoUy', 'LimnoUy - Limnología'),
    ('SBBM', 'SBBM - Bioquímica y Biología Molecular'),
    ('SBF', 'SBF - Biofísica'),
    ('SIB/NIB', 'SIB/NIB - Ingeniería Biomédica'),
    ('SNU', 'SNU - Neurociencias'),
    ('SUBI', 'SUBI - Bioinformática'),
    ('SUG', 'SUG - Genética'),
    ('SUMI', 'SUMI - Microscopía e Imagenología')
]

def main():
    print(f"Cargando {EXCEL_PATH}...")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb['Maestra']

    public_dict = {}
    seccionales_dict = {code: {'codigo': code, 'nombre': nombre, 'padron': []} for code, nombre in OFFICIAL_SECCIONALES}

    count = 0
    for r in range(2, ws.max_row + 1):
        ci_val = ws.cell(r, 1).value
        if ci_val is None or str(ci_val).strip() == '':
            continue
        
        try:
            ci_num = int(float(ci_val))
            ci_str = str(ci_num).zfill(8)
        except:
            ci_str = re.sub(r'\D', '', str(ci_val)).zfill(8)
        
        nombre = str(ws.cell(r, 2).value or '').strip()
        correo = str(ws.cell(r, 3).value or '').strip()
        nivel = str(ws.cell(r, 4).value or 'Sin dato').strip()
        afiliacion = str(ws.cell(r, 5).value or 'Sin dato').strip()
        
        sec1 = str(ws.cell(r, 6).value or '').strip()
        sec2 = str(ws.cell(r, 7).value or '').strip()
        sec3 = str(ws.cell(r, 8).value or '').strip()
        
        ingreso_val = ws.cell(r, 9).value
        if isinstance(ingreso_val, (int, float)):
            ingreso = str(int(ingreso_val))
        else:
            ingreso = str(ingreso_val or '2021 o anterior').strip()
        
        p2021 = str(ws.cell(r, 10).value or 'No').strip()
        p2022 = str(ws.cell(r, 11).value or 'No').strip()
        p2023 = str(ws.cell(r, 12).value or 'No').strip()
        p2024 = str(ws.cell(r, 13).value or 'No').strip()
        p2025 = str(ws.cell(r, 14).value or 'No').strip()
        p2026 = str(ws.cell(r, 15).value or 'No').strip()
        
        mecanismo2026 = str(ws.cell(r, 16).value or 'No registrado').strip()
        if mecanismo2026 in ['', 'None', '-', '0']:
            mecanismo2026 = 'No registrado'
            
        movimiento = str(ws.cell(r, 17).value or '').strip()
        if movimiento in ['', 'None', '-', '0']:
            movimiento = 'Sin movimientos'
            
        estado = str(ws.cell(r, 18).value or '').strip()
        if not estado or estado.startswith('='):
            current_year = 2026
            try:
                ingreso_num = int(float(ingreso))
            except:
                ingreso_num = 2021
            if ingreso_num == current_year:
                estado = 'Activo' if p2026 == 'Sí' else 'Inactivo'
            elif ingreso_num == current_year - 1:
                estado = 'Activo' if p2025 == 'Sí' else 'Inactivo'
            else:
                if p2025 == 'Sí' and p2024 == 'Sí':
                    estado = 'Activo'
                elif p2025 == 'No':
                    estado = 'Inactivo'
                elif p2025 == 'Sí' and p2024 == 'No':
                    estado = 'Activo - pendiente de pago'
                else:
                    estado = 'Inactivo'
                    
        if p2026 == 'Sí':
            estado_cuota_2026 = 'AL DÍA (PAGO 2026 REGISTRADO)'
        elif movimiento != 'Sin movimientos':
            estado_cuota_2026 = 'CUBIERTO POR REASIGNACIÓN (PAGO 2026 MOVIDO A CUOTA ANTERIOR)'
        elif p2026 == 'No corresponde':
            estado_cuota_2026 = 'NO CORRESPONDE (INGRESO POSTERIOR)'
        else:
            estado_cuota_2026 = 'PENDIENTE DE PAGO 2026'

        ci_display = f"{ci_str[:1]}.{ci_str[1:4]}.{ci_str[4:7]}-{ci_str[7:]}"
        
        # 1. PÚBLICO (Privacidad Estricta: SIN NOMBRE, SIN CORREO)
        public_dict[ci_str] = {
            'ci': ci_str,
            'ci_display': ci_display,
            'estado': estado,
            'nivel': nivel,
            'afiliacion': afiliacion,
            'ingreso': ingreso,
            'seccionales': {
                'sec1': sec1 if sec1 not in ['', '0', 'None'] else 'Ninguna',
                'sec2': sec2 if sec2 not in ['', '0', 'None'] else 'Ninguna',
                'sec3': sec3 if sec3 not in ['', '0', 'None'] else 'Ninguna'
            },
            'cuotas': {
                '2021': p2021,
                '2022': p2022,
                '2023': p2023,
                '2024': p2024,
                '2025': p2025,
                '2026': p2026
            },
            'mecanismo2026': mecanismo2026,
            'movimiento': movimiento,
            'estadoCuota2026': estado_cuota_2026
        }
        
        # 2. SECCIONALES
        for code, full_name in OFFICIAL_SECCIONALES:
            pref = None
            if sec1 and (code in sec1 or full_name in sec1):
                pref = 'Principal'
            elif sec2 and (code in sec2 or full_name in sec2):
                pref = 'Secundaria'
            elif sec3 and (code in sec3 or full_name in sec3):
                pref = 'Terciaria'
                
            if pref:
                seccionales_dict[code]['padron'].append({
                    'nombre': nombre,
                    'ci': ci_display,
                    'ci_raw': ci_str,
                    'nivel': nivel,
                    'afiliacion': afiliacion,
                    'correo': correo,
                    'ingreso': ingreso,
                    'preferencia': pref,
                    'estado': estado,
                    'movimiento': movimiento,
                    'cuota2026': estado_cuota_2026
                })
                
        count += 1

    print(f"Procesados {count} socios.")

    # Guardar JS y JSON
    with open(os.path.join(DATA_DIR, 'socios_publico.js'), 'w', encoding='utf-8') as f:
        f.write('// Dataset público SUB - Privacidad Estricta (sin nombres ni correos)\n')
        f.write('const SOCIOS_PUBLICO = ' + json.dumps(public_dict, ensure_ascii=False, indent=2) + ';\n')

    with open(os.path.join(DATA_DIR, 'socios_publico.json'), 'w', encoding='utf-8') as f:
        json.dump(public_dict, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA_DIR, 'seccionales_data.js'), 'w', encoding='utf-8') as f:
        f.write('// Directorio Seccionales SUB - Acceso Directivo\n')
        f.write('const SECCIONALES_DATA = ' + json.dumps(seccionales_dict, ensure_ascii=False, indent=2) + ';\n')

    with open(os.path.join(DATA_DIR, 'seccionales_data.json'), 'w', encoding='utf-8') as f:
        json.dump(seccionales_dict, f, ensure_ascii=False, indent=2)

    print("Datasets actualizados con éxito en data/")

if __name__ == '__main__':
    main()
