import os
import csv
import io
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__, template_folder='templates')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, 'simple_results.csv')
HISTORIC_CSV_PATH = os.path.join(DATA_DIR, 'all_history_results.csv')

def init_csv():
    headers = ['Attempt ID', 'Reaction Time (ms)', 'Set Size', 'Stimulus Type', 'Target Present', 'Response Given', 'Is Correct', 'Search Type', 'Subject ID', 'Age', 'Gender', 'Timestamp', 'Session ID']
    for path in [CSV_PATH, HISTORIC_CSV_PATH]:
        needs_init = True
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    first_row = next(reader, None)
                    if first_row == headers:
                        needs_init = False
            except Exception:
                pass
        if needs_init:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

init_csv()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_file(os.path.join(app.root_path, 'static', 'favicon.png'), mimetype='image/png')

@app.route('/api/save_trial', methods=['POST'])
def save_trial():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Datos inválidos"}), 400
        
        attempt_id = data.get('attempt_id')
        rt = data.get('rt')
        set_size = data.get('set_size')
        stimulus_type = data.get('stimulus_type', 'default')
        target_present = data.get('target_present')
        response_given = data.get('response_given')
        is_correct = data.get('is_correct')
        search_type = data.get('search_type', 'feature')
        subject_id = data.get('subject_id', 'Anonimo')
        age = data.get('age', '')
        gender = data.get('gender', '')
        session_id = data.get('session_id', 'SES-UNKNOWN')
        
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        row = [attempt_id, rt, set_size, stimulus_type, target_present, response_given, is_correct, search_type, subject_id, age, gender, timestamp, session_id]
        
        # Save to active session CSV
        with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            
        # Save to permanent historic CSV
        with open(HISTORIC_CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            
        # Calculate averages grouped by Set Size
        averages = {}
        counts = {}
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # skip headers
            for row in reader:
                if len(row) >= 3:
                    try:
                        row_rt = float(row[1])
                        row_size = int(row[2])
                        averages[row_size] = averages.get(row_size, 0) + row_rt
                        counts[row_size] = counts.get(row_size, 0) + 1
                    except ValueError:
                        continue
                        
        stats = {size: round(averages[size] / counts[size], 2) for size in averages}
        
        return jsonify({
            "status": "success",
            "message": "Ensayo guardado",
            "averages": stats
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_data():
    try:
        if os.path.exists(CSV_PATH):
            os.remove(CSV_PATH)
        init_csv()
        return jsonify({"status": "success", "message": "Datos de sesión activa limpiados"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/export_excel', methods=['GET'])
def export_excel():
    try:
        # Load active session
        if not os.path.exists(CSV_PATH):
            return jsonify({"status": "error", "message": "No hay datos de sesión para exportar"}), 404
        
        df = pd.read_csv(CSV_PATH)
        if df.empty:
            return jsonify({"status": "error", "message": "La sesión actual está vacía"}), 400
            
        # Load permanent history
        if os.path.exists(HISTORIC_CSV_PATH):
            df_history = pd.read_csv(HISTORIC_CSV_PATH)
        else:
            df_history = pd.DataFrame()
            
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook  = writer.book
            
            # --- STYLES ---
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'fg_color': '#1e40af', # Royal Blue
                'font_color': '#ffffff',
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'border': 1,
                'align': 'center'
            })
            
            correct_format = workbook.add_format({
                'bg_color': '#d1fae5', # Light Green
                'font_color': '#065f46',
                'border': 1,
                'align': 'center'
            })
            
            incorrect_format = workbook.add_format({
                'bg_color': '#fee2e2', # Light Red
                'font_color': '#991b1b',
                'border': 1,
                'align': 'center'
            })
            
            # --- SHEET 1: Datos de Sesión ---
            df_display = df.copy()
            df_display.rename(columns={
                'Attempt ID': 'ID de Ensayo',
                'Reaction Time (ms)': 'Tiempo de Reaccion (ms)',
                'Set Size': 'Cantidad de Elementos',
                'Stimulus Type': 'Tipo de Estimulo',
                'Target Present': 'Objetivo Presente',
                'Response Given': 'Respuesta del Evaluado',
                'Is Correct': 'Respuesta Correcta',
                'Search Type': 'Tipo de Busqueda',
                'Subject ID': 'ID de Participante',
                'Age': 'Edad',
                'Gender': 'Genero',
                'Timestamp': 'Fecha/Hora'
            }, inplace=True)
            
            df_display.to_excel(writer, sheet_name='Sesión Actual', index=False)
            worksheet1 = writer.sheets['Sesión Actual']
            
            for col_num, value in enumerate(df_display.columns.values):
                worksheet1.write(0, col_num, value, header_format)
                
            for row_idx in range(len(df_display)):
                is_correct = df_display.iloc[row_idx]['Respuesta Correcta']
                fmt = correct_format if str(is_correct).lower() in ['true', '1', 'yes', 'correct', 'si'] else incorrect_format
                for col_idx in range(len(df_display.columns)):
                    val = df_display.iloc[row_idx, col_idx]
                    if isinstance(val, (bool, pd.BooleanDtype)):
                        val = str(val)
                    if col_idx == 6: # Respuesta Correcta column
                        worksheet1.write(row_idx + 1, col_idx, val, fmt)
                    else:
                        worksheet1.write(row_idx + 1, col_idx, val, cell_format)
            
            worksheet1.set_column('A:L', 18)
            worksheet1.set_row(0, 26)
            
            # --- SHEET 2: Resumen Clínico ---
            df['Is Correct Num'] = df['Is Correct'].apply(lambda x: 1 if str(x).lower() in ['true', '1', 'yes', 'correct'] else 0)
            valid_df = df[(df['Is Correct Num'] == 1) & (df['Response Given'] != 'TIMEOUT') & (df['Reaction Time (ms)'] < 90000)]
            
            # Averages grouped by Search Type and Set Size
            summary_df = valid_df.groupby(['Search Type', 'Set Size']).agg(
                Average_RT_ms=('Reaction Time (ms)', 'mean')
            ).reset_index()
            
            accuracy_df = df.groupby(['Search Type', 'Set Size']).agg(
                Accuracy_Rate=('Is Correct Num', 'mean')
            ).reset_index()
            
            summary_df = pd.merge(summary_df, accuracy_df, on=['Search Type', 'Set Size'], how='outer')
            summary_df['Average_RT_ms'] = summary_df['Average_RT_ms'].fillna(0).round(2)
            summary_df['Accuracy_Rate'] = (summary_df['Accuracy_Rate'].fillna(0) * 100).round(2)
            
            summary_df.rename(columns={
                'Search Type': 'Tipo de Búsqueda',
                'Set Size': 'Tamaño del Conjunto',
                'Average_RT_ms': 'Tiempo de Reacción Promedio (ms)',
                'Accuracy_Rate': 'Tasa de Aciertos (%)'
            }, inplace=True)
            
            summary_df.to_excel(writer, sheet_name='Resumen Sesión', index=False)
            worksheet2 = writer.sheets['Resumen Sesión']
            
            for col_num, value in enumerate(summary_df.columns.values):
                worksheet2.write(0, col_num, value, header_format)
                
            for row_idx in range(len(summary_df)):
                for col_idx in range(len(summary_df.columns)):
                    worksheet2.write(row_idx + 1, col_idx, summary_df.iloc[row_idx, col_idx], cell_format)
            worksheet2.set_column('A:D', 32)
            worksheet2.set_row(0, 26)
            
            # Create charts for active session (Only if data exists for both)
            chart1 = workbook.add_chart({'type': 'line'})
            
            # Split for Feature and Conjunction rows
            feat_rows = summary_df[summary_df['Tipo de Búsqueda'] == 'feature']
            conj_rows = summary_df[summary_df['Tipo de Búsqueda'] == 'conjunction']
            
            if not feat_rows.empty:
                chart1.add_series({
                    'name':       'Búsqueda Paralela (Feature)',
                    'categories': '=Resumen Sesión!$B$2:$B$' + str(len(feat_rows) + 1),
                    'values':     '=Resumen Sesión!$C$2:$C$' + str(len(feat_rows) + 1),
                    'line':       {'color': '#10b981', 'width': 2.5},
                    'marker':     {'type': 'circle', 'size': 8, 'fill': {'color': '#10b981'}},
                })
            if not conj_rows.empty:
                chart1.add_series({
                    'name':       'Búsqueda Serial (Conjunction)',
                    'categories': '=Resumen Sesión!$B$' + str(len(feat_rows) + 2) + ':$B$' + str(len(summary_df) + 1),
                    'values':     '=Resumen Sesión!$C$' + str(len(feat_rows) + 2) + ':$C$' + str(len(summary_df) + 1),
                    'line':       {'color': '#ef4444', 'width': 2.5},
                    'marker':     {'type': 'square', 'size': 8, 'fill': {'color': '#ef4444'}},
                })
                
            chart1.set_title({'name': 'Tiempo de Reacción Promedio vs Set Size'})
            chart1.set_x_axis({'name': 'Set Size (Cantidad de Elementos)'})
            chart1.set_y_axis({'name': 'Tiempo (ms)'})
            worksheet2.insert_chart('F2', chart1)
            
            # --- SHEET 3: Historial del Evaluador (Consolidado Histórico) ---
            if not df_history.empty:
                df_history['Is Correct Num'] = df_history['Is Correct'].apply(lambda x: 1 if str(x).lower() in ['true', '1', 'yes', 'correct'] else 0)
                
                # Group by evaluated subject to create historical analysis
                subject_groups = df_history.groupby(['Subject ID', 'Age', 'Gender'])
                
                history_rows = []
                for name, group in subject_groups:
                    sub_id, age, gender = name
                    total_trials = len(group)
                    
                    correct_group = group[(group['Is Correct Num'] == 1) & (group['Reaction Time (ms)'] < 90000) & (group['Response Given'] != 'TIMEOUT')]
                    avg_rt = correct_group['Reaction Time (ms)'].mean() if not correct_group.empty else 0
                    accuracy = (group['Is Correct Num'].sum() / total_trials) * 100
                    last_eval = group['Timestamp'].max()
                    
                    # Detailed metrics
                    feat_correct = correct_group[correct_group['Search Type'] == 'feature']
                    tr_paralela = feat_correct['Reaction Time (ms)'].mean() if not feat_correct.empty else 0
                    
                    conj_correct = correct_group[correct_group['Search Type'] == 'conjunction']
                    tr_serial = conj_correct['Reaction Time (ms)'].mean() if not conj_correct.empty else 0
                    
                    # Slope calculation
                    sizes = sorted(correct_group['Set Size'].unique())
                    slope = 0.0
                    if len(sizes) >= 2:
                        min_size = sizes[0]
                        max_size = sizes[-1]
                        
                        feat_min = feat_correct[feat_correct['Set Size'] == min_size]['Reaction Time (ms)'].mean()
                        feat_max = feat_correct[feat_correct['Set Size'] == max_size]['Reaction Time (ms)'].mean()
                        conj_min = conj_correct[conj_correct['Set Size'] == min_size]['Reaction Time (ms)'].mean()
                        conj_max = conj_correct[conj_correct['Set Size'] == max_size]['Reaction Time (ms)'].mean()
                        
                        feat_slope = (feat_max - feat_min) / (max_size - min_size) if (pd.notnull(feat_min) and pd.notnull(feat_max)) else 0.0
                        conj_slope = (conj_max - conj_min) / (max_size - min_size) if (pd.notnull(conj_min) and pd.notnull(conj_max)) else 0.0
                        
                        import math
                        slope = max(0.0 if math.isnan(feat_slope) else feat_slope, 0.0 if math.isnan(conj_slope) else conj_slope)
                        
                    errors = total_trials - len(correct_group)
                    
                    if slope <= 8:
                        nota_clinica = f"El efecto de pendiente ({round(slope, 1)} ms/elemento) indica que el numero de distractores no afecto significativamente tu velocidad de procesamiento. Esto representa un procesamiento en paralelo automatico (Pop-Out) y un excelente control atencional involuntario."
                        diagnostico = "Busqueda Paralela"
                    else:
                        nota_clinica = f"El efecto de pendiente ({round(slope, 1)} ms/elemento) indica que tu cerebro necesito realizar una busqueda serial y secuencial para analizar cada estimulo. A mayor numero de distractores, mayor tiempo de respuesta y carga cognitiva."
                        diagnostico = "Busqueda Serial"
                    
                    history_rows.append({
                        'ID de Participante': sub_id,
                        'Edad': age,
                        'Género': gender,
                        'Ensayos Realizados': total_trials,
                        'T.R. Promedio (ms)': round(avg_rt, 2),
                        'Precisión (%)': round(accuracy, 2),
                        'TR Paralela (ms)': round(float(tr_paralela), 2),
                        'TR Serial (ms)': round(float(tr_serial), 2),
                        'Pendiente (ms/elem)': round(float(slope), 2),
                        'Errores': int(errors),
                        'Diagnóstico Clínico': diagnostico,
                        'Nota Clínica': nota_clinica,
                        'Última Evaluación': last_eval
                    })
                    
                hist_summary_df = pd.DataFrame(history_rows)
                hist_summary_df.to_excel(writer, sheet_name='Historial Clínico', index=False)
                worksheet3 = writer.sheets['Historial Clínico']
                
                for col_num, value in enumerate(hist_summary_df.columns.values):
                    worksheet3.write(0, col_num, value, header_format)
                    
                for row_idx in range(len(hist_summary_df)):
                    for col_idx in range(len(hist_summary_df.columns)):
                        worksheet3.write(row_idx + 1, col_idx, hist_summary_df.iloc[row_idx, col_idx], cell_format)
                        
                worksheet3.set_column('A:M', 22)
                worksheet3.set_row(0, 26)
            
        output.seek(0)
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="reporte_evaluador_busqueda_visual.xlsx"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/export_history_excel', methods=['GET'])
def export_history_excel():
    try:
        if not os.path.exists(HISTORIC_CSV_PATH):
            return jsonify({"status": "error", "message": "No hay datos en el historial para exportar"}), 404
        
        df_history = pd.read_csv(HISTORIC_CSV_PATH)
        if df_history.empty:
            return jsonify({"status": "error", "message": "El historial está vacío"}), 400
            
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook  = writer.book
            
            # --- STYLES ---
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'fg_color': '#1e3a8a', # Dark Blue
                'font_color': '#ffffff',
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'border': 1,
                'align': 'center'
            })
            
            correct_format = workbook.add_format({
                'bg_color': '#d1fae5', # Light Green
                'font_color': '#065f46',
                'border': 1,
                'align': 'center'
            })
            
            incorrect_format = workbook.add_format({
                'bg_color': '#fee2e2', # Light Red
                'font_color': '#991b1b',
                'border': 1,
                'align': 'center'
            })
            
            # --- SHEET 1: Resumen de Participantes ---
            df_history['Is Correct Num'] = df_history['Is Correct'].apply(lambda x: 1 if str(x).lower() in ['true', '1', 'yes', 'correct'] else 0)
            
            if 'Session ID' not in df_history.columns:
                df_history['Session ID'] = 'SES-LEGACY'
            df_history['Session ID'] = df_history['Session ID'].fillna(
                df_history.groupby(['Subject ID', 'Age', 'Gender'])['Timestamp'].transform('min').fillna('SES-LEGACY')
            )
            
            subject_groups = df_history.groupby(['Session ID', 'Subject ID', 'Age', 'Gender'])
            
            history_rows = []
            for name, group in subject_groups:
                session_id, sub_id, age, gender = name
                total_trials = len(group)
                
                correct_group = group[(group['Is Correct Num'] == 1) & (group['Reaction Time (ms)'] < 90000) & (group['Response Given'] != 'TIMEOUT')]
                avg_rt = correct_group['Reaction Time (ms)'].mean() if not correct_group.empty else 0
                accuracy = (group['Is Correct Num'].sum() / total_trials) * 100
                last_eval = group['Timestamp'].max()
                
                # Detailed metrics
                feat_correct = correct_group[correct_group['Search Type'] == 'feature']
                tr_paralela = feat_correct['Reaction Time (ms)'].mean() if not feat_correct.empty else 0
                
                conj_correct = correct_group[correct_group['Search Type'] == 'conjunction']
                tr_serial = conj_correct['Reaction Time (ms)'].mean() if not conj_correct.empty else 0
                
                # Slope calculation in python
                sizes = sorted(correct_group['Set Size'].unique())
                slope = 0.0
                if len(sizes) >= 2:
                    min_size = sizes[0]
                    max_size = sizes[-1]
                    
                    feat_min = feat_correct[feat_correct['Set Size'] == min_size]['Reaction Time (ms)'].mean()
                    feat_max = feat_correct[feat_correct['Set Size'] == max_size]['Reaction Time (ms)'].mean()
                    conj_min = conj_correct[conj_correct['Set Size'] == min_size]['Reaction Time (ms)'].mean()
                    conj_max = conj_correct[conj_correct['Set Size'] == max_size]['Reaction Time (ms)'].mean()
                    
                    feat_slope = (feat_max - feat_min) / (max_size - min_size) if (pd.notnull(feat_min) and pd.notnull(feat_max)) else 0.0
                    conj_slope = (conj_max - conj_min) / (max_size - min_size) if (pd.notnull(conj_min) and pd.notnull(conj_max)) else 0.0
                    
                    import math
                    slope = max(0.0 if math.isnan(feat_slope) else feat_slope, 0.0 if math.isnan(conj_slope) else conj_slope)
                    
                errors = total_trials - len(correct_group)
                
                if slope <= 8:
                    nota_clinica = f"El efecto de pendiente ({round(slope, 1)} ms/elemento) indica que el numero de distractores no afecto significativamente tu velocidad de procesamiento. Esto representa un procesamiento en paralelo automatico (Pop-Out) y un excelente control atencional involuntario."
                    diagnostico = "Busqueda Paralela"
                else:
                    nota_clinica = f"El efecto de pendiente ({round(slope, 1)} ms/elemento) indica que tu cerebro necesito realizar una busqueda serial y secuencial para analizar cada estimulo. A mayor numero de distractores, mayor tiempo de respuesta y carga cognitiva."
                    diagnostico = "Busqueda Serial"
                
                history_rows.append({
                    'ID de Sesión': session_id,
                    'ID de Participante': sub_id,
                    'Edad': age,
                    'Género': gender,
                    'Ensayos Realizados': total_trials,
                    'T.R. Promedio (ms)': round(avg_rt, 2),
                    'Precisión (%)': round(accuracy, 2),
                    'TR Paralela (ms)': round(float(tr_paralela), 2),
                    'TR Serial (ms)': round(float(tr_serial), 2),
                    'Pendiente (ms/elem)': round(float(slope), 2),
                    'Errores': int(errors),
                    'Diagnóstico Clínico': diagnostico,
                    'Nota Clínica': nota_clinica,
                    'Última Evaluación': last_eval
                })
                
            hist_summary_df = pd.DataFrame(history_rows)
            hist_summary_df.to_excel(writer, sheet_name='Resumen de Participantes', index=False)
            worksheet1 = writer.sheets['Resumen de Participantes']
            
            for col_num, value in enumerate(hist_summary_df.columns.values):
                worksheet1.write(0, col_num, value, header_format)
                
            for row_idx in range(len(hist_summary_df)):
                for col_idx in range(len(hist_summary_df.columns)):
                    worksheet1.write(row_idx + 1, col_idx, hist_summary_df.iloc[row_idx, col_idx], cell_format)
                    
            worksheet1.set_column('A:N', 22)
            worksheet1.set_row(0, 26)
            
            # --- SHEET 2: Detalle de Respuestas Históricas ---
            df_details = df_history.copy()
            df_details.rename(columns={
                'Attempt ID': 'ID de Ensayo',
                'Reaction Time (ms)': 'Tiempo de Reaccion (ms)',
                'Set Size': 'Cantidad de Elementos',
                'Stimulus Type': 'Tipo de Estimulo',
                'Target Present': 'Objetivo Presente',
                'Response Given': 'Respuesta del Evaluado',
                'Is Correct': 'Respuesta Correcta',
                'Search Type': 'Tipo de Busqueda',
                'Subject ID': 'ID de Participante',
                'Age': 'Edad',
                'Gender': 'Genero',
                'Timestamp': 'Fecha/Hora',
                'Session ID': 'ID de Sesion'
            }, inplace=True)
            
            if 'Is Correct Num' in df_details.columns:
                df_details.drop(columns=['Is Correct Num'], inplace=True)
                
            df_details.to_excel(writer, sheet_name='Detalle de Respuestas', index=False)
            worksheet2 = writer.sheets['Detalle de Respuestas']
            
            for col_num, value in enumerate(df_details.columns.values):
                worksheet2.write(0, col_num, value, header_format)
                
            for row_idx in range(len(df_details)):
                is_correct = df_details.iloc[row_idx]['Respuesta Correcta']
                fmt = correct_format if str(is_correct).lower() in ['true', '1', 'yes', 'correct', 'si'] else incorrect_format
                for col_idx in range(len(df_details.columns)):
                    val = df_details.iloc[row_idx, col_idx]
                    if isinstance(val, (bool, pd.BooleanDtype)):
                        val = str(val)
                    if col_idx == 6: # Respuesta Correcta column
                        worksheet2.write(row_idx + 1, col_idx, val, fmt)
                    else:
                        worksheet2.write(row_idx + 1, col_idx, val, cell_format)
                        
            worksheet2.set_column('A:M', 20)
            worksheet2.set_row(0, 26)
            
        output.seek(0)
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="historial_completo_busqueda_visual.xlsx"
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        if not os.path.exists(HISTORIC_CSV_PATH):
            return jsonify([])
        df_history = pd.read_csv(HISTORIC_CSV_PATH)
        if df_history.empty:
            return jsonify([])
        
        if 'Session ID' not in df_history.columns:
            df_history['Session ID'] = 'SES-LEGACY'
        df_history['Session ID'] = df_history['Session ID'].fillna(
            df_history.groupby(['Subject ID', 'Age', 'Gender'])['Timestamp'].transform('min').fillna('SES-LEGACY')
        )
        
        df_history['Is Correct Num'] = df_history['Is Correct'].apply(lambda x: 1 if str(x).lower() in ['true', '1', 'yes', 'correct'] else 0)
        
        subject_groups = df_history.groupby(['Session ID', 'Subject ID', 'Age', 'Gender'])
        
        history_rows = []
        for name, group in subject_groups:
            sess_id, sub_id, age, gender = name
            total_trials = len(group)
            
            correct_group = group[(group['Is Correct Num'] == 1) & (group['Reaction Time (ms)'] < 90000) & (group['Response Given'] != 'TIMEOUT')]
            avg_rt = correct_group['Reaction Time (ms)'].mean() if not correct_group.empty else 0
            accuracy = (group['Is Correct Num'].sum() / total_trials) * 100
            last_eval = group['Timestamp'].max()
            
            # Detailed metrics
            feat_correct = correct_group[correct_group['Search Type'] == 'feature']
            tr_paralela = feat_correct['Reaction Time (ms)'].mean() if not feat_correct.empty else 0
            
            conj_correct = correct_group[correct_group['Search Type'] == 'conjunction']
            tr_serial = conj_correct['Reaction Time (ms)'].mean() if not conj_correct.empty else 0
            
            # Slope calculation in python
            sizes = sorted(correct_group['Set Size'].unique())
            slope = 0.0
            if len(sizes) >= 2:
                min_size = sizes[0]
                max_size = sizes[-1]
                
                feat_min = feat_correct[feat_correct['Set Size'] == min_size]['Reaction Time (ms)'].mean()
                feat_max = feat_correct[feat_correct['Set Size'] == max_size]['Reaction Time (ms)'].mean()
                conj_min = conj_correct[conj_correct['Set Size'] == min_size]['Reaction Time (ms)'].mean()
                conj_max = conj_correct[conj_correct['Set Size'] == max_size]['Reaction Time (ms)'].mean()
                
                feat_slope = (feat_max - feat_min) / (max_size - min_size) if (pd.notnull(feat_min) and pd.notnull(feat_max)) else 0.0
                conj_slope = (conj_max - conj_min) / (max_size - min_size) if (pd.notnull(conj_min) and pd.notnull(conj_max)) else 0.0
                
                import math
                slope = max(0.0 if math.isnan(feat_slope) else feat_slope, 0.0 if math.isnan(conj_slope) else conj_slope)
                
            errors = total_trials - len(correct_group)
            
            if slope <= 8:
                nota_clinica = f"El efecto de pendiente ({round(slope, 1)} ms/elemento) indica que el numero de distractores no afecto significativamente tu velocidad de procesamiento. Esto representa un procesamiento en paralelo automatico (Pop-Out) y un excelente control atencional involuntario."
                diagnostico = "Busqueda Paralela"
            else:
                nota_clinica = f"El efecto de pendiente ({round(slope, 1)} ms/elemento) indica que tu cerebro necesito realizar una busqueda serial y secuencial para analizar cada estimulo. A mayor numero de distractores, mayor tiempo de respuesta y carga cognitiva."
                diagnostico = "Busqueda Serial"
                
            history_rows.append({
                'session_id': str(sess_id),
                'subject_id': str(sub_id),
                'age': int(age) if pd.notnull(age) else 0,
                'gender': str(gender),
                'total_trials': int(total_trials),
                'avg_rt': round(float(avg_rt), 2),
                'accuracy': round(float(accuracy), 2),
                'last_eval': str(last_eval),
                'tr_paralela': round(float(tr_paralela), 2),
                'tr_serial': round(float(tr_serial), 2),
                'pendiente': round(float(slope), 2),
                'errores': int(errors),
                'diagnostico': diagnostico,
                'nota_clinica': nota_clinica
            })
            
        history_rows.sort(key=lambda x: x['last_eval'], reverse=True)
        return jsonify(history_rows)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/clear_history', methods=['POST'])
def clear_history_data():
    try:
        if os.path.exists(HISTORIC_CSV_PATH):
            os.remove(HISTORIC_CSV_PATH)
        init_csv()
        return jsonify({"status": "success", "message": "Historial clínico limpiado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/delete_subject', methods=['POST'])
def delete_subject():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Falta el ID del participante o sesión"}), 400
        
        session_id = data.get('session_id')
        subject_id = data.get('subject_id')
        
        if not session_id and not subject_id:
            return jsonify({"status": "error", "message": "Falta el ID del participante o sesión"}), 400
        
        if os.path.exists(HISTORIC_CSV_PATH):
            df_history = pd.read_csv(HISTORIC_CSV_PATH)
            if 'Session ID' not in df_history.columns:
                df_history['Session ID'] = 'SES-LEGACY'
            
            df_history['Session ID'] = df_history['Session ID'].fillna(
                df_history.groupby(['Subject ID', 'Age', 'Gender'])['Timestamp'].transform('min').fillna('SES-LEGACY')
            )
            
            if session_id:
                df_history = df_history[df_history['Session ID'].astype(str) != str(session_id)]
            elif subject_id:
                df_history = df_history[df_history['Subject ID'].astype(str) != str(subject_id)]
                
            df_history.to_csv(HISTORIC_CSV_PATH, index=False)
            
        return jsonify({"status": "success", "message": "Registro eliminado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
