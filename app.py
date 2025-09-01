from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
import numpy as np
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_sales_data(file_path):
    """Process uploaded sales data and generate insights"""
    try:
        # Read the file based on extension
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Basic data cleaning
        df.columns = df.columns.str.strip().str.lower()
        
        # Try to identify common column names
        date_cols = [col for col in df.columns if any(word in col for word in ['date', 'time', 'created', 'order'])]
        amount_cols = [col for col in df.columns if any(word in col for word in ['amount', 'price', 'total', 'revenue', 'sales', 'value'])]
        product_cols = [col for col in df.columns if any(word in col for word in ['product', 'item', 'name', 'category'])]
        customer_cols = [col for col in df.columns if any(word in col for word in ['customer', 'client', 'user', 'buyer'])]
        
        insights = {
            'total_records': len(df),
            'columns': list(df.columns),
            'date_columns': date_cols,
            'amount_columns': amount_cols,
            'product_columns': product_cols,
            'customer_columns': customer_cols,
            'data_preview': df.head().to_html(classes='table table-striped'),
            'summary_stats': {},
            'charts': {}
        }
        
        # Generate summary statistics for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            insights['summary_stats'] = df[numeric_cols].describe().to_html(classes='table table-striped')
        
        # Generate insights based on available data
        if amount_cols:
            main_amount_col = amount_cols[0]
            insights['total_sales'] = df[main_amount_col].sum()
            insights['average_sale'] = df[main_amount_col].mean()
            insights['max_sale'] = df[main_amount_col].max()
            insights['min_sale'] = df[main_amount_col].min()
            
            # Create sales distribution chart
            fig = go.Figure(data=[go.Histogram(x=df[main_amount_col], nbinsx=20)])
            fig.update_layout(title='Sales Amount Distribution', xaxis_title='Amount', yaxis_title='Frequency')
            insights['charts']['sales_distribution'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        if date_cols and amount_cols:
            date_col = date_cols[0]
            amount_col = amount_cols[0]
            
            # Convert date column
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df_clean = df.dropna(subset=[date_col, amount_col])
            
            if len(df_clean) > 0:
                # Sales over time
                daily_sales = df_clean.groupby(df_clean[date_col].dt.date)[amount_col].sum().reset_index()
                
                fig = go.Figure(data=[go.Scatter(x=daily_sales[date_col], y=daily_sales[amount_col], mode='lines+markers')])
                fig.update_layout(title='Sales Over Time', xaxis_title='Date', yaxis_title='Sales Amount')
                insights['charts']['sales_timeline'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        if product_cols and amount_cols:
            product_col = product_cols[0]
            amount_col = amount_cols[0]
            
            # Top products by sales
            top_products = df.groupby(product_col)[amount_col].sum().nlargest(10)
            
            fig = go.Figure(data=[go.Bar(x=top_products.index, y=top_products.values)])
            fig.update_layout(title='Top 10 Products by Sales', xaxis_title='Product', yaxis_title='Sales Amount')
            insights['charts']['top_products'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return insights
        
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the data
        insights = process_sales_data(file_path)
        
        if 'error' in insights:
            flash(f'Error processing file: {insights["error"]}')
            return redirect(url_for('index'))
        
        return render_template('dashboard.html', insights=insights, filename=filename)
    else:
        flash('Invalid file type. Please upload CSV or Excel files only.')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', insights=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
